#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# Output directory
# ============================================================
OUT_DIR = Path("evaluation_paradigms_all")
OUT_DIR.mkdir(exist_ok=True, parents=True)


# ============================================================
# Signal model
# s(t) = A sin(2π f t + β sin(2π f_mod t)) + offset
# ============================================================
def s_formula(t, A=1.0, f=0.08, beta=1.1, f_mod=0.02, offset=0.0):
    t = np.asarray(t, dtype=float)
    return A * np.sin(2 * np.pi * f * t + beta * np.sin(2 * np.pi * f_mod * t)) + offset


def gaussian_noise(x, sigma=0.18, seed=0):
    rng = np.random.default_rng(seed)
    return x + rng.normal(0.0, sigma, size=len(x))


def make_two_state_transition(t, split, p1, p2):
    x = np.empty_like(t, dtype=float)
    x[:split] = s_formula(t[:split], **p1)
    x[split:] = s_formula(t[split:], **p2)
    return x


def make_symmetric_markov_switching(t, p_state1, p_state2, p_switch=0.30, dwell=10, seed=1):
    """
    Symmetric 2-state Markov switching:
        P = [[1-p, p],
             [p, 1-p]]
    States are piecewise constant over blocks of length `dwell`.
    """
    rng = np.random.default_rng(seed)
    n = len(t)
    states = np.zeros(n, dtype=int)
    cur = 0

    for start in range(0, n, dwell):
        end = min(n, start + dwell)
        states[start:end] = cur
        if rng.random() < p_switch:
            cur = 1 - cur

    x = np.empty(n, dtype=float)
    for i in range(n):
        params = p_state1 if states[i] == 0 else p_state2
        x[i] = s_formula(np.array([t[i]]), **params)[0]

    return x, states


# ============================================================
# Global setup
# ============================================================
T = 150
HISTORY_LEN = 50
t = np.arange(T)
future_t = t[HISTORY_LEN:]

# Choose where the two-state transition happens.
# It can be anywhere:
#   < HISTORY_LEN : transition in history
#   = HISTORY_LEN : transition at forecast boundary
#   > HISTORY_LEN : transition in future
TWO_STATE_SPLIT = 78


# ============================================================
# Parameter regimes
# ============================================================
# Clean / base
clean_params = dict(A=1.0, f=0.080, beta=1.05, f_mod=0.020, offset=0.0)

# Distribution shift for SPM:
# train on one frequency regime, test on another
train_spm = dict(A=1.0, f=0.080, beta=1.05, f_mod=0.020, offset=0.0)
test_spm_shift = dict(A=1.0, f=0.125, beta=1.05, f_mod=0.020, offset=0.0)

# Two-state / Markov states
state1 = dict(A=0.95, f=0.070, beta=0.90, f_mod=0.018, offset=0.0)
state2 = dict(A=1.12, f=0.115, beta=1.25, f_mod=0.030, offset=0.0)


# ============================================================
# 1) Clean condition
# ============================================================
gt_clean = s_formula(t, **clean_params)
pred_clean = s_formula(
    future_t, A=0.98, f=0.079, beta=0.98, f_mod=0.021, offset=0.0
)


# ============================================================
# 2) Noisy condition
# ============================================================
gt_noisy = gaussian_noise(gt_clean, sigma=0.18, seed=4)
pred_noisy = s_formula(
    future_t, A=0.98, f=0.079, beta=0.98, f_mod=0.021, offset=0.0
)


# ============================================================
# 3) Distribution shift for SPM
# History: train regime
# Future ground truth: shifted test regime
# Prediction: biased toward train regime
# ============================================================
gt_shift = np.empty(T, dtype=float)
gt_shift[:HISTORY_LEN] = s_formula(t[:HISTORY_LEN], **train_spm)
gt_shift[HISTORY_LEN:] = s_formula(t[HISTORY_LEN:], **test_spm_shift)

pred_shift = s_formula(future_t, **train_spm)


