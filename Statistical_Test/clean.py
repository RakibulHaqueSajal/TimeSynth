#!/usr/bin/env python3
"""
Clean paradigm: baseline-contrast paired tests (Linear baseline),
done separately for each signal family (Drift / SPM / DPM).

Why this version
----------------
MixedLM frequently fails (singular covariance / inversion) when:
  - intersection-valid masking leaves few sequences
  - model effects become collinear / near-deterministic
  - random-effect variance collapses

Here we do the statistically correct and stable thing given your setup:
ALL models are tested on the SAME sequences (paired by seq_id).

For each model m and sequence i:
    d_i = metric_{m,i} - metric_{Linear,i}

We report:
  - mean(d)  (negative = model better than Linear)
  - 95% CI on mean(d)
  - paired t-test p-value (normal approx)
  - Holm adjusted p-values across all models vs Linear (per signal, per metric)

For freq/phase, we enforce "intersection-valid" seq_ids per signal:
only seq_ids valid for ALL models are kept to avoid biased comparisons.
"""

import os
import math
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.serif'] = ['Nimbus Roman', 'DejaVu Serif']
from typing import Dict, List, Tuple, Optional


# -------------------------
# USER CONFIG (edit)
# -------------------------
OUT_ROOT = "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Model_Comparison/Statistical/Clean_BaselineVsLinear"

SIGNALS = ["Drift_Harmonic", "Single_Phase_Modulation", "Dual_Phase_Modulation"]

# SIGNALS = ["Single_Phase_Modulation"]
HISTORY_LEN = 50
FS = 10.0
PHASE_UNIT = "deg"

# Must include Linear, plus whatever you want to compare
FAMILIES = [
    "Linear",
    "PatchTST",
    "NBeats",
    "MICN_Mean",
    "ModernTCN",
    "MICN_Regre",
    "FreMLP",
    "Transformer",
    "Autoformer",
    "MLinear",
    "DLinear",
    "FITS",
]

BASELINE = "Linear"


