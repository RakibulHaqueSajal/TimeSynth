#!/usr/bin/env python3
"""
Noisy paradigm stats (baseline = Linear), per-signal, per-metric.

You asked for ONLY these two:
  Option A: paired Δ vs Linear at each SNR_Level_k + Holm across models
  Option B: AUC degradation vs k (relative to clean) per sequence, compare AUC vs Linear (paired) + Holm

You will paste your REGISTRY (signal -> family -> [(name, path), ...]) at the bottom.
This script assumes each run folder contains:
  test_true_with_history.npy, test_pred_with_history.npy

Notes:
- Pairing is by sequence index (seq_id = row index).
- For freq/phase we use intersection-valid masks to avoid bias.
"""

import os, re, math, csv
from typing import Dict, List, Tuple, Any, Optional
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple

# -------------------------
# Core helpers
# -------------------------
def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)

def _parse_family(model_name: str) -> str:
    return model_name.split("-", 1)[0]

def _extract_level(name: str, path: str, tag: str) -> int:
    # 1) in NAME
    m = re.search(rf"{tag}[-_ ]?(\d+)", name, flags=re.IGNORECASE)
    if m:
        return int(m.group(1))
    # 2) in PATH
    m = re.search(rf"[_/]{tag}[_-](\d+)", path, flags=re.IGNORECASE)
    if m:
        return int(m.group(1))
    # 3) fallback: trailing "-k"
    m = re.search(r"-([0-9]+)$", name)
    if m:
        return int(m.group(1))
    return 0

def holm_adjust(pvals: np.ndarray) -> np.ndarray:
    pvals = np.asarray(pvals, float)
    m = pvals.size
    order = np.argsort(pvals)
    adj = np.empty(m, float)
    prev = 0.0
    for k, idx in enumerate(order):
        mult = (m - k)
        val = min(1.0, mult * pvals[idx])
        val = max(val, prev)
        adj[idx] = val
        prev = val
    return adj

def _norm_cdf(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2)))

def paired_ttest_normal_approx(d: np.ndarray) -> Tuple[float, float]:
    d = np.asarray(d, float)
    d = d[np.isfinite(d)]
    n = d.size
    if n < 3:
        return np.nan, np.nan
    mu = d.mean()
    sd = d.std(ddof=1)
    if not np.isfinite(sd) or sd == 0:
        if mu == 0:
            return 0.0, 1.0
        return float(np.sign(mu) * np.inf), 0.0
    t = mu / (sd / math.sqrt(n))
    p = 2.0 * (1.0 - _norm_cdf(abs(t)))
    return float(t), float(p)

def mean_ci_95(d: np.ndarray) -> Tuple[float, float, float, float]:
    d = np.asarray(d, float)
    d = d[np.isfinite(d)]
    n = d.size
    if n == 0:
        return np.nan, np.nan, np.nan, np.nan
    mu = d.mean()
    sd = d.std(ddof=1) if n > 1 else 0.0
    se = sd / math.sqrt(n) if n > 1 else 0.0
    lo = mu - 1.96 * se
    hi = mu + 1.96 * se
    return float(mu), float(se), float(lo), float(hi)

# -------------------------
# Metric functions (same logic style you used)
# -------------------------
def _load_true_pred(model_path: str, split="test") -> Tuple[np.ndarray, np.ndarray]:
    t = np.load(os.path.join(model_path, f"{split}_true_with_history.npy"))
    p = np.load(os.path.join(model_path, f"{split}_pred_with_history.npy"))
    if t.ndim == 3:
        t = t.squeeze(-1)
    if p.ndim == 3:
        p = p.squeeze(-1)
    return t, p

def per_series_mae(model_path: str, history_len: int, split="test") -> np.ndarray:
    true, pred = _load_true_pred(model_path, split=split)
    Y = true[:, history_len:]
    YH = pred[:, history_len:]
    return np.mean(np.abs(YH - Y), axis=1)

