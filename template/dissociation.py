#!/usr/bin/env python3
"""
Dissociation figures: pairwise scatter plots among the three fidelity metrics.

Three figures, each with three panels (one per signal family):
  1. MAE vs Phase Error
  2. MAE vs Frequency Error
  3. Frequency Error vs Phase Error

Each point = one model.  Color = architecture family.

Output:
    <OUT_DIR>/dissociation_mae_vs_phase.png / .pdf
    <OUT_DIR>/dissociation_mae_vs_freq.png  / .pdf
    <OUT_DIR>/dissociation_freq_vs_phase.png / .pdf
"""

import os
import csv
from typing import Dict, List, Tuple

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

matplotlib.rcParams["font.family"] = "serif"
matplotlib.rcParams["font.serif"] = ["Nimbus Roman", "DejaVu Serif"]

# ──────────────────────────────────────────────────────────────────────
# Paths
# ──────────────────────────────────────────────────────────────────────
CLEAN_RESULT = (
    "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/"
    "Time_Series_Forecast/Model_Comparison/Clean_Paradigm/Clean_Result"
)
STAT_ROOT = (
    "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/"
    "Time_Series_Forecast/Model_Comparison/Statistical"
)

GROUPS = ["Best_Models", "Best_Exclude_Linear", "CNN", "Linear", "MLinear", "Transformer"]

SIGNALS = [
    ("Drift_Harmonic",          "Drift Harmonic"),
    ("Single_Phase_Modulation", "Single Phase Modulation"),
    ("Dual_Phase_Modulation",   "Dual Phase Modulation"),
]

OUT_DIR = os.path.join(STAT_ROOT, "Dissociation_Figure")

# Architecture families
MODEL_FAMILIES = {
    "PatchTST":    "Transformer",
    "Transformer": "Transformer",
    "Autoformer":  "Transformer",
    "ModernTCN":   "CNN",
    "MICN_Mean":   "CNN",
    "MICN_Regre":  "CNN",
    "FreMLP":      "MLP",
    "NBeats":      "MLP",
    "DLinear":     "Linear-family",
    "MLinear":     "Linear-family",
    "FITS":        "Linear-family",
    "Linear":      "Baseline",
}

FAMILY_COLORS = {
    "Transformer":     "#E91E63",
    "CNN":     "#FF9800",
    "MLP":           "#4CAF50",
    "Linear-family": "#607D8B",
    "Baseline":      "#000000",
}

FAMILY_MARKERS = {
    "Transformer":     "^",
    "CNN":     "D",
    "MLP":           "s",
    "Linear-family": "o",
    "Baseline":      "X",
}


# ──────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────
def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)


def _read_csv(path: str) -> List[dict]:
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


# ──────────────────────────────────────────────────────────────────────
# Load raw medians
# ──────────────────────────────────────────────────────────────────────
def _load_metric(metric_dir: str, csv_name: str) -> Dict[str, Dict[str, float]]:
    """Load median values for one metric across all groups.

    Returns {signal: {model: median_value}}.
    """
    sig_keys = [s[0] for s in SIGNALS]
    data: Dict[str, Dict[str, float]] = {s: {} for s in sig_keys}
    for group in GROUPS:
        csv_path = os.path.join(CLEAN_RESULT, metric_dir, group, csv_name)
        if os.path.isfile(csv_path):
            for row in _read_csv(csv_path):
                sig, fam = row["signal"], row["family"]
                if sig in sig_keys and fam not in data[sig]:
                    data[sig][fam] = float(row["median"])
    return data


def load_raw_medians() -> Dict[str, Dict[str, Tuple[float, float]]]:
    """Returns {signal: {model: (median_mae, median_phase_deg)}}"""
    mae_data = _load_metric(
        "amp_error", "mae_across_signals_clean_mae_stats.csv"
    )
    phase_data = _load_metric(
        "phase_error",
        "phase_error_across_signals_clean_deg_phase_error_deg_stats.csv",
    )
    sig_keys = [s[0] for s in SIGNALS]
    result: Dict[str, Dict[str, Tuple[float, float]]] = {s: {} for s in sig_keys}
    for sig in sig_keys:
        common = set(mae_data[sig].keys()) & set(phase_data[sig].keys())
        for m in common:
            result[sig][m] = (mae_data[sig][m], phase_data[sig][m])
    return result


def load_raw_medians_mae_freq() -> Dict[str, Dict[str, Tuple[float, float]]]:
    """Returns {signal: {model: (median_mae, median_freq_error)}}"""
    mae_data = _load_metric(
        "amp_error", "mae_across_signals_clean_mae_stats.csv"
    )
    freq_data = _load_metric(
        "freq_error",
        "freq_error_across_signals_clean_freq_error_stats.csv",
    )
    sig_keys = [s[0] for s in SIGNALS]
    result: Dict[str, Dict[str, Tuple[float, float]]] = {s: {} for s in sig_keys}
    for sig in sig_keys:
        common = set(mae_data[sig].keys()) & set(freq_data[sig].keys())
        for m in common:
            result[sig][m] = (mae_data[sig][m], freq_data[sig][m])
    return result