# ============================================================
# 4) Two-state transition
# Single transition S1 -> S2, at arbitrary time TWO_STATE_SPLIT
# ============================================================
gt_two_state = make_two_state_transition(t, TWO_STATE_SPLIT, state1, state2)

pred_two_state = np.empty(len(future_t), dtype=float)
switch_in_future = TWO_STATE_SPLIT - HISTORY_LEN

if switch_in_future <= 0:
    # Transition happened before forecast start; future is all state2-like
    pred_two_state[:] = s_formula(
        future_t, A=1.02, f=0.102, beta=1.10, f_mod=0.025, offset=0.0
    )
elif switch_in_future >= len(future_t):
    # Transition happens after displayed future; future is all state1-like
    pred_two_state[:] = s_formula(
        future_t, A=0.98, f=0.082, beta=0.98, f_mod=0.020, offset=0.0
    )
else:
    pred_two_state[:switch_in_future] = s_formula(
        future_t[:switch_in_future], A=0.98, f=0.082, beta=0.98, f_mod=0.020, offset=0.0
    )
    pred_two_state[switch_in_future:] = s_formula(
        future_t[switch_in_future:], A=1.02, f=0.102, beta=1.10, f_mod=0.025, offset=0.0
    )


# ============================================================
# 5) Symmetric Markov switching
# ============================================================
gt_markov, states_markov = make_symmetric_markov_switching(
    t, state1, state2, p_switch=0.35, dwell=10, seed=5
)

pred_markov = s_formula(
    future_t, A=1.00, f=0.095, beta=1.00, f_mod=0.023, offset=0.0
)


# ============================================================
# Plot helpers
# ============================================================
def plot_main(ax, gt, pred_future, title, note=None):
    ax.axvspan(0, HISTORY_LEN, alpha=0.12)
    ax.axvline(HISTORY_LEN, linestyle="--", linewidth=1.2)

    ax.plot(t[:HISTORY_LEN + 1], gt[:HISTORY_LEN + 1], linewidth=2.2, label="Observed history")
    ax.plot(t[HISTORY_LEN:], gt[HISTORY_LEN:], linewidth=2.2, label="Ground-truth future")
    ax.plot(future_t, pred_future, linestyle="--", linewidth=2.2, label="Predicted future")

    ax.set_title(title, fontsize=16, fontweight="bold")
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude")
    ax.grid(alpha=0.25)

    if note is not None:
        ax.text(
            0.02,
            0.96,
            note,
            transform=ax.transAxes,
            va="top",
            ha="left",
            fontsize=10,
            bbox=dict(
                boxstyle="round,pad=0.25",
                facecolor="white",
                alpha=0.85,
                edgecolor="0.6",
            ),
        )


def add_two_state_overlay(ax, split, labels=("S1", "S2")):
    """
    Shows state regions and explicitly separates:
      - forecast boundary (already dashed in plot_main)
      - state transition (dotted here)
    """
    y0, y1 = ax.get_ylim()
    h = 0.10 * (y1 - y0)
    base = y0 + 0.02 * (y1 - y0)

    segments = [(0, split, labels[0]), (split, T, labels[1])]

    for a, b, lab in segments:
        ax.axvspan(a, b, ymin=0.0, ymax=0.08, alpha=0.10)
        xc = 0.5 * (a + b)
        ax.text(
            xc,
            base + 0.5 * h,
            lab,
            ha="center",
            va="center",
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.9, edgecolor="0.6"),
        )

    ax.axvline(split, linestyle=":", linewidth=1.4)

    ax.text(
        HISTORY_LEN + 1,
        y1 - 0.08 * (y1 - y0),
        "forecast boundary",
        fontsize=9,
    )
    ax.text(
        split + 1,
        y1 - 0.16 * (y1 - y0),
        "state transition",
        fontsize=9,
    )