def _peak_freq_rfft_with_confidence(
    x,
    fs: float,
    drop_dc: bool = True,
    parabolic: bool = True,
    peak_frac_thresh: float = 0.1,
    power_thresh: float = 1e-8,
):
    x = np.asarray(x, float)
    x = x - x.mean()
    n = len(x)
    if n <= 2:
        return 0.0, False
    X = np.fft.rfft(x, n=n)
    P = (np.abs(X) ** 2).astype(float)
    f = np.fft.rfftfreq(n, d=1.0 / fs)
    start = 1 if drop_dc else 0
    total_power = P[start:].sum()
    if total_power <= power_thresh:
        return 0.0, False
    k = start + int(np.argmax(P[start:]))
    if (not parabolic) or k == 0 or k == len(P) - 1:
        f_est = f[k]
    else:
        denom = (P[k - 1] - 2 * P[k] + P[k + 1])
        delta = 0.0 if abs(denom) < 1e-12 else 0.5 * (P[k - 1] - P[k + 1]) / denom
        f_est = (k + delta) * (fs / n)
    peak_power = P[k]
    frac = peak_power / total_power if total_power > 0 else 0.0
    reliable = frac >= peak_frac_thresh
    return float(f_est), bool(reliable)

def per_series_freq_error(
    model_path: str,
    history_len: int,
    fs: float,
    split="test",
    peak_frac_thresh=0.1,
    power_thresh=1e-8,
) -> np.ndarray:
    true, pred = _load_true_pred(model_path, split=split)
    Y = true[:, history_len:]
    YH = pred[:, history_len:]
    N = Y.shape[0]
    out = np.full(N, np.nan, float)
    for i in range(N):
        f_t, ok_t = _peak_freq_rfft_with_confidence(Y[i], fs=fs, peak_frac_thresh=peak_frac_thresh, power_thresh=power_thresh)
        f_p, ok_p = _peak_freq_rfft_with_confidence(YH[i], fs=fs, peak_frac_thresh=peak_frac_thresh, power_thresh=power_thresh)
        if ok_t and ok_p:
            out[i] = abs(f_p - f_t)
    return out

