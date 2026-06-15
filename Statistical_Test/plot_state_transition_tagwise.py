#!/usr/bin/env python3
"""
Plot model comparison figures from a tagwise state-transition CSV.

Input CSV format is the output of Statistical_Test/state_transition.py:
    tag,model,baseline,n_used,median_model,median_baseline,median_delta,z_wilcoxon,p_value,p_holm

Default outputs:
  - line plot: median delta vs Linear across tags
  - heatmap:   median delta vs Linear by model x tag

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
except ModuleNotFoundError as exc:
    raise SystemExit(
        "matplotlib is required to plot figures. Activate the environment "
        "you use for the stats scripts, then rerun this script."
    ) from exc

matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.serif'] = ['Nimbus Roman', 'DejaVu Serif']


DEFAULT_CSV_DIR = (
    "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/"
    "Time_Series_Forecast/Model_Comparison/Statistical_Results/"
    "Single_State_Change/tagwise_paired_tests"
)

# All three metrics
DEFAULT_CSVS = [
    os.path.join(DEFAULT_CSV_DIR, "tagwise_vs_Linear_mae.csv"),
    os.path.join(DEFAULT_CSV_DIR, "tagwise_vs_Linear_freq.csv"),
    os.path.join(DEFAULT_CSV_DIR, "tagwise_vs_Linear_phase.csv"),
]


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


def _tag_sort_key(tag: str) -> Tuple[int, int, str]:
    if tag == "win_no_transition_A":
        return (0, 0, tag)
    if tag == "win_no_transition_B":
        return (3, 0, tag)
    if tag.startswith("hist_d"):
        return (1, int(tag.split("hist_d")[1]), tag)
    if tag.startswith("fut_d"):
        return (2, int(tag.split("fut_d")[1]), tag)
    return (4, 0, tag)


def load_tagwise_csv(csv_path: str) -> Tuple[List[Dict[str, object]], str]:
    rows: List[Dict[str, object]] = []
    with open(csv_path, newline="") as handle:
        reader = csv.DictReader(handle)
        for raw in reader:
            row = {
                "tag": raw["tag"],
                "model": raw["model"],
                "baseline": raw["baseline"],
                "n_used": _to_int(raw["n_used"]),
                "median_model": _to_float(raw["median_model"]),
                "median_baseline": _to_float(raw["median_baseline"]),
                "median_delta": _to_float(raw["median_delta"]),
                "z_wilcoxon": _to_float(raw["z_wilcoxon"]),
                "p_value": _to_float(raw["p_value"]),
                "p_holm": _to_float(raw["p_holm"]),
            }
            rows.append(row)

    if not rows:
        raise ValueError(f"No rows found in {csv_path}")

    baseline = str(rows[0]["baseline"])
    return rows, baseline


# Future tags to keep (reduce clutter on the less-informative side)
_KEEP_FUT = {"fut_d02", "fut_d10", "fut_d20", "fut_d40"}


def build_model_series(
    rows: List[Dict[str, object]],
    baseline: str,
) -> Tuple[List[str], List[str], Dict[str, Dict[str, np.ndarray]]]:
    all_tags = sorted({str(row["tag"]) for row in rows}, key=_tag_sort_key)
    tags = [t for t in all_tags if not t.startswith("fut_d") or t in _KEEP_FUT]
    kept = set(tags)
    rows = [r for r in rows if str(r["tag"]) in kept]
    non_baseline_models = sorted({str(row["model"]) for row in rows if row["model"] != baseline})
    models = [baseline] + non_baseline_models

    tag_to_idx = {tag: idx for idx, tag in enumerate(tags)}
    model_data: Dict[str, Dict[str, np.ndarray]] = {}
    for model in models:
        size = len(tags)
        model_data[model] = {
            "delta": np.full(size, np.nan, dtype=float),
            "p_holm": np.full(size, np.nan, dtype=float),
            "n_used": np.full(size, np.nan, dtype=float),
        }

    for row in rows:
        model = str(row["model"])
        idx = tag_to_idx[str(row["tag"])]
        model_data[model]["delta"][idx] = float(row["median_delta"])
        model_data[model]["p_holm"][idx] = float(row["p_holm"])
        model_data[model]["n_used"][idx] = float(row["n_used"])

    return tags, models, model_data


def infer_metric_name(csv_path: str) -> str:
    base = os.path.basename(csv_path)
    stem = os.path.splitext(base)[0]
    if "_mae" in stem:
        return "mae"
    if "_freq" in stem:
        return "freq"
    if "_phase" in stem:
        return "phase"
    return "metric"


def metric_label(metric: str) -> str:
    labels = {
        "mae": "Median delta vs Linear (MAE)",
        "freq": "Median delta vs Linear (|Delta f|)",
        "phase": "Median delta vs Linear (|Delta phase|)",
    }
    return labels.get(metric, "Median delta vs Linear")


def plot_line_comparison(
    tags: List[str],
    models: List[str],
    model_data: Dict[str, Dict[str, np.ndarray]],
    baseline: str,
    metric: str,
    out_path: str,
    alpha_sig: float,
) -> None:
    ensure_dir(os.path.dirname(out_path))

    fig, ax = plt.subplots(figsize=(max(12.0, 0.58 * len(tags) + 4.0), 6.8), dpi=250)
    colors = plt.cm.tab20(np.linspace(0, 1, max(len(models), 2)))
    x = np.arange(len(tags))

    for idx, model in enumerate(models):
        if model == baseline:
            continue

        delta = model_data[model]["delta"]
        p_holm = model_data[model]["p_holm"]
        color = colors[idx]

        ax.plot(x, delta, marker="o", linewidth=1.7, markersize=4.0, color=color, label=model)

        sig_mask = np.isfinite(p_holm) & (p_holm < alpha_sig)
        if np.any(sig_mask):
            ax.scatter(
                x[sig_mask],
                delta[sig_mask],
                s=42,
                color=color,
                edgecolors="black",
                linewidths=0.6,
                zorder=5,
            )

    ax.axhline(0.0, color="black", linestyle="--", linewidth=1.1)
    ax.set_xticks(x)
    ax.set_xticklabels(tags, rotation=45, ha="right")
    ax.set_xlabel("Tag")
    ax.set_ylabel(metric_label(metric))
    ax.set_title(f"State-transition tagwise comparison ({metric})")
    ax.grid(True, axis="y", linestyle="--", alpha=0.35)

    # Despine for publication style
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for xpos in x:
        ax.axvline(x=xpos - 0.5, color="0.92", linewidth=0.6, zorder=0)

    ax.text(
        0.99,
        0.01,
        f"Filled marker: Holm p < {alpha_sig:g}\nNegative is better than {baseline}",
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


def _shorten_tag(tag: str) -> str:
    """Abbreviate tag names for cleaner x-axis labels."""
    if tag == "win_no_transition_A":
        return "A"
    if tag == "win_no_transition_B":
        return "B"
    if tag.startswith("hist_d"):
        num = tag.split("hist_d")[1].lstrip("0") or "0"
        return f"H{num}"
    if tag.startswith("fut_d"):
        num = tag.split("fut_d")[1].lstrip("0") or "0"
        return f"F{num}"
    return tag


def _tag_group(tag: str) -> str:
    """Return group name for vertical separator logic."""
    if tag.startswith("win_no_transition_A"):
        return "A"
    if tag.startswith("hist_d"):
        return "hist"
    if tag.startswith("fut_d"):
        return "fut"
    if tag.startswith("win_no_transition_B"):
        return "B"
    return "other"


def plot_heatmap(
    tags: List[str],
    models: List[str],
    model_data: Dict[str, Dict[str, np.ndarray]],
    baseline: str,
    metric: str,
    out_path: str,
    alpha_sig: float,
) -> None:
    ensure_dir(os.path.dirname(out_path))

    # --- Sort models by average performance (best first) ------------------
    plot_models = [model for model in models if model != baseline]
    plot_models = sorted(plot_models, key=lambda m: np.nanmean(model_data[m]["delta"]))

    # Negate: positive = improvement over Linear
    matrix = -np.vstack([model_data[model]["delta"] for model in plot_models])

    # Color scale (diverging at 0)
    finite = matrix[np.isfinite(matrix)]
    if finite.size == 0:
        vlim = 1.0
    else:
        vlim = float(np.max(np.abs(finite)))
        if vlim == 0:
            vlim = 1.0

    n_models = len(plot_models)
    n_tags = len(tags)
    short_labels = [_shorten_tag(t) for t in tags]

    # --- Figure -----------------------------------------------------------
    fig_w = max(10.0, 0.65 * n_tags + 4.0)
    fig_h = max(7.0, 0.70 * n_models + 3.0)
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=300)

    # Blue = positive = better, Red = negative = worse
    im = ax.imshow(
        matrix, cmap="RdBu", aspect="auto",
        vmin=-vlim, vmax=vlim,
    )

    # --- Gridlines between cells ------------------------------------------
    for i in range(n_models + 1):
        ax.axhline(i - 0.5, color="#CCCCCC", linewidth=0.5)
    for j in range(n_tags + 1):
        ax.axvline(j - 0.5, color="#CCCCCC", linewidth=0.5)

    # --- Group separators (thick lines between A / hist / fut / B) --------
    groups = [_tag_group(t) for t in tags]
    for j in range(1, n_tags):
        if groups[j] != groups[j - 1]:
            ax.axvline(j - 0.5, color="#444444", linewidth=2.0, zorder=3)

    # --- Axes labels ------------------------------------------------------
    ax.set_xticks(np.arange(n_tags))
    ax.set_xticklabels(short_labels, fontsize=15, fontweight="bold", rotation=0, ha="center")
    ax.set_xlabel("Signal Tag", fontsize=17, fontweight="bold")

    # Group labels below x-axis
    group_spans = {}
    for j, g in enumerate(groups):
        group_spans.setdefault(g, []).append(j)
    group_nice = {"A": "No Tran. A", "hist": "In Context", "fut": "No Context", "B": "No Tran. B"}
    for g, indices in group_spans.items():
        mid = (indices[0] + indices[-1]) / 2.0
        ax.text(
            mid, n_models + 0.3, group_nice.get(g, g),
            ha="center", va="top", fontsize=15, fontweight="bold", color="#333333",
        )

    ax.set_yticks(np.arange(n_models))
    ax.set_yticklabels(plot_models, fontsize=16, fontweight="bold")
    ax.set_ylabel("Model", fontsize=17, fontweight="bold")

    # --- Title ------------------------------------------------------------
    metric_nice = {"mae": "\u0394MAE", "freq": "\u0394|Freq Error|", "phase": "\u0394|Phase Error|"}.get(metric, metric)
    ax.set_title(
        f"Model Performance Across Signal Tags \u2014 {metric_nice}\n"
        f"(State Transition)",
        fontweight="bold", fontsize=19, pad=16,
    )

    # --- Significance markers in cells (no numeric values) -----------------
    for i, model in enumerate(plot_models):
        pvals = model_data[model]["p_holm"]
        for j in range(n_tags):
            value = matrix[i, j]
            if not np.isfinite(value):
                cell_text = "N/A"
                text_color = "#888888"
            elif np.isfinite(pvals[j]) and pvals[j] < alpha_sig:
                cell_text = "*"
                norm_val = (value + vlim) / (2.0 * vlim)
                text_color = "white" if norm_val < 0.25 or norm_val > 0.75 else "#222222"
            else:
                continue

            ax.text(
                j, i, cell_text,
                ha="center", va="center",
                fontsize=28, fontweight="bold",
                color=text_color,
            )

    # --- Enhanced color bar -----------------------------------------------
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Improvement over Linear", fontsize=18, fontweight="bold")
    cbar.ax.tick_params(labelsize=14)
    cbar.ax.text(
        0.5, 1.03, "Better",
        transform=cbar.ax.transAxes,
        ha="center", va="bottom", fontsize=16, fontweight="bold", color="#1565C0",
    )
    cbar.ax.text(
        0.5, -0.03, "Worse",
        transform=cbar.ax.transAxes,
        ha="center", va="top", fontsize=16, fontweight="bold", color="#C62828",
    )

    # Despine for publication style
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    cbar.ax.spines["top"].set_visible(False)
    cbar.ax.spines["right"].set_visible(False)

    # --- Significance note (top right corner) -----------------------------
    ax.text(
        1.0, 1.02,
        f"* = Holm-adjusted p < {alpha_sig:g}",
        transform=ax.transAxes, ha="right", va="bottom",
        fontsize=14, fontstyle="italic", color="black",
    )

    # --- Save -------------------------------------------------------------
    fig.tight_layout()
    fig.savefig(out_path, bbox_inches="tight")
    fig.savefig(os.path.splitext(out_path)[0] + ".pdf", bbox_inches="tight")
    plt.close(fig)


def infer_output_dir(csv_path: str, output_dir: str = "") -> str:
    if output_dir:
        return output_dir
    return os.path.join(os.path.dirname(csv_path), "plots")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plot tagwise state-transition model comparison figures.")
    parser.add_argument(
        "--csv", nargs="*", default=None,
        help="Path(s) to tagwise_vs_Linear CSV file(s). Defaults to all three metrics (mae, freq, phase).",
    )
    parser.add_argument("--outdir", default="", help="Output directory. Defaults to <csv_dir>/plots.")
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.05,
        help="Holm-adjusted significance threshold for markers and heatmap stars.",
    )
    parser.add_argument(
        "--skip-heatmap",
        action="store_true",
        help="Only generate the line plot.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Use provided CSVs or default to all three metrics
    csv_paths = args.csv if args.csv else [p for p in DEFAULT_CSVS if os.path.isfile(p)]
    if not csv_paths:
        raise SystemExit("No CSV files found. Provide --csv or check DEFAULT_CSVS paths.")

    for csv_path in csv_paths:
        print(f"\n--- Processing: {os.path.basename(csv_path)} ---")
        rows, baseline = load_tagwise_csv(csv_path)
        tags, models, model_data = build_model_series(rows, baseline)
        metric = infer_metric_name(csv_path)

        outdir = infer_output_dir(csv_path, args.outdir)
        ensure_dir(outdir)

        stem = os.path.splitext(os.path.basename(csv_path))[0]
        line_path = os.path.join(outdir, f"{stem}_line.png")
        plot_line_comparison(tags, models, model_data, baseline, metric, line_path, args.alpha)
        print(f"Wrote line plot: {line_path}")

        if not args.skip_heatmap:
            heatmap_path = os.path.join(outdir, f"{stem}_heatmap.png")
            plot_heatmap(tags, models, model_data, baseline, metric, heatmap_path, args.alpha)
            print(f"Wrote heatmap: {heatmap_path}")


if __name__ == "__main__":
    main()
