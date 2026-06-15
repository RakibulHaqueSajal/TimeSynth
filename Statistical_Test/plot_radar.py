#!/usr/bin/env python3
"""
Radar / compass plot summarising each model's performance across paradigms.

Axes (one per spoke):
    1. Clean Accuracy       – mean improvement over Linear on clean data
    2. Noise Robustness     – mean improvement over Linear across noise levels
    3. Shift Robustness     – mean improvement over Linear across shift levels
    4. State Transition     – mean improvement over Linear across transition tags
    5. Markov Fidelity      – mean pwin_overlap across probability levels

All "improvement" scores are  -delta_vs_linear  (positive = better than Linear).
Scores are min-max normalised to [0, 1] across models so every axis uses the
full range.  Linear is excluded (it is the zero baseline).

Outputs are saved to:
    <OUT_DIR>/radar_all_models.png / .pdf
    <OUT_DIR>/radar_per_model/  (one small radar per model)
"""

import os
import csv
import math
from typing import Dict, List

import numpy as np

import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams["font.family"] = "serif"
matplotlib.rcParams["font.serif"] = ["Nimbus Roman", "DejaVu Serif"]

# ──────────────────────────────────────────────────────────────────────
# Paths
# ──────────────────────────────────────────────────────────────────────
STAT_ROOT = (
    "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/"
    "Time_Series_Forecast/Model_Comparison/Statistical"
)

CLEAN_DIR = os.path.join(STAT_ROOT, "Clean_BaselineVsLinear")
NOISE_DIR = os.path.join(STAT_ROOT, "Noise_Dir")
SHIFT_DIR = os.path.join(STAT_ROOT, "Shift_Dir")
STATE_DIR = os.path.join(STAT_ROOT, "Single_State_Change", "tagwise_paired_tests")
MARKOV_CSV = os.path.join(
    STAT_ROOT, "Markov_Proxy_KL_Thresholding_Grouped",
    "All_Models", "markov_results_All_Models.csv",
)
MARKOV_NPZ = os.path.join(
    STAT_ROOT, "Markov_Proxy_KL_Thresholding",
    "All_Models", "overlap_table_All_Models_allp.npz",
)

OUT_DIR = os.path.join(STAT_ROOT, "Radar_Plots")

SIGNALS = ["Drift_Harmonic", "Single_Phase_Modulation", "Dual_Phase_Modulation"]
METRICS = ["mae", "freq", "phase"]
BASELINE = "Linear"

# ──────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────
def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)


def _to_float(v: str) -> float:
    if v is None:
        return math.nan
    v = v.strip()
    return float(v) if v else math.nan


def _read_csv(path: str) -> List[dict]:
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


# ──────────────────────────────────────────────────────────────────────
# 1. Clean Accuracy
# ──────────────────────────────────────────────────────────────────────
def score_clean(models: List[str]) -> Dict[str, float]:
    """Average -delta_vs_linear across signals & metrics."""
    accum: Dict[str, List[float]] = {m: [] for m in models}
    for sig in SIGNALS:
        for met in METRICS:
            path = os.path.join(CLEAN_DIR, sig, "tables", f"{met}_delta_vs_{BASELINE}.csv")
            if not os.path.isfile(path):
                continue
            for row in _read_csv(path):
                m = row["model"]
                if m in accum:
                    accum[m].append(-_to_float(row["delta_vs_linear"]))
    return {m: float(np.nanmean(v)) if v else 0.0 for m, v in accum.items()}


# ──────────────────────────────────────────────────────────────────────
# 2. Noise Robustness
# ──────────────────────────────────────────────────────────────────────
def score_noise(models: List[str]) -> Dict[str, float]:
    """Average -delta_vs_linear across noise levels, signals, metrics."""
    accum: Dict[str, List[float]] = {m: [] for m in models}
    for f in os.listdir(NOISE_DIR):
        if not (f.startswith("OptionA_") and f.endswith("_per_level.csv")):
            continue
        for row in _read_csv(os.path.join(NOISE_DIR, f)):
            m = row["model"]
            if m in accum:
                accum[m].append(-_to_float(row["delta_vs_linear"]))
    return {m: float(np.nanmean(v)) if v else 0.0 for m, v in accum.items()}


# ──────────────────────────────────────────────────────────────────────
# 3. Shift Robustness
# ──────────────────────────────────────────────────────────────────────
def score_shift(models: List[str]) -> Dict[str, float]:
    """Average -delta_vs_linear across shift levels, signals, metrics."""
    accum: Dict[str, List[float]] = {m: [] for m in models}
    for f in os.listdir(SHIFT_DIR):
        if not (f.startswith("Shift_OptionA_") and f.endswith(".csv")):
            continue
        for row in _read_csv(os.path.join(SHIFT_DIR, f)):
            m = row["model"]
            if m in accum:
                accum[m].append(-_to_float(row["delta_vs_linear"]))
    return {m: float(np.nanmean(v)) if v else 0.0 for m, v in accum.items()}


