import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# -------------------------------------------------
# Parameters
# -------------------------------------------------
np.random.seed(7)
T = 150
history_len = 50
t = np.arange(T)
tf = t[history_len:]

p_switch = 0.5

f_s1 = 0.06
f_s2 = 0.11

# -------------------------------------------------
# Generate Markov state sequence
# -------------------------------------------------
states = np.zeros(T, dtype=int)
for i in range(1, T):
    if np.random.rand() < p_switch:
        states[i] = 1 - states[i-1]
    else:
        states[i] = states[i-1]

# -------------------------------------------------
# Generate true signal
# -------------------------------------------------
true = np.zeros(T)
for i in range(T):
    f = f_s2 if states[i] == 1 else f_s1
    true[i] = np.sin(2 * np.pi * f * i)

# Predicted future — slightly off phase to show imperfect prediction
pred = np.zeros(len(tf))
for idx, i in enumerate(tf):
    f = f_s2 if states[i] == 1 else f_s1
    pred[idx] = 0.97 * np.sin(2 * np.pi * f * i + 0.18)

# -------------------------------------------------
# Plot
# -------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 4.2), dpi=220)

# Shade S1/S2 regions
import matplotlib.patches as mpatches
prev_state = states[0]
seg_start = 0
for i in range(1, T + 1):
    current_state = states[i - 1] if i < T else -1
    if current_state != prev_state or i == T:
        color = "tab:blue" if prev_state == 0 else "tab:orange"
        ax.axvspan(seg_start, i - 1, color=color, alpha=0.12)
        seg_start = i - 1
        prev_state = current_state

# History shading overlay
ax.axvspan(0, history_len, color="grey", alpha=0.05)

# Forecast boundary
ax.axvline(history_len, linestyle="--", linewidth=1.6, color="grey")

# Signals
ax.plot(t[:history_len], true[:history_len], lw=2.4, color="tab:blue", label="Observed history")
ax.plot(t[history_len:], true[history_len:], lw=2.4, color="tab:orange", label="Ground-truth future")
ax.plot(tf, pred, "--", lw=2.4, color="tab:green", label="Predicted future")

# Text box annotation
ax.text(0.01, 0.97, "Two states with equal switching probability",
        transform=ax.transAxes, fontsize=9, va="top", ha="left",
        bbox=dict(boxstyle="square,pad=0.3", facecolor="white", edgecolor="grey", alpha=0.8))

# Style
#ax.set_title("Symmetric Markov switching", fontsize=16, fontweight="bold", pad=12)
ax.set_xlabel("Time", fontsize=13)
ax.set_ylabel("Amplitude", fontsize=13)
ax.set_ylim(-1.28, 1.2)
ax.set_xlim(0, T)
ax.grid(alpha=0.2)

# Legend — signal lines + S1/S2 patches
s1_patch = mpatches.Patch(color="tab:blue", alpha=0.4, label="S1")
s2_patch = mpatches.Patch(color="tab:orange", alpha=0.4, label="S2")
handles, labels = ax.get_legend_handles_labels()
ax.legend(
    handles=handles + [s1_patch, s2_patch],
    frameon=False,
    ncol=5,
    loc="upper center",
    bbox_to_anchor=(0.5, 1.22),
    fontsize=11
)

plt.tight_layout(rect=[0, 0, 1, 0.93])

out_path = "symmetric_markov_final.png"

plt.savefig(out_path, dpi=220, bbox_inches="tight")
plt.close()
print("Saved:", out_path)