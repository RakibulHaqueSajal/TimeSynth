#!/usr/bin/env python3
"""
Plot model comparison figures from an Option A noise CSV.

Input CSV format is the output of Statistical_Test/noise.py:
    signal,metric,shift,model,n_paired,delta_vs_linear,ci_lo,ci_hi,t_approx,p_value,p_holm

Default outputs:
  - line plot: delta vs Linear across shift levels
  - heatmap:   delta vs Linear by model x shift

Interpretation:
  - y < 0 means the model is better than Linear
  - y > 0 means the model is worse than Linear
"""

import argparse
import csv
import math
import os
from typing import Dict, List, Tuple

import numpy as np

try:
    import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
except ModuleNotFoundError as exc:
    raise SystemExit(
        "matplotlib is required to plot figures. Activate the environment "
        "you use for the stats scripts, then rerun this script."
    ) from exc

matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.serif'] = ['Nimbus Roman', 'DejaVu Serif']


DEFAULT_CSV_DIR = (
    "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/"
    "Time_Series_Forecast/Model_Comparison/Statistical/Shift_Dir"
)

DEFAULT_CSVS = sorted([
    os.path.join(DEFAULT_CSV_DIR, f)
    for f in os.listdir(DEFAULT_CSV_DIR)
    if f.startswith("Shift_OptionA_") and f.endswith(".csv")
]) if os.path.isdir(DEFAULT_CSV_DIR) else []


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _to_float(value: str) -> float:
    if value is None:
        return math.nan
    value = value.strip()
    if value == "":
        return math.nan
    return float(value)


def _to_int(value: str) -> int:
    return int(float(value))


def load_optionA_csv(csv_path: str) -> Tuple[List[Dict[str, object]], str, str]:
    rows: List[Dict[str, object]] = []
    with open(csv_path, newline="") as handle:
        reader = csv.DictReader(handle)
        for raw in reader:
            row = {
                "signal": raw["signal"],
                "metric": raw["metric"],
                "shift": _to_int(raw["shift"]),
                "model": raw["model"],
                "n_paired": _to_int(raw["n_paired"]),
                "delta_vs_linear": _to_float(raw["delta_vs_linear"]),
                "ci_lo": _to_float(raw["ci_lo"]),
                "ci_hi": _to_float(raw["ci_hi"]),
                "t_approx": _to_float(raw["t_approx"]),
                "p_value": _to_float(raw["p_value"]),
                "p_holm": _to_float(raw["p_holm"]),
            }
            rows.append(row)

    if not rows:
        raise ValueError(f"No rows found in {csv_path}")

    signal = str(rows[0]["signal"])
    metric = str(rows[0]["metric"])
    return rows, signal, metric


def build_model_series(
    rows: List[Dict[str, object]],
) -> Tuple[List[int], List[str], Dict[str, Dict[str, np.ndarray]]]:
    levels = sorted({int(row["shift"]) for row in rows})
    non_baseline_models = sorted({str(row["model"]) for row in rows if row["model"] != "Linear"})
    model_order = ["Linear"] + non_baseline_models

    level_to_idx = {level: idx for idx, level in enumerate(levels)}
    model_data: Dict[str, Dict[str, np.ndarray]] = {}
    for model in model_order:
        size = len(levels)
        model_data[model] = {
            "delta": np.full(size, np.nan, dtype=float),
            "ci_lo": np.full(size, np.nan, dtype=float),
            "ci_hi": np.full(size, np.nan, dtype=float),
            "p_holm": np.full(size, np.nan, dtype=float),
            "n_paired": np.full(size, np.nan, dtype=float),
        }

    for row in rows:
        model = str(row["model"])
        idx = level_to_idx[int(row["shift"])]
        model_data[model]["delta"][idx] = float(row["delta_vs_linear"])
        model_data[model]["ci_lo"][idx] = float(row["ci_lo"])
        model_data[model]["ci_hi"][idx] = float(row["ci_hi"])
        model_data[model]["p_holm"][idx] = float(row["p_holm"])
        model_data[model]["n_paired"][idx] = float(row["n_paired"])

    return levels, model_order, model_data


def metric_label(metric: str) -> str:
    labels = {
        "mae": "Delta vs Linear (MAE)",
        "freq": "Delta vs Linear (|Delta f|)",
        "phase": "Delta vs Linear (|Delta phase|)",
    }
    return labels.get(metric, "Delta vs Linear")