def add_markov_overlay(ax, states, step=10):
    y0, y1 = ax.get_ylim()
    h = 0.10 * (y1 - y0)
    base = y0 + 0.02 * (y1 - y0)

    for s in range(0, len(states), step):
        e = min(len(states), s + step)
        alpha = 0.10 if states[s] == 0 else 0.18
        ax.axvspan(s, e, ymin=0.0, ymax=0.08, alpha=alpha)
        xc = 0.5 * (s + e)
        label = "S1" if states[s] == 0 else "S2"
        ax.text(
            xc,
            base + 0.5 * h,
            label,
            ha="center",
            va="center",
            fontsize=8,
        )


def save_figure(fig, name):
    png = OUT_DIR / f"{name}.png"
    svg = OUT_DIR / f"{name}.svg"
    fig.savefig(png, bbox_inches="tight")
    fig.savefig(svg, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {png}")
    print(f"Saved {svg}")


# ============================================================
# Save individual figures
# ============================================================
# Clean
fig, ax = plt.subplots(figsize=(10, 4.2), dpi=220)
plot_main(ax, gt_clean, pred_clean, "Clean condition")
ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.18))
fig.tight_layout()
save_figure(fig, "clean_condition")

# Noisy
fig, ax = plt.subplots(figsize=(10, 4.2), dpi=220)
plot_main(ax, gt_noisy, pred_noisy, "Noisy condition", note="Gaussian noise added")
ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.18))
fig.tight_layout()
save_figure(fig, "noisy_condition")

# Distribution shift
fig, ax = plt.subplots(figsize=(10, 4.2), dpi=220)
plot_main(
    ax,
    gt_shift,
    pred_shift,
    "Distribution shift",
    note="History: train frequency regime\nFuture: shifted test frequency regime",
)
ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.18))
fig.tight_layout()
save_figure(fig, "spm_distribution_shift")

# Two-state transition
fig, ax = plt.subplots(figsize=(10, 4.2), dpi=220)
plot_main(
    ax,
    gt_two_state,
    pred_two_state,
    "Two-state transition",
    note="Single transition from S1 to S2\nTransition time is independent of forecast boundary",
)
add_two_state_overlay(ax, TWO_STATE_SPLIT, labels=("S1", "S2"))
ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.18))
fig.tight_layout()
save_figure(fig, "two_state_transition")

# Symmetric Markov switching
fig, ax = plt.subplots(figsize=(10, 4.2), dpi=220)
plot_main(
    ax,
    gt_markov,
    pred_markov,
    "Symmetric Markov switching",
    note="Two states with equal switching probability",
)
add_markov_overlay(ax, states_markov, step=10)
ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.18))
fig.tight_layout()
save_figure(fig, "symmetric_markov_switching")


# ============================================================
# Optional combined figure
# ============================================================
fig, axes = plt.subplots(5, 1, figsize=(11, 18), dpi=220)

plot_main(axes[0], gt_clean, pred_clean, "Clean condition")
plot_main(axes[1], gt_noisy, pred_noisy, "Noisy condition", note="Gaussian noise added")
plot_main(
    axes[2],
    gt_shift,
    pred_shift,
    "Distribution shift",
    note="History: train frequency regime\nFuture: shifted test frequency regime",
)
plot_main(
    axes[3],
    gt_two_state,
    pred_two_state,
    "Two-state transition",
    note="Single transition from S1 to S2\nTransition time is independent of forecast boundary",
)
add_two_state_overlay(axes[3], TWO_STATE_SPLIT, labels=("S1", "S2"))

plot_main(
    axes[4],
    gt_markov,
    pred_markov,
    "Symmetric Markov switching",
    note="Two states with equal switching probability",
)
add_markov_overlay(axes[4], states_markov, step=10)

handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 0.995))
fig.tight_layout(rect=[0, 0, 1, 0.98])

combined_png = OUT_DIR / "all_paradigms_combined.png"
combined_svg = OUT_DIR / "all_paradigms_combined.svg"
fig.savefig(combined_png, bbox_inches="tight")
fig.savefig(combined_svg, bbox_inches="tight")
plt.close(fig)

print(f"Saved {combined_png}")
print(f"Saved {combined_svg}")