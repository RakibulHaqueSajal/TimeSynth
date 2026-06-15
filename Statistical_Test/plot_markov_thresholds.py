#!/usr/bin/env python3
"""
Generate pass/fail heatmaps at multiple KL thresholds from a saved npz file.

Usage:
    python plot_markov_thresholds.py
    python plot_markov_thresholds.py --npz /path/to/overlap_table_All_Models_allp.npz
    python plot_markov_thresholds.py --thresholds 0.05 0.10 0.15 0.20
"""

import argparse
import os
from typing import Dict, List

import numpy as np

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
except ModuleNotFoundError as exc:
    raise SystemExit("matplotlib is required. Activate the correct environment.") from exc


DEFAULT_NPZ = (
    "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/"
    "Time_Series_Forecast/Model_Comparison/Statistical/"
    "Markov_Proxy_KL_Thresholding/All_Models/overlap_table_All_Models_allp.npz"
)

DEFAULT_THRESHOLDS = [0.05, 0.10, 0.15, 0.20]


def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)


def load_npz(npz_path: str):
    """Load npz and return (rows_by_p, group_name)."""
    data = np.load(npz_path, allow_pickle=True)
    rows = data["rows"]

    rows_by_p: Dict[float, List[dict]] = {}
    group_name = "All_Models"

    for r in rows:
        if not isinstance(r, dict):
            continue
        if "chosen_kl_pwin" not in r:
            continue
        p = float(r.get("lvl", 0))
        rows_by_p.setdefault(p, []).append(r)
        if "group" in r:
            group_name = r["group"]

    return rows_by_p, group_name


def plot_pass_fail_at_threshold(
    rows_by_p: Dict[float, List[dict]],
    group_name: str,
    kl_threshold: float,
    save_path: str,
):
    """Single pass/fail heatmap at a given KL threshold."""
    prob_levels = sorted(rows_by_p.keys())
    all_rows = [r for rows in rows_by_p.values() for r in rows]
    families = sorted(set(r["fam"] for r in all_rows))

    # Build pass matrix using the given threshold (recomputed, not from saved flag)
    n_fam = len(families)
    n_prob = len(prob_levels)
    pass_matrix = np.zeros((n_fam, n_prob), dtype=int)

    for i, fam in enumerate(families):
        for j, p in enumerate(prob_levels):
            matching = [r for r in rows_by_p[p] if r.get("fam") == fam]
            if matching and matching[0].get("chosen_kl_pwin", 999) < kl_threshold:
                pass_matrix[i, j] = 1

    # Sort by pass rate (descending), then alphabetically
    pass_counts = pass_matrix.sum(axis=1)
    sort_idx = sorted(range(n_fam), key=lambda i: (-pass_counts[i], families[i]))
    families = [families[i] for i in sort_idx]
    pass_matrix = pass_matrix[sort_idx]
    pass_counts = pass_counts[sort_idx]

    n_models = len(families)

    # --- Figure -----------------------------------------------------------
    fig_h = max(5.5, 0.55 * n_models + 3.0)
    fig, ax = plt.subplots(figsize=(12.0, fig_h), dpi=250)

    cmap = plt.cm.colors.ListedColormap(["#FFCDD2", "#BBDEFB"])
    ax.imshow(pass_matrix, cmap=cmap, aspect="auto", vmin=0, vmax=1)

    # Gridlines
    for i in range(n_models + 1):
        ax.axhline(i - 0.5, color="#AAAAAA", linewidth=0.8)
    for j in range(n_prob + 1):
        ax.axvline(j - 0.5, color="#AAAAAA", linewidth=0.8)

    # Y-axis with pass rate
    y_labels = [f"{fam}  ({int(pc)}/{n_prob})" for fam, pc in zip(families, pass_counts)]
    ax.set_yticks(np.arange(n_models))
    ax.set_yticklabels(y_labels, fontsize=11, fontweight="bold")
    ax.set_ylabel("Model", fontsize=13, fontweight="bold")

    # X-axis
    ax.set_xticks(np.arange(n_prob))
    ax.set_xticklabels([f"p = {p:.2f}" for p in prob_levels], fontsize=10, fontweight="bold")
    ax.set_xlabel("Probability of State Change", fontsize=12, fontweight="bold")

    # Title
    ax.set_title(
        f"Model Robustness Across State Change Probabilities\n"
        f"(KL Threshold = {kl_threshold})",
        fontweight="bold", fontsize=15, pad=14,
    )

    # Despine for publication style
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Legend as footnote at bottom
    legend_handles = [
        mpatches.Patch(facecolor="#BBDEFB", edgecolor="black", lw=0.8,
                       label="Captured (KL < threshold)"),
        mpatches.Patch(facecolor="#FFCDD2", edgecolor="black", lw=0.8,
                       label="Missed (KL \u2265 threshold)"),
    ]
    leg = ax.legend(
        handles=legend_handles,
        fontsize=12,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.08),
        ncol=2,
        frameon=True,
        framealpha=0.95,
        edgecolor="#666666",
        fancybox=True,
        handlelength=2.0,
        handleheight=1.2,
    )
    for text in leg.get_texts():
        text.set_fontweight("bold")

    # Save
    fig.tight_layout()
    fig.savefig(save_path, dpi=250, bbox_inches="tight")
    fig.savefig(os.path.splitext(save_path)[0] + ".pdf", bbox_inches="tight")
    plt.close(fig)


def parse_args():
    parser = argparse.ArgumentParser(description="Generate pass/fail heatmaps at multiple KL thresholds.")
    parser.add_argument("--npz", default=DEFAULT_NPZ, help="Path to overlap_table npz file.")
    parser.add_argument(
        "--thresholds", nargs="*", type=float, default=None,
        help=f"KL thresholds to plot. Default: {DEFAULT_THRESHOLDS}",
    )
    parser.add_argument("--outdir", default="", help="Output directory. Defaults to npz parent dir.")
    return parser.parse_args()


def main():
    args = parse_args()
    thresholds = args.thresholds if args.thresholds else DEFAULT_THRESHOLDS
    outdir = args.outdir if args.outdir else os.path.join(os.path.dirname(args.npz), "threshold_comparison")
    ensure_dir(outdir)

    rows_by_p, group_name = load_npz(args.npz)
    print(f"Loaded {sum(len(v) for v in rows_by_p.values())} rows from {os.path.basename(args.npz)}")
    print(f"Probability levels: {sorted(rows_by_p.keys())}")
    print(f"Thresholds to plot: {thresholds}")
    print()

    for th in thresholds:
        out_path = os.path.join(outdir, f"passfail_KL_{th:.2f}.png")
        plot_pass_fail_at_threshold(rows_by_p, group_name, th, out_path)
        print(f"  KL={th:.2f} -> {out_path}")

    print(f"\nAll done. Outputs in: {outdir}")


if __name__ == "__main__":
    main()
