#!/usr/bin/env python3
"""
Generate publication figures for the clean-condition results.

Main figure (Fig. 4):
  (A) Clean paradigm illustration  (top, full width)
  (B) Dual-phase |Δphase| bars    (bottom-left)
  (C) Drift-harmonic |Δphase| bars (bottom-right)

Appendix figures:
  Supp Fig 1: Dual-phase  — all 3 metrics side by side
  Supp Fig 2: Single-phase — all 3 metrics side by side
  Supp Fig 3: Drift-harmonic — all 3 metrics side by side
"""

import os
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from matplotlib.gridspec import GridSpec

matplotlib.rcParams["font.family"] = "serif"
matplotlib.rcParams["font.serif"] = ["Nimbus Roman", "DejaVu Serif"]

# ── paths ──────────────────────────────────────────────────────────────
TABLE_ROOT = (
    "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/"
    "Time_Series_Forecast/Model_Comparison/Statistical/Clean_BaselineVsLinear"
)
# Where to load the paradigm illustration data from
# Use Dual Phase Modulation to show the full -1 to 1 oscillatory range
PARADIGM_MODEL_PATH = (
    "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/"
    "Time_Series_Forecast/Train_Test_Validation/"
    "long_term_forecast_PatchTST_50_100_PatchTST_Dual_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_15_Shift_0"
)
HISTORY_LEN = 50

OUT_DIR = (
    "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/"
    "Time_Series_Forecast/new_plots/clean_paper"
)
os.makedirs(OUT_DIR, exist_ok=True)

SIGNALS = ["Dual_Phase_Modulation", "Single_Phase_Modulation", "Drift_Harmonic"]
METRICS = ["phase", "freq", "mae"]
METRIC_TITLES = {
    "phase": r"|$\Delta$phase| (deg)",
    "freq":  r"|$\Delta$f|",
    "mae":   "MAE",
}
SIGNAL_LABELS = {
    "Dual_Phase_Modulation":   "Dual-Phase Modulation",
    "Single_Phase_Modulation": "Single-Phase Modulation",
    "Drift_Harmonic":          "Drift Harmonic",
}


# ── tier colours (match existing style) ────────────────────────────────
TEAL   = "#0D7377"
GREEN  = "#4CAF50"
ORANGE = "#FFA726"
RED    = "#EF5350"
GRAY   = "#D3D3D3"


def tier_color(val, is_baseline=False, max_val=1.0):
    if is_baseline:
        return GRAY
    if max_val <= 0:
        max_val = 1.0
    frac = val / max_val if max_val != 0 else 0.0
    if val < 0:
        return RED
    if frac > 0.50:
        return TEAL
    if frac > 0.25:
        return GREEN
    return ORANGE


# ── load table helper ──────────────────────────────────────────────────
def load_table(signal, metric):
    csv = os.path.join(TABLE_ROOT, signal, "tables", f"{metric}_delta_vs_Linear.csv")
    return pd.read_csv(csv)


