#!/usr/bin/env python3
"""
Pareto Frontier Analysis of model performance across evaluation paradigms.

A model is Pareto-dominated if another model is at least as good on ALL axes
and strictly better on at least one.  Models on the Pareto frontier are not
dominated by any other model.

Outputs:
    <OUT_DIR>/pareto_combined.png / .pdf    – overlay with frontier vs dominated
    <OUT_DIR>/pareto_per_model/             – individual cards labelled frontier/dominated
    <OUT_DIR>/pareto_summary.csv            – table with scores and frontier status

Reuses scoring functions from plot_radar.py.
"""

import os
import sys
import math
import csv
from typing import Dict, List, Tuple

import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

matplotlib.rcParams["font.family"] = "serif"
matplotlib.rcParams["font.serif"] = ["Nimbus Roman", "DejaVu Serif"]

# ──────────────────────────────────────────────────────────────────────
# Import scoring functions from plot_radar
# ──────────────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))
from plot_radar import (
    score_clean,
    score_noise,
    score_shift,
    score_state_transition,
    score_markov,
    min_max_normalise,
    _read_csv,
    CLEAN_DIR,
    SIGNALS,
    BASELINE,
    STAT_ROOT,
)

AXIS_NAMES = [
    "Clean Accuracy",
    "Noise Robustness",
    "Shift Robustness",
    "State Transition",
    "Markov Fidelity",
]

OUT_DIR = os.path.join(STAT_ROOT, "Pareto_Frontier")

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


# ──────────────────────────────────────────────────────────────────────
# Pareto dominance
# ──────────────────────────────────────────────────────────────────────
def find_pareto_frontier(
    models: List[str],
    matrix: Dict[str, List[float]],
) -> Tuple[List[str], List[str]]:
    """
    Returns (frontier, dominated) model lists.
    Model A dominates model B if A >= B on all axes and A > B on at least one.
    """
    frontier = []
    dominated = []

    for m in models:
        m_vals = np.array(matrix[m])
        is_dominated = False
        for other in models:
            if other == m:
                continue
            o_vals = np.array(matrix[other])
            # other dominates m if other >= m everywhere AND other > m somewhere
            if np.all(o_vals >= m_vals) and np.any(o_vals > m_vals):
                is_dominated = True
                break
        if is_dominated:
            dominated.append(m)
        else:
            frontier.append(m)

    return frontier, dominated


# ──────────────────────────────────────────────────────────────────────
# Radar helpers
# ──────────────────────────────────────────────────────────────────────
def _radar_angles(n_axes: int):
    angles = np.linspace(0, 2 * np.pi, n_axes, endpoint=False).tolist()
    angles += angles[:1]
    return angles


def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)