def plot_line_comparison(
    levels: List[int],
    models: List[str],
    model_data: Dict[str, Dict[str, np.ndarray]],
    signal: str,
    metric: str,
    out_path: str,
    alpha_sig: float,
) -> None:
    ensure_dir(os.path.dirname(out_path))

    fig, ax = plt.subplots(figsize=(10.5, 6.5), dpi=250)
    colors = plt.cm.tab20(np.linspace(0, 1, max(len(models), 2)))

    for idx, model in enumerate(models):
        if model == "Linear":
            continue

        delta = model_data[model]["delta"]
        ci_lo = model_data[model]["ci_lo"]
        ci_hi = model_data[model]["ci_hi"]
        p_holm = model_data[model]["p_holm"]

        color = colors[idx]
        ax.plot(levels, delta, marker="o", linewidth=1.8, markersize=4.5, color=color, label=model)
        if np.isfinite(ci_lo).any() and np.isfinite(ci_hi).any():
            ax.fill_between(levels, ci_lo, ci_hi, color=color, alpha=0.12)

        sig_mask = np.isfinite(p_holm) & (p_holm < alpha_sig)
        if np.any(sig_mask):
            ax.scatter(
                np.asarray(levels)[sig_mask],
                delta[sig_mask],
                s=44,
                color=color,
                edgecolors="black",
                linewidths=0.6,
                zorder=5,
            )

    ax.axhline(0.0, color="black", linestyle="--", linewidth=1.1)
    ax.set_xticks(levels)
    ax.set_xlabel("Shift level")
    ax.set_ylabel(metric_label(metric))
    ax.set_title(f"{signal}: model comparison across shift levels ({metric})")
    ax.grid(True, axis="y", linestyle="--", alpha=0.35)

    # Despine for publication style
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.text(
        0.99,
        0.01,
        f"Filled marker: Holm p < {alpha_sig:g}\nNegative is better than Linear",
        ha="right",
        va="bottom",
        transform=ax.transAxes,
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "0.8", "alpha": 0.9},
    )

    ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False)
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight")
    fig.savefig(os.path.splitext(out_path)[0] + ".pdf", bbox_inches="tight")
    plt.close(fig)