# -------------------------
# You provide this (NO REGISTRY in this file)
# -------------------------
def get_clean_paths_for_signal(signal: str, families: List[str]) -> Dict[str, str]:
    """
    Example implementation using explicit templates.
    Returns {family: path_to_shift0_run} for the requested signal.
    """

    BASE = "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"

    # Map: signal -> family -> format string that already points to Shift_0
    PATHS_SHIFT0: Dict[str, Dict[str, str]] = {
        "Drift_Harmonic": {
            "Linear":      BASE + "long_term_forecast_Linear_50_100_Linear_Drift_Harmonic_Clean_70_10_20_0.001_0.0001_16_Shift_0",
            "PatchTST":    BASE + "long_term_forecast_PatchTST_50_100_PatchTST_Drift_Harmonic_Clean_70_10_20_0.0001_0.0001_15_Shift_0",
            "NBeats":      BASE + "long_term_forecast_NBeats_50_100_Nbeats_Drift_Harmonic_Clean_70_10_20_0.0001_0.0001_16_Shift_0",
            "MICN_Mean":   BASE + "long_term_forecast_MICN_50_100_MICN_Mean_Drift_Harmonic_Clean_70_10_20_0.0001_0.0001_16_Shift_0",
            "ModernTCN":   BASE + "long_term_forecast_ModernTCN_50_100_ModernTCN_Drift_Harmonic_Clean_70_10_20_0.0_0.001_16_Shift_0",
            "Autoformer":  BASE + "long_term_forecast_Autoformer_50_100_Autoformer_Drift_Harmonic_Clean_70_10_20_0.0001_0.0001_16_Shift_0",
            "Transformer": BASE + "long_term_forecast_Transformer_50_100_Transformer_Drift_Harmonic_Clean_70_10_20_0.0001_0.0001_16_Shift_0",
            "DLinear":     BASE + "long_term_forecast_DLinear_50_100_DLinear_Drift_Harmonic_Clean_70_10_20_0.001_0.0001_16_Shift_0",
            "MLinear":     BASE + "long_term_forecast_MLinear_50_100_MLinear_Drift_Harmonic_Clean_70_10_20_0.0001_0.0001_16_Shift_0",
            "FITS":        BASE + "long_term_forecast_FITS_50_100_FITS_Drift_Harmonic_Clean_70_10_20_0.001_0.0001_16_Shift_0",
            "FreMLP":      BASE + "long_term_forecast_FreMLP_50_100_FreMLP__Drift_Harmonic_Clean_70_10_20_0.0001_0.0001_16_Shift_0",
            "MICN_Regre":  BASE + "long_term_forecast_MICN_50_100_MICN_Regre_Drift_Harmonic_Clean_70_10_20_0.0001_0.0001_16_Shift_0",
        },

        "Single_Phase_Modulation": {
            "Linear":      BASE + "long_term_forecast_Linear_50_100_Linear_Single_Phase_Modulation_Clean_70_10_20_0.001_0.0001_16_Shift_0",
            "PatchTST":    BASE + "long_term_forecast_PatchTST_50_100_PatchTST_Single_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_15_Shift_0",
            "NBeats":      BASE + "long_term_forecast_NBeats_50_100_Nbeats_Single_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_0",
            "MICN_Mean":   BASE + "long_term_forecast_MICN_50_100_MICN_Mean_Single_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_0",
            "ModernTCN":   BASE + "long_term_forecast_ModernTCN_50_100_ModernTCN_Single_Phase_Modulation_Clean_70_10_20_0.0_0.001_16_Shift_0",
            "Autoformer":  BASE + "long_term_forecast_Autoformer_50_100_Autoformer_Single_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_0",
            "Transformer": BASE + "long_term_forecast_Transformer_50_100_Transformer_Single_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_0",
            "DLinear":     BASE + "long_term_forecast_DLinear_50_100_DLinear_Single_Phase_Modulation_Clean_70_10_20_0.001_0.0001_16_Shift_0",
            "MLinear":     BASE + "long_term_forecast_MLinear_50_100_MLinear_Single_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_0",
            "FITS":        BASE + "long_term_forecast_FITS_50_100_FITS_Single_Phase_Modulation_Clean_70_10_20_0.001_0.0001_16_Shift_0",
            "FreMLP":      BASE + "long_term_forecast_FreMLP_50_100_FreMLP__Single_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_0",
            "MICN_Regre":  BASE + "long_term_forecast_MICN_50_100_MICN_Regre_Single_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_0",
        },

        "Dual_Phase_Modulation": {
            "Linear":      BASE + "long_term_forecast_Linear_50_100_Linear_Dual_Phase_Modulation_Clean_70_10_20_0.001_0.0001_16_Shift_0",
            "PatchTST":    BASE + "long_term_forecast_PatchTST_50_100_PatchTST_Dual_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_15_Shift_0",
            "NBeats":      BASE + "long_term_forecast_NBeats_50_100_Nbeats_Dual_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_0",
            "MICN_Mean":   BASE + "long_term_forecast_MICN_50_100_MICN_Mean_Dual_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_0",
            "ModernTCN":   BASE + "long_term_forecast_ModernTCN_50_100_ModernTCN_Dual_Phase_Modulation_Clean_70_10_20_0.0_0.001_16_Shift_0",
            "Autoformer":  BASE + "long_term_forecast_Autoformer_50_100_Autoformer_Dual_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_0",
            "Transformer": BASE + "long_term_forecast_Transformer_50_100_Transformer_Dual_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_0",
            "DLinear":     BASE + "long_term_forecast_DLinear_50_100_DLinear_Dual_Phase_Modulation_Clean_70_10_20_0.001_0.0001_16_Shift_0",
            "MLinear":     BASE + "long_term_forecast_MLinear_50_100_MLinear_Dual_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_0",
            "FITS":        BASE + "long_term_forecast_FITS_50_100_FITS_Dual_Phase_Modulation_Clean_70_10_20_0.001_0.0001_16_Shift_0",
            "FreMLP":      BASE + "long_term_forecast_FreMLP_50_100_FreMLP__Dual_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_0",
            "MICN_Regre":  BASE + "long_term_forecast_MICN_50_100_MICN_Regre_Dual_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_0",
        },
    }

    if signal not in PATHS_SHIFT0:
        raise KeyError(f"Unknown signal '{signal}'. Add it to PATHS_SHIFT0.")

    fam_to_path = {}
    missing = []
    for fam in families:
        p = PATHS_SHIFT0[signal].get(fam)
        if p is None:
            missing.append(fam)
        else:
            fam_to_path[fam] = p

    if missing:
        raise KeyError(f"[{signal}] Missing Shift_0 paths for families: {missing}")

    return fam_to_path


# -------------------------
# Helpers
# -------------------------
def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)