# ──────────────────────────────────────────────────────────────────────
# Combined radar: frontier solid + coloured, dominated dashed + grey
# ──────────────────────────────────────────────────────────────────────
def plot_pareto_combined(
    models: List[str],
    matrix: Dict[str, List[float]],
    frontier: List[str],
    dominated: List[str],
    out_path: str,
):
    n_axes = len(AXIS_NAMES)
    angles = _radar_angles(n_axes)

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True), dpi=250)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(AXIS_NAMES, fontsize=15, fontweight="bold")
    ax.tick_params(axis="x", pad=18)

    ax.set_ylim(0, 1.15)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"], fontsize=9, color="#555555")
    ax.set_rlabel_position(160)

    ax.grid(True, color="#CCCCCC", linewidth=0.5)
    ax.spines["polar"].set_visible(False)

    # Plot dominated models first (behind)
    for model in dominated:
        vals = matrix[model] + matrix[model][:1]
        ax.plot(angles, vals, linewidth=1.2, linestyle="--", color="#BBBBBB",
                label=f"{model} (dominated)", alpha=0.7)
        ax.fill(angles, vals, alpha=0.02, color="#BBBBBB")

    # Plot frontier models on top
    for model in frontier:
        vals = matrix[model] + matrix[model][:1]
        color = MODEL_COLORS.get(model, "#333333")
        ax.plot(angles, vals, linewidth=2.5, label=f"{model} (frontier)", color=color)
        ax.fill(angles, vals, alpha=0.10, color=color)

    ax.set_title(
        "Pareto Frontier Analysis Across Evaluation Paradigms",
        fontsize=17, fontweight="bold", pad=30,
    )

    # Custom legend: frontier coloured, dominated grey
    handles = []
    for m in frontier:
        handles.append(plt.Line2D(
            [0], [0], color=MODEL_COLORS.get(m, "#333333"),
            linewidth=2.5, label=m,
        ))
    handles.append(plt.Line2D(
        [0], [0], color="#BBBBBB", linewidth=1.2, linestyle="--",
        label=f"Dominated ({len(dominated)} models)",
    ))

    ax.legend(
        handles=handles,
        loc="upper left",
        bbox_to_anchor=(1.15, 1.05),
        fontsize=12,
        framealpha=0.95,
        edgecolor="#666666",
        fancybox=True,
        title="Pareto Frontier",
        title_fontsize=13,
    )

    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight")
    fig.savefig(os.path.splitext(out_path)[0] + ".pdf", bbox_inches="tight")
    plt.close(fig)


# ──────────────────────────────────────────────────────────────────────
# Per-model cards with frontier/dominated label
# ──────────────────────────────────────────────────────────────────────
def plot_pareto_per_model(
    models: List[str],
    matrix: Dict[str, List[float]],
    frontier: List[str],
    out_dir: str,
):
    ensure_dir(out_dir)
    n_axes = len(AXIS_NAMES)
    angles = _radar_angles(n_axes)

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
        is_frontier = model in frontier
        color = MODEL_COLORS.get(model, "#333333") if is_frontier else "#BBBBBB"
        label_tag = "Pareto frontier" if is_frontier else "Dominated"
        tag_color = "#2ca02c" if is_frontier else "#C62828"

        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(AXIS_NAMES, fontsize=8, fontweight="bold")
        ax.set_ylim(0, 1.05)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels(["", "", "", "", ""], fontsize=7)
        ax.set_rlabel_position(30)
        ax.grid(True, color="#CCCCCC", linewidth=0.4)
        ax.spines["polar"].set_visible(False)

        lw = 2.5 if is_frontier else 1.5
        ls = "-" if is_frontier else "--"
        ax.plot(angles, vals, linewidth=lw, linestyle=ls, color=color)
        ax.fill(angles, vals, alpha=0.18 if is_frontier else 0.06, color=color)

        # Model name as title
        ax.set_title(model, fontsize=13, fontweight="bold", pad=15)

        # Frontier/Dominated badge
        ax.text(
            0.5, -0.08, label_tag,
            transform=ax.transAxes, ha="center", va="top",
            fontsize=11, fontweight="bold", color="white",
            bbox=dict(
                boxstyle="round,pad=0.3",
                facecolor=tag_color,
                edgecolor=tag_color,
                alpha=0.9,
            ),
        )

        # Score annotations
        for i, (a, v) in enumerate(zip(angles[:-1], matrix[model])):
            ax.annotate(
                f"{v:.2f}",
                xy=(a, v),
                fontsize=8, fontweight="bold",
                color=color if is_frontier else "#666666",
                ha="center", va="bottom",
            )

    for idx in range(n_models, len(axes_flat)):
        axes_flat[idx].set_visible(False)

    fig.suptitle(
        "Pareto Frontier: Individual Model Profiles",
        fontsize=17, fontweight="bold", y=1.01,
    )
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "pareto_per_model.png"), bbox_inches="tight")
    fig.savefig(os.path.join(out_dir, "pareto_per_model.pdf"), bbox_inches="tight")
    plt.close(fig)