def plot_heatmap(
    levels: List[int],
    models: List[str],
    model_data: Dict[str, Dict[str, np.ndarray]],
    signal: str,
    metric: str,
    out_path: str,
) -> None:
    ensure_dir(os.path.dirname(out_path))

    # Sort models by average performance (best first)
    plot_models = [model for model in models if model != "Linear"]
    plot_models = sorted(plot_models, key=lambda m: np.nanmean(model_data[m]["delta"]))

    # Negate: positive = improvement over Linear
    matrix_raw = -np.vstack([model_data[model]["delta"] for model in plot_models])

    # Reorder columns: center shift 0, negatives left, positives right
    # Original order: [0, 1, 2, 3, 4]
    # Display order:  [2, 1, 0, 3, 4]  →  labels: [-2, -1, 0, +1, +2]
    display_order = [2, 1, 0, 3, 4]  # indices into original levels list
    display_labels = ["-2", "-1", "0", "+1", "+2"]
    matrix = matrix_raw[:, display_order]

    # Reorder p_holm arrays to match display order
    pholm_reordered = {}
    for model in plot_models:
        pholm_reordered[model] = model_data[model]["p_holm"][display_order]

    # Color scale (diverging at 0)
    finite = matrix[np.isfinite(matrix)]
    if finite.size == 0:
        vlim = 1.0
    else:
        vlim = float(np.max(np.abs(finite)))
        if vlim == 0:
            vlim = 1.0

    n_models = len(plot_models)
    n_levels = len(display_labels)

    # --- Figure -----------------------------------------------------------
    fig_h = max(6.0, 0.60 * n_models + 3.0)
    fig, ax = plt.subplots(figsize=(12.0, fig_h), dpi=250)

    # Blue = positive = better, Red = negative = worse
    im = ax.imshow(
        matrix, cmap="RdBu", aspect="auto",
        vmin=-vlim, vmax=vlim,
    )

    # Gridlines between cells
    for i in range(n_models + 1):
        ax.axhline(i - 0.5, color="#CCCCCC", linewidth=0.5)
    for j in range(n_levels + 1):
        ax.axvline(j - 0.5, color="#CCCCCC", linewidth=0.5)

    # Axes labels
    ax.set_xticks(np.arange(n_levels))
    ax.set_xticklabels(
        [f"Shift {lbl}" for lbl in display_labels],
        fontsize=13, fontweight="bold",
    )
    ax.set_xlabel(
        "Shift Level",
        fontsize=15, fontweight="bold",
    )

    ax.set_yticks(np.arange(n_models))
    ax.set_yticklabels(plot_models, fontsize=14, fontweight="bold")
    ax.set_ylabel("Model", fontsize=15, fontweight="bold")

    # Title
    sig_label = signal.replace("_", " ")
    metric_nice = {"mae": "\u0394MAE", "freq": "\u0394|Freq Error|", "phase": "\u0394|Phase Error|"}.get(metric, metric)
    ax.set_title(
        f"Model Performance Across Shift Levels \u2014 {metric_nice}\n"
        f"({sig_label})",
        fontweight="bold", fontsize=17, pad=14,
    )

    # Value labels + significance in cells
    for i, model in enumerate(plot_models):
        pvals = pholm_reordered[model]
        for j in range(n_levels):
            value = matrix[i, j]
            if not np.isfinite(value):
                cell_text = "N/A"
                text_color = "#888888"
            else:
                cell_text = f"{value:+.2f}"
                if np.isfinite(pvals[j]) and pvals[j] < 0.05:
                    cell_text += " *"

                # White text on dark cells, black on light
                norm_val = (value + vlim) / (2.0 * vlim)
                text_color = "white" if norm_val < 0.25 or norm_val > 0.75 else "#222222"

            ax.text(
                j, i, cell_text,
                ha="center", va="center",
                fontsize=20, fontweight="bold",
                color=text_color,
            )

    # Enhanced color bar with direction labels
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(
        "Improvement over Linear",
        fontsize=16, fontweight="bold",
    )
    cbar.ax.tick_params(labelsize=13)
    cbar.ax.text(
        0.5, 1.03, "Better",
        transform=cbar.ax.transAxes,
        ha="center", va="bottom", fontsize=14, fontweight="bold", color="#1565C0",
    )
    cbar.ax.text(
        0.5, -0.03, "Worse",
        transform=cbar.ax.transAxes,
        ha="center", va="top", fontsize=14, fontweight="bold", color="#C62828",
    )

    # Despine for publication style
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    cbar.ax.spines["top"].set_visible(False)
    cbar.ax.spines["right"].set_visible(False)

    # Significance note (compact, below plot)
    ax.text(
        1.0, -0.06,
        "* = Holm-adjusted p < 0.05",
        transform=ax.transAxes, ha="right", va="top",
        fontsize=13, fontstyle="italic", color="black",
    )

    # Save
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight")
    fig.savefig(os.path.splitext(out_path)[0] + ".pdf", bbox_inches="tight")
    plt.close(fig)


def infer_output_dir(csv_path: str, output_dir: str = "") -> str:
    if output_dir:
        return output_dir
    return os.path.join(os.path.dirname(csv_path), "plots")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plot model comparison figures for Option A shift results.")
    parser.add_argument(
        "--csv", nargs="*", default=None,
        help="Path(s) to Option A CSV file(s). Defaults to all Shift_OptionA CSVs found.",
    )
    parser.add_argument("--outdir", default="", help="Output directory. Defaults to <csv_dir>/plots.")
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.05,
        help="Holm-adjusted significance threshold for filled markers.",
    )
    parser.add_argument(
        "--skip-heatmap",
        action="store_true",
        help="Only generate the line plot.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    csv_paths = args.csv if args.csv else DEFAULT_CSVS
    if not csv_paths:
        raise SystemExit("No CSV files found. Provide --csv or check DEFAULT_CSV_DIR.")

    for csv_path in csv_paths:
        print(f"\n--- Processing: {os.path.basename(csv_path)} ---")
        rows, signal, metric = load_optionA_csv(csv_path)
        levels, models, model_data = build_model_series(rows)

        outdir = infer_output_dir(csv_path, args.outdir)
        ensure_dir(outdir)

        base_name = f"OptionA_{signal}_{metric}"
        line_path = os.path.join(outdir, f"{base_name}_line.png")
        plot_line_comparison(levels, models, model_data, signal, metric, line_path, args.alpha)
        print(f"Wrote line plot: {line_path}")

        if not args.skip_heatmap:
            heatmap_path = os.path.join(outdir, f"{base_name}_heatmap.png")
            plot_heatmap(levels, models, model_data, signal, metric, heatmap_path)
            print(f"Wrote heatmap: {heatmap_path}")


if __name__ == "__main__":
    main()