# ──────────────────────────────────────────────────────────────────────
# 4. State Transition
# ──────────────────────────────────────────────────────────────────────
def score_state_transition(models: List[str]) -> Dict[str, float]:
    """Average -median_delta across tags & metrics."""
    accum: Dict[str, List[float]] = {m: [] for m in models}
    for met in METRICS:
        path = os.path.join(STATE_DIR, f"tagwise_vs_{BASELINE}_{met}.csv")
        if not os.path.isfile(path):
            continue
        for row in _read_csv(path):
            m = row["model"]
            if m in accum:
                accum[m].append(-_to_float(row["median_delta"]))
    return {m: float(np.nanmean(v)) if v else 0.0 for m, v in accum.items()}


# ──────────────────────────────────────────────────────────────────────
# 5. Markov Fidelity
# ──────────────────────────────────────────────────────────────────────
def score_markov(models: List[str]) -> Dict[str, float]:
    """Average pwin_overlap across probability levels (higher = better)."""
    accum: Dict[str, List[float]] = {m: [] for m in models}
    if not os.path.isfile(MARKOV_CSV):
        return {m: 0.0 for m in models}
    for row in _read_csv(MARKOV_CSV):
        fam = row["family"]
        if fam in accum:
            val = _to_float(row["pwin_overlap"])
            if np.isfinite(val):
                accum[fam].append(val)
    return {m: float(np.nanmean(v)) if v else 0.0 for m, v in accum.items()}


# ──────────────────────────────────────────────────────────────────────
# 6. Markov Threshold Robustness (pass-rate from NPZ)
# ──────────────────────────────────────────────────────────────────────
def score_markov_threshold(models: List[str], kl_thresholds=None) -> Dict[str, float]:
    """
    Average pass-rate across KL thresholds and probability levels.
    Uses the NPZ file from plot_markov_thresholds.py.
    Higher = model passes more threshold/probability combinations.
    """
    if kl_thresholds is None:
        kl_thresholds = [0.05, 0.10, 0.15, 0.20]

    if not os.path.isfile(MARKOV_NPZ):
        return {m: 0.0 for m in models}

    data = np.load(MARKOV_NPZ, allow_pickle=True)
    rows = data["rows"]

    # Group rows by probability level
    rows_by_p: Dict[float, List[dict]] = {}
    for r in rows:
        if not isinstance(r, dict) or "chosen_kl_pwin" not in r:
            continue
        p = float(r.get("lvl", 0))
        rows_by_p.setdefault(p, []).append(r)

    prob_levels = sorted(rows_by_p.keys())
    n_prob = len(prob_levels)
    if n_prob == 0:
        return {m: 0.0 for m in models}

    # For each model, compute pass-rate averaged across all thresholds
    result: Dict[str, float] = {}
    for m in models:
        total_pass = 0
        total_tests = 0
        for th in kl_thresholds:
            for p in prob_levels:
                matching = [r for r in rows_by_p[p] if r.get("fam") == m]
                if matching:
                    kl_val = matching[0].get("chosen_kl_pwin", 999)
                    if kl_val < th:
                        total_pass += 1
                    total_tests += 1
        result[m] = total_pass / total_tests if total_tests > 0 else 0.0

    return result


# ──────────────────────────────────────────────────────────────────────
# Normalisation
# ──────────────────────────────────────────────────────────────────────
def min_max_normalise(scores: Dict[str, float]) -> Dict[str, float]:
    vals = list(scores.values())
    lo, hi = min(vals), max(vals)
    rng = hi - lo if hi != lo else 1.0
    return {m: (v - lo) / rng for m, v in scores.items()}


# ──────────────────────────────────────────────────────────────────────
# Radar plotting
# ──────────────────────────────────────────────────────────────────────
AXIS_NAMES = [
    "Clean Accuracy",
    "Noise Robustness",
    "Shift Robustness",
    "State Transition",
    "Markov Fidelity",
]

# Distinct colours for each model
MODEL_COLORS = {
    "PatchTST":    "#1f77b4",
    "NBeats":      "#ff7f0e",
    "MICN_Mean":   "#2ca02c",
    "MICN_Regre":  "#d62728",
    "ModernTCN":   "#9467bd",
    "FreMLP":      "#8c564b",
    "Transformer": "#e377c2",
    "Autoformer":  "#7f7f7f",
    "MLinear":     "#bcbd22",
    "DLinear":     "#17becf",
    "FITS":        "#aec7e8",
}


def _radar_axes(n_axes: int):
    """Return angles for n_axes spokes, starting from top (90°)."""
    angles = np.linspace(0, 2 * np.pi, n_axes, endpoint=False).tolist()
    angles += angles[:1]  # close the polygon
    return angles