def holm_adjust(pvals: np.ndarray) -> np.ndarray:
    """
    Holm step-down adjusted p-values.
    """
    pvals = np.asarray(pvals, float)
    m = pvals.size
    order = np.argsort(pvals)
    adj = np.empty(m, float)
    prev = 0.0
    for k, idx in enumerate(order):
        mult = (m - k)
        val = min(1.0, mult * pvals[idx])
        val = max(val, prev)  # enforce monotonicity
        adj[idx] = val
        prev = val
    return adj


def _norm_cdf(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2)))


def paired_ttest_normal_approx(d: np.ndarray) -> Tuple[float, float]:
    """
    Two-sided paired t-test using normal approximation.
    Returns (t_stat, p_value).

    Notes:
      - If variance=0: either perfect tie (p=1) or constant shift (p=0).
    """
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
    """
    Mean and 95% CI (normal approx) for paired differences.
    Returns (mean, se, ci_lo, ci_hi).
    """
    d = np.asarray(d, float)
    d = d[np.isfinite(d)]
    n = d.size
    if n == 0:
        return np.nan, np.nan, np.nan, np.nan
    mu = d.mean()
    sd = d.std(ddof=1) if n > 1 else 0.0
    se = sd / math.sqrt(n) if n > 1 else 0.0
    ci_lo = mu - 1.96 * se
    ci_hi = mu + 1.96 * se
    return float(mu), float(se), float(ci_lo), float(ci_hi)


# -------------------------
# Metric functions
# -------------------------
def _load_true_pred(model_path: str, split="test") -> Tuple[np.ndarray, np.ndarray]:
    t = np.load(os.path.join(model_path, f"{split}_true_with_history.npy"))
    p = np.load(os.path.join(model_path, f"{split}_pred_with_history.npy"))
    if t.ndim == 3:
        t = t.squeeze(-1)
    if p.ndim == 3:
        p = p.squeeze(-1)
    return t, p


def per_series_mae(model_path: str, split="test", history_len=50) -> np.ndarray:
    true, pred = _load_true_pred(model_path, split=split)
    Y = true[:, history_len:]
    YH = pred[:, history_len:]
    return np.mean(np.abs(YH - Y), axis=1)


def _peak_freq_rfft_with_confidence(
    x,
    fs: float = 1.0,
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
    split="test",
    history_len=50,
    fs=10.0,
    peak_frac_thresh=0.1,
    power_thresh=1e-8,
) -> np.ndarray:
    true, pred = _load_true_pred(model_path, split=split)
    Y = true[:, history_len:]
    YH = pred[:, history_len:]

    N = Y.shape[0]
    out = np.full(N, np.nan, dtype=float)

    for i in range(N):
        f_t, ok_t = _peak_freq_rfft_with_confidence(
            Y[i], fs=fs, peak_frac_thresh=peak_frac_thresh, power_thresh=power_thresh
        )
        f_p, ok_p = _peak_freq_rfft_with_confidence(
            YH[i], fs=fs, peak_frac_thresh=peak_frac_thresh, power_thresh=power_thresh
        )
        if ok_t and ok_p:
            out[i] = abs(f_p - f_t)
    return out


def _analytic_signal_fft(x, pad_factor=2):
    x = np.asarray(x, dtype=float)
    n = x.size
    x = x - x.mean()

    pad_factor = 1 if (pad_factor is None or pad_factor < 1) else int(pad_factor)
    n_fft = int(pad_factor * n)

    X = np.fft.fft(x, n=n_fft)

    H = np.zeros(n_fft, dtype=float)
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
    ang = np.asarray(ang, dtype=float)
    ang_unwrapped = np.unwrap(ang)
    return (ang_unwrapped + np.pi) % (2 * np.pi) - np.pi


def per_series_phase_error(
    model_path: str,
    split="test",
    history_len=50,
    unit="deg",
    amp_frac_thresh=0.2,
) -> np.ndarray:
    true, pred = _load_true_pred(model_path, split=split)
    Y = true[:, history_len:]
    YH = pred[:, history_len:]

    N = Y.shape[0]
    out = np.full(N, np.nan, dtype=float)
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


