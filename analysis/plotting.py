"""Figure conventions for the revision: navy bold titles, blue italic subtitles, teal good / red warning,
error bars on every summary plot, SVG + high-resolution PNG."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

NAVY, BLUE, TEAL, RED, GRAY = "#16356c", "#2a5fa0", "#1b9e77", "#d62728", "#777777"

plt.rcParams.update({"font.family": "sans-serif", "font.size": 9, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.titleweight": "bold", "axes.titlecolor": NAVY,
                     "axes.labelcolor": "#222222", "legend.frameon": False, "svg.fonttype": "none"})


def title(ax, main, sub=None):
    ax.set_title(main, color=NAVY, fontweight="bold", loc="left", fontsize=10)
    if sub:
        ax.text(0.0, 1.02, sub, transform=ax.transAxes, color=BLUE, style="italic", fontsize=8.5, va="bottom")


def save(fig, path_no_ext, dpi=300):
    os.makedirs(os.path.dirname(path_no_ext), exist_ok=True)
    fig.savefig(path_no_ext + ".svg")
    fig.savefig(path_no_ext + ".png", dpi=dpi)
    plt.close(fig)
    return path_no_ext + ".png"