def _analytic_signal_fft(x, pad_factor=2):
    x = np.asarray(x, float)
    n = x.size
    x = x - x.mean()
    pad_factor = 1 if (pad_factor is None or pad_factor < 1) else int(pad_factor)
    n_fft = int(pad_factor * n)
    X = np.fft.fft(x, n=n_fft)
    H = np.zeros(n_fft, float)
    if n_fft % 2 == 0:
        H[0] = 1.0
        H[n_fft // 2] = 1.0
        H[1:n_fft // 2] = 2.0
    else:
        H[0] = 1.0
        H[1:(n_fft + 1) // 2] = 2.0
    z_full = np.fft.ifft(X * H, n=n_fft)
    return z_full[:n]

def _wrap_to_pi(ang):
    ang = np.asarray(ang, float)
    ang_unwrapped = np.unwrap(ang)
    return (ang_unwrapped + np.pi) % (2 * np.pi) - np.pi

def per_series_phase_error(
    model_path: str,
    history_len: int,
    unit: str = "deg",
    split="test",
    amp_frac_thresh: float = 0.2,
) -> np.ndarray:
    true, pred = _load_true_pred(model_path, split=split)
    Y = true[:, history_len:]
    YH = pred[:, history_len:]
    N = Y.shape[0]
    out = np.full(N, np.nan, float)
    to_unit = (lambda a: a) if unit == "rad" else (lambda a: np.degrees(a))
    for i in range(N):
        y = Y[i] - Y[i].mean()
        yh = YH[i] - YH[i].mean()
        zt = _analytic_signal_fft(y)
        zp = _analytic_signal_fft(yh)
        At = np.abs(zt)
        med_amp = np.median(At)
        if not np.isfinite(med_amp) or med_amp == 0:
            continue
        mask = At > (amp_frac_thresh * med_amp)
        if not np.any(mask):
            continue
        phi_t = np.unwrap(np.angle(zt))
        phi_p = np.unwrap(np.angle(zp))
        dphi = _wrap_to_pi(phi_p - phi_t)
        sel = dphi[mask]
        if sel.size == 0:
            continue
        out[i] = float(np.mean(np.abs(to_unit(sel))))
    return out

def compute_metric_vector(metric: str, path: str, history_len: int, fs: float, phase_unit: str) -> np.ndarray:
    if metric == "mae":
        return per_series_mae(path, history_len=history_len)
    if metric == "freq":
        return per_series_freq_error(path, history_len=history_len, fs=fs)
    if metric == "phase":
        return per_series_phase_error(path, history_len=history_len, unit=phase_unit)
    raise ValueError(metric)

# -------------------------
# Registry access: pick run paths at (signal, family, SNR_Level=k)
# -------------------------
def get_paths_for_signal_level(
    REGISTRY: Dict[str, Dict[str, List[Tuple[str, str]]]],
    signal: str,
    families: List[str],
    level: int,
    tag: str = "SNR_Level",
) -> Dict[str, str]:
    """
    Returns {family: path} for the requested signal at SNR_Level=level.
    Picks the first matching entry per family.
    """
    if signal not in REGISTRY:
        raise KeyError(f"signal not in REGISTRY: {signal}")
    out = {}
    missing = []
    for fam in families:
        found = None
        for name, path in REGISTRY[signal].get(fam, []):
            if _extract_level(name, path, tag=tag) == level:
                found = path
                break
        if found is None:
            missing.append(fam)
        else:
            out[fam] = found
    if missing:
        raise KeyError(f"[{signal}] missing families at {tag}={level}: {missing}")
    return out

# -------------------------
# Option A: per SNR level paired Δ vs Linear + Holm
# -------------------------
def optionA_per_level_tests(
    REGISTRY: Dict[str, Dict[str, List[Tuple[str, str]]]],
    signal: str,
    families: List[str],
    baseline: str,
    levels: List[int],
    metric: str,
    history_len: int,
    fs: float,
    phase_unit: str,
    tag: str = "SNR_Level",
) -> pd.DataFrame:
    """
    Returns one big table with rows:
      (signal, metric, level, model, n_paired, delta_mean, ci_lo, ci_hi, p_value, p_holm)

    For freq/phase: intersection-valid across ALL models at that level.
    """
    rows = []
    for lvl in levels:
        fam_to_path = get_paths_for_signal_level(REGISTRY, signal, families, lvl, tag=tag)

        # metric vectors at this level
        vec = {fam: compute_metric_vector(metric, p, history_len, fs, phase_unit) for fam, p in fam_to_path.items()}

        if baseline not in vec:
            raise RuntimeError(f"[{signal}] baseline '{baseline}' missing at level={lvl}")

        # valid mask
        N = vec[baseline].shape[0]
        if metric in ("freq", "phase"):
            valid = np.ones(N, bool)
            for fam in families:
                valid &= np.isfinite(vec[fam])
        else:
            valid = np.isfinite(vec[baseline])

        idx = np.where(valid)[0]
        if idx.size == 0:
            # still emit baseline row as empty so you know it failed
            rows.append(dict(signal=signal, metric=metric, level=lvl, model=baseline,
                             n_paired=0, delta_vs_linear=0.0, ci_lo=np.nan, ci_hi=np.nan,
                             t_approx=np.nan, p_value=np.nan, p_holm=np.nan))
            continue

        base = vec[baseline]

        # baseline row
        rows.append(dict(signal=signal, metric=metric, level=lvl, model=baseline,
                         n_paired=int(idx.size), delta_vs_linear=0.0, ci_lo=0.0, ci_hi=0.0,
                         t_approx=np.nan, p_value=np.nan, p_holm=np.nan))

        pvals = []
        tmp = []  # store non-baseline rows to holm-adjust
        for fam in families:
            if fam == baseline:
                continue
            d = vec[fam][idx] - base[idx]
            mu, se, lo, hi = mean_ci_95(d)
            t, p = paired_ttest_normal_approx(d)
            tmp.append(dict(signal=signal, metric=metric, level=lvl, model=fam,
                            n_paired=int(idx.size), delta_vs_linear=mu, ci_lo=lo, ci_hi=hi,
                            t_approx=t, p_value=p))
            pvals.append(p)

        # holm correction across models at this (signal, metric, lvl)
        pvals = np.asarray(pvals, float)
        p_holm = holm_adjust(pvals) if pvals.size else np.array([])
        for r, ph in zip(tmp, p_holm):
            r["p_holm"] = float(ph)
            rows.append(r)

    df = pd.DataFrame(rows)
    # useful ordering
    df = df.sort_values(["level", "delta_vs_linear"], ascending=[True, True]).reset_index(drop=True)
    return df

# -------------------------
# Option B: AUC degradation vs k (relative to clean) + compare AUC vs Linear
# -------------------------
def optionB_auc_degradation_tests(
    REGISTRY: Dict[str, Dict[str, List[Tuple[str, str]]]],
    signal: str,
    families: List[str],
    baseline: str,
    levels: List[int],          # e.g., [0,1,2,3,4,5,6]
    metric: str,
    history_len: int,
    fs: float,
    phase_unit: str,
    tag: str = "SNR_Level",
    require_all_levels_finite: bool = True,
) -> pd.DataFrame:
    """
    AUC degradation per sequence:
        Delta_{m,i,k} = x_{m,i,k} - x_{m,i,0}
        AUC_{m,i} = mean_{k in levels, k>0}(Delta_{m,i,k})

    Then compare vs Linear:
        g_{m,i} = AUC_{m,i} - AUC_{Linear,i}

    For freq/phase:
      - if require_all_levels_finite=True:
            keep seq i only if finite for ALL models across ALL levels used.
        else:
            keep seq i per-model-pair (baseline+model) across all levels (n differs per model).
    """
    if 0 not in levels:
        raise ValueError("levels must include 0 (Clean) for AUC degradation")

    # load vectors for every level
    vec_by_level: Dict[int, Dict[str, np.ndarray]] = {}
    for lvl in levels:
        fam_to_path = get_paths_for_signal_level(REGISTRY, signal, families, lvl, tag=tag)
        vec_by_level[lvl] = {fam: compute_metric_vector(metric, p, history_len, fs, phase_unit) for fam, p in fam_to_path.items()}

    # sanity N
    N = vec_by_level[0][baseline].shape[0]
    for lvl in levels:
        for fam in families:
            if vec_by_level[lvl][fam].shape[0] != N:
                raise RuntimeError(f"[{signal}] N mismatch at level={lvl}, fam={fam}")

    # compute AUC per family per sequence
    ks = [k for k in levels if k != 0]
    auc = {fam: np.full(N, np.nan, float) for fam in families}

    for fam in families:
        x0 = vec_by_level[0][fam]
        # stack deltas across k>0: shape (len(ks), N)
        D = []
        for k in ks:
            D.append(vec_by_level[k][fam] - x0)
        D = np.vstack(D)  # (K, N)
        auc[fam] = np.nanmean(D, axis=0)

    # build table vs baseline
    rows = []
    # baseline row (AUC delta vs itself = 0)
    rows.append(dict(signal=signal, metric=metric, model=baseline,
                     n_paired=np.nan, delta_auc_vs_linear=0.0, ci_lo=0.0, ci_hi=0.0,
                     t_approx=np.nan, p_value=np.nan, p_holm=np.nan))

    base_auc = auc[baseline]

    tmp = []
    pvals = []

    if metric in ("freq", "phase") and require_all_levels_finite:
        # strict: finite for ALL models across ALL levels (via AUC + baseline AUC)
        valid = np.isfinite(base_auc)
        for fam in families:
            valid &= np.isfinite(auc[fam])
        idx_global = np.where(valid)[0]

        for fam in families:
            if fam == baseline:
                continue
            d = auc[fam][idx_global] - base_auc[idx_global]
            mu, se, lo, hi = mean_ci_95(d)
            t, p = paired_ttest_normal_approx(d)
            tmp.append(dict(signal=signal, metric=metric, model=fam,
                            n_paired=int(idx_global.size),
                            delta_auc_vs_linear=mu, ci_lo=lo, ci_hi=hi, t_approx=t, p_value=p))
            pvals.append(p)

    else:
        # per-model-pair mask (baseline + model)
        for fam in families:
            if fam == baseline:
                continue
            valid = np.isfinite(base_auc) & np.isfinite(auc[fam])
            idx = np.where(valid)[0]
            d = auc[fam][idx] - base_auc[idx]
            mu, se, lo, hi = mean_ci_95(d)
            t, p = paired_ttest_normal_approx(d)
            tmp.append(dict(signal=signal, metric=metric, model=fam,
                            n_paired=int(idx.size),
                            delta_auc_vs_linear=mu, ci_lo=lo, ci_hi=hi, t_approx=t, p_value=p))
            pvals.append(p)

    pvals = np.asarray(pvals, float)
    p_holm = holm_adjust(pvals) if pvals.size else np.array([])
    for r, ph in zip(tmp, p_holm):
        r["p_holm"] = float(ph)
        rows.append(r)

    df = pd.DataFrame(rows)
    df = df.sort_values(["delta_auc_vs_linear"], ascending=True).reset_index(drop=True)
    return df

# -------------------------
# Example "main" (single example)
# -------------------------
if __name__ == "__main__":
    # --------- YOU EDIT THESE ----------
    OUT_DIR   = "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Model_Comparison/Statistical/Noise_Dir"   # change me
    SIGNAL    = "Single_Phase_Modulation"             # single example
    BASELINE  = "Linear"
    FAMILIES  = ["Linear", "PatchTST", "NBeats", "MICN_Mean",  "MICN_Regre", "FreMLP", "Transformer","Autoformer", "MLinear",  "DLinear", "FITS"]  # example subset
    LEVELS    = list(range(0, 7))            # 0..6
    TAG       = "SNR_Level"                  # noisy tag in folder names
    HISTORY   = 50
    FS        = 10.0
    PHASE_UNIT = "deg"
    METRICS   = ["mae", "freq", "phase"]     # run all three
    # -----------------------------------

    ensure_dir(OUT_DIR)

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # PASTE YOUR REGISTRY HERE:
    # REGISTRY: Dict[str, Dict[str, List[Tuple[str, str]]]] = {...}
    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
     # REGISTRY[signal][family] = [(name, path), ...]
    REGISTRY: Dict[str, Dict[str, List[Tuple[str, str]]]] = {}

    def add_family_from_fmt(
        REG: Dict[str, Dict[str, List[Tuple[str, str]]]],
        signal: str,
        family: str,
        name_fmt: str,
        path_fmt: str,
        k_values=(0, 1, 2, 3, 4, 5, 6),
    ):
        REG.setdefault(signal, {}).setdefault(family, [])
        for k in k_values:
            REG[signal][family].append((name_fmt.format(k=k), path_fmt.format(k=k)))

    BASE = (
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/"
        "Time_Series_Forecast/Train_Test_Validation/"
    )

    # -------------------------
    # Drift_Harmonic
    # -------------------------
    add_family_from_fmt(
        REGISTRY, "Drift_Harmonic", "Linear",
        name_fmt="Linear-{k}",
        path_fmt=BASE + "long_term_forecast_Linear_50_100_Linear_Drift_Harmonic_Clean_70_10_20_0.001_0.0001_16_SNR_Level_{k}",
    )

    add_family_from_fmt(
        REGISTRY, "Drift_Harmonic", "NBeats",
        name_fmt="NBeats-{k}",
        path_fmt=BASE + "long_term_forecast_NBeats_50_100_Nbeats_Drift_Harmonic_Clean_70_10_20_0.0001_0.0001_16_SNR_Level_{k}",
    )

    add_family_from_fmt(
        REGISTRY, "Drift_Harmonic", "FreMLP",
        name_fmt="FreMLP-{k}",
        path_fmt=BASE + "long_term_forecast_FreMLP_50_100_FreMLP__Drift_Harmonic_Clean_70_10_20_0.0001_0.0001_16_SNR_Level_{k}",
    )

    add_family_from_fmt(
        REGISTRY, "Drift_Harmonic", "ModernTCN",
        name_fmt="ModernTCN-{k}",
        path_fmt=BASE + "long_term_forecast_ModernTCN_50_100_ModernTCN_Drift_Harmonic_Clean_70_10_20_0.0_0.001_16_SNR_Level_{k}",
    )

    add_family_from_fmt(
        REGISTRY, "Drift_Harmonic", "MICN_Regre",
        name_fmt="MICN_Regre-{k}",
        path_fmt=BASE + "long_term_forecast_MICN_50_100_MICN_Regre_Drift_Harmonic_Clean_70_10_20_0.0001_0.0001_16_SNR_Level_{k}",
    )

    add_family_from_fmt(
        REGISTRY, "Drift_Harmonic", "MICN_Mean",
        name_fmt="MICN_Mean-{k}",
        path_fmt=BASE + "long_term_forecast_MICN_50_100_MICN_Mean_Drift_Harmonic_Clean_70_10_20_0.0001_0.0001_16_SNR_Level_{k}",
    )

    add_family_from_fmt(
        REGISTRY, "Drift_Harmonic", "PatchTST",
        name_fmt="PatchTST-{k}",
        path_fmt=BASE + "long_term_forecast_PatchTST_50_100_PatchTST_Drift_Harmonic_Clean_70_10_20_0.0001_0.0001_15_SNR_Level_{k}",
    )

    add_family_from_fmt(
        REGISTRY, "Drift_Harmonic", "Transformer",
        name_fmt="Transformer-{k}",
        path_fmt=BASE + "long_term_forecast_Transformer_50_100_Transformer_Drift_Harmonic_Clean_70_10_20_0.0001_0.0001_16_SNR_Level_{k}",
    )

    add_family_from_fmt(
        REGISTRY, "Drift_Harmonic", "Autoformer",
        name_fmt="Autoformer-{k}",
        path_fmt=BASE + "long_term_forecast_Autoformer_50_100_Autoformer_Drift_Harmonic_Clean_70_10_20_0.0001_0.0001_16_SNR_Level_{k}",
    )

    add_family_from_fmt(
        REGISTRY, "Drift_Harmonic", "MLinear",
        name_fmt="MLinear-{k}",
        path_fmt=BASE + "long_term_forecast_MLinear_50_100_MLinear_Drift_Harmonic_Clean_70_10_20_0.0001_0.0001_16_SNR_Level_{k}",
    )

    add_family_from_fmt(
        REGISTRY, "Drift_Harmonic", "DLinear",
        name_fmt="DLinear-{k}",
        path_fmt=BASE + "long_term_forecast_DLinear_50_100_DLinear_Drift_Harmonic_Clean_70_10_20_0.001_0.0001_16_SNR_Level_{k}",
    )

    # IMPORTANT FIX: your pasted snippet had FITS pointing to Single_Phase_Modulation; Drift_Harmonic must be Drift_Harmonic
    add_family_from_fmt(
        REGISTRY, "Drift_Harmonic", "FITS",
        name_fmt="FITS-{k}",
        path_fmt=BASE + "long_term_forecast_FITS_50_100_FITS_Drift_Harmonic_Clean_70_10_20_0.001_0.0001_16_SNR_Level_{k}",
    )

    # -------------------------
    # Single_Phase_Modulation
    # -------------------------
    add_family_from_fmt(
        REGISTRY, "Single_Phase_Modulation", "Linear",
        "Linear-{k}",
        BASE + "long_term_forecast_Linear_50_100_Linear_Single_Phase_Modulation_Clean_70_10_20_0.001_0.0001_16_SNR_Level_{k}",
    )
    add_family_from_fmt(
        REGISTRY, "Single_Phase_Modulation", "DLinear",
        "DLinear-{k}",
        BASE + "long_term_forecast_DLinear_50_100_DLinear_Single_Phase_Modulation_Clean_70_10_20_0.001_0.0001_16_SNR_Level_{k}",
    )
    add_family_from_fmt(
        REGISTRY, "Single_Phase_Modulation", "FITS",
        "FITS-{k}",
        BASE + "long_term_forecast_FITS_50_100_FITS_Single_Phase_Modulation_Clean_70_10_20_0.001_0.0001_16_SNR_Level_{k}",
    )
    add_family_from_fmt(
        REGISTRY, "Single_Phase_Modulation", "MLinear",
        "MLinear-{k}",
        BASE + "long_term_forecast_MLinear_50_100_MLinear_Single_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_SNR_Level_{k}",
    )
    add_family_from_fmt(
        REGISTRY, "Single_Phase_Modulation", "NBeats",
        "NBeats-{k}",
        BASE + "long_term_forecast_NBeats_50_100_Nbeats_Single_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_SNR_Level_{k}",
    )
    add_family_from_fmt(
        REGISTRY, "Single_Phase_Modulation", "FreMLP",
        "FreMLP-{k}",
        BASE + "long_term_forecast_FreMLP_50_100_FreMLP__Single_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_SNR_Level_{k}",
    )
    add_family_from_fmt(
        REGISTRY, "Single_Phase_Modulation", "ModernTCN",
        "ModernTCN-{k}",
        BASE + "long_term_forecast_ModernTCN_50_100_ModernTCN_Single_Phase_Modulation_Clean_70_10_20_0.0_0.001_16_SNR_Level_{k}",
    )
    add_family_from_fmt(
        REGISTRY, "Single_Phase_Modulation", "MICN_Regre",
        "MICN_Regre-{k}",
        BASE + "long_term_forecast_MICN_50_100_MICN_Regre_Single_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_SNR_Level_{k}",
    )
    add_family_from_fmt(
        REGISTRY, "Single_Phase_Modulation", "MICN_Mean",
        "MICN_Mean-{k}",
        BASE + "long_term_forecast_MICN_50_100_MICN_Mean_Single_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_SNR_Level_{k}",
    )
    add_family_from_fmt(
        REGISTRY, "Single_Phase_Modulation", "Transformer",
        "Transformer-{k}",
        BASE + "long_term_forecast_Transformer_50_100_Transformer_Single_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_SNR_Level_{k}",
    )
    add_family_from_fmt(
        REGISTRY, "Single_Phase_Modulation", "Autoformer",
        "Autoformer-{k}",
        BASE + "long_term_forecast_Autoformer_50_100_Autoformer_Single_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_SNR_Level_{k}",
    )
    add_family_from_fmt(
        REGISTRY, "Single_Phase_Modulation", "PatchTST",
        "PatchTST-{k}",
        BASE + "long_term_forecast_PatchTST_50_100_PatchTST_Single_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_15_SNR_Level_{k}",
    )

    # -------------------------
    # Dual_Phase_Modulation
    # -------------------------
    add_family_from_fmt(
        REGISTRY, "Dual_Phase_Modulation", "Linear",
        "Linear-{k}",
        BASE + "long_term_forecast_Linear_50_100_Linear_Dual_Phase_Modulation_Clean_70_10_20_0.001_0.0001_16_SNR_Level_{k}",
    )
    add_family_from_fmt(
        REGISTRY, "Dual_Phase_Modulation", "DLinear",
        "DLinear-{k}",
        BASE + "long_term_forecast_DLinear_50_100_DLinear_Dual_Phase_Modulation_Clean_70_10_20_0.001_0.0001_16_SNR_Level_{k}",
    )
    add_family_from_fmt(
        REGISTRY, "Dual_Phase_Modulation", "FITS",
        "FITS-{k}",
        BASE + "long_term_forecast_FITS_50_100_FITS_Dual_Phase_Modulation_Clean_70_10_20_0.001_0.0001_16_SNR_Level_{k}",
    )
    add_family_from_fmt(
        REGISTRY, "Dual_Phase_Modulation", "MLinear",
        "MLinear-{k}",
        BASE + "long_term_forecast_MLinear_50_100_MLinear_Dual_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_SNR_Level_{k}",
    )
    add_family_from_fmt(
        REGISTRY, "Dual_Phase_Modulation", "NBeats",
        "NBeats-{k}",
        BASE + "long_term_forecast_NBeats_50_100_Nbeats_Dual_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_SNR_Level_{k}",
    )
    add_family_from_fmt(
        REGISTRY, "Dual_Phase_Modulation", "FreMLP",
        "FreMLP-{k}",
        BASE + "long_term_forecast_FreMLP_50_100_FreMLP__Dual_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_SNR_Level_{k}",
    )
    add_family_from_fmt(
        REGISTRY, "Dual_Phase_Modulation", "ModernTCN",
        "ModernTCN-{k}",
        BASE + "long_term_forecast_ModernTCN_50_100_ModernTCN_Dual_Phase_Modulation_Clean_70_10_20_0.0_0.001_16_SNR_Level_{k}",
    )
    add_family_from_fmt(
        REGISTRY, "Dual_Phase_Modulation", "MICN_Mean",
        "MICN_Mean-{k}",
        BASE + "long_term_forecast_MICN_50_100_MICN_Mean_Dual_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_SNR_Level_{k}",
    )
    add_family_from_fmt(
        REGISTRY, "Dual_Phase_Modulation", "MICN_Regre",
        "MICN_Regre-{k}",
        BASE + "long_term_forecast_MICN_50_100_MICN_Regre_Dual_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_SNR_Level_{k}",
    )
    add_family_from_fmt(
        REGISTRY, "Dual_Phase_Modulation", "Transformer",
        "Transformer-{k}",
        BASE + "long_term_forecast_Transformer_50_100_Transformer_Dual_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_SNR_Level_{k}",
    )
    add_family_from_fmt(
        REGISTRY, "Dual_Phase_Modulation", "Autoformer",
        "Autoformer-{k}",
        BASE + "long_term_forecast_Autoformer_50_100_Autoformer_Dual_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_SNR_Level_{k}",
    )
    add_family_from_fmt(
        REGISTRY, "Dual_Phase_Modulation", "PatchTST",
        "PatchTST-{k}",
        BASE + "long_term_forecast_PatchTST_50_100_PatchTST_Dual_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_15_SNR_Level_{k}",
    )

# (optional) quick sanity print
# print(REGISTRY.keys())
# print(REGISTRY["Drift_Harmonic"].keys())
# print(REGISTRY["Drift_Harmonic"]["Linear"][:2]) # placeholder so script doesn't crash if you forget

    # --- Option A: per-level tests ---
    for metric in METRICS:
        dfA = optionA_per_level_tests(
            REGISTRY=REGISTRY,
            signal=SIGNAL,
            families=FAMILIES,
            baseline=BASELINE,
            levels=LEVELS,
            metric=metric,
            history_len=HISTORY,
            fs=FS,
            phase_unit=PHASE_UNIT,
            tag=TAG,
        )
        outA = os.path.join(OUT_DIR, f"OptionA_{SIGNAL}_{metric}_per_level.csv")
        dfA.to_csv(outA, index=False)
        print(f"[Option A] wrote: {outA}")

    # --- Option B: AUC degradation vs noise (k>0), compare vs baseline ---
    for metric in METRICS:
        dfB = optionB_auc_degradation_tests(
            REGISTRY=REGISTRY,
            signal=SIGNAL,
            families=FAMILIES,
            baseline=BASELINE,
            levels=LEVELS,
            metric=metric,
            history_len=HISTORY,
            fs=FS,
            phase_unit=PHASE_UNIT,
            tag=TAG,
            require_all_levels_finite=True,   # strict & fair for freq/phase
        )
        outB = os.path.join(OUT_DIR, f"OptionB_{SIGNAL}_{metric}_auc.csv")
        dfB.to_csv(outB, index=False)
        print(f"[Option B] wrote: {outB}")

    print("Done.")