# ── bar-plot on a given Axes ───────────────────────────────────────────
def draw_bar(ax, tbl, title, fontscale=1.0, show_legend=True, show_xlabel=True,
             legend_loc="lower right"):
    """
    Horizontal bar chart of improvement over Linear baseline.

    fontscale: multiplier applied to ALL font sizes so the same function
               works for both full-width main-figure panels and the wider
               appendix panels.
    """
    d = tbl.copy()
    d["improvement"] = -d["delta_vs_linear"]
    d["ci_lo_plot"]  = -d["ci_hi"]
    d["ci_hi_plot"]  = -d["ci_lo"]
    d = d.sort_values("improvement", ascending=False).reset_index(drop=True)

    models   = d["model"].tolist()
    n        = len(models)
    y        = np.arange(n)
    delta    = d["improvement"].values
    ci_lo    = d["ci_lo_plot"].values
    ci_hi    = d["ci_hi_plot"].values
    xerr     = np.vstack([delta - ci_lo, ci_hi - delta])

    pos_vals = delta[delta > 0]
    max_pos  = float(pos_vals.max()) if len(pos_vals) > 0 else 1.0
    colors   = [
        tier_color(v, is_baseline=(m == "Linear"), max_val=max_pos)
        for v, m in zip(delta, models)
    ]

    ax.barh(
        y, delta, xerr=xerr,
        capsize=3,
        color=colors, edgecolor="black", linewidth=0.5,
        ecolor="#333333", error_kw=dict(lw=1.2),
        height=0.65,
    )

    # zero line
    ax.axvline(0.0, linestyle="-", linewidth=2.0, color="black", zorder=4)

    # data labels
    x_range = max(abs(delta.min()), abs(delta.max()), 0.01)
    for i, v in enumerate(delta):
        label  = f"{v:+.1%}" if abs(v) < 1.0 else f"{v:+.2f}"
        offset = x_range * 0.025
        ha     = "left" if v >= 0 else "right"
        xpos   = v + offset if v >= 0 else v - offset
        ax.text(
            xpos, y[i], label,
            va="center", ha=ha,
            fontsize=7 * fontscale, fontweight="bold", color="#222222",
        )

    ax.set_yticks(y)
    ax.set_yticklabels(models, fontsize=8 * fontscale, fontweight="bold")
    ax.invert_yaxis()

    pad = x_range * 0.32
    ax.set_xlim(-max(abs(delta.min()), 0) - pad,
                max(abs(delta.max()), 0) + pad)

    if show_xlabel:
        ax.set_xlabel(
            "Improvement over Linear Baseline (positive = better)",
            fontsize=8 * fontscale, fontweight="bold",
        )
    else:
        ax.set_xlabel("")
    ax.set_title(title, fontweight="bold", fontsize=9 * fontscale, pad=8)

    ax.grid(True, axis="x", linestyle="--", alpha=0.30, color="#888888")
    ax.grid(True, axis="y", linestyle=":", alpha=0.15, color="#AAAAAA")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    if show_legend:
        color_set = set(colors)
        handles = []
        if TEAL   in color_set: handles.append(mpatches.Patch(fc=TEAL,   ec="black", lw=0.6, label="Best"))
        if GREEN  in color_set: handles.append(mpatches.Patch(fc=GREEN,  ec="black", lw=0.6, label="Good"))
        if ORANGE in color_set: handles.append(mpatches.Patch(fc=ORANGE, ec="black", lw=0.6, label="Moderate"))
        if RED    in color_set: handles.append(mpatches.Patch(fc=RED,    ec="black", lw=0.6, label="Worse than baseline"))
        if GRAY   in color_set: handles.append(mpatches.Patch(fc=GRAY,   ec="black", lw=0.6, label="Baseline (Linear)"))
        handles.append(Line2D([0], [0], color="black", lw=2.0, ls="-", label="Linear Baseline (x = 0)"))
        handles.append(mpatches.Patch(fc="none", ec="none", label="Error bars = 95% CI"))

        leg = ax.legend(
            handles=handles, title="Performance Tier",
            title_fontsize=7 * fontscale, fontsize=6.5 * fontscale,
            loc=legend_loc,
            framealpha=0.95, edgecolor="#666666",
            fancybox=True, borderpad=0.8,
            labelspacing=0.4, handlelength=1.4, handleheight=1.0,
        )
        leg.get_title().set_fontweight("bold")


# ── paradigm panel (A) ─────────────────────────────────────────────────
def draw_paradigm(ax):
    """Clean-paradigm illustration: observed history + GT future + predicted future."""
    true = np.load(os.path.join(PARADIGM_MODEL_PATH, "test_true_with_history.npy"))
    pred = np.load(os.path.join(PARADIGM_MODEL_PATH, "test_pred_with_history.npy"))
    if true.ndim == 3:
        true = true.squeeze(-1)
    if pred.ndim == 3:
        pred = pred.squeeze(-1)

    # pick a visually clear oscillatory sequence:
    # want large amplitude range AND near-median MAE
    amp_range = np.ptp(true, axis=1)                     # peak-to-peak per seq
    mae = np.mean(np.abs(pred[:, HISTORY_LEN:] - true[:, HISTORY_LEN:]), axis=1)
    # among the top-25 % amplitude sequences, pick the one closest to median MAE
    top_amp_idx = np.where(amp_range >= np.percentile(amp_range, 75))[0]
    median_mae = np.median(mae)
    best = top_amp_idx[np.argmin(np.abs(mae[top_amp_idx] - median_mae))]
    idx = best

    seq_true = true[idx]
    seq_pred = pred[idx]
    T = len(seq_true)
    t = np.arange(T)

    ax.axvspan(0, HISTORY_LEN - 1, color="#B3D4FC", alpha=0.35, label="Observed History")
    ax.axvline(HISTORY_LEN - 1, color="gray", linestyle="--", linewidth=1.0)

    ax.plot(t[:HISTORY_LEN], seq_true[:HISTORY_LEN],
            color="#1565C0", linewidth=1.8)
    ax.plot(t[HISTORY_LEN - 1:], seq_true[HISTORY_LEN - 1:],
            color="#E65100", linewidth=1.8, label="Ground-Truth Future")
    ax.plot(t[HISTORY_LEN - 1:], seq_pred[HISTORY_LEN - 1:],
            color="#2E7D32", linewidth=1.8, linestyle="--", label="Predicted Future")

    ax.set_xlabel("Time", fontsize=9, fontweight="bold")
    ax.set_ylabel("Amplitude", fontsize=9, fontweight="bold")
    ax.set_title("Clean Paradigm", fontsize=10, fontweight="bold", pad=8)
    ax.tick_params(labelsize=8)
    ax.grid(alpha=0.20)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # legend above the panel
    handles = [
        mpatches.Patch(fc="#B3D4FC", ec="none", alpha=0.6, label="Observed History"),
        mpatches.Patch(fc="#E65100", ec="none", label="Ground-Truth Future"),
        mpatches.Patch(fc="#2E7D32", ec="none", label="Predicted Future"),
    ]
    ax.legend(
        handles=handles, loc="upper center",
        bbox_to_anchor=(0.5, 1.22), ncol=3,
        fontsize=8, frameon=False,
    )