# -------------------------
# Core: build per-model vectors + valid mask
# -------------------------
def compute_metric_vectors(
    fam_to_path: Dict[str, str],
    metric: str,
    history_len: int,
    fs: float,
    phase_unit: str,
) -> Dict[str, np.ndarray]:
    """
    Returns dict: family -> vector[N] (may include NaNs for freq/phase).
    """
    if metric == "mae":
        fn = lambda p: per_series_mae(p, history_len=history_len)
    elif metric == "freq":
        fn = lambda p: per_series_freq_error(p, history_len=history_len, fs=fs)
    elif metric == "phase":
        fn = lambda p: per_series_phase_error(p, history_len=history_len, unit=phase_unit)
    else:
        raise ValueError(f"Unknown metric={metric}")

    out = {}
    for fam, path in fam_to_path.items():
        out[fam] = np.asarray(fn(path), float)

    # sanity: same N
    Ns = [v.shape[0] for v in out.values()]
    if len(set(Ns)) != 1:
        raise RuntimeError(f"metric={metric}: inconsistent N across models: {Ns}")
    return out


def intersection_valid_mask(vectors: Dict[str, np.ndarray]) -> np.ndarray:
    """
    valid[i] = finite for ALL models
    """
    fams = list(vectors.keys())
    N = vectors[fams[0]].shape[0]
    valid = np.ones(N, dtype=bool)
    for fam in fams:
        valid &= np.isfinite(vectors[fam])
    return valid


def build_delta_table_vs_linear(
    vectors: Dict[str, np.ndarray],
    baseline: str,
    valid_mask: np.ndarray,
) -> pd.DataFrame:
    """
    vectors: family -> metric vector (length N)
    valid_mask: which seq_ids are included
    Returns table: delta_vs_linear = mean(model-baseline) + CI + p + Holm
    """
    if baseline not in vectors:
        raise RuntimeError(f"Baseline '{baseline}' missing from vectors: {list(vectors.keys())}")

    base = vectors[baseline]
    idx = np.where(valid_mask)[0]
    if idx.size == 0:
        raise RuntimeError("No valid sequences after masking.")

    rows = []
    # baseline row
    rows.append({
        "model": baseline,
        "n_paired": int(idx.size),
        "delta_vs_linear": 0.0,
        "se": 0.0,
        "ci_lo": 0.0,
        "ci_hi": 0.0,
        "t_approx": np.nan,
        "p_value": np.nan,
        "p_holm": np.nan,
    })

    fams = [f for f in vectors.keys() if f != baseline]
    for fam in fams:
        d = vectors[fam][idx] - base[idx]
        mu, se, lo, hi = mean_ci_95(d)
        t, p = paired_ttest_normal_approx(d)
        rows.append({
            "model": fam,
            "n_paired": int(idx.size),
            "delta_vs_linear": mu,  # negative = better
            "se": se,
            "ci_lo": lo,
            "ci_hi": hi,
            "t_approx": t,
            "p_value": p,
        })

    tbl = pd.DataFrame(rows)

    # Holm across non-baseline tests
    mask = tbl["model"] != baseline
    pvals = tbl.loc[mask, "p_value"].values
    tbl.loc[mask, "p_holm"] = holm_adjust(pvals) if pvals.size else np.array([])
    tbl = tbl.sort_values("delta_vs_linear", ascending=True).reset_index(drop=True)
    return tbl

def _tier_color(val: float, is_baseline: bool = False, max_val: float = 1.0) -> str:
    """
    Color-code by performance tier (relative to data range):
      Best  (> 50% of max):       dark teal
      Good  (25-50% of max):      green
      Moderate (0 - 25% of max):  orange/gold
      Worse (< 0):                salmon/red
      Baseline:                   light gray
    """
    if is_baseline:
        return "#D3D3D3"
    if max_val <= 0:
        max_val = 1.0
    frac = val / max_val if max_val != 0 else 0.0
    if val < 0:
        return "#EF5350"       # red
    if frac > 0.50:
        return "#0D7377"       # dark teal
    if frac > 0.25:
        return "#4CAF50"       # green
    return "#FFA726"           # orange


