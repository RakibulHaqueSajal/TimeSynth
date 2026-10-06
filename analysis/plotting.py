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


def title(ax, main, sub=None, wrap_at=78):
    """
    Navy bold title with an optional blue italic subtitle placed BELOW it.

    The subtitle is drawn just above the axes and the title is padded above that, so the two
    never overlap (they did when both were anchored at y = 1.0). Long subtitles are wrapped.
    """
    import textwrap
    if sub:
        sub = "\n".join(textwrap.wrap(sub, wrap_at))
        n_lines = sub.count("\n") + 1
        ax.set_title(main, color=NAVY, fontweight="bold", loc="left", fontsize=10,
                     pad=12 + 10 * n_lines)
        ax.text(0.0, 1.015, sub, transform=ax.transAxes, color=BLUE, style="italic",
                fontsize=8.5, va="bottom", ha="left")
    else:
        ax.set_title(main, color=NAVY, fontweight="bold", loc="left", fontsize=10, pad=8)


def save(fig, path_no_ext, dpi=300):
    os.makedirs(os.path.dirname(path_no_ext), exist_ok=True)
    fig.savefig(path_no_ext + ".svg")
    fig.savefig(path_no_ext + ".png", dpi=dpi)
    plt.close(fig)
    return path_no_ext + ".png"
