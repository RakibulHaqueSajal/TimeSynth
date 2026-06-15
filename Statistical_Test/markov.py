#!/usr/bin/env python3
"""
Gaussian-overlap HMM-proxy comparison, organized in FAMILY_GROUPS style.

Modified behavior:
- Uses KL thresholding as a decision rule:
    PASS if selected KL < KL_THRESHOLD
    FAIL otherwise

Important:
- This is a threshold / acceptance criterion, NOT a statistical significance test.
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
# Helpers: registry + filesystem
# ============================================================

def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)


def _parse_family(model_name: str) -> str:
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


def subset_registry(REGISTRY, signal: str, families: List[str]) -> Dict[str, Dict[str, List[Tuple[str, str]]]]:
    out = {signal: {}}
    for fam in families:
        if fam in REGISTRY.get(signal, {}):
            out[signal][fam] = REGISTRY[signal][fam]
        else:
            print(f"[WARN] family '{fam}' not in REGISTRY[{signal}]")
    return out


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
    if len(y) < win:
        return np.zeros((0, 1), dtype=float)

    Z: List[float] = []
    for a in range(0, len(y) - win + 1, hop):
        seg = y[a:a + win]
        Z.append(dom_freq_welch(seg, fs=fs, nperseg=win))
    return np.asarray(Z, dtype=float)[:, None]


# ============================================================
# 2) HMM probe
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


def decode_with_fitted_hmm(
    model: GaussianHMM,
    Z_all: np.ndarray,
    lengths: List[int],
    norm_stats: Tuple[np.ndarray, np.ndarray],
) -> List[np.ndarray]:
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
# 4) Gaussian metrics + overlap plots
# ============================================================

def kl_gaussian_1d(mu0: float, s0: float, mu1: float, s1: float) -> float:
    s0 = max(float(s0), 1e-12)
    s1 = max(float(s1), 1e-12)
    return float(np.log(s1 / s0) + (s0**2 + (mu0 - mu1)**2) / (2.0 * s1**2) - 0.5)


def continuous_jsd_tv_overlap(
    mu_t: float,
    s_t: float,
    mu_p: float,
    s_p: float,
    grid_points: int = 5000,
    tail_std: float = 8.0,
):
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


def plot_gaussian_overlap(
    x_true: np.ndarray,
    x_pred: np.ndarray,
    title: str,
    save_path: str,
    grid_points: int = 5000,
):
    x_true = np.asarray(x_true, dtype=float)
    x_pred = np.asarray(x_pred, dtype=float)

    mu_t, s_t = float(x_true.mean()), float(x_true.std(ddof=0))
    mu_p, s_p = float(x_pred.mean()), float(x_pred.std(ddof=0))

    cont = continuous_jsd_tv_overlap(mu_t, s_t, mu_p, s_p, grid_points=grid_points)

    kl_PQ = kl_gaussian_1d(mu_t, s_t, mu_p, s_p)
    kl_QP = kl_gaussian_1d(mu_p, s_p, mu_t, s_t)
    kl_sym = kl_PQ + kl_QP

    left = min(mu_t - 6 * max(s_t, 1e-12), mu_p - 6 * max(s_p, 1e-12))
    right = max(mu_t + 6 * max(s_t, 1e-12), mu_p + 6 * max(s_p, 1e-12))
    x = np.linspace(left, right, int(grid_points))

    ft = norm.pdf(x, loc=mu_t, scale=max(s_t, 1e-12))
    fp = norm.pdf(x, loc=mu_p, scale=max(s_p, 1e-12))

    plt.figure(figsize=(11, 5))
    plt.plot(x, ft, linewidth=2, label=f"TRUE N({mu_t:.3f}, {s_t:.3f})")
    plt.plot(x, fp, linewidth=2, label=f"PRED N({mu_p:.3f}, {s_p:.3f})")
    plt.fill_between(x, np.minimum(ft, fp), alpha=0.35, label=f"Overlap ≈ {cont['overlap']:.3f}")
    plt.axvline(mu_t, linestyle="--", linewidth=2)
    plt.axvline(mu_p, linestyle="--", linewidth=2)

    txt = (
        f"Overlap = {cont['overlap']:.3f}\n"
        f"TV = {cont['tv']:.3f}\n"
        f"JSD = {cont['jsd']:.3f}\n"
        f"KL(P||Q) = {kl_PQ:.4f}\n"
        f"KL(Q||P) = {kl_QP:.4f}\n"
        f"KL_sym = {kl_sym:.4f}"
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
        "mu_true": mu_t,
        "std_true": s_t,
        "mu_pred": mu_p,
        "std_pred": s_p,
        "overlap": cont["overlap"],
        "tv": cont["tv"],
        "jsd": cont["jsd"],
        "kl_PQ": kl_PQ,
        "kl_QP": kl_QP,
        "kl_sym": kl_sym,
    }


# ============================================================
# 5) End-to-end single-run execution
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


def run_one_model(
    root: str,
    out_dir: str,
    cfg: ProbeConfig,
    kl_metric_name: str,
    kl_threshold: float,
) -> Dict[str, Any]:
    true_path = os.path.join(root, "test_true_with_history.npy")
    pred_path = os.path.join(root, "test_pred_with_history.npy")

    if (not os.path.exists(true_path)) or (not os.path.exists(pred_path)):
        raise FileNotFoundError(
            f"Missing npy in {root}: need test_true_with_history.npy and test_pred_with_history.npy"
        )

    ensure_dir(out_dir)

    true = _squeeze_wh(np.load(true_path, mmap_mode="r"))
    pred = _squeeze_wh(np.load(pred_path, mmap_mode="r"))

    if true.shape != pred.shape:
        raise ValueError(f"TRUE and PRED shapes differ: {true.shape} vs {pred.shape}")

    N, T = true.shape
    if T < (cfg.L + cfg.H):
        raise ValueError(f"T too small: T={T} < L+H={cfg.L+cfg.H}")

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
        raise RuntimeError("No eligible sequences for TRUE HISTORY.")

    Z_true_all = np.vstack(Z_true_list)

    hmm, best_score, norm_stats = fit_global_hmm_2state(
        Z_all=Z_true_all,
        lengths=len_true,
        n_iter=cfg.hmm_n_iter,
        tol=cfg.hmm_tol,
        seeds=cfg.hmm_seeds,
    )

    s_true_raw = decode_with_fitted_hmm(hmm, Z_true_all, len_true, norm_stats)
    s_true, mapping, (m0_raw, m1_raw) = canonicalize_states_by_feature_means(s_true_raw, Z_true_list)

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
        raise RuntimeError("No eligible sequences for PRED FUTURE.")

    if len(keep2) != len(keep_ids):
        pos = {idx: i for i, idx in enumerate(keep_ids)}
        sel = [pos[idx] for idx in keep2]
        s_true = [s_true[i] for i in sel]

    keep_ids = keep2
    Z_pred_all = np.vstack(Z_pred_list)

    s_pred_raw = decode_with_fitted_hmm(hmm, Z_pred_all, len_pred, norm_stats)
    s_pred = [np.vectorize(mapping.get)(np.asarray(s, dtype=int)) for s in s_pred_raw]

    p_win_true, p_samp_true, p_win_pred, p_samp_pred = [], [], [], []
    for st, sp in zip(s_true, s_pred):
        pw_t, ps_t = estimate_p_win_and_p_sample(st, hop=cfg.hop)
        pw_p, ps_p = estimate_p_win_and_p_sample(sp, hop=cfg.hop)
        p_win_true.append(pw_t)
        p_samp_true.append(ps_t)
        p_win_pred.append(pw_p)
        p_samp_pred.append(ps_p)

    p_win_true = np.asarray(p_win_true, dtype=float)
    p_samp_true = np.asarray(p_samp_true, dtype=float)
    p_win_pred = np.asarray(p_win_pred, dtype=float)
    p_samp_pred = np.asarray(p_samp_pred, dtype=float)

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

    if kl_metric_name not in met_pwin:
        raise KeyError(f"Unknown KL metric '{kl_metric_name}'. Choose from kl_PQ, kl_QP, kl_sym")

    chosen_kl_pwin = float(met_pwin[kl_metric_name])
    chosen_kl_psam = float(met_psam[kl_metric_name])

    pass_pwin = bool(chosen_kl_pwin < kl_threshold)
    pass_psam = bool(chosen_kl_psam < kl_threshold)

    np.savez_compressed(
        os.path.join(out_dir, "metrics.npz"),
        p_win_true=p_win_true,
        p_win_pred=p_win_pred,
        p_samp_true=p_samp_true,
        p_samp_pred=p_samp_pred,
        met_pwin=np.array([met_pwin], dtype=object),
        met_psam=np.array([met_psam], dtype=object),
        hmm_best_score=float(best_score),
        mapping=np.array([mapping], dtype=object),
        raw_state_feature_means=np.array([m0_raw, m1_raw], dtype=float),
        cfg=np.array([cfg.__dict__], dtype=object),
        root=root,
        kl_metric_name=kl_metric_name,
        kl_threshold=float(kl_threshold),
        pwin_pass_threshold=pass_pwin,
        psam_pass_threshold=pass_psam,
    )

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
        "pwin_kl_PQ": float(met_pwin["kl_PQ"]),
        "pwin_kl_QP": float(met_pwin["kl_QP"]),
        "pwin_kl_sym": float(met_pwin["kl_sym"]),
        "psam_kl_PQ": float(met_psam["kl_PQ"]),
        "psam_kl_QP": float(met_psam["kl_QP"]),
        "psam_kl_sym": float(met_psam["kl_sym"]),
        "chosen_kl_metric": kl_metric_name,
        "chosen_kl_pwin": chosen_kl_pwin,
        "chosen_kl_psam": chosen_kl_psam,
        "pwin_pass_threshold": pass_pwin,
        "psam_pass_threshold": pass_psam,
        "out_dir": out_dir,
    }


# ============================================================
# 6) Group-level plots
# ============================================================

def plot_bars(names: List[str], values: List[float], ylabel: str, title: str, save_path: str, threshold: float = None):
    x = np.arange(len(names))
    plt.figure(figsize=(max(10, 0.65 * len(names)), 4.8))
    plt.bar(x, values)
    if threshold is not None:
        plt.axhline(threshold, linestyle="--", linewidth=2)
    plt.xticks(x, names, rotation=45, ha="right")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches="tight")
    plt.close()


### HeatMap: KL Divergence across models and probability levels

def plot_kl_heatmap(rows_by_p: Dict[float, List[Dict]], group_name: str, save_path: str):
    """Heatmap showing KL values for each model at each probability level."""
    prob_levels = sorted(rows_by_p.keys())
    all_rows = [r for rows in rows_by_p.values() for r in rows if "chosen_kl_pwin" in r]
    
    if not all_rows:
        return
    
    families = sorted(set(r["fam"] for r in all_rows))
    kl_matrix = np.full((len(families), len(prob_levels)), np.nan)
    
    for i, fam in enumerate(families):
        for j, p in enumerate(prob_levels):
            matching = [r for r in rows_by_p[p] if r.get("fam") == fam and "chosen_kl_pwin" in r]
            if matching:
                kl_matrix[i, j] = matching[0]["chosen_kl_pwin"]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    im = ax.imshow(kl_matrix, cmap="RdYlGn_r", aspect="auto", vmin=0, vmax=0.15)
    
    ax.set_xticks(np.arange(len(prob_levels)))
    ax.set_yticks(np.arange(len(families)))
    ax.set_xticklabels([f"{p:.2f}" for p in prob_levels])
    ax.set_yticklabels(families)
    ax.set_xlabel("Probability Level")
    ax.set_ylabel("Model Family")
    ax.set_title(f"{group_name}: KL Divergence Heatmap (p_win)")
    
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("KL divergence")
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches="tight")
    plt.close()

### plot pass fail grid 

def plot_pass_fail_grid(rows_by_p: Dict[float, List[Dict]], group_name: str, save_path: str, kl_threshold: float):
    """Publication-quality grid showing PASS/FAIL status for each model at each probability level."""
    import matplotlib.patches as mpatches

    prob_levels = sorted(rows_by_p.keys())
    all_rows = [r for rows in rows_by_p.values() for r in rows if "pwin_pass_threshold" in r]
    families = sorted(set(r["fam"] for r in all_rows))

    # Build pass matrix
    pass_matrix = np.zeros((len(families), len(prob_levels)), dtype=int)
    for i, fam in enumerate(families):
        for j, p in enumerate(prob_levels):
            matching = [r for r in rows_by_p[p] if r.get("fam") == fam]
            if matching and matching[0].get("pwin_pass_threshold", False):
                pass_matrix[i, j] = 1

    # --- Sort models by pass rate (descending), then alphabetically -------
    pass_counts = pass_matrix.sum(axis=1)
    n_probs = len(prob_levels)
    sort_idx = sorted(
        range(len(families)),
        key=lambda i: (-pass_counts[i], families[i]),
    )
    families = [families[i] for i in sort_idx]
    pass_matrix = pass_matrix[sort_idx]
    pass_counts = pass_counts[sort_idx]

    # --- Pass rate per column (summary row) -------------------------------
    col_pass_counts = pass_matrix.sum(axis=0)
    n_models = len(families)

    # --- Figure -----------------------------------------------------------
    fig_h = max(5.5, 0.55 * n_models + 3.0)
    fig, ax = plt.subplots(figsize=(12.0, fig_h), dpi=250)

    # Green = PASS, Red = FAIL
    cmap = plt.cm.colors.ListedColormap(["#EF5350", "#4CAF50"])
    im = ax.imshow(pass_matrix, cmap=cmap, aspect="auto", vmin=0, vmax=1)

    # --- Gridlines --------------------------------------------------------
    for i in range(n_models + 1):
        ax.axhline(i - 0.5, color="#AAAAAA", linewidth=0.8)
    for j in range(n_probs + 1):
        ax.axvline(j - 0.5, color="#AAAAAA", linewidth=0.8)


    # --- Y-axis: model names with pass rate -------------------------------
    y_labels = [
        f"{fam}  ({int(pc)}/{n_probs})"
        for fam, pc in zip(families, pass_counts)
    ]
    ax.set_yticks(np.arange(n_models))
    ax.set_yticklabels(y_labels, fontsize=11, fontweight="bold")
    ax.set_ylabel("Model", fontsize=13, fontweight="bold")

    # --- X-axis: probability levels ---------------------------------------
    ax.set_xticks(np.arange(n_probs))
    ax.set_xticklabels(
        [f"p = {p:.2f}" for p in prob_levels],
        fontsize=10, fontweight="bold",
    )
    ax.set_xlabel(
        "Probability of State Change",
        fontsize=12, fontweight="bold",
    )

    # --- Title ------------------------------------------------------------
    ax.set_title(
        f"Model Robustness Across State Change Probabilities\n"
        f"(KL Threshold = {kl_threshold})",
        fontweight="bold", fontsize=15, pad=14,
    )

    # --- Legend (outside plot) --------------------------------------------
    legend_handles = [
        mpatches.Patch(facecolor="#4CAF50", edgecolor="black", lw=0.8,
                       label="Captured: KL < threshold"),
        mpatches.Patch(facecolor="#EF5350", edgecolor="black", lw=0.8,
                       label="Missed: KL >= threshold"),
        mpatches.Patch(facecolor="none", edgecolor="none", label=""),
        mpatches.Patch(facecolor="none", edgecolor="none",
                       label="Higher p = easier detection"),
        mpatches.Patch(facecolor="none", edgecolor="none",
                       label="Lower p = harder detection"),
    ]
    # Total summary
    total_pass = int(pass_matrix.sum())
    total_cells = n_models * n_probs
    legend_handles.append(mpatches.Patch(facecolor="none", edgecolor="none", label=""))
    legend_handles.append(mpatches.Patch(
        facecolor="none", edgecolor="none",
        label=f"Overall: {total_pass}/{total_cells} ({100*total_pass/total_cells:.0f}%) pass",
    ))

    leg = ax.legend(
        handles=legend_handles,
        title="Legend",
        title_fontsize=12,
        fontsize=10,
        loc="upper left",
        bbox_to_anchor=(1.02, 1.0),
        framealpha=0.95,
        edgecolor="#666666",
        fancybox=True,
        shadow=True,
        borderpad=1.0,
        labelspacing=0.6,
        handlelength=2.0,
        handleheight=1.5,
    )
    leg.get_title().set_fontweight("bold")

    # --- Save -------------------------------------------------------------
    fig.tight_layout()
    fig.savefig(save_path, dpi=250, bbox_inches="tight")
    fig.savefig(os.path.splitext(save_path)[0] + ".pdf", bbox_inches="tight")
    plt.close(fig)

### KL Trend Across Probability

def plot_kl_trends(rows_by_p: Dict[float, List[Dict]], group_name: str, save_path: str, kl_threshold: float):
    """Line plot showing KL divergence trends across probability levels."""
    prob_levels = sorted(rows_by_p.keys())
    all_rows = [r for rows in rows_by_p.values() for r in rows if "chosen_kl_pwin" in r]
    families = sorted(set(r["fam"] for r in all_rows))
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for fam in families:
        kl_vals = []
        for p in prob_levels:
            matching = [r for r in rows_by_p[p] if r.get("fam") == fam and "chosen_kl_pwin" in r]
            if matching:
                kl_vals.append(matching[0]["chosen_kl_pwin"])
            else:
                kl_vals.append(np.nan)
        ax.plot(prob_levels, kl_vals, marker="o", label=fam, linewidth=2)
    
    ax.axhline(kl_threshold, color="red", linestyle="--", linewidth=2, label=f"Threshold ({kl_threshold})")
    ax.set_xlabel("Probability Level")
    ax.set_ylabel("KL Divergence (p_win)")
    ax.set_title(f"{group_name}: KL Trends Across Probability Levels")
    ax.legend(loc="best", fontsize=9)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches="tight")
    plt.close()


### plot param scatter: KL vs p_win_true mean
def plot_param_scatter(rows_by_p: Dict[float, List[Dict]], group_name: str, save_path: str):
    """Scatter plot: mean vs std of Gaussian approximations."""
    all_rows = [r for rows in rows_by_p.values() for r in rows if "pwin_mu_true" in r]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # p_win scatter
    ax1.scatter([r["pwin_mu_true"] for r in all_rows], 
                [r["pwin_mu_pred"] for r in all_rows], 
                s=100, alpha=0.6)
    ax1.plot([0, 1], [0, 1], "k--", alpha=0.5)
    ax1.set_xlabel("TRUE p_win mean")
    ax1.set_ylabel("PRED p_win mean")
    ax1.set_title(f"{group_name}: p_win Mean Comparison")
    ax1.grid(True, alpha=0.3)
    
    # p_sample scatter
    ax2.scatter([r["psam_mu_true"] for r in all_rows], 
                [r["psam_mu_pred"] for r in all_rows], 
                s=100, alpha=0.6, color="orange")
    ax2.plot([0, 1], [0, 1], "k--", alpha=0.5)
    ax2.set_xlabel("TRUE p_sample mean")
    ax2.set_ylabel("PRED p_sample mean")
    ax2.set_title(f"{group_name}: p_sample Mean Comparison")
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches="tight")
    plt.close()

### Plot_kl_boxplot
def plot_kl_boxplot(rows_by_p: Dict[float, List[Dict]], group_name: str, save_path: str):
    """Box plot showing KL distribution for each probability level."""
    prob_levels = sorted(rows_by_p.keys())
    all_rows = [r for rows in rows_by_p.values() for r in rows if "chosen_kl_pwin" in r]
    
    data = [
        [r["chosen_kl_pwin"] for r in rows_by_p[p] if "chosen_kl_pwin" in r]
        for p in prob_levels
    ]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.boxplot(data, labels=[f"{p:.2f}" for p in prob_levels])
    ax.set_xlabel("Probability Level")
    ax.set_ylabel("KL Divergence (p_win)")
    ax.set_title(f"{group_name}: KL Distribution by Probability Level")
    ax.grid(True, alpha=0.3, axis="y")
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=200, bbox_inches="tight")
    plt.close()

# ============================================================
# MAIN
# ============================================================

def main():
    PROB_LEVELS = [0.1, 0.3, 0.5, 0.7, 0.9]
    SIGNAL = "PhaseMod_TwoState"

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

    # -----------------------------
    # DECISION RULE SETTINGS
    # -----------------------------
    KL_METRIC_NAME = "kl_sym"   # choose: "kl_PQ", "kl_QP", "kl_sym"
    KL_THRESHOLD = 0.05

    OUT_ROOT = (
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/"
        "Model_Comparison/Statistical/Markov_Proxy_KL_Thresholding_Grouped/"
    )
    ensure_dir(OUT_ROOT)

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
        # "Linear": ["Linear", "DLinear", "FITS"],
        # "MLinear": ["MLinear", "NBeats", "FreMLP"],
        # "CNN": ["ModernTCN", "MICN_Mean", "MICN_Regre"],
        # "Transformer": ["PatchTST", "Transformer", "Autoformer"],
        # "Best_Models": ["Linear", "PatchTST", "NBeats", "MICN_Mean"],
        # "Best_Exclude_Linear": ["PatchTST", "NBeats", "MICN_Mean"],
        "All_Models": [
            "Linear", "DLinear", "FITS", "MLinear", "NBeats", "FreMLP",
            "ModernTCN", "MICN_Mean", "MICN_Regre", "PatchTST", "Transformer", "Autoformer"
        ],
    }

    for group_name, fam_list in FAMILY_GROUPS.items():
        print("\n==================================================")
        print(f"[GROUP] {group_name} -> {fam_list}")
        print("==================================================")

        group_out_root = os.path.join(OUT_ROOT, group_name)
        ensure_dir(group_out_root)

        REG_GROUP = subset_registry(REGISTRY, SIGNAL, fam_list)
        if not REG_GROUP.get(SIGNAL, {}):
            print(f"[WARN] Empty registry for group={group_name}. Skipping.")
            continue

        models_by_lvl = build_models_by_shift_for_signal(
            REGISTRY=REG_GROUP,
            signal=SIGNAL,
            families=fam_list,
            levels=PROB_LEVELS,
        )
        flat = flatten_runs(models_by_lvl, fam_list)

        rows_by_p: Dict[float, List[Dict[str, Any]]] = {float(p): [] for p in PROB_LEVELS}

        for lvl, fam, name, path in flat:
            if path is None:
                print(f"[SKIP] group={group_name} p={lvl} fam={fam}: missing registry entry")
                continue

            lvl_f = float(lvl)
            lvl_tag = f"p_{lvl_f:.5f}"
            model_out_dir = os.path.join(group_out_root, lvl_tag, fam)
            ensure_dir(model_out_dir)

            try:
                print(f"[RUN ] group={group_name} | {lvl_tag} | {fam} | {path}")
                row = run_one_model(
                    root=path,
                    out_dir=model_out_dir,
                    cfg=cfg,
                    kl_metric_name=KL_METRIC_NAME,
                    kl_threshold=KL_THRESHOLD,
                )
                row.update({"group": group_name, "lvl": lvl_f, "fam": fam, "name": name})
                rows_by_p[lvl_f].append(row)
                print(
                    f"[OK  ] chosen_kl_pwin={row['chosen_kl_pwin']:.4f} "
                    f"chosen_kl_psam={row['chosen_kl_psam']:.4f} "
                    f"PASS(pwin)={row['pwin_pass_threshold']} "
                    f"PASS(psam)={row['psam_pass_threshold']}"
                )
            except Exception as e:
                print(f"[FAIL] group={group_name} | {lvl_tag} | {fam} | {path}\n  - {e}")
                rows_by_p[lvl_f].append({
                    "group": group_name,
                    "lvl": lvl_f,
                    "fam": fam,
                    "name": name,
                    "root": path,
                    "error": str(e),
                })

        all_rows_group = []
        for p in sorted(rows_by_p.keys()):
            rows_p = rows_by_p[p]
            all_rows_group.extend(rows_p)

            ok_rows = [r for r in rows_p if "chosen_kl_pwin" in r and "chosen_kl_psam" in r]
            lvl_tag = f"p_{float(p):.5f}"
            out_dir_p = os.path.join(group_out_root, lvl_tag)
            ensure_dir(out_dir_p)

            out_npz = os.path.join(out_dir_p, f"overlap_table_{group_name}_{lvl_tag}.npz")
            np.savez_compressed(
                out_npz,
                rows=np.array(rows_p, dtype=object),
                kl_metric_name=KL_METRIC_NAME,
                kl_threshold=float(KL_THRESHOLD),
            )
            print(f"[OK] Saved group table: {out_npz}")

            if not ok_rows:
                print(f"[WARN] No successful runs for group={group_name} {lvl_tag}, skipping bar charts.")
                continue

            ok_rows = sorted(ok_rows, key=lambda d: d["fam"])
            names = [r["fam"] for r in ok_rows]

            pwin_overlap_vals = [r["pwin_overlap"] for r in ok_rows]
            psam_overlap_vals = [r["psam_overlap"] for r in ok_rows]
            pwin_kl_vals = [r["chosen_kl_pwin"] for r in ok_rows]
            psam_kl_vals = [r["chosen_kl_psam"] for r in ok_rows]

            plot_bars(
                names, pwin_overlap_vals,
                ylabel="Gaussian overlap ∫ min(f_true, f_pred)",
                title=f"{group_name} | p_win overlap | {lvl_tag}",
                save_path=os.path.join(out_dir_p, f"overlap_bar_pwin_{group_name}_{lvl_tag}.png")
            )
            plot_bars(
                names, psam_overlap_vals,
                ylabel="Gaussian overlap ∫ min(f_true, f_pred)",
                title=f"{group_name} | p_sample overlap | {lvl_tag}",
                save_path=os.path.join(out_dir_p, f"overlap_bar_psample_{group_name}_{lvl_tag}.png")
            )
            plot_bars(
                names, pwin_kl_vals,
                ylabel=f"{KL_METRIC_NAME} (p_win)",
                title=f"{group_name} | {KL_METRIC_NAME} on p_win | {lvl_tag}",
                save_path=os.path.join(out_dir_p, f"kl_bar_pwin_{group_name}_{lvl_tag}.png"),
                threshold=KL_THRESHOLD,
            )
            plot_bars(
                names, psam_kl_vals,
                ylabel=f"{KL_METRIC_NAME} (p_sample)",
                title=f"{group_name} | {KL_METRIC_NAME} on p_sample | {lvl_tag}",
                save_path=os.path.join(out_dir_p, f"kl_bar_psample_{group_name}_{lvl_tag}.png"),
                threshold=KL_THRESHOLD,
            )
                        # ...existing bar chart code...
            
            # Add new plots
            plot_kl_heatmap(rows_by_p, group_name, 
                           os.path.join(group_out_root, f"kl_heatmap_{group_name}.png"))
            plot_pass_fail_grid(rows_by_p, group_name,
                              os.path.join(group_out_root, f"passfail_grid_{group_name}.png"),
                              KL_THRESHOLD)
            plot_kl_trends(rows_by_p, group_name,
                          os.path.join(group_out_root, f"kl_trends_{group_name}.png"),
                          KL_THRESHOLD)
            plot_param_scatter(rows_by_p, group_name,
                             os.path.join(group_out_root, f"param_scatter_{group_name}.png"))
            plot_kl_boxplot(rows_by_p, group_name,
                          os.path.join(group_out_root, f"kl_boxplot_{group_name}.png"))

        # --- Save flat CSV for easy re-plotting later -------------------------
        import csv as _csv
        csv_path = os.path.join(group_out_root, f"markov_results_{group_name}.csv")
        csv_fields = [
            "group", "prob_level", "family",
            "chosen_kl_pwin", "chosen_kl_psam",
            "pwin_overlap", "psam_overlap",
            "pwin_mu_true", "pwin_std_true", "pwin_mu_pred", "pwin_std_pred",
            "psam_mu_true", "psam_std_true", "psam_mu_pred", "psam_std_pred",
            "pwin_pass_threshold", "psam_pass_threshold",
        ]
        with open(csv_path, "w", newline="") as fh:
            writer = _csv.DictWriter(fh, fieldnames=csv_fields, extrasaction="ignore")
            writer.writeheader()
            for p in sorted(rows_by_p.keys()):
                for r in rows_by_p[p]:
                    if "chosen_kl_pwin" not in r:
                        continue  # skip failed runs
                    writer.writerow({
                        "group": group_name,
                        "prob_level": f"{p:.2f}",
                        "family": r.get("fam", ""),
                        "chosen_kl_pwin": r.get("chosen_kl_pwin", ""),
                        "chosen_kl_psam": r.get("chosen_kl_psam", ""),
                        "pwin_overlap": r.get("pwin_overlap", ""),
                        "psam_overlap": r.get("psam_overlap", ""),
                        "pwin_mu_true": r.get("pwin_mu_true", ""),
                        "pwin_std_true": r.get("pwin_std_true", ""),
                        "pwin_mu_pred": r.get("pwin_mu_pred", ""),
                        "pwin_std_pred": r.get("pwin_std_pred", ""),
                        "psam_mu_true": r.get("psam_mu_true", ""),
                        "psam_std_true": r.get("psam_std_true", ""),
                        "psam_mu_pred": r.get("psam_mu_pred", ""),
                        "psam_std_pred": r.get("psam_std_pred", ""),
                        "pwin_pass_threshold": r.get("pwin_pass_threshold", ""),
                        "psam_pass_threshold": r.get("psam_pass_threshold", ""),
                    })
        print(f"[OK] Saved CSV for re-plotting: {csv_path}")

        out_npz_all = os.path.join(group_out_root, f"overlap_table_{group_name}_allp.npz")
        np.savez_compressed(
            out_npz_all,
            rows=np.array(all_rows_group, dtype=object),
            kl_metric_name=KL_METRIC_NAME,
            kl_threshold=float(KL_THRESHOLD),
        )
        print(f"[OK] Saved group all-p table: {out_npz_all}")

    print("\nAll done.")


if __name__ == "__main__":
    main()