def plot_delta_vs_linear(tbl: pd.DataFrame, title: str, out_png: str):
    """
    Publication-quality horizontal bar plot.
    Positive = improvement over Linear baseline.
    Color-coded by performance tier, sorted best-to-worst,
    with data labels, enhanced error bars, legend, and top-3 highlight.
    """
    ensure_dir(os.path.dirname(out_png))

    d = tbl.copy()

    # --- Negate so positive = improvement ---------------------------------
    d["improvement"] = -d["delta_vs_linear"]
    d["ci_lo_plot"] = -d["ci_hi"]       # negation swaps bounds
    d["ci_hi_plot"] = -d["ci_lo"]

    # --- Priority 3: Sort best-to-worst (top to bottom) -------------------
    d = d.sort_values("improvement", ascending=False).reset_index(drop=True)

    models = d["model"].tolist()
    n_models = len(models)
    y = np.arange(n_models)
    delta = d["improvement"].values
    ci_lo = d["ci_lo_plot"].values
    ci_hi = d["ci_hi_plot"].values
    xerr = np.vstack([delta - ci_lo, ci_hi - delta])

    # --- Priority 1 #2: Color by performance tier -------------------------
    pos_vals = delta[delta > 0]
    max_positive = float(pos_vals.max()) if len(pos_vals) > 0 else 1.0
    colors = [
        _tier_color(v, is_baseline=(m == "Linear"), max_val=max_positive)
        for v, m in zip(delta, models)
    ]

    # --- Figure -----------------------------------------------------------
    fig, ax = plt.subplots(
        figsize=(9.0, max(3.5, 0.45 * n_models + 1.2)),
        dpi=250,
    )

    bars = ax.barh(
        y,
        delta,
        xerr=xerr,
        capsize=4,
        color=colors,
        edgecolor="black",
        linewidth=0.6,
        ecolor="#333333",        # Priority 2 #5: darker error bars
        error_kw=dict(lw=1.5),  # thicker error bars
        height=0.65,
    )


    # --- Priority 1 #1: Prominent baseline reference line -----------------
    ax.axvline(0.0, linestyle="-", linewidth=2.5, color="black", zorder=4)
    # No separate annotation — baseline line is explained in the legend

    # --- Priority 1 #4: Data labels on bars ------------------------------
    x_range = max(abs(delta.min()), abs(delta.max()), 0.01)
    for i, v in enumerate(delta):
        label = f"{v:+.1%}" if abs(v) < 1.0 else f"{v:+.2f}"
        offset = x_range * 0.02
        ha = "left" if v >= 0 else "right"
        xpos = v + offset if v >= 0 else v - offset
        ax.text(
            xpos, y[i], label,
            va="center", ha=ha,
            fontsize=8, fontweight="bold", color="#222222",
        )

    # --- Axes -------------------------------------------------------------
    ax.set_yticks(y)
    ax.set_yticklabels(models, fontsize=10, fontweight="bold")
    ax.invert_yaxis()

    # Symmetric x-axis with padding for labels
    pad = x_range * 0.25
    ax.set_xlim(-max(abs(delta.min()), 0) - pad,
                max(abs(delta.max()), 0) + pad)

    ax.set_xlabel(
        "Improvement over Linear Baseline (positive = better)",
        fontsize=11, fontweight="bold",
    )

    ax.set_title(title, fontweight="bold", fontsize=14, pad=12)

    # --- Gridlines --------------------------------------------------------
    ax.grid(True, axis="x", linestyle="--", alpha=0.30, color="#888888")
    ax.grid(True, axis="y", linestyle=":", alpha=0.15, color="#AAAAAA")

    # Despine for publication style
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # --- Legend (only include tiers that actually appear) ------------------
    color_set = set(colors)
    tier_patches = []
    if "#0D7377" in color_set:
        tier_patches.append(mpatches.Patch(facecolor="#0D7377", edgecolor="black", lw=0.8,
                           label="Best"))
    if "#4CAF50" in color_set:
        tier_patches.append(mpatches.Patch(facecolor="#4CAF50", edgecolor="black", lw=0.8,
                           label="Good"))
    if "#FFA726" in color_set:
        tier_patches.append(mpatches.Patch(facecolor="#FFA726", edgecolor="black", lw=0.8,
                           label="Moderate"))
    if "#EF5350" in color_set:
        tier_patches.append(mpatches.Patch(facecolor="#EF5350", edgecolor="black", lw=0.8,
                           label="Worse than baseline"))
    if "#D3D3D3" in color_set:
        tier_patches.append(mpatches.Patch(facecolor="#D3D3D3", edgecolor="black", lw=0.8,
                           label="Baseline (Linear)"))
    tier_patches.append(Line2D([0], [0], color="black", linewidth=2.5, linestyle="-",
               label="Linear Baseline (x = 0)"))
    tier_patches.append(mpatches.Patch(facecolor="none", edgecolor="none",
                       label="Error bars = 95% CI"))

    leg = ax.legend(
        handles=tier_patches,
        title="Performance Tier",
        title_fontsize=10,
        fontsize=9,
        loc="upper left",
        bbox_to_anchor=(1.02, 1.0),
        framealpha=0.95,
        edgecolor="#666666",
        fancybox=True,
        shadow=True,
        borderpad=1.0,
        labelspacing=0.6,
        handlelength=1.8,
        handleheight=1.2,
    )
    leg.get_title().set_fontweight("bold")

    # --- Save -------------------------------------------------------------
    fig.tight_layout()
    fig.savefig(out_png, bbox_inches="tight")
    fig.savefig(os.path.splitext(out_png)[0] + ".pdf", bbox_inches="tight")
    plt.close(fig)

