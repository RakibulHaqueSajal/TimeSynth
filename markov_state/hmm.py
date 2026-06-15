import numpy as np

# ============================================================
# 1) Feature extraction: Welch dominant frequency per window
#    (matches your earlier setup: FS, WIN, STRIDE/HOP, nperseg=WIN)
# ============================================================

def dom_freq_welch(seg, fs, nperseg):
    from scipy.signal import welch
    seg = np.asarray(seg, dtype=float)
    seg = seg - seg.mean()
    nperseg = min(int(nperseg), len(seg))
    f, Pxx = welch(seg, fs=fs, nperseg=nperseg)
    return float(f[np.argmax(Pxx)])

def windowed_welch_domfreq(y, fs, win=16, hop=8):
    """
    y: [T]
    returns:
      Z: [K,1]  (dominant frequency per window)
      centers: [K] (center index in sample coordinates, within y)
    """
    y = np.asarray(y, dtype=float)
    if len(y) < win:
        return np.zeros((0, 1), dtype=float), np.zeros((0,), dtype=int)

    Z, centers = [], []
    for a in range(0, len(y) - win + 1, hop):
        seg = y[a:a + win]
        fd = dom_freq_welch(seg, fs=fs, nperseg=win)
        Z.append(fd)
        centers.append(a + win // 2)

    return np.asarray(Z, dtype=float)[:, None], np.asarray(centers, dtype=int)


# ============================================================
# 2) Global HMM fit on TRUE only
# ============================================================

def fit_global_hmm_2state(Z_all, lengths, n_iter=800, tol=1e-4, seeds=(0,1,2,3,4,5,10,20)):
    from hmmlearn.hmm import GaussianHMM

    Z_all = np.asarray(Z_all, dtype=np.float64)
    lengths = list(map(int, lengths))

    # normalize once (store stats)
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


# ============================================================
# 3) Metrics on decoded states
# ============================================================

def flip_rate(s):
    s = np.asarray(s, dtype=int)
    if len(s) < 2:
        return 0.0
    return float((s[1:] != s[:-1]).mean())

def dwell_lengths(s):
    s = np.asarray(s, dtype=int)
    lens = []
    cur = 1
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            cur += 1
        else:
            lens.append(cur)
            cur = 1
    lens.append(cur)
    return np.asarray(lens, dtype=int)

def transition_matrix_counts(s):
    s = np.asarray(s, dtype=int)
    C = np.zeros((2, 2), dtype=np.int64)
    for a, b in zip(s[:-1], s[1:]):
        C[a, b] += 1
    return C

def transition_matrix_probs(C):
    C = C.astype(float)
    row = C.sum(axis=1, keepdims=True) + 1e-12
    return C / row

def estimate_p_from_window_states(s_win, hop):
    """
    p_win = flip-rate at window-step time.
    Convert to per-sample switching probability:
      p_sample = 1 - (1 - p_win)^(1/hop)
    """
    p_win = flip_rate(s_win)
    hop = max(int(hop), 1)
    p_sample = 1.0 - (1.0 - p_win) ** (1.0 / hop)
    return p_win, p_sample

def aggregate_stats(states_list, hop):
    p_win_list, p_samp_list = [], []
    mean_dwell_list, med_dwell_list = [], []
    C_total = np.zeros((2,2), dtype=np.int64)

    for s in states_list:
        p_win, p_samp = estimate_p_from_window_states(s, hop=hop)
        p_win_list.append(p_win)
        p_samp_list.append(p_samp)

        dw = dwell_lengths(s)
        mean_dwell_list.append(float(dw.mean()))
        med_dwell_list.append(float(np.median(dw)))

        C_total += transition_matrix_counts(s)

    return {
        "p_win_mean": float(np.mean(p_win_list)),
        "p_samp_mean": float(np.mean(p_samp_list)),
        "dwell_mean": float(np.mean(mean_dwell_list)),
        "dwell_median": float(np.mean(med_dwell_list)),
        "C": C_total,
        "P": transition_matrix_probs(C_total),
    }


# ============================================================
# 4) Canonicalize state labels (avoid label swapping)
#    We enforce: state 0 = lower dom-freq, state 1 = higher dom-freq
# ============================================================

def canonicalize_states_by_feature_means(states_list, Z_list):
    """
    states_list: list of [K] ints in {0,1}
    Z_list:      list of [K,1] features aligned to states_list
    Returns:
      states_list_canon, mapping dict old->new
    """
    # collect feature means per raw state label
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

    # want new_state0 = lower mean feature
    if m0 <= m1:
        mapping = {0: 0, 1: 1}
    else:
        mapping = {0: 1, 1: 0}

    out = []
    for s in states_list:
        s = np.asarray(s, dtype=int)
        out.append(np.vectorize(mapping.get)(s))

    return out, mapping, (m0, m1)


# ============================================================
# 5) End-to-end: fit on TRUE, decode TRUE+PRED with SAME model
# ============================================================

def build_features_from_with_history(path, fs, L, H, win, hop, min_windows):
    wh = np.load(path)  # [N, L+H, 1]
    assert wh.ndim == 3 and wh.shape[2] == 1, f"Unexpected shape: {wh.shape}"
    assert wh.shape[1] >= (L + H), f"Expected time dim >= L+H, got {wh.shape[1]} vs {L+H}"

    Z_list, centers_list, keep_ids = [], [], []
    lengths = []

    for n in range(wh.shape[0]):
        y = wh[n, L:L+H, 0]  # future only
        Z, centers = windowed_welch_domfreq(y, fs=fs, win=win, hop=hop)
        if Z.shape[0] < min_windows:
            continue
        Z_list.append(Z)
        centers_list.append(centers)
        lengths.append(int(Z.shape[0]))
        keep_ids.append(n)

    if len(Z_list) == 0:
        raise RuntimeError("No samples produced enough windows. Reduce win/hop or min_windows.")

    Z_all = np.vstack(Z_list)
    return Z_all, lengths, Z_list, centers_list, np.asarray(keep_ids, dtype=int)

def run_truefit_decode_truepred(
    root,
    fs=10,
    L=50,
    H=100,
    win=16,
    hop=8,
    min_windows=5,
    hmm_n_iter=800,
    hmm_tol=1e-4,
    hmm_seeds=(0,1,2,3,4,5,10,20),
):
    true_path = f"{root}/test_true_with_history.npy"
    pred_path = f"{root}/test_pred_with_history.npy"

    # ----- TRUE features -----
    Z_true_all, len_true, Z_true_list, centers_true, keep_true = build_features_from_with_history(
        true_path, fs, L, H, win, hop, min_windows
    )

    # Fit HMM on TRUE only
    model, best_score, norm_stats = fit_global_hmm_2state(
        Z_true_all, len_true, n_iter=hmm_n_iter, tol=hmm_tol, seeds=hmm_seeds
    )

    # Decode TRUE using the fitted model
    s_true_list_raw = decode_with_fitted_hmm(model, Z_true_all, len_true, norm_stats)

    # Canonicalize labels using TRUE features
    s_true_list, mapping, (m0_raw, m1_raw) = canonicalize_states_by_feature_means(
        s_true_list_raw, Z_true_list
    )

    # ----- PRED features (IMPORTANT: use same sample subset as TRUE kept_ids) -----
    wh_pred = np.load(pred_path)
    assert wh_pred.ndim == 3 and wh_pred.shape[2] == 1

    Z_pred_list, len_pred = [], []
    for n in keep_true:
        y = wh_pred[n, L:L+H, 0]
        Z, _ = windowed_welch_domfreq(y, fs=fs, win=win, hop=hop)
        # TRUE filtering guarantees Z has enough windows for these indices
        Z_pred_list.append(Z)
        len_pred.append(int(Z.shape[0]))

    Z_pred_all = np.vstack(Z_pred_list)

    # Decode PRED using the SAME fitted model + SAME normalization
    s_pred_list_raw = decode_with_fitted_hmm(model, Z_pred_all, len_pred, norm_stats)

    # Apply the SAME canonical mapping learned from TRUE
    s_pred_list = [np.vectorize(mapping.get)(np.asarray(s, dtype=int)) for s in s_pred_list_raw]

    # ----- Aggregate stats -----
    stats_true = aggregate_stats(s_true_list, hop=hop)
    stats_pred = aggregate_stats(s_pred_list, hop=hop)

    print("========================================")
    print("GLOBAL HMM (fit on TRUE only) + Welch dom-freq feature")
    print("----------------------------------------")
    print(f"fs={fs} win={win} hop={hop} nperseg=win")
    print(f"Used samples (kept):          {len(keep_true)}")
    print(f"Total windows (TRUE):         {int(Z_true_all.shape[0])}")
    print(f"Total windows (PRED):         {int(Z_pred_all.shape[0])}")
    print(f"Best log-likelihood (TRUE):   {best_score:.6f}")
    print(f"Canonical mapping (old->new): {mapping}  (feature means raw-state0/1: {m0_raw:.4f}, {m1_raw:.4f})")
    print("----------------------------------------")

    print("=== TRUE decoded (same model) ===")
    print("Mean p_win (HMM step):        ", stats_true["p_win_mean"])
    print("Mean p_sample (converted):    ", stats_true["p_samp_mean"])
    print("Mean dwell (HMM steps):       ", stats_true["dwell_mean"])
    print("Median dwell (HMM steps):     ", stats_true["dwell_median"])
    print("Counts:\n", stats_true["C"])
    print("P:\n", stats_true["P"])

    print("\n=== PRED decoded (same model) ===")
    print("Mean p_win (HMM step):        ", stats_pred["p_win_mean"])
    print("Mean p_sample (converted):    ", stats_pred["p_samp_mean"])
    print("Mean dwell (HMM steps):       ", stats_pred["dwell_mean"])
    print("Median dwell (HMM steps):     ", stats_pred["dwell_median"])
    print("Counts:\n", stats_pred["C"])
    print("P:\n", stats_pred["P"])

    print("\n=== Delta (PRED - TRUE) ===")
    print("Delta p_win:                  ", stats_pred["p_win_mean"] - stats_true["p_win_mean"])
    print("Delta p_sample:               ", stats_pred["p_samp_mean"] - stats_true["p_samp_mean"])
    print("========================================")

    return {
        "model": model,
        "norm_stats": norm_stats,
        "keep_ids": keep_true,
        "states_true": s_true_list,
        "states_pred": s_pred_list,
        "stats_true": stats_true,
        "stats_pred": stats_pred,
        "mapping": mapping,
    }


# ============================================================
# 6) Example usage
# ============================================================

if __name__ == "__main__":
    root = "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/long_term_forecast_Linear_50_100_Linear_PhaseMod_Single_Freq_TwoState_p_0.30000_70_10_20_0.001_0.0001_16_Markov"

    results = run_truefit_decode_truepred(
        root=root,
        fs=10,
        L=50,
        H=100,
        win=16,
        hop=8,
        min_windows=5,
        hmm_n_iter=800,
        hmm_tol=1e-4,
        hmm_seeds=(0,1,2,3,4,5,10,20),
    )