# =====================================================================
#  MAIN FIGURE  (Fig. 4)
# =====================================================================
def make_main_figure():
    """
    Full-width figure (~180 mm / 7 in) with three panels:
      A  — paradigm illustration  (top, full width)
      B  — Dual-phase |Δphase|   (bottom-left)
      C  — Drift-harmonic |Δphase| (bottom-right)

    Font sizes are chosen so that at 7-inch width printed at ~90%
    scale in a two-column paper, labels remain >= 7 pt.
    """
    # ── Option 1: Full 3-panel figure (A + B + C) ─────────────────────
    fig_full = plt.figure(figsize=(7.2, 9.2), dpi=300)
    gs = GridSpec(
        3, 2, figure=fig_full,
        height_ratios=[1, 1.8, 0.12],
        hspace=0.50, wspace=0.60,
    )

    ax_a = fig_full.add_subplot(gs[0, :])
    draw_paradigm(ax_a)

    ax_b = fig_full.add_subplot(gs[1, 0])
    tbl_b = load_table("Dual_Phase_Modulation", "phase")
    draw_bar(ax_b, tbl_b,
             title="Dual-Phase Modulation\n" + r"|$\Delta$phase| (deg)",
             fontscale=1.0, show_legend=False, show_xlabel=False)

    ax_c = fig_full.add_subplot(gs[1, 1])
    tbl_c = load_table("Drift_Harmonic", "phase")
    draw_bar(ax_c, tbl_c,
             title="Drift Harmonic\n" + r"|$\Delta$phase| (deg)",
             fontscale=1.0, show_legend=False, show_xlabel=False)

    # shared x-label between both panels
    fig_full.text(0.5, 0.17, "Improvement over Linear Baseline (positive = better)",
                  ha="center", fontsize=9, fontweight="bold")

    ax_leg = fig_full.add_subplot(gs[2, :])
    ax_leg.axis("off")
    legend_handles = [
        mpatches.Patch(fc=TEAL,   ec="black", lw=0.6, label="Best"),
        mpatches.Patch(fc=ORANGE, ec="black", lw=0.6, label="Moderate"),
        mpatches.Patch(fc=RED,    ec="black", lw=0.6, label="Worse than baseline"),
        mpatches.Patch(fc=GRAY,   ec="black", lw=0.6, label="Baseline (Linear)"),
        Line2D([0], [0], color="black", lw=2.0, ls="-", label="Linear Baseline (x = 0)"),
        mpatches.Patch(fc="none", ec="none", label="Error bars = 95% CI"),
    ]
    leg = ax_leg.legend(handles=legend_handles, loc="center", ncol=6,
                        prop=dict(size=8.5, weight="bold"),
                        frameon=True, edgecolor="#666666",
                        fancybox=True, handlelength=1.4, handleheight=1.0,
                        columnspacing=1.2)

    out_full = os.path.join(OUT_DIR, "Fig4_clean_main_full.pdf")
    fig_full.savefig(out_full, bbox_inches="tight")
    fig_full.savefig(out_full.replace(".pdf", ".png"), bbox_inches="tight")
    plt.close(fig_full)
    print(f"Full main figure saved to {out_full}")

    # ── Option 2: B+C only (if you keep your existing panel A) ──────
    fig = plt.figure(figsize=(7.2, 5.8), dpi=300)
    gs2 = GridSpec(3, 2, figure=fig,
                   height_ratios=[1, 0.03, 0.07],
                   hspace=0.25, wspace=0.60)

    ax_b2 = fig.add_subplot(gs2[0, 0])
    draw_bar(ax_b2, tbl_b,
             title="Dual-Phase Modulation\n" + r"|$\Delta$phase| (deg)",
             fontscale=1.0, show_legend=False, show_xlabel=False)

    ax_c2 = fig.add_subplot(gs2[0, 1])
    draw_bar(ax_c2, tbl_c,
             title="Drift Harmonic\n" + r"|$\Delta$phase| (deg)",
             fontscale=1.0, show_legend=False, show_xlabel=False)

    # shared x-label in its own row
    ax_xlabel = fig.add_subplot(gs2[1, :])
    ax_xlabel.axis("off")
    ax_xlabel.text(0.5, 0.5, "Improvement over Linear Baseline (positive = better)",
                   ha="center", va="center", fontsize=9, fontweight="bold",
                   transform=ax_xlabel.transAxes)

    # legend row
    ax_leg2 = fig.add_subplot(gs2[2, :])
    ax_leg2.axis("off")
    ax_leg2.legend(handles=legend_handles, loc="center", ncol=6,
                   prop=dict(size=8.5, weight="bold"),
                   frameon=True, edgecolor="#666666",
                   fancybox=True, handlelength=1.4, handleheight=1.0,
                   columnspacing=1.2)

    out = os.path.join(OUT_DIR, "Fig4_clean_BC_only.pdf")
    fig.savefig(out, bbox_inches="tight")
    fig.savefig(out.replace(".pdf", ".png"), bbox_inches="tight")
    plt.close(fig)
    print(f"B+C only figure saved to {out}")