def load_raw_medians_freq_phase() -> Dict[str, Dict[str, Tuple[float, float]]]:
    """Returns {signal: {model: (median_freq_error, median_phase_deg)}}"""
    freq_data = _load_metric(
        "freq_error",
        "freq_error_across_signals_clean_freq_error_stats.csv",
    )
    phase_data = _load_metric(
        "phase_error",
        "phase_error_across_signals_clean_deg_phase_error_deg_stats.csv",
    )
    sig_keys = [s[0] for s in SIGNALS]
    result: Dict[str, Dict[str, Tuple[float, float]]] = {s: {} for s in sig_keys}
    for sig in sig_keys:
        common = set(freq_data[sig].keys()) & set(phase_data[sig].keys())
        for m in common:
            result[sig][m] = (freq_data[sig][m], phase_data[sig][m])
    return result


# ──────────────────────────────────────────────────────────────────────
# Plot — combined 2×3 figure
# ──────────────────────────────────────────────────────────────────────
def _scatter_on_ax(ax, model_data):
    """Plot all non-baseline models on a single axes."""
    for model, (x_val, y_val) in model_data.items():
        fam = MODEL_FAMILIES.get(model, "Baseline")
        if fam == "Baseline":
            continue
        ax.scatter(
            x_val, y_val,
            marker=FAMILY_MARKERS[fam],
            s=120,
            c=FAMILY_COLORS[fam],
            edgecolors="white",
            linewidths=0.5,
            alpha=0.9,
            zorder=5,
        )


def _add_slab_cues(ax, model_data, y_unit: str):
    """Overlay a 'Comparable MAE' slab with per-family mean fidelity ticks
    inside it, plus a red arrow between the top and bottom family means.

    The slab is the IQR of MAE values in this panel. Inside the slab,
    each architecture family's mean fidelity is drawn as a colored
    horizontal tick. The vertical gap between the top and bottom ticks
    is the dissociation at comparable MAE.
    """
    # Subtle perfect-fidelity reference.
    ax.axhline(0, color="gray", linestyle=":", linewidth=0.8,
               alpha=0.45, zorder=1)

    # Group points by family, excluding the Baseline linear model.
    pts_by_fam: Dict[str, List[Tuple[float, float]]] = {}
    for m, (x, y) in model_data.items():
        fam = MODEL_FAMILIES.get(m, "Baseline")
        if fam == "Baseline":
            continue
        pts_by_fam.setdefault(fam, []).append((x, y))

    all_xs = [x for pts in pts_by_fam.values() for x, _ in pts]
    if len(all_xs) < 4:
        return

    # Comparable-MAE slab: central 60% of MAE values (p20-p80). Uniform
    # across panels, wide enough to include linear-family members that sit
    # just outside the tighter IQR on drift-harmonic signals.
    x_lo = float(np.percentile(all_xs, 20))
    x_hi = float(np.percentile(all_xs, 80))

    # Shade the slab.
    ax.axvspan(x_lo, x_hi, facecolor="#FFF3C4", edgecolor="none",
               alpha=0.55, zorder=0)

    # Family means inside slab.
    fam_means: Dict[str, float] = {}
    for fam, pts in pts_by_fam.items():
        ys_in = [y for x, y in pts if x_lo <= x <= x_hi]
        if ys_in:
            fam_means[fam] = float(np.mean(ys_in))
    if len(fam_means) < 2:
        return

    # Wide horizontal tick for each family inside the slab.
    tick_pad = 0.08 * (x_hi - x_lo)
    tick_lo, tick_hi = x_lo + tick_pad, x_hi - tick_pad
    for fam, ym in fam_means.items():
        ax.plot(
            [tick_lo, tick_hi], [ym, ym],
            color=FAMILY_COLORS[fam], linewidth=4.0,
            alpha=0.9, zorder=5, solid_capstyle="round",
        )

    # Vertical Δ arrow between top and bottom family means.
    fam_low = min(fam_means.items(), key=lambda kv: kv[1])
    fam_high = max(fam_means.items(), key=lambda kv: kv[1])
    x_arrow = (x_lo + x_hi) / 2.0
    ax.annotate(
        "", xy=(x_arrow, fam_low[1]), xytext=(x_arrow, fam_high[1]),
        arrowprops=dict(arrowstyle="<->", color="#C62828", lw=2.0,
                        shrinkA=2, shrinkB=2),
        zorder=6,
    )
    gap = fam_high[1] - fam_low[1]
    if y_unit == "deg":
        gap_lbl = f"Δ = {gap:.0f}°" if gap >= 1 else "Δ < 1°"
    else:
        if gap >= 0.01:
            gap_lbl = f"Δ = {gap:.2f} Hz"
        elif gap >= 0.001:
            gap_lbl = f"Δ = {gap:.3f} Hz"
        else:
            gap_lbl = "Δ < 0.001 Hz"
    ax.text(
        x_arrow, (fam_low[1] + fam_high[1]) / 2.0, "  " + gap_lbl,
        color="#C62828", fontsize=16, fontweight="bold",
        va="center", ha="left", zorder=7,
        bbox=dict(boxstyle="round,pad=0.3", fc="white",
                  ec="#C62828", lw=1.0, alpha=0.95),
    )


