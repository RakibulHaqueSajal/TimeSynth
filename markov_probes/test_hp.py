#!/usr/bin/env python3
"""
Global HMM probe (fit on TRUE HISTORY) + dynamics mismatch on switching probability
using CONTINUOUS distribution metrics + smooth overlap figure (Gaussian fit).

Key change vs histogram version:
- NO discrete PMFs, NO binning-based KL/JSD.
- We fit Gaussian N(mu, sigma) to the per-sequence samples (sample variation),
  then compute CONTINUOUS metrics:

  1) Gaussian-overlap (OVL):
     OVL = ∫ min(f_true(x), f_pred(x)) dx     in [0,1]

  2) Jensen–Shannon divergence for Gaussians (continuous):
     JSD(P,Q) = 0.5 KL(P||M) + 0.5 KL(Q||M),  M = 0.5 P + 0.5 Q  (a mixture)
     Since M is a mixture (not Gaussian), KL has no closed form.
     We compute it by numerical quadrature on a dense grid (stable, deterministic).

  3) Symmetric KL for Gaussians (closed-form):
     KL(N0||N1) has closed form; KL_sym = KL(P||Q) + KL(Q||P)

  4) Total Variation (TV) distance (continuous):
     TV = 0.5 ∫ |f_true(x) - f_pred(x)| dx  in [0,1]
     computed via numerical quadrature.

Figures:
- Plots the two fitted Gaussian PDFs (TRUE vs PRED)
- Shades the overlap region min(f_true, f_pred)
- Annotates OVL, TV, JSD, KLs, and the fitted (mu, sigma)

This avoids binning artifacts (e.g., false "Overlap=0" due to histogram bins).

Dependencies:
- numpy
- scipy (welch + norm.pdf)
- hmmlearn
- matplotlib
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, List, Tuple, Iterable, Any

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
from scipy.stats import norm
from hmmlearn.hmm import GaussianHMM


# ============================================================
# 1) Feature extraction: Welch dominant frequency per window
# ============================================================

def dom_freq_welch(seg: np.ndarray, fs: float, nperseg: int) -> float:
    seg = np.asarray(seg, dtype=float)
    seg = seg - seg.mean()
    nperseg = min(int(nperseg), len(seg))
    f, Pxx = welch(seg, fs=fs, nperseg=nperseg)
    return float(f[np.argmax(Pxx)])


def windowed_welch_domfreq(y: np.ndarray, fs: float, win: int = 16, hop: int = 8) -> Tuple[np.ndarray, np.ndarray]:
    y = np.asarray(y, dtype=float)
    if len(y) < win:
        return np.zeros((0, 1), dtype=float), np.zeros((0,), dtype=int)

    Z: List[float] = []
    centers: List[int] = []
    for a in range(0, len(y) - win + 1, hop):
        seg = y[a:a + win]
        fd = dom_freq_welch(seg, fs=fs, nperseg=win)
        Z.append(fd)
        centers.append(a + win // 2)

    return np.asarray(Z, dtype=float)[:, None], np.asarray(centers, dtype=int)


# ============================================================
# 2) Global HMM probe: fit on TRUE HISTORY only
# ============================================================

def fit_global_hmm_2state(
    Z_all: np.ndarray,
    lengths: List[int],
    n_iter: int = 800,
    tol: float = 1e-4,
    seeds: Iterable[int] = (0, 1, 2),
):
    Z_all = np.asarray(Z_all, dtype=np.float64)
    lengths = list(map(int, lengths))

    mu = Z_all.mean(axis=0, keepdims=True)
    sig = Z_all.std(axis=0, keepdims=True) + 1e-8
    Zs = (Z_all - mu) / sig

    best_model = None
    best_score = -np.inf

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
        score = float(model.score(Zs, lengths=lengths))
        if score > best_score:
            best_score = score
            best_model = model

    if best_model is None:
        raise RuntimeError("HMM fitting failed to produce a model.")

    return best_model, best_score, (mu, sig)


def decode_with_fitted_hmm(model, Z_all: np.ndarray, lengths: List[int], norm_stats: Tuple[np.ndarray, np.ndarray]) -> List[np.ndarray]:
    mu, sig = norm_stats
    Z_all = np.asarray(Z_all, dtype=np.float64)
    Zs = (Z_all - mu) / sig
    states_all = model.predict(Zs, lengths=lengths)

    out: List[np.ndarray] = []
    idx = 0
    for L in lengths:
        out.append(np.asarray(states_all[idx:idx + L], dtype=int).copy())
        idx += L
    return out


# ============================================================
# 3) Canonicalize state labels (avoid label swapping)
# ============================================================

def canonicalize_states_by_feature_means(
    states_list: List[np.ndarray],
    Z_list: List[np.ndarray],
) -> Tuple[List[np.ndarray], Dict[int, int], Tuple[float, float]]:
    vals0: List[np.ndarray] = []
    vals1: List[np.ndarray] = []

    for s, Z in zip(states_list, Z_list):
        s = np.asarray(s, dtype=int)
        z = np.asarray(Z, dtype=float).reshape(len(s), -1)
        z1 = z[:, 0]
        vals0.append(z1[s == 0])
        vals1.append(z1[s == 1])

    v0 = np.concatenate([a for a in vals0 if a.size > 0], axis=0) if any(a.size > 0 for a in vals0) else np.array([])
    v1 = np.concatenate([a for a in vals1 if a.size > 0], axis=0) if any(a.size > 0 for a in vals1) else np.array([])

    m0 = float(v0.mean()) if v0.size else np.inf
    m1 = float(v1.mean()) if v1.size else -np.inf

    if m0 <= m1:
        mapping = {0: 0, 1: 1}
    else:
        mapping = {0: 1, 1: 0}

    states_canon: List[np.ndarray] = []
    for s in states_list:
        s = np.asarray(s, dtype=int)
        states_canon.append(np.vectorize(mapping.get)(s))

    return states_canon, mapping, (m0, m1)


# ============================================================
# 4) Switching probability metrics
# ============================================================

def flip_rate(s: np.ndarray) -> float:
    s = np.asarray(s, dtype=int)
    if len(s) < 2:
        return 0.0
    return float((s[1:] != s[:-1]).mean())


def p_sample_from_p_win(p_win: float, hop: int) -> float:
    hop = max(int(hop), 1)
    p_win = float(np.clip(p_win, 0.0, 1.0))
    return float(1.0 - (1.0 - p_win) ** (1.0 / hop))


def estimate_p_win_and_p_sample(states_win: np.ndarray, hop: int) -> Tuple[float, float]:
    p_win = flip_rate(states_win)
    p_samp = p_sample_from_p_win(p_win, hop=hop)
    return p_win, p_samp


# ============================================================
# 5) Data loading + feature building for specific segments
# ============================================================

def _load_with_history(path: str) -> np.ndarray:
    wh = np.load(path)
    if wh.ndim != 3 or wh.shape[2] != 1:
        raise ValueError(f"Expected shape [N, T, 1], got {wh.shape} from {path}")
    return wh


def build_features_true_history(
    true_path: str,
    fs: float,
    L: int,
    win: int,
    hop: int,
    min_windows: int,
) -> Tuple[np.ndarray, List[int], List[np.ndarray], np.ndarray]:
    wh = _load_with_history(true_path)
    if wh.shape[1] < L:
        raise ValueError(f"Time dim too short: got {wh.shape[1]} < L={L}")

    Z_list: List[np.ndarray] = []
    lengths: List[int] = []
    keep_ids: List[int] = []

    for n in range(wh.shape[0]):
        y = wh[n, 0:L, 0]
        Z, _ = windowed_welch_domfreq(y, fs=fs, win=win, hop=hop)
        if Z.shape[0] < min_windows:
            continue
        Z_list.append(Z)
        lengths.append(int(Z.shape[0]))
        keep_ids.append(n)

    if len(Z_list) == 0:
        raise RuntimeError("No sequences produced enough HISTORY windows. Reduce win/hop or min_windows.")

    Z_all = np.vstack(Z_list)
    return Z_all, lengths, Z_list, np.asarray(keep_ids, dtype=int)


def build_features_pred_future_for_kept(
    pred_path: str,
    keep_ids: np.ndarray,
    fs: float,
    L: int,
    H: int,
    win: int,
    hop: int,
    min_windows: int,
) -> Tuple[np.ndarray, List[int], List[np.ndarray], np.ndarray]:
    wh = _load_with_history(pred_path)
    if wh.shape[1] < (L + H):
        raise ValueError(f"Time dim too short: got {wh.shape[1]} < L+H={L+H}")

    Z_list: List[np.ndarray] = []
    lengths: List[int] = []
    keep_out: List[int] = []

    for n in keep_ids.tolist():
        y = wh[n, L:L + H, 0]
        Z, _ = windowed_welch_domfreq(y, fs=fs, win=win, hop=hop)
        if Z.shape[0] < min_windows:
            continue
        Z_list.append(Z)
        lengths.append(int(Z.shape[0]))
        keep_out.append(int(n))

    if len(Z_list) == 0:
        raise RuntimeError("No kept sequences produced enough FUTURE windows. Reduce win/hop or min_windows.")

    Z_all = np.vstack(Z_list)
    return Z_all, lengths, Z_list, np.asarray(keep_out, dtype=int)


# ============================================================
# 6) CONTINUOUS Gaussian metrics + figure
# ============================================================

def kl_gaussian_1d(mu0: float, s0: float, mu1: float, s1: float) -> float:
    """
    KL( N0 || N1 ) for 1D Gaussians.
    """
    s0 = max(float(s0), 1e-12)
    s1 = max(float(s1), 1e-12)
    return float(np.log(s1 / s0) + (s0**2 + (mu0 - mu1)**2) / (2.0 * s1**2) - 0.5)


def continuous_jsd_and_tv_and_overlap(
    mu_t: float, s_t: float,
    mu_p: float, s_p: float,
    grid_points: int = 5000,
    tail_std: float = 8.0,
) -> Dict[str, float]:
    """
    Compute continuous metrics via numerical quadrature on a dense grid:
      - overlap = ∫ min(f_t, f_p)
      - TV      = 0.5 ∫ |f_t - f_p|
      - JSD     = 0.5 KL(f_t || m) + 0.5 KL(f_p || m), m = 0.5 f_t + 0.5 f_p
    """
    s_t = max(float(s_t), 1e-12)
    s_p = max(float(s_p), 1e-12)

    # Choose integration range covering both distributions
    left = min(mu_t - tail_std * s_t, mu_p - tail_std * s_p)
    right = max(mu_t + tail_std * s_t, mu_p + tail_std * s_p)
    x = np.linspace(left, right, int(grid_points))

    ft = norm.pdf(x, loc=mu_t, scale=s_t)
    fp = norm.pdf(x, loc=mu_p, scale=s_p)
    m = 0.5 * (ft + fp)

    # Overlap and TV
    overlap = float(np.trapz(np.minimum(ft, fp), x))
    tv = float(0.5 * np.trapz(np.abs(ft - fp), x))

    # Continuous JSD via quadrature of KL terms
    eps = 1e-300
    kl_t_m = float(np.trapz(ft * (np.log(ft + eps) - np.log(m + eps)), x))
    kl_p_m = float(np.trapz(fp * (np.log(fp + eps) - np.log(m + eps)), x))
    jsd = float(0.5 * kl_t_m + 0.5 * kl_p_m)

    return {"overlap": overlap, "tv": tv, "jsd": jsd}


def plot_gaussian_overlap(
    x_true: np.ndarray,
    x_pred: np.ndarray,
    title: str,
    save_path: str | None = None,
    grid_points: int = 5000,
):
    """
    Fit Gaussians to samples and plot the two PDFs + overlap shading.
    Also computes continuous overlap, TV, JSD, and closed-form Gaussian KLs.
    """
    x_true = np.asarray(x_true, dtype=float)
    x_pred = np.asarray(x_pred, dtype=float)

    mu_t, s_t = float(x_true.mean()), float(x_true.std(ddof=0))
    mu_p, s_p = float(x_pred.mean()), float(x_pred.std(ddof=0))

    # Continuous metrics
    cont = continuous_jsd_and_tv_and_overlap(mu_t, s_t, mu_p, s_p, grid_points=grid_points)

    # Closed-form Gaussian KLs
    kl_PQ = kl_gaussian_1d(mu_t, s_t, mu_p, s_p)
    kl_QP = kl_gaussian_1d(mu_p, s_p, mu_t, s_t)
    kl_sym = kl_PQ + kl_QP

    # Plot range
    left = min(mu_t - 6 * s_t, mu_p - 6 * s_p)
    right = max(mu_t + 6 * s_t, mu_p + 6 * s_p)
    x = np.linspace(left, right, grid_points)

    ft = norm.pdf(x, loc=mu_t, scale=max(s_t, 1e-12))
    fp = norm.pdf(x, loc=mu_p, scale=max(s_p, 1e-12))

    plt.figure(figsize=(11, 5))
    plt.plot(x, ft, linewidth=2, label=f"TRUE N({mu_t:.3f}, {s_t:.3f})")
    plt.plot(x, fp, linewidth=2, label=f"PRED N({mu_p:.3f}, {s_p:.3f})")
    plt.fill_between(x, np.minimum(ft, fp), alpha=0.35, label=f"Overlap ≈ {cont['overlap']:.3f}")
    plt.axvline(mu_t, linestyle="--", linewidth=2)
    plt.axvline(mu_p, linestyle="--", linewidth=2)

    txt = (
        f"Overlap = {cont['overlap']:.3f}  (1=identical, 0=disjoint)\n"
        f"TV = {cont['tv']:.3f}\n"
        f"JSD = {cont['jsd']:.3f}\n"
        f"KL(P||Q)={kl_PQ:.3f}, KL(Q||P)={kl_QP:.3f}, KL_sym={kl_sym:.3f}"
    )
    plt.gca().text(0.02, 0.98, txt, transform=plt.gca().transAxes, va="top", ha="left")

    plt.title(title)
    plt.xlabel("Switching probability")
    plt.ylabel("Density")
    plt.legend(loc="upper right")
    plt.tight_layout()

    if save_path is not None:
        plt.savefig(save_path, dpi=200, bbox_inches="tight")
    plt.show()

    return {
        "mu_true": mu_t, "std_true": s_t,
        "mu_pred": mu_p, "std_pred": s_p,
        "overlap": cont["overlap"],
        "tv": cont["tv"],
        "jsd": cont["jsd"],
        "kl_PQ": kl_PQ,
        "kl_QP": kl_QP,
        "kl_sym": kl_sym,
    }


# ============================================================
# 7) End-to-end runner
# ============================================================

@dataclass
class ProbeConfig:
    fs: float = 10.0
    L: int = 50
    H: int = 100
    win: int = 16
    hop: int = 4
    min_windows: int = 5
    hmm_n_iter: int = 800
    hmm_tol: float = 1e-4
    hmm_seeds: Tuple[int, ...] = (0, 1, 2)
    make_plots: bool = True
    plot_dir: str | None = None  # if None, saves into root
    grid_points: int = 5000


def run_truehist_probe_compare_predfut(root: str, cfg: ProbeConfig) -> Dict[str, Any]:
    true_path = os.path.join(root, "test_true_with_history.npy")
    pred_path = os.path.join(root, "test_pred_with_history.npy")

    # --- TRUE HISTORY features for probe training ---
    Z_true_all, len_true, Z_true_list, keep_true = build_features_true_history(
        true_path=true_path,
        fs=cfg.fs,
        L=cfg.L,
        win=cfg.win,
        hop=cfg.hop,
        min_windows=cfg.min_windows,
    )

    # Fit global HMM probe on TRUE HISTORY only
    hmm_model, best_score, norm_stats = fit_global_hmm_2state(
        Z_all=Z_true_all,
        lengths=len_true,
        n_iter=cfg.hmm_n_iter,
        tol=cfg.hmm_tol,
        seeds=cfg.hmm_seeds,
    )

    # Decode TRUE HISTORY with probe
    s_true_raw = decode_with_fitted_hmm(hmm_model, Z_true_all, len_true, norm_stats)

    # Canonicalize labels based on TRUE HISTORY feature means
    s_true, mapping, (m0_raw, m1_raw) = canonicalize_states_by_feature_means(s_true_raw, Z_true_list)

    # --- PRED FUTURE features for evaluation ---
    Z_pred_all, len_pred, Z_pred_list, keep_both = build_features_pred_future_for_kept(
        pred_path=pred_path,
        keep_ids=keep_true,
        fs=cfg.fs,
        L=cfg.L,
        H=cfg.H,
        win=cfg.win,
        hop=cfg.hop,
        min_windows=cfg.min_windows,
    )

    # Align if some sequences dropped
    if keep_both.shape[0] != keep_true.shape[0]:
        pos = {int(idx): i for i, idx in enumerate(keep_true.tolist())}
        sel = [pos[int(idx)] for idx in keep_both.tolist()]
        s_true = [s_true[i] for i in sel]
        keep_true = keep_both

    # Decode PRED FUTURE with SAME probe + SAME normalization
    s_pred_raw = decode_with_fitted_hmm(hmm_model, Z_pred_all, len_pred, norm_stats)
    s_pred = [np.vectorize(mapping.get)(np.asarray(s, dtype=int)) for s in s_pred_raw]

    # --- Per-sequence switching probabilities ---
    p_win_true_hist: List[float] = []
    p_samp_true_hist: List[float] = []
    p_win_pred_fut: List[float] = []
    p_samp_pred_fut: List[float] = []

    for st, sp in zip(s_true, s_pred):
        pw_t, ps_t = estimate_p_win_and_p_sample(st, hop=cfg.hop)
        pw_p, ps_p = estimate_p_win_and_p_sample(sp, hop=cfg.hop)
        p_win_true_hist.append(pw_t)
        p_samp_true_hist.append(ps_t)
        p_win_pred_fut.append(pw_p)
        p_samp_pred_fut.append(ps_p)

    p_win_true_hist = np.asarray(p_win_true_hist, dtype=float)
    p_samp_true_hist = np.asarray(p_samp_true_hist, dtype=float)
    p_win_pred_fut = np.asarray(p_win_pred_fut, dtype=float)
    p_samp_pred_fut = np.asarray(p_samp_pred_fut, dtype=float)

    summary = {
        "N_kept": int(len(keep_true)),
        "p_win_true_hist_mean": float(p_win_true_hist.mean()),
        "p_win_true_hist_std": float(p_win_true_hist.std(ddof=0)),
        "p_win_pred_fut_mean": float(p_win_pred_fut.mean()),
        "p_win_pred_fut_std": float(p_win_pred_fut.std(ddof=0)),
        "delta_mean_p_win": float(p_win_pred_fut.mean() - p_win_true_hist.mean()),
        "p_samp_true_hist_mean": float(p_samp_true_hist.mean()),
        "p_samp_true_hist_std": float(p_samp_true_hist.std(ddof=0)),
        "p_samp_pred_fut_mean": float(p_samp_pred_fut.mean()),
        "p_samp_pred_fut_std": float(p_samp_pred_fut.std(ddof=0)),
        "delta_mean_p_samp": float(p_samp_pred_fut.mean() - p_samp_true_hist.mean()),
    }

    print("========================================")
    print("GLOBAL HMM PROBE (fit TRUE HISTORY) | compare TRUE-HIST vs PRED-FUT")
    print("----------------------------------------")
    print(f"root: {root}")
    print(f"fs={cfg.fs} win={cfg.win} hop={cfg.hop} | L={cfg.L} H={cfg.H}")
    print(f"Used sequences:               {summary['N_kept']}")
    print(f"Total windows (TRUE-HIST):    {int(Z_true_all.shape[0])}")
    print(f"Total windows (PRED-FUT):     {int(Z_pred_all.shape[0])}")
    print(f"Best log-likelihood (TRUE):   {best_score:.6f}")
    print(f"Canonical mapping (old->new): {mapping} | raw state means m0/m1: {m0_raw:.4f}, {m1_raw:.4f}")
    print("----------------------------------------")
    print("p_win  TRUE-HIST mean/std:", summary["p_win_true_hist_mean"], summary["p_win_true_hist_std"])
    print("p_win  PRED-FUT  mean/std:", summary["p_win_pred_fut_mean"], summary["p_win_pred_fut_std"])
    print("Delta mean p_win (PRED-TRUE):", summary["delta_mean_p_win"])
    print("")
    print("p_samp TRUE-HIST mean/std:", summary["p_samp_true_hist_mean"], summary["p_samp_true_hist_std"])
    print("p_samp PRED-FUT  mean/std:", summary["p_samp_pred_fut_mean"], summary["p_samp_pred_fut_std"])
    print("Delta mean p_samp (PRED-TRUE):", summary["delta_mean_p_samp"])
    print("========================================")

    # --- Continuous distribution metrics + plots ---
    plot_paths = {"p_win": None, "p_sample": None}
    metrics = {"p_win": None, "p_sample": None}

    if cfg.make_plots:
        out_dir = cfg.plot_dir if cfg.plot_dir is not None else root
        os.makedirs(out_dir, exist_ok=True)

        plot_paths["p_win"] = os.path.join(out_dir, "gaussian_overlap_pwin_truehist_vs_predfut.png")
        plot_paths["p_sample"] = os.path.join(out_dir, "gaussian_overlap_psample_truehist_vs_predfut.png")

        metrics["p_win"] = plot_gaussian_overlap(
            p_win_true_hist, p_win_pred_fut,
            title="Gaussian approximation of p_win: TRUE history vs PRED future",
            save_path=plot_paths["p_win"],
            grid_points=cfg.grid_points,
        )
        metrics["p_sample"] = plot_gaussian_overlap(
            p_samp_true_hist, p_samp_pred_fut,
            title="Gaussian approximation of p_sample: TRUE history vs PRED future",
            save_path=plot_paths["p_sample"],
            grid_points=cfg.grid_points,
        )

    return {
        "keep_ids": keep_true,
        "hmm": {
            "model": hmm_model,
            "best_score": float(best_score),
            "norm_stats": norm_stats,
            "mapping": mapping,
            "raw_state_feature_means": (float(m0_raw), float(m1_raw)),
        },
        "per_sequence": {
            "p_win_true_hist": p_win_true_hist,
            "p_win_pred_fut": p_win_pred_fut,
            "p_samp_true_hist": p_samp_true_hist,
            "p_samp_pred_fut": p_samp_pred_fut,
        },
        "summary": summary,
        "continuous_metrics": metrics,
        "plot_paths": plot_paths,
        "config": cfg.__dict__.copy(),
    }


# ============================================================
# 8) Example usage
# ============================================================

if __name__ == "__main__":
    root = "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/long_term_forecast_PatchTST_50_100_PatchTST_PhaseMod_Single_Freq_TwoState_p_0.30000_70_10_20_0.0001_0.0001_15_State"

    cfg = ProbeConfig(
        fs=10.0,
        L=50,
        H=100,
        win=16,
        hop=4,
        min_windows=5,
        hmm_n_iter=800,
        hmm_tol=1e-4,
        hmm_seeds=(0, 1, 2),
        make_plots=True,
        plot_dir=None,
        grid_points=5000,
    )

    results = run_truehist_probe_compare_predfut(root=root, cfg=cfg)
    print("Saved plots:", results["plot_paths"])
    print("Continuous metrics (p_win):", results["continuous_metrics"]["p_win"])
    print("Continuous metrics (p_sample):", results["continuous_metrics"]["p_sample"])