# =====================================================================
#  APPENDIX FIGURES  (one per signal family, 3 metrics each)
# =====================================================================
def make_appendix_figure(signal, supp_num):
    """
    Full-width figure with three side-by-side panels: |Δphase|, |Δf|, MAE.
    """
    fig = plt.figure(figsize=(7.5, 5.0), dpi=300)
    gs_app = GridSpec(3, 3, figure=fig,
                      height_ratios=[1, 0.03, 0.07],
                      hspace=0.25, wspace=0.75)

    for j, metric in enumerate(METRICS):
        ax = fig.add_subplot(gs_app[0, j])
        tbl = load_table(signal, metric)
        draw_bar(
            ax, tbl,
            title=f"{SIGNAL_LABELS[signal]}\n{METRIC_TITLES[metric]}",
            fontscale=0.9,
            show_legend=False,
            show_xlabel=False,
        )

    # shared x-label
    ax_xlabel = fig.add_subplot(gs_app[1, :])
    ax_xlabel.axis("off")
    ax_xlabel.text(0.5, 0.5, "Improvement over Linear Baseline (positive = better)",
                   ha="center", va="center", fontsize=8, fontweight="bold",
                   transform=ax_xlabel.transAxes)

    # shared legend
    ax_leg = fig.add_subplot(gs_app[2, :])
    ax_leg.axis("off")
    leg_handles = [
        mpatches.Patch(fc=TEAL,   ec="black", lw=0.6, label="Best"),
        mpatches.Patch(fc=ORANGE, ec="black", lw=0.6, label="Moderate"),
        mpatches.Patch(fc=RED,    ec="black", lw=0.6, label="Worse than baseline"),
        mpatches.Patch(fc=GRAY,   ec="black", lw=0.6, label="Baseline (Linear)"),
        Line2D([0], [0], color="black", lw=2.0, ls="-", label="Linear Baseline (x = 0)"),
        mpatches.Patch(fc="none", ec="none", label="Error bars = 95% CI"),
    ]
    ax_leg.legend(handles=leg_handles, loc="center", ncol=6,
                  fontsize=7, frameon=True, edgecolor="#666666",
                  fancybox=True, handlelength=1.4, handleheight=1.0,
                  columnspacing=1.0)

    out = os.path.join(OUT_DIR, f"SuppFig{supp_num}_{signal}_clean.pdf")
    fig.savefig(out, bbox_inches="tight")
    fig.savefig(out.replace(".pdf", ".png"), bbox_inches="tight")
    plt.close(fig)
    print(f"Appendix figure saved to {out}")


# =====================================================================
if __name__ == "__main__":
    make_main_figure()

    # Appendix: one figure per signal family
    for i, sig in enumerate(SIGNALS, start=1):
        make_appendix_figure(sig, supp_num=i)

    print("\nAll figures generated.")