def plot_combined(out_path: str):
    """3×2 grid: each row = one signal family, col 0 = MAE vs Phase, col 1 = MAE vs Freq."""
    raw_phase = load_raw_medians()          # (mae, phase)
    raw_freq = load_raw_medians_mae_freq()  # (mae, freq)

    fig, axes = plt.subplots(3, 2, figsize=(10, 13), dpi=250)

    panel = 0  # running counter for A–F labels
    for row, (sig_key, sig_label) in enumerate(SIGNALS):
        # ── Col 0: MAE vs Phase ──────────────────────────────────────
        ax = axes[row, 0]
        _scatter_on_ax(ax, raw_phase[sig_key])
        _add_slab_cues(ax, raw_phase[sig_key], y_unit="deg")

        ax.set_title(sig_label, fontsize=16, fontweight="bold", pad=10)
        ax.set_ylabel(
            "Median |$\\Delta$Phase| (deg)",
            fontsize=16, fontweight="bold",
        )
        if row == 2:
            ax.set_xlabel("Median MAE", fontsize=16, fontweight="bold")
        ax.tick_params(axis="both", labelsize=14)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.text(
            -0.02, 1.05, chr(65 + panel) + ".",
            transform=ax.transAxes, fontsize=20, fontweight="bold",
            va="bottom", ha="right",
        )
        panel += 1

        # ── Col 1: MAE vs Frequency ─────────────────────────────────
        ax = axes[row, 1]
        _scatter_on_ax(ax, raw_freq[sig_key])
        _add_slab_cues(ax, raw_freq[sig_key], y_unit="Hz")

        ax.set_title(sig_label, fontsize=16, fontweight="bold", pad=10)
        ax.set_ylabel(
            "Median |$\\Delta f$| (Hz)",
            fontsize=16, fontweight="bold",
        )
        if row == 2:
            ax.set_xlabel("Median MAE", fontsize=16, fontweight="bold")
        ax.tick_params(axis="both", labelsize=14)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.text(
            -0.02, 1.05, chr(65 + panel) + ".",
            transform=ax.transAxes, fontsize=20, fontweight="bold",
            va="bottom", ha="right",
        )
        panel += 1

    # ── Shared legend ────────────────────────────────────────────────
    legend_handles = [
        Line2D([0], [0], marker=FAMILY_MARKERS[fam], color="w",
               markerfacecolor=FAMILY_COLORS[fam], markersize=16,
               markeredgecolor="white", markeredgewidth=0.5,
               label=fam)
        for fam in FAMILY_COLORS if fam != "Baseline"
    ]
    fig.legend(
        handles=legend_handles,
        loc="lower center",
        ncol=4,
        prop=dict(size=18, weight="bold"),
        frameon=False,
        bbox_to_anchor=(0.5, -0.04),
        columnspacing=2.0,
        handletextpad=0.6,
    )

    fig.suptitle(
        "Dissociation Between Conventional (MAE) and Fidelity Metrics",
        fontsize=18, fontweight="bold", y=1.04,
    )
    fig.text(
        0.5, 1.008,
        "Yellow band = comparable-MAE window   ·   "
        "Red arrow = fidelity gap between architecture families at similar MAE",
        ha="center", va="top",
        fontsize=15, fontweight="bold", style="italic", color="#333333",
    )

    fig.tight_layout(w_pad=2.0, h_pad=2.8)
    fig.subplots_adjust(bottom=0.08, top=0.93)
    fig.savefig(out_path, bbox_inches="tight")
    fig.savefig(os.path.splitext(out_path)[0] + ".pdf", bbox_inches="tight")
    plt.close(fig)


# ──────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────
def main():
    ensure_dir(OUT_DIR)

    out = os.path.join(OUT_DIR, "dissociation_combined.png")
    plot_combined(out)
    print(f"Saved: {out}")
    print(f"Saved: {os.path.splitext(out)[0]}.pdf")
    print("Done.")


if __name__ == "__main__":
    main()