# -------------------------
# Orchestration: per signal, per metric
# -------------------------
def run_clean_baseline_tests(
    signals: List[str],
    families: List[str],
    out_root: str,
    history_len: int,
    fs: float,
    phase_unit: str,
    baseline: str = "Linear",
):
    ensure_dir(out_root)

    # (metric_name, use_intersection_valid)
    metrics = [
        ("mae", False),
        ("freq", True),
        ("phase", True),
    ]

    for sig in signals:
        print(f"\n=== CLEAN baseline tests: {sig} ===")

        # user-supplied mapping family->Shift_0 path
        fam_to_path = get_clean_paths_for_signal(sig, families)

        if baseline not in fam_to_path:
            raise RuntimeError(f"[{sig}] baseline '{baseline}' missing from fam_to_path keys: {list(fam_to_path.keys())}")

        sig_dir = os.path.join(out_root, sig)
        tab_dir = os.path.join(sig_dir, "tables")
        fig_dir = os.path.join(sig_dir, "figures")
        ensure_dir(tab_dir)
        ensure_dir(fig_dir)

        for metric, use_intersection in metrics:
            vectors = compute_metric_vectors(
                fam_to_path=fam_to_path,
                metric=metric,
                history_len=history_len,
                fs=fs,
                phase_unit=phase_unit,
            )

            # choose valid mask
            if use_intersection:
                valid = intersection_valid_mask(vectors)
            else:
                # MAE should be finite, but keep it safe
                any_fam = next(iter(vectors.keys()))
                N = vectors[any_fam].shape[0]
                valid = np.isfinite(vectors[baseline])
                if valid.size != N:
                    valid = np.ones(N, dtype=bool)

            n_used = int(np.sum(valid))
            if n_used == 0:
                print(f"[SKIP] {sig} metric={metric}: no valid sequences after masking")
                continue

            tbl = build_delta_table_vs_linear(vectors, baseline=baseline, valid_mask=valid)

            out_csv = os.path.join(tab_dir, f"{metric}_delta_vs_{baseline}.csv")
            tbl.to_csv(out_csv, index=False)

            metric_title = {"mae": "MAE", "freq": "|Δf|", "phase": "|Δphase| (deg)"}[metric]
            sig_label = sig.replace("_", " ")
            out_png = os.path.join(fig_dir, f"{metric}_delta_vs_{baseline}.png")
            plot_delta_vs_linear(
                tbl,
                title=f"Performance Improvement Over Linear Baseline\n({sig_label}, Clean Data) — {metric_title}",
                out_png=out_png,
            )

            better = tbl[
                (tbl["model"] != baseline) &
                (tbl["delta_vs_linear"] < 0) &
                (tbl["p_holm"] < 0.05)
            ]
            print(f"  metric={metric}: n_used={n_used}")
            if len(better) == 0:
                print("    No models significantly better than Linear (Holm p<0.05).")
            else:
                print("    Significant improvements (Holm p<0.05):")
                for _, r in better.iterrows():
                    print(f"      {r['model']:>12s}  Δ={r['delta_vs_linear']:+.4g}  p_holm={r['p_holm']:.3g}")

        print(f"✓ Saved outputs under: {sig_dir}")


# -------------------------
# Entry point
# -------------------------
if __name__ == "__main__":
    if BASELINE not in FAMILIES:
        raise RuntimeError("FAMILIES must include the baseline 'Linear'.")

    run_clean_baseline_tests(
        signals=SIGNALS,
        families=FAMILIES,
        out_root=OUT_ROOT,
        history_len=HISTORY_LEN,
        fs=FS,
        phase_unit=PHASE_UNIT,
        baseline=BASELINE,
    )

    print("\nAll done.")