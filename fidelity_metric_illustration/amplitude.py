import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------
# Synthetic example
# -------------------------------------------------
T = 140
history_len = 50
t = np.arange(T)
tf = t[history_len:]

# full signal
true = np.sin(2 * np.pi * 0.07 * t)

# prediction only on future
pred_future = 0.65* np.sin(2 * np.pi * 0.07 * tf + 0.25)

# -------------------------------------------------
# Plot
# -------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 4.8), dpi=220)

# History shading and boundary
ax.axvspan(0, history_len, alpha=0.12)
ax.axvline(history_len, linestyle="--", linewidth=1.2)

# Plot history and future
ax.plot(t[:history_len+1], true[:history_len+1], linewidth=2.2, label="Observed history")
ax.plot(t[history_len:], true[history_len:], linewidth=2.2, label="Ground-truth future")
ax.plot(tf, pred_future, linestyle="--", linewidth=2.2, label="Predicted future")

# Shade error region in future
ax.fill_between(tf, true[history_len:], pred_future, alpha=0.15)

# Show pointwise absolute error at a few locations
sample_idx = [10, 25, 45, 65, 80]
for k in sample_idx:
    x = tf[k]
    y_true = true[history_len + k]
    y_pred = pred_future[k]
    ax.plot([x, x], [y_true, y_pred], linewidth=1.8)

# -------------------------------------------------
# Highlight one pointwise error more clearly
# -------------------------------------------------
k = 25
x = tf[k]
y_true_k = true[history_len + k]
y_pred_k = pred_future[k]
y_mid = 0.5 * (y_true_k + y_pred_k)

# Emphasize chosen error bar
ax.plot([x, x], [y_true_k, y_pred_k], linewidth=2.8)

# Mark endpoints
ax.plot(x, y_true_k, marker="o", markersize=5)
ax.plot(x, y_pred_k, marker="o", markersize=5)

# Boxed annotation placed away from the waveform
ax.annotate(
    r"Pointwise absolute error" + "\n" + r"$|y_{\mathrm{pred}} - y_{\mathrm{true}}|$",
    xy=(x, y_mid),
    xytext=(x + 16, 0.72),
    textcoords="data",
    ha="left",
    va="center",
    fontsize=11,
    bbox=dict(boxstyle="round,pad=0.35", facecolor="white", alpha=0.95, edgecolor="0.5"),
    arrowprops=dict(arrowstyle="->", lw=1.5, shrinkA=5, shrinkB=5)
)

# Formula box
ax.text(
    0.98, 0.05,
    r"$\mathrm{MAE}=\frac{1}{H}\sum_{t=1}^{H}|y_{\mathrm{pred}}(t)-y_{\mathrm{true}}(t)|$",
    transform=ax.transAxes,
    ha="right",
    va="bottom",
    fontsize=12,
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.9, edgecolor="0.7")
)

ax.set_title("Mean absolute error (MAE)", fontsize=16, fontweight="bold")
ax.set_xlabel("Time")
ax.set_ylabel("Amplitude")
ax.grid(alpha=0.25)
ax.legend(frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 1.16))

plt.tight_layout()
plt.savefig("amplitude_mae_illustration.png", dpi=220)
plt.show()