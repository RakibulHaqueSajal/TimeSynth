#!/usr/bin/env python3
"""
Calibrate HMM transition-prob error on TRUE, build significance window,
and plot violin of forecast deltas.

- Fits 2-state GaussianHMM on features from TRUE futures only.
- Decodes TRUE and PRED with same HMM + same normalization.
- Computes per-sequence p_hat (per-sample switching prob).
- Error on TRUE: e = p_hat_true - p_gt
  -> Fit Gaussian (mu, sigma) and compute 0.05% two-sided cutoffs.
- For PRED: delta = p_hat_pred - p_gt
- Violin plot of deltas (TRUE vs PRED) with significance band.

Dependencies:
  pip install numpy scipy hmmlearn matplotlib
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Feature extraction (Welch dom-freq per window)
# -----------------------------
def dom_freq_welch(seg, fs, nperseg):
    from scipy.signal import welch
    seg = np.asarray(seg, dtype=float)
    seg = seg - seg.mean()
    nperseg = min(int(nperseg), len(seg))
    f, Pxx = welch(seg, fs=fs, nperseg=nperseg)
    return float(f[np.argmax(Pxx)])

def windowed_welch_domfreq(y, fs, win=16, hop=8):
    y = np.asarray(y, dtype=float).reshape(-1)
    if len(y) < win:
        return np.zeros((0, 1), dtype=float), np.zeros((0,), dtype=int)

    Z, centers = [], []
    for a in range(0, len(y) - win + 1, hop):
        seg = y[a:a + win]
        fd = dom_freq_welch(seg, fs=fs, nperseg=win)
        Z.append(fd)
        centers.append(a + win // 2)
    return np.asarray(Z, dtype=float)[:, None], np.asarray(centers, dtype=int)

# -----------------------------
# HMM fit/decode
# -----------------------------
def fit_global_hmm_2state(Z_all, lengths, n_iter=800, tol=1e-4, seeds=(0, 5, 10, 20)):
    from hmmlearn.hmm import GaussianHMM

    Z_all = np.asarray(Z_all, dtype=np.float64)
    lengths = list(map(int, lengths))

    mu = Z_all.mean(axis=0, keepdims=True)
    sig = Z_all.std(axis=0, keepdims=True) + 1e-8
    Zs = (Z_all - mu) / sig

    best_model, best_score = None, -np.inf
    for seed in seeds:
        model = GaussianHMM(
            n_components=2,
            covariance_type="diag",
            n_iter=int(n_iter),
            tol=float(tol),
            random_state=int(seed),
            init_params="stmc",
            params="stmc",
        )
        model.fit(Zs, lengths=lengths)
        score = model.score(Zs, lengths=lengths)
        if score > best_score:
            best_score = score
            best_model = model

    return best_model, best_score, (mu, sig)

def decode_with_fitted_hmm(model, Z_all, lengths, norm_stats):
    mu, sig = norm_stats
    Z_all = np.asarray(Z_all, dtype=np.float64)
    Zs = (Z_all - mu) / sig
    states_all = model.predict(Zs, lengths=lengths)

    out, idx = [], 0
    for L in lengths:
        out.append(states_all[idx:idx + L].copy())
        idx += L
    return out

# -----------------------------
# Canonicalize labels by feature means (TRUE only)
# -----------------------------
def canonicalize_states_by_feature_means(states_list, Z_list):
    vals0, vals1 = [], []
    for s, Z in zip(states_list, Z_list):
        s = np.asarray(s, dtype=int)
        z = np.asarray(Z, dtype=float).reshape(-1)
        vals0.append(z[s == 0])
        vals1.append(z[s == 1])

    v0 = np.concatenate([a for a in vals0 if a.size > 0], axis=0)
    v1 = np.concatenate([a for a in vals1 if a.size > 0], axis=0)

    m0 = float(v0.mean()) if v0.size else np.inf
    m1 = float(v1.mean()) if v1.size else -np.inf

    mapping = {0: 0, 1: 1} if m0 <= m1 else {0: 1, 1: 0}
    out = [np.vectorize(mapping.get)(np.asarray(s, dtype=int)) for s in states_list]
    return out, mapping, (m0, m1)

# -----------------------------
# Per-sequence p_hat (per-sample)
# -----------------------------
def flip_rate(s):
    s = np.asarray(s, dtype=int)
    if len(s) < 2:
        return 0.0
    return float((s[1:] != s[:-1]).mean())

def p_sample_from_state_seq(s, hop):
    """
    s is at "HMM step" resolution.
    p_step = flip rate per step
    convert to per-sample: p = 1 - (1-p_step)^(1/hop)
    """
    p_step = flip_rate(s)
    hop = max(int(hop), 1)
    return float(1.0 - (1.0 - p_step) ** (1.0 / hop))

def per_sequence_p_hats(states_list, hop):
    return np.asarray([p_sample_from_state_seq(s, hop=hop) for s in states_list], dtype=float)

# -----------------------------
# Build Welch features from with_history
# -----------------------------
def build_features_from_with_history_welch(path, fs, L, H, win, hop, min_windows):
    wh = np.load(path)  # [N, L+H, 1]
    assert wh.ndim == 3 and wh.shape[2] == 1, f"Unexpected shape: {wh.shape}"
    assert wh.shape[1] >= (L + H), f"Expected time dim >= L+H, got {wh.shape[1]} vs {L+H}"

    Z_list, keep_ids, lengths = [], [], []
    for n in range(wh.shape[0]):
        y = wh[n, L:L+H, 0]  # future only
        Z, _ = windowed_welch_domfreq(y, fs=fs, win=win, hop=hop)
        if Z.shape[0] < min_windows:
            continue
        Z_list.append(Z)
        lengths.append(int(Z.shape[0]))
        keep_ids.append(n)

    if len(Z_list) == 0:
        raise RuntimeError("No samples produced enough windows. Reduce win/hop or min_windows.")

    Z_all = np.vstack(Z_list)
    return Z_all, lengths, Z_list, np.asarray(keep_ids, dtype=int)

# -----------------------------
# Significance window from TRUE errors (Gaussian)
# -----------------------------
def gaussian_significance_window(errors, alpha_total=0.0005):
    """
    alpha_total=0.0005 corresponds to 0.05% two-sided total mass outside the band.
    """
    from scipy.stats import norm
    errors = np.asarray(errors, dtype=float)
    mu = float(errors.mean())
    sigma = float(errors.std(ddof=1) + 1e-12)
    z = float(norm.ppf(1.0 - alpha_total / 2.0))
    lo = mu - z * sigma
    hi = mu + z * sigma
    return {"mu": mu, "sigma": sigma, "z": z, "lo": lo, "hi": hi}

# -----------------------------
# Main runner
# -----------------------------
def run_with_significance_and_violin(
    root,
    p_gt=0.3,       # assumed per-sample ground-truth switching probability
    fs=10,
    L=50,
    H=100,
    win=16,
    hop=8,
    min_windows=5,
    hmm_n_iter=800,
    hmm_tol=1e-4,
    hmm_seeds=(0, 5, 10, 20),
    out_png=None,
):
    true_path = os.path.join(root, "test_true_with_history.npy")
    pred_path = os.path.join(root, "test_pred_with_history.npy")
    if not os.path.exists(true_path):
        raise FileNotFoundError(true_path)
    if not os.path.exists(pred_path):
        raise FileNotFoundError(pred_path)

    # --- TRUE features ---
    Z_true_all, len_true, Z_true_list, keep_true = build_features_from_with_history_welch(
        true_path, fs, L, H, win, hop, min_windows
    )

    # Fit HMM on TRUE only
    model, best_score, norm_stats = fit_global_hmm_2state(
        Z_true_all, len_true, n_iter=hmm_n_iter, tol=hmm_tol, seeds=hmm_seeds
    )

    # Decode TRUE
    s_true_raw = decode_with_fitted_hmm(model, Z_true_all, len_true, norm_stats)

    # Canonicalize using TRUE
    s_true, mapping, (m0, m1) = canonicalize_states_by_feature_means(s_true_raw, Z_true_list)

    # Per-sequence p_hat on TRUE (per-sample)
    p_hat_true = per_sequence_p_hats(s_true, hop=hop)
    err_true = p_hat_true - float(p_gt)

    band = gaussian_significance_window(err_true, alpha_total=0.0005)

    # --- PRED features for same samples ---
    wh_pred = np.load(pred_path)
    assert wh_pred.ndim == 3 and wh_pred.shape[2] == 1

    Z_pred_list, len_pred = [], []
    for n in keep_true:
        y = wh_pred[n, L:L+H, 0]
        Z, _ = windowed_welch_domfreq(y, fs=fs, win=win, hop=hop)
        Z_pred_list.append(Z)
        len_pred.append(int(Z.shape[0]))
    Z_pred_all = np.vstack(Z_pred_list)

    # Decode PRED with same HMM + same normalization
    s_pred_raw = decode_with_fitted_hmm(model, Z_pred_all, len_pred, norm_stats)
    s_pred = [np.vectorize(mapping.get)(np.asarray(s, dtype=int)) for s in s_pred_raw]

    # Per-sequence p_hat on PRED (per-sample)
    p_hat_pred = per_sequence_p_hats(s_pred, hop=hop)
    delta_pred = p_hat_pred - float(p_gt)

    # --- Plot violins of deltas ---
    data = [err_true, delta_pred]  # both are "estimate - p_gt" (TRUE error vs PRED delta)
    labels = ["TRUE: p̂ - p_gt", "PRED: p̂ - p_gt"]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    parts = ax.violinplot(data, showmedians=True, showextrema=True)
    ax.set_xticks([1, 2])
    ax.set_xticklabels(labels, rotation=10)

    # significance band from TRUE error distribution
    ax.axhspan(band["lo"], band["hi"], alpha=0.2)
    ax.axhline(0.0)  # zero deviation line
    ax.set_ylabel("Delta (per-sample switching prob)")

    ax.set_title(
        f"HMM probe (Welch features): p_gt={p_gt} | band=({band['lo']:.4g},{band['hi']:.4g}) "
        f"| z={band['z']:.3f} | LL={best_score:.1f}"
    )

    # Also print a quick “significance” check using mean
    mean_true = float(np.mean(err_true))
    mean_pred = float(np.mean(delta_pred))
    pred_sig = (mean_pred < band["lo"]) or (mean_pred > band["hi"])

    print("========================================")
    print("HMM significance calibration (Gaussian, 0.05% two-sided)")
    print("----------------------------------------")
    print(f"p_gt (per-sample):            {p_gt}")
    print(f"TRUE sequences used:          {len(keep_true)}")
    print(f"Best log-likelihood (TRUE):   {best_score:.6f}")
    print(f"Canonical mapping:            {mapping} (feature means raw-state0/1: {m0:.4f}, {m1:.4f})")
    print("----------------------------------------")
    print(f"TRUE error mean/std:          {band['mu']:.6g} / {band['sigma']:.6g}")
    print(f"z for alpha=0.0005:           {band['z']:.6g}")
    print(f"Significance band [lo, hi]:   [{band['lo']:.6g}, {band['hi']:.6g}]")
    print("----------------------------------------")
    print(f"Mean(TRUE delta):             {mean_true:.6g}  (should be near band mu)")
    print(f"Mean(PRED delta):             {mean_pred:.6g}  -> significant? {pred_sig}")
    print("========================================")

    if out_png is None:
        out_png = os.path.join(root, f"hmm_violin_sig_pgt_{p_gt:.3f}_win{win}_hop{hop}.png")

    fig.tight_layout()
    fig.savefig(out_png, dpi=200)
    print(f"Saved plot: {out_png}")

    return {
        "band": band,
        "p_hat_true": p_hat_true,
        "p_hat_pred": p_hat_pred,
        "err_true": err_true,
        "delta_pred": delta_pred,
        "plot_path": out_png,
    }

# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    root = "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/long_term_forecast_Linear_50_100_Linear_PhaseMod_Single_Freq_TwoState_p_0.30000_70_10_20_0.001_0.0001_16_State"

    run_with_significance_and_violin(
        root=root,
        p_gt=0.3,
        fs=10,
        L=50,
        H=100,
        win=16,
        hop=8,
        min_windows=5,
        hmm_n_iter=800,
        hmm_tol=1e-4,
        hmm_seeds=(0, 5, 10, 20),
    )
