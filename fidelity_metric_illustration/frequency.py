import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------
# Synthetic example
# -------------------------------------------------
T = 140
history_len = 50
t = np.arange(T)
tf = t[history_len:]

# ground-truth signal
f_true = 0.070
true = np.sin(2 * np.pi * f_true * t)

# prediction with slightly different frequency
f_pred = 0.078
pred_future = np.sin(2 * np.pi * f_pred * tf)


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

# choose one true period
t1_true, t2_true = true_peaks[1], true_peaks[2]
T_true = t2_true - t1_true

# choose one predicted period near the same region
pred_mid = np.argmin(np.abs(pred_peaks - (t1_true + 0.5 * T_true)))
pred_mid = max(1, min(pred_mid, len(pred_peaks) - 2))
t1_pred, t2_pred = pred_peaks[pred_mid], pred_peaks[pred_mid + 1]
T_pred = t2_pred - t1_pred

# center point for Δf annotation
x_df = 0.5 * ((t1_true + t2_true) / 2 + (t1_pred + t2_pred) / 2)


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
# Period annotations (fixed so labels do not overlap)
# -------------------------------------------------
y_true_arrow = -1.10
y_pred_arrow = -1.40

# mark selected peaks
ax.plot([t1_true, t2_true], [1.03, 1.03], marker="o", linestyle="None", markersize=4)
ax.plot([t1_pred, t2_pred], [0.92, 0.92], marker="o", linestyle="None", markersize=4)

# TRUE PERIOD
ax.annotate(
    "",
    xy=(t2_true, y_true_arrow),
    xytext=(t1_true, y_true_arrow),
    arrowprops=dict(arrowstyle="<->", lw=2.0)
)
ax.text(
    (t1_true + t2_true) / 2-3.0,
    y_true_arrow + 0.10,
    r"$T_{\mathrm{true}}$",
    ha="center",
    fontsize=13
)

# PREDICTED PERIOD
ax.annotate(
    "",
    xy=(t2_pred, y_pred_arrow),
    xytext=(t1_pred, y_pred_arrow),
    arrowprops=dict(arrowstyle="<->", lw=2.0, linestyle="--")
)
ax.text(
    (t1_pred + t2_pred) / 2+3.0,
    y_pred_arrow + 0.10,
    r"$T_{\mathrm{pred}}$",
    ha="center",
    fontsize=13
)

# guide lines from selected peaks to the period arrows
for x in [t1_true, t2_true]:
    ax.plot([x, x], [0.9, y_true_arrow + 0.02], linestyle=":", linewidth=1.0)
for x in [t1_pred, t2_pred]:
    ax.plot([x, x], [0.8, y_pred_arrow + 0.02], linestyle=":", linewidth=1.0)

# -------------------------------------------------
# Δf annotation
# -------------------------------------------------
ax.annotate(
    r"$\Delta f = |f_{\mathrm{pred}} - f_{\mathrm{true}}|$",
    xy=(x_df, y_true_arrow - 0.02),
    xytext=(x_df + 18, 0.82),
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
ax.set_title("Frequency error", fontsize=16, fontweight="bold")
ax.set_xlabel("Time")
ax.set_ylabel("Amplitude")
ax.set_ylim(-1.52, 1.18)
ax.grid(alpha=0.25)

# legend outside the plotting area
ax.legend(
    frameon=False,
    ncol=3,
    loc="upper center",
    bbox_to_anchor=(0.5, 1.18)
)
plt.savefig("frequency_error_illustration.png", dpi=220)

plt.tight_layout(rect=[0, 0, 1, 0.92])
plt.show()