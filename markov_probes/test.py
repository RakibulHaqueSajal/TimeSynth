#!/usr/bin/env python3
"""
Batch HMM-probe dynamics check across MANY models using CONTINUOUS (Gaussian) metrics.

Goal:
- For each model run directory:
  1) Fit ONE global 2-state GaussianHMM probe on TRUE HISTORY (0:L) using Welch dom-freq features.
  2) Decode TRUE HISTORY and PRED FUTURE (L:L+H) using SAME probe.
  3) Compute per-sequence switching stats: p_win and p_sample.
  4) Fit Gaussians to p_win (TRUE vs PRED) and to p_sample (TRUE vs PRED).
  5) Save overlap figures (Gaussian PDFs + shaded overlap) into a NEW directory per model.
- After all models:
  - Produce a bar chart of Gaussian overlap across models (for p_win and p_sample).

Why continuous:
- No histogram binning => no “fake disjoint” artifacts. Uses smooth PDFs and continuous overlap integral.

Outputs:
- Per-model directory:
    gaussian_overlap_pwin_truehist_vs_predfut.png
    gaussian_overlap_psample_truehist_vs_predfut.png
    metrics.npz  (overlap/TV/JSD/KL + means/stds)
- Global summary directory:
    overlap_bar_pwin.png
    overlap_bar_psample.png
    overlap_table.npz (all metrics in a single array of dicts)

Dependencies:
- numpy
- scipy
- hmmlearn
- matplotlib
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from typing import Dict, List, Tuple, Iterable, Any

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
from scipy.stats import norm
from hmmlearn.hmm import GaussianHMM


# ============================================================
# Small utilities (taken from your group-processing style)
# ============================================================

def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)

def _parse_family(model_name: str):
    base = model_name.split("-", 1)[0]
    if "_p_" in base:
        base = base.split("_p_", 1)[0]
    return base

def add_family_from_fmt(
    REGISTRY: Dict[str, Dict[str, List[Tuple[str, str]]]],
    signal: str,
    family: str,
    name_fmt: str,
    path_fmt: str,
    levels=None,
):
    if levels is None:
        levels = [0, 1, 2, 3, 4]
    REGISTRY.setdefault(signal, {}).setdefault(family, [])
    for k in levels:
        if isinstance(k, float):
            k_str = f"{k:.5f}"
        else:
            k_str = f"{k:d}"
        REGISTRY[signal][family].append((name_fmt.format(k=k_str), path_fmt.format(k=k_str)))

def build_models_by_shift_for_signal(
    REGISTRY: Dict[str, Dict[str, List[Tuple[str, str]]]],
    signal: str,
    families: List[str],
    levels: List[Any],
) -> Dict[Any, List[Tuple[str, str]]]:
    if signal not in REGISTRY:
        raise KeyError(f"Unknown signal: {signal}")
    by_lvl: Dict[Any, List[Tuple[str, str]]] = {}
    for lvl in levels:
        token = f"p_{lvl:.5f}" if isinstance(lvl, float) else None
        bucket = []
        for fam in families:
            found = False
            for name, path in REGISTRY[signal].get(fam, []):
                if token is None:
                    found = True
                    bucket.append((name, path))
                    break
                else:
                    if token in name or token in path:
                        found = True
                        bucket.append((name, path))
                        break
            if not found:
                print(f"[WARN] Missing run for fam={fam} at lvl={lvl}")
        if bucket:
            by_lvl[lvl] = bucket
    return by_lvl

def flatten_runs(models_by_lvl: Dict[Any, List[Tuple[str, str]]], families: List[str]):
    """
    Ensures one run per family per level. Returns list of (lvl, fam, name, path).
    """
    out = []
    for lvl, items in models_by_lvl.items():
        chosen = {}
        for name, path in items:
            fam = _parse_family(name)
            if fam in families and fam not in chosen:
                chosen[fam] = (name, path)
        for fam in families:
            if fam in chosen:
                name, path = chosen[fam]
                out.append((lvl, fam, name, path))
            else:
                out.append((lvl, fam, None, None))
    return out

def _squeeze_wh(x: np.ndarray) -> np.ndarray:
    """Accept [N,T] or [N,T,1], return [N,T]."""
    if x.ndim == 3:
        if x.shape[2] != 1:
            raise ValueError(f"Expected last dim=1 for 3D array, got {x.shape}")
        x = x[..., 0]
    if x.ndim != 2:
        raise ValueError(f"Expected 2D after squeeze, got shape {x.shape}")
    return x


# ============================================================
# 1) Feature extraction: Welch dominant frequency per window
# ============================================================

def dom_freq_welch(seg: np.ndarray, fs: float, nperseg: int) -> float:
    seg = np.asarray(seg, dtype=float)
    seg = seg - seg.mean()
    nperseg = min(int(nperseg), len(seg))
    f, Pxx = welch(seg, fs=fs, nperseg=nperseg)
    return float(f[np.argmax(Pxx)])

def windowed_welch_domfreq(y: np.ndarray, fs: float, win: int, hop: int) -> np.ndarray:
    """
    Returns Z: [K,1] dominant frequency per window.
    """
    y = np.asarray(y, dtype=float)
    if len(y) < win:
        return np.zeros((0, 1), dtype=float)

    Z: List[float] = []
    for a in range(0, len(y) - win + 1, hop):
        seg = y[a:a + win]
        Z.append(dom_freq_welch(seg, fs=fs, nperseg=win))
    return np.asarray(Z, dtype=float)[:, None]


# ============================================================
# 2) HMM probe (fit on TRUE HISTORY only) + decode
# ============================================================

def fit_global_hmm_2state(
    Z_all: np.ndarray,
    lengths: List[int],
    n_iter: int,
    tol: float,
    seeds: Iterable[int],
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

def decode_with_fitted_hmm(model: GaussianHMM, Z_all: np.ndarray, lengths: List[int], norm_stats: Tuple[np.ndarray, np.ndarray]) -> List[np.ndarray]:
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

def canonicalize_states_by_feature_means(states_list: List[np.ndarray], Z_list: List[np.ndarray]):
    """
    Canonicalize labels so state 0 = lower mean feature.
    Returns: states_canon, mapping, (m0_raw, m1_raw)
    """
    vals0, vals1 = [], []
    for s, Z in zip(states_list, Z_list):
        s = np.asarray(s, dtype=int)
        z = np.asarray(Z, dtype=float).reshape(len(s), -1)[:, 0]
        vals0.append(z[s == 0])
        vals1.append(z[s == 1])

    v0 = np.concatenate([a for a in vals0 if a.size], axis=0) if any(a.size for a in vals0) else np.array([])
    v1 = np.concatenate([a for a in vals1 if a.size], axis=0) if any(a.size for a in vals1) else np.array([])

    m0 = float(v0.mean()) if v0.size else np.inf
    m1 = float(v1.mean()) if v1.size else -np.inf

    mapping = {0: 0, 1: 1} if (m0 <= m1) else {0: 1, 1: 0}
    states_canon = [np.vectorize(mapping.get)(np.asarray(s, dtype=int)) for s in states_list]
    return states_canon, mapping, (m0, m1)


# ============================================================
# 3) Switching metrics
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
    pw = flip_rate(states_win)
    ps = p_sample_from_p_win(pw, hop=hop)
    return pw, ps


# ============================================================
# 4) Continuous Gaussian metrics + overlap plots
# ============================================================

def kl_gaussian_1d(mu0: float, s0: float, mu1: float, s1: float) -> float:
    s0 = max(float(s0), 1e-12)
    s1 = max(float(s1), 1e-12)
    return float(np.log(s1 / s0) + (s0**2 + (mu0 - mu1)**2) / (2.0 * s1**2) - 0.5)

def continuous_jsd_tv_overlap(mu_t: float, s_t: float, mu_p: float, s_p: float, grid_points: int = 5000, tail_std: float = 8.0):
    """
    Continuous:
      overlap = ∫ min(f_t, f_p) dx
      TV      = 0.5 ∫ |f_t - f_p| dx
      JSD     = 0.5 KL(f_t||m) + 0.5 KL(f_p||m), m = 0.5(f_t + f_p)
    computed by quadrature on a dense grid.
    """
    s_t = max(float(s_t), 1e-12)
    s_p = max(float(s_p), 1e-12)

    left = min(mu_t - tail_std * s_t, mu_p - tail_std * s_p)
    right = max(mu_t + tail_std * s_t, mu_p + tail_std * s_p)
    x = np.linspace(left, right, int(grid_points))

    ft = norm.pdf(x, loc=mu_t, scale=s_t)
    fp = norm.pdf(x, loc=mu_p, scale=s_p)
    m = 0.5 * (ft + fp)

    overlap = float(np.trapz(np.minimum(ft, fp), x))
    tv = float(0.5 * np.trapz(np.abs(ft - fp), x))

    eps = 1e-300
    kl_t_m = float(np.trapz(ft * (np.log(ft + eps) - np.log(m + eps)), x))
    kl_p_m = float(np.trapz(fp * (np.log(fp + eps) - np.log(m + eps)), x))
    jsd = float(0.5 * kl_t_m + 0.5 * kl_p_m)

    return {"overlap": overlap, "tv": tv, "jsd": jsd}

def plot_gaussian_overlap(x_true: np.ndarray, x_pred: np.ndarray, title: str, save_path: str, grid_points: int = 5000):
    """
    Fit Gaussian to samples and plot PDFs + overlap region.
    Returns continuous metrics dict.
    """
    x_true = np.asarray(x_true, dtype=float)
    x_pred = np.asarray(x_pred, dtype=float)

    mu_t, s_t = float(x_true.mean()), float(x_true.std(ddof=0))
    mu_p, s_p = float(x_pred.mean()), float(x_pred.std(ddof=0))

    cont = continuous_jsd_tv_overlap(mu_t, s_t, mu_p, s_p, grid_points=grid_points)

    kl_PQ = kl_gaussian_1d(mu_t, s_t, mu_p, s_p)
    kl_QP = kl_gaussian_1d(mu_p, s_p, mu_t, s_t)
    kl_sym = kl_PQ + kl_QP

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
        f"KL(P||Q)={kl_PQ:.2f}, KL(Q||P)={kl_QP:.2f}, KL_sym={kl_sym:.2f}"
    )
    plt.gca().text(0.02, 0.98, txt, transform=plt.gca().transAxes, va="top", ha="left")

    plt.title(title)
    plt.xlabel("Switching probability")
    plt.ylabel("Density")
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches="tight")
    plt.close()

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
# 5) End-to-end single-run execution (continuous metrics)
# ============================================================

@dataclass
class ProbeConfig:
    fs: float = 10.0
    L: int = 50
    H: int = 100
    win: int = 16
    hop: int = 8
    min_windows: int = 5
    hmm_n_iter: int = 800
    hmm_tol: float = 1e-4
    hmm_seeds: Tuple[int, ...] = (0, 1, 2)
    grid_points: int = 5000

def run_one_model(root: str, out_dir: str, cfg: ProbeConfig) -> Dict[str, Any]:
    """
    Runs probe on one model directory and saves:
      - Gaussian overlap plot for p_win
      - Gaussian overlap plot for p_sample
      - metrics.npz
    Returns a flat dict with key summary metrics for global bar charts.
    """
    true_path = os.path.join(root, "test_true_with_history.npy")
    pred_path = os.path.join(root, "test_pred_with_history.npy")

    if (not os.path.exists(true_path)) or (not os.path.exists(pred_path)):
        raise FileNotFoundError(f"Missing npy in {root}: need test_true_with_history.npy and test_pred_with_history.npy")

    ensure_dir(out_dir)

    # Load arrays
    true = _squeeze_wh(np.load(true_path, mmap_mode="r"))
    pred = _squeeze_wh(np.load(pred_path, mmap_mode="r"))

    if true.shape != pred.shape:
        raise ValueError(f"TRUE and PRED shapes differ: {true.shape} vs {pred.shape}")

    N, T = true.shape
    if T < (cfg.L + cfg.H):
        raise ValueError(f"T too small: T={T} < L+H={cfg.L+cfg.H}")

    # Build TRUE HISTORY features
    Z_true_list: List[np.ndarray] = []
    len_true: List[int] = []
    keep_ids: List[int] = []

    for n in range(N):
        y_hist = true[n, 0:cfg.L]
        Z = windowed_welch_domfreq(y_hist, fs=cfg.fs, win=cfg.win, hop=cfg.hop)
        if Z.shape[0] < cfg.min_windows:
            continue
        Z_true_list.append(Z)
        len_true.append(int(Z.shape[0]))
        keep_ids.append(n)

    if not keep_ids:
        raise RuntimeError("No eligible sequences for TRUE HISTORY. Reduce win/hop/min_windows or check data.")

    Z_true_all = np.vstack(Z_true_list)

    # Fit HMM probe on TRUE HISTORY
    hmm, best_score, norm_stats = fit_global_hmm_2state(
        Z_all=Z_true_all,
        lengths=len_true,
        n_iter=cfg.hmm_n_iter,
        tol=cfg.hmm_tol,
        seeds=cfg.hmm_seeds,
    )

    # Decode TRUE HISTORY
    s_true_raw = decode_with_fitted_hmm(hmm, Z_true_all, len_true, norm_stats)
    s_true, mapping, (m0_raw, m1_raw) = canonicalize_states_by_feature_means(s_true_raw, Z_true_list)

    # Build PRED FUTURE features for SAME keep_ids
    Z_pred_list: List[np.ndarray] = []
    len_pred: List[int] = []
    keep2: List[int] = []

    for n in keep_ids:
        y_fut = pred[n, cfg.L:cfg.L + cfg.H]
        Z = windowed_welch_domfreq(y_fut, fs=cfg.fs, win=cfg.win, hop=cfg.hop)
        if Z.shape[0] < cfg.min_windows:
            continue
        Z_pred_list.append(Z)
        len_pred.append(int(Z.shape[0]))
        keep2.append(n)

    if not keep2:
        raise RuntimeError("No eligible sequences for PRED FUTURE. Reduce win/hop/min_windows or check predictions.")

    # Align TRUE lists if some were dropped in PRED FUTURE
    if len(keep2) != len(keep_ids):
        pos = {idx: i for i, idx in enumerate(keep_ids)}
        sel = [pos[idx] for idx in keep2]
        s_true = [s_true[i] for i in sel]

    keep_ids = keep2
    Z_pred_all = np.vstack(Z_pred_list)

    # Decode PRED FUTURE with SAME probe
    s_pred_raw = decode_with_fitted_hmm(hmm, Z_pred_all, len_pred, norm_stats)
    s_pred = [np.vectorize(mapping.get)(np.asarray(s, dtype=int)) for s in s_pred_raw]

    # Per-sequence p_win/p_sample
    p_win_true, p_samp_true, p_win_pred, p_samp_pred = [], [], [], []
    for st, sp in zip(s_true, s_pred):
        pw_t, ps_t = estimate_p_win_and_p_sample(st, hop=cfg.hop)
        pw_p, ps_p = estimate_p_win_and_p_sample(sp, hop=cfg.hop)
        p_win_true.append(pw_t); p_samp_true.append(ps_t)
        p_win_pred.append(pw_p); p_samp_pred.append(ps_p)

    p_win_true = np.asarray(p_win_true, dtype=float)
    p_samp_true = np.asarray(p_samp_true, dtype=float)
    p_win_pred = np.asarray(p_win_pred, dtype=float)
    p_samp_pred = np.asarray(p_samp_pred, dtype=float)

    # Save Gaussian overlap plots
    pwin_fig = os.path.join(out_dir, "gaussian_overlap_pwin_truehist_vs_predfut.png")
    psam_fig = os.path.join(out_dir, "gaussian_overlap_psample_truehist_vs_predfut.png")

    met_pwin = plot_gaussian_overlap(
        p_win_true, p_win_pred,
        title="Gaussian approximation of p_win: TRUE history vs PRED future",
        save_path=pwin_fig,
        grid_points=cfg.grid_points,
    )
    met_psam = plot_gaussian_overlap(
        p_samp_true, p_samp_pred,
        title="Gaussian approximation of p_sample: TRUE history vs PRED future",
        save_path=psam_fig,
        grid_points=cfg.grid_points,
    )

    # Save metrics for this model
    np.savez_compressed(
        os.path.join(out_dir, "metrics.npz"),
        p_win_true=p_win_true, p_win_pred=p_win_pred,
        p_samp_true=p_samp_true, p_samp_pred=p_samp_pred,
        met_pwin=np.array([met_pwin], dtype=object),
        met_psam=np.array([met_psam], dtype=object),
        hmm_best_score=float(best_score),
        mapping=np.array([mapping], dtype=object),
        raw_state_feature_means=np.array([m0_raw, m1_raw], dtype=float),
        cfg=np.array([cfg.__dict__], dtype=object),
        root=root,
    )

    # Return flat summary for global bar charts
    return {
        "root": root,
        "N_used": int(len(keep_ids)),
        "pwin_overlap": float(met_pwin["overlap"]),
        "psam_overlap": float(met_psam["overlap"]),
        "pwin_mu_true": float(met_pwin["mu_true"]),
        "pwin_mu_pred": float(met_pwin["mu_pred"]),
        "psam_mu_true": float(met_psam["mu_true"]),
        "psam_mu_pred": float(met_psam["mu_pred"]),
        "pwin_jsd": float(met_pwin["jsd"]),
        "psam_jsd": float(met_psam["jsd"]),
        "pwin_tv": float(met_pwin["tv"]),
        "psam_tv": float(met_psam["tv"]),
        "out_dir": out_dir,
    }


# ============================================================
# 6) Global bar charts
# ============================================================

def plot_overlap_bars(names: List[str], values: List[float], title: str, save_path: str):
    x = np.arange(len(names))
    plt.figure(figsize=(max(10, 0.65 * len(names)), 4.8))
    plt.bar(x, values)
    plt.xticks(x, names, rotation=45, ha="right")
    plt.ylabel("Gaussian overlap  ∫ min(f_true, f_pred)")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches="tight")
    plt.close()


# ============================================================
# MAIN: configure registry + batch run
# ============================================================

if __name__ == "__main__":

    # =============================
    # USER SETTINGS
    # =============================
    PROB_LEVELS = [0.3, 0.7]
    SIGNAL = "PhaseMod_TwoState"

    # Probe params (match your evaluation slicing)
    cfg = ProbeConfig(
        fs=10.0,
        L=50,
        H=100,
        win=16,
        hop=8,
        min_windows=5,
        hmm_n_iter=800,
        hmm_tol=1e-4,
        hmm_seeds=(0, 1, 2),
        grid_points=5000,
    )

    # Output root directory (global)
    OUT_DIR = "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Model_Comparison/Markov_Compariosn/Simple_Parameter_Change/hmm_proxy_gaussian_overlap"
    ensure_dir(OUT_DIR)

    # =============================
    # REGISTRY
    # =============================
    REGISTRY: Dict[str, Dict[str, List[Tuple[str, str]]]] = {}

    add_family_from_fmt(
        REGISTRY, SIGNAL, "Linear",
        name_fmt="Linear_p_{k}",
        path_fmt="/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
                 "long_term_forecast_Linear_50_100_Linear_PhaseMod_Single_Freq_TwoState_p_{k}_70_10_20_0.001_0.0001_16_State",
        levels=PROB_LEVELS,
    )
    add_family_from_fmt(
        REGISTRY, SIGNAL, "DLinear",
        name_fmt="DLinear_p_{k}",
        path_fmt="/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
                 "long_term_forecast_DLinear_50_100_DLinear_PhaseMod_Single_Freq_TwoState_p_{k}_70_10_20_0.001_0.0001_16_State",
        levels=PROB_LEVELS,
    )
    add_family_from_fmt(
        REGISTRY, SIGNAL, "FITS",
        name_fmt="FITS_p_{k}",
        path_fmt="/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
                 "long_term_forecast_FITS_50_100_FITS_PhaseMod_Single_Freq_TwoState_p_{k}_70_10_20_0.001_0.0001_16_State",
        levels=PROB_LEVELS,
    )
    add_family_from_fmt(
        REGISTRY, SIGNAL, "MLinear",
        name_fmt="MLinear_p_{k}",
        path_fmt="/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
                 "long_term_forecast_MLinear_50_100_MLinear_PhaseMod_Single_Freq_TwoState_p_{k}_70_10_20_0.0001_0.0001_16_State",
        levels=PROB_LEVELS,
    )
    add_family_from_fmt(
        REGISTRY, SIGNAL, "NBeats",
        name_fmt="NBeats_p_{k}",
        path_fmt="/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
                 "long_term_forecast_NBeats_50_100_NBeats_PhaseMod_Single_Freq_TwoState_p_{k}_70_10_20_0.0001_0.0001_16_State",
        levels=PROB_LEVELS,
    )
    add_family_from_fmt(
        REGISTRY, SIGNAL, "FreMLP",
        name_fmt="FreMLP_p_{k}",
        path_fmt="/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
                 "long_term_forecast_FreMLP_50_100_FreMLP_PhaseMod_Single_Freq_TwoState_p_{k}_70_10_20_0.0001_0.0001_16_State",
        levels=PROB_LEVELS,
    )
    add_family_from_fmt(
        REGISTRY, SIGNAL, "ModernTCN",
        name_fmt="ModernTCN_p_{k}",
        path_fmt="/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
                 "long_term_forecast_ModernTCN_50_100_ModernTCN_PhaseMod_Single_Freq_TwoState_p_{k}_70_10_20_0.0_0.001_16_State",
        levels=PROB_LEVELS,
    )
    add_family_from_fmt(
        REGISTRY, SIGNAL, "MICN_Mean",
        name_fmt="MICN_Mean_p_{k}",
        path_fmt="/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
                 "long_term_forecast_MICN_50_100_MICN_Mean_PhaseMod_Single_Freq_TwoState_p_{k}_70_10_20_0.0001_0.0001_16_State",
        levels=PROB_LEVELS,
    )
    add_family_from_fmt(
        REGISTRY, SIGNAL, "MICN_Regre",
        name_fmt="MICN_Regre_p_{k}",
        path_fmt="/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
                 "long_term_forecast_MICN_50_100_MICN_Regre_PhaseMod_Single_Freq_TwoState_p_{k}_70_10_20_0.0001_0.0001_16_State",
        levels=PROB_LEVELS,
    )
    add_family_from_fmt(
        REGISTRY, SIGNAL, "PatchTST",
        name_fmt="PatchTST_p_{k}",
        path_fmt="/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
                 "long_term_forecast_PatchTST_50_100_PatchTST_PhaseMod_Single_Freq_TwoState_p_{k}_70_10_20_0.0001_0.0001_15_State",
        levels=PROB_LEVELS,
    )
    add_family_from_fmt(
        REGISTRY, SIGNAL, "Transformer",
        name_fmt="Transformer_p_{k}",
        path_fmt="/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
                 "long_term_forecast_Transformer_50_100_Transformer_PhaseMod_Single_Freq_TwoState_p_{k}_70_10_20_0.0001_0.0001_16_State",
        levels=PROB_LEVELS,
    )
    add_family_from_fmt(
        REGISTRY, SIGNAL, "Autoformer",
        name_fmt="Autoformer_p_{k}",
        path_fmt="/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
                 "long_term_forecast_Autoformer_50_100_Autoformer_PhaseMod_Single_Freq_TwoState_p_{k}_70_10_20_0.0001_0.0001_16_State",
        levels=PROB_LEVELS,
    )

    FAMILY_GROUPS = {
        "All": ["Linear","DLinear","FITS","MLinear","NBeats","FreMLP","ModernTCN","MICN_Mean","MICN_Regre","PatchTST","Transformer","Autoformer"],
    }

    # =============================
    # BATCH RUN
    # =============================
    all_rows: List[Dict[str, Any]] = []

    for group_name, families in FAMILY_GROUPS.items():
        print(f"\n==================== GROUP: {group_name} ====================")

        models_by_lvl = build_models_by_shift_for_signal(
            REGISTRY=REGISTRY,
            signal=SIGNAL,
            families=families,
            levels=PROB_LEVELS,
        )
        flat = flatten_runs(models_by_lvl, families)

        for lvl, fam, name, path in flat:
            if path is None:
                print(f"[SKIP] lvl={lvl} fam={fam} : missing registry entry")
                continue

            lvl_tag = f"p_{lvl:.5f}" if isinstance(lvl, float) else f"lvl_{lvl}"
            model_out_dir = os.path.join(OUT_DIR, lvl_tag, fam)
            ensure_dir(model_out_dir)

            try:
                print(f"[RUN ] {lvl_tag} | {fam} | {path}")
                row = run_one_model(root=path, out_dir=model_out_dir, cfg=cfg)
                row.update({"lvl": float(lvl) if isinstance(lvl, float) else lvl, "fam": fam, "name": name})
                all_rows.append(row)
                print(f"[OK  ] overlap(p_win)={row['pwin_overlap']:.3f} overlap(p_sample)={row['psam_overlap']:.3f} | saved -> {model_out_dir}")
            except Exception as e:
                print(f"[FAIL] {lvl_tag} | {fam} | {path}\n  - {e}")
                all_rows.append({
                    "lvl": float(lvl) if isinstance(lvl, float) else lvl,
                    "fam": fam,
                    "name": name,
                    "root": path,
                    "error": str(e),
                })

    # Save global results
    out_npz = os.path.join(OUT_DIR, "overlap_table.npz")
    np.savez_compressed(out_npz, rows=np.array(all_rows, dtype=object))
    print(f"\n[OK] Saved global table: {out_npz}")

    # =============================
    # BAR CHARTS (per prob level)
    # =============================
    # Build per-level plots for p_win and p_sample overlaps
    ok_rows = [r for r in all_rows if "pwin_overlap" in r and "psam_overlap" in r]

    if not ok_rows:
        print("[WARN] No successful runs to plot.")
        sys.exit(2)

    for lvl in sorted({r["lvl"] for r in ok_rows}):
        rows_lvl = [r for r in ok_rows if r["lvl"] == lvl]
        rows_lvl = sorted(rows_lvl, key=lambda d: d["fam"])

        names = [r["fam"] for r in rows_lvl]
        pwin_vals = [r["pwin_overlap"] for r in rows_lvl]
        psam_vals = [r["psam_overlap"] for r in rows_lvl]

        lvl_tag = f"p_{lvl:.5f}" if isinstance(lvl, float) else f"lvl_{lvl}"
        out_dir_lvl = os.path.join(OUT_DIR, lvl_tag)
        ensure_dir(out_dir_lvl)

        p1 = os.path.join(out_dir_lvl, "overlap_bar_pwin.png")
        p2 = os.path.join(out_dir_lvl, "overlap_bar_psample.png")

        plot_overlap_bars(
            names, pwin_vals,
            title=f"Gaussian overlap of p_win (TRUE hist vs PRED fut) | {lvl_tag}",
            save_path=p1
        )
        plot_overlap_bars(
            names, psam_vals,
            title=f"Gaussian overlap of p_sample (TRUE hist vs PRED fut) | {lvl_tag}",
            save_path=p2
        )

        print(f"[OK] Saved bar charts for {lvl_tag}:")
        print(f"  - {p1}")
        print(f"  - {p2}")

    sys.exit(0)