def plot_radar_all(
    models: List[str],
    matrix: Dict[str, List[float]],
    out_path: str,
):
    """Overlay all models on one radar plot."""
    n_axes = len(AXIS_NAMES)
    angles = _radar_axes(n_axes)

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True), dpi=250)

    # Start from top
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # Spoke labels — push outward with padding
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(AXIS_NAMES, fontsize=15, fontweight="bold")
    ax.tick_params(axis="x", pad=18)

    # Radial ticks — place at angle away from spokes
    ax.set_ylim(0, 1.15)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"], fontsize=9, color="#555555")
    ax.set_rlabel_position(160)

    # Grid styling
    ax.grid(True, color="#CCCCCC", linewidth=0.5)
    ax.spines["polar"].set_visible(False)

    for model in models:
        vals = matrix[model] + matrix[model][:1]  # close polygon
        color = MODEL_COLORS.get(model, "#333333")
        ax.plot(angles, vals, linewidth=2.0, label=model, color=color)
        ax.fill(angles, vals, alpha=0.08, color=color)

    ax.set_title(
        "Comparative Model Performance Across Evaluation Paradigms",
        fontsize=17, fontweight="bold", pad=30,
    )

    ax.legend(
        loc="upper left",
        bbox_to_anchor=(1.15, 1.05),
        fontsize=12,
        framealpha=0.95,
        edgecolor="#666666",
        fancybox=True,
        title="Model",
        title_fontsize=13,
    )

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight")
    fig.savefig(os.path.splitext(out_path)[0] + ".pdf", bbox_inches="tight")
    plt.close(fig)


def plot_radar_per_model(
    models: List[str],
    matrix: Dict[str, List[float]],
    out_dir: str,
):
    """One small radar card per model."""
    ensure_dir(out_dir)
    n_axes = len(AXIS_NAMES)
    angles = _radar_axes(n_axes)

    n_models = len(models)
    n_cols = 4
    n_rows = math.ceil(n_models / n_cols)

    fig, axes = plt.subplots(
        n_rows, n_cols,
        figsize=(5 * n_cols, 5 * n_rows),
        subplot_kw=dict(polar=True),
        dpi=250,
    )
    axes_flat = np.array(axes).flatten()

    for idx, model in enumerate(models):
        ax = axes_flat[idx]
        vals = matrix[model] + matrix[model][:1]
        color = MODEL_COLORS.get(model, "#333333")

        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(AXIS_NAMES, fontsize=9, fontweight="bold")
        ax.set_ylim(0, 1.05)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels(["", "", "", "", ""], fontsize=7)
        ax.set_rlabel_position(30)
        ax.grid(True, color="#CCCCCC", linewidth=0.4)
        ax.spines["polar"].set_visible(False)

        ax.plot(angles, vals, linewidth=2.2, color=color)
        ax.fill(angles, vals, alpha=0.18, color=color)
        ax.set_title(model, fontsize=13, fontweight="bold", pad=15)

        # Print scores
        for i, (a, v) in enumerate(zip(angles[:-1], matrix[model])):
            ax.annotate(
                f"{v:.2f}",
                xy=(a, v),
                fontsize=8, fontweight="bold", color=color,
                ha="center", va="bottom",
            )

    # Hide unused subplots
    for idx in range(n_models, len(axes_flat)):
        axes_flat[idx].set_visible(False)

    fig.suptitle(
        "Individual Model Performance Profiles Across Evaluation Paradigms",
        fontsize=17, fontweight="bold", y=1.01,
    )
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "radar_per_model.png"), bbox_inches="tight")
    fig.savefig(os.path.join(out_dir, "radar_per_model.pdf"), bbox_inches="tight")
    plt.close(fig)


# ──────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────
def main():
    ensure_dir(OUT_DIR)

    # Discover models from clean CSVs (exclude baseline)
    sample_csv = os.path.join(
        CLEAN_DIR, SIGNALS[0], "tables", f"mae_delta_vs_{BASELINE}.csv"
    )
    all_models = sorted(
        {row["model"] for row in _read_csv(sample_csv) if row["model"] != BASELINE}
    )
    print(f"Models: {all_models}")

    # Compute raw scores per axis
    raw_scores = {
        "Clean Accuracy":    score_clean(all_models),
        "Noise Robustness":  score_noise(all_models),
        "Shift Robustness":  score_shift(all_models),
        "State Transition":  score_state_transition(all_models),
        "Markov Fidelity":   score_markov(all_models),
    }

    # Print raw scores
    print("\n--- Raw scores (higher = better) ---")
    for axis, scores in raw_scores.items():
        print(f"\n{axis}:")
        for m in all_models:
            print(f"  {m:>14s}: {scores[m]:+.4f}")

    # Normalise each axis to [0, 1]
    norm_scores = {axis: min_max_normalise(sc) for axis, sc in raw_scores.items()}

    # Build matrix: model -> [score_axis0, score_axis1, ...]
    matrix: Dict[str, List[float]] = {}
    for model in all_models:
        matrix[model] = [norm_scores[ax][model] for ax in AXIS_NAMES]

    # Plot combined radar
    plot_radar_all(all_models, matrix, os.path.join(OUT_DIR, "radar_all_models.png"))
    print(f"\nSaved combined radar: {os.path.join(OUT_DIR, 'radar_all_models.png')}")

    # Plot per-model cards
    plot_radar_per_model(all_models, matrix, os.path.join(OUT_DIR, "radar_per_model"))
    print(f"Saved per-model radars: {os.path.join(OUT_DIR, 'radar_per_model')}")

    print("\nDone.")


if __name__ == "__main__":
    main()