# ──────────────────────────────────────────────────────────────────────
# Summary CSV
# ──────────────────────────────────────────────────────────────────────
def save_summary_csv(
    models: List[str],
    matrix: Dict[str, List[float]],
    frontier: List[str],
    out_path: str,
):
    with open(out_path, "w", newline="") as fh:
        writer = csv.writer(fh)
        header = ["model"] + AXIS_NAMES + ["mean_score", "pareto_status"]
        writer.writerow(header)
        for m in models:
            scores = matrix[m]
            mean_sc = float(np.mean(scores))
            status = "frontier" if m in frontier else "dominated"
            writer.writerow([m] + [f"{s:.4f}" for s in scores] + [f"{mean_sc:.4f}", status])


# ──────────────────────────────────────────────────────────────────────
# Dominance report
# ──────────────────────────────────────────────────────────────────────
def print_dominance_report(
    models: List[str],
    matrix: Dict[str, List[float]],
    frontier: List[str],
    dominated: List[str],
):
    print("\n" + "=" * 60)
    print("PARETO FRONTIER ANALYSIS")
    print("=" * 60)

    print(f"\nPareto frontier ({len(frontier)} models):")
    for m in frontier:
        scores = matrix[m]
        print(f"  {m:>14s}  scores: {['%.3f' % s for s in scores]}  mean={np.mean(scores):.3f}")

    print(f"\nDominated ({len(dominated)} models):")
    for m in dominated:
        scores = matrix[m]
        # Find which frontier models dominate this one
        dominators = []
        m_vals = np.array(matrix[m])
        for f in frontier:
            f_vals = np.array(matrix[f])
            if np.all(f_vals >= m_vals) and np.any(f_vals > m_vals):
                dominators.append(f)
        dom_str = ", ".join(dominators) if dominators else "dominated by non-frontier"
        print(f"  {m:>14s}  scores: {['%.3f' % s for s in scores]}  "
              f"mean={np.mean(scores):.3f}  dominated by: {dom_str}")

    print()


# ──────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────
def main():
    ensure_dir(OUT_DIR)

    # Discover models
    sample_csv = os.path.join(
        CLEAN_DIR, SIGNALS[0], "tables", f"mae_delta_vs_{BASELINE}.csv"
    )
    all_models = sorted(
        {row["model"] for row in _read_csv(sample_csv) if row["model"] != BASELINE}
    )
    print(f"Models: {all_models}")

    # Compute raw scores
    raw_scores = {
        "Clean Accuracy":   score_clean(all_models),
        "Noise Robustness": score_noise(all_models),
        "Shift Robustness": score_shift(all_models),
        "State Transition": score_state_transition(all_models),
        "Markov Fidelity":  score_markov(all_models),
    }

    # Normalise
    norm_scores = {axis: min_max_normalise(sc) for axis, sc in raw_scores.items()}

    # Build matrix
    matrix: Dict[str, List[float]] = {}
    for model in all_models:
        matrix[model] = [norm_scores[ax][model] for ax in AXIS_NAMES]

    # Pareto analysis
    frontier, dominated = find_pareto_frontier(all_models, matrix)

    # Report
    print_dominance_report(all_models, matrix, frontier, dominated)

    # Combined radar
    out_combined = os.path.join(OUT_DIR, "pareto_combined.png")
    plot_pareto_combined(all_models, matrix, frontier, dominated, out_combined)
    print(f"Saved: {out_combined}")

    # Per-model cards
    per_model_dir = os.path.join(OUT_DIR, "pareto_per_model")
    plot_pareto_per_model(all_models, matrix, frontier, per_model_dir)
    print(f"Saved: {per_model_dir}/")

    # Summary CSV
    csv_path = os.path.join(OUT_DIR, "pareto_summary.csv")
    save_summary_csv(all_models, matrix, frontier, csv_path)
    print(f"Saved: {csv_path}")

    print("\nDone.")


if __name__ == "__main__":
    main()
