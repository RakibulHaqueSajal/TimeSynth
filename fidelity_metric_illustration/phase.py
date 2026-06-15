import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------
# Synthetic example
# -------------------------------------------------
T = 140
history_len = 50
t = np.arange(T)
tf = t[history_len:]

# same frequency, different phase
f_phase = 0.070
phi_true = 0.0
phi_pred = 0.8

# full signal
true = np.sin(2 * np.pi * f_phase * t + phi_true)

# prediction only on future
pred_future = np.sin(2 * np.pi * f_phase * tf + phi_pred)


# -------------------------------------------------
# Helper: find approximate peak locations
# -------------------------------------------------
def peak_times_from_signal(x_t, x_y):
    peaks = []
    for i in range(1, len(x_y) - 1):
        if x_y[i] > x_y[i - 1] and x_y[i] > x_y[i + 1]:
            peaks.append(x_t[i])
    return np.array(peaks, dtype=float)


true_future = true[history_len:]
true_peaks = peak_times_from_signal(tf, true_future)
pred_peaks = peak_times_from_signal(tf, pred_future)

# pick one pair of nearby peaks
idx_true = 2
t_peak_true = true_peaks[idx_true]

idx_pred = np.argmin(np.abs(pred_peaks - t_peak_true))
t_peak_pred = pred_peaks[idx_pred]

x_mid = 0.5 * (t_peak_true + t_peak_pred)


# -------------------------------------------------
# Plot
# -------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 4.8), dpi=220)

# history shading and forecast boundary
ax.axvspan(0, history_len, alpha=0.08)
ax.axvline(history_len, linestyle="--", linewidth=1.2)

# signals
ax.plot(
    t[:history_len + 1],
    true[:history_len + 1],
    linewidth=2.2,
    label="Observed history"
)
ax.plot(
    t[history_len:],
    true[history_len:],
    linewidth=2.2,
    label="Ground-truth future"
)
ax.plot(
    tf,
    pred_future,
    linestyle="--",
    linewidth=2.2,
    label="Predicted future"
)

# -------------------------------------------------
# Peak markers and guide lines
# -------------------------------------------------
ax.plot(t_peak_true, 1.03, marker="o", markersize=5)
ax.plot(t_peak_pred, 0.92, marker="o", markersize=5)

ax.plot([t_peak_true, t_peak_true], [0.9, -1.05], linestyle=":", linewidth=1.0)
ax.plot([t_peak_pred, t_peak_pred], [0.8, -1.05], linestyle=":", linewidth=1.0)

# -------------------------------------------------
# Phase gap annotation
# -------------------------------------------------
y_phase_arrow = -1.18
ax.annotate(
    "",
    xy=(t_peak_true, y_phase_arrow),
    xytext=(t_peak_pred, y_phase_arrow),
    arrowprops=dict(arrowstyle="<->", lw=2.0)
)

ax.text(
    x_mid,
    y_phase_arrow + 0.10,
    r"$\Delta \phi$",
    ha="center",
    va="bottom",
    fontsize=14
)

# explanatory boxed callout
ax.annotate(
    r"$\Delta \phi = |\phi_{\mathrm{pred}} - \phi_{\mathrm{true}}|$",
    xy=(x_mid, y_phase_arrow),
    xytext=(x_mid + 18, 0.82),
    textcoords="data",
    ha="left",
    va="center",
    fontsize=13,
    bbox=dict(
        boxstyle="round,pad=0.35",
        facecolor="white",
        alpha=0.95,
        edgecolor="0.5"
    ),
    arrowprops=dict(arrowstyle="->", lw=1.5)
)

# -------------------------------------------------
# Style
# -------------------------------------------------
ax.set_title("Phase error", fontsize=16, fontweight="bold")
ax.set_xlabel("Time")
ax.set_ylabel("Amplitude")
ax.set_ylim(-1.45, 1.18)
ax.grid(alpha=0.25)

# legend outside plotting area
ax.legend(
    frameon=False,
    ncol=3,
    loc="upper center",
    bbox_to_anchor=(0.5, 1.18)
)

plt.tight_layout(rect=[0, 0, 1, 0.92])
plt.savefig("phase_error_illustration.png", dpi=220)
plt.show()