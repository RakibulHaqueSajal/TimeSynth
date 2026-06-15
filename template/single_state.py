import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# -------------------------------------------------
# Parameters
# -------------------------------------------------
T = 150
history_len = 50
t = np.arange(T)
tf = t[history_len:]

transition = 31

# -------------------------------------------------
# State definitions
# -------------------------------------------------
f_s1 = 0.06
f_s2 = 0.11

true = np.zeros(T)

for i in range(T):
    if i < transition:
        true[i] = np.sin(2*np.pi*f_s1*i)
    else:
        true[i] = np.sin(2*np.pi*f_s2*i)

# predicted future
pred = 0.96*np.sin(2*np.pi*0.108*tf + 0.22)

# -------------------------------------------------
# Plot
# -------------------------------------------------
fig, ax = plt.subplots(figsize=(10,4.8), dpi=220)

# S1 region
ax.axvspan(0, transition, color="tab:blue", alpha=0.08)

# S2 region
ax.axvspan(transition, T, color="tab:orange", alpha=0.08)

# history shading overlay
ax.axvspan(0, history_len, color="grey", alpha=0.05)

# forecast boundary
ax.axvline(history_len, linestyle="--", linewidth=1.8)

# state transition marker
ax.axvline(transition, linestyle=":", linewidth=2)

# signals
ax.plot(t[:history_len], true[:history_len], lw=2.6, label="Observed history")
ax.plot(t[history_len:], true[history_len:], lw=2.6, label="Ground-truth future")
ax.plot(tf, pred, "--", lw=2.6, label="Predicted future")

# state labels
ax.text(12, 1.05, "S1", fontsize=20, fontweight="bold", color="tab:blue")
ax.text(90, 1.05, "S2", fontsize=20, fontweight="bold", color="tab:orange")

# transition annotation
ax.annotate(
    "state transition",
    xy=(transition,0.8),
    xytext=(42,1.25),
    arrowprops=dict(arrowstyle="->", lw=1.6),
    fontsize=14
)

# style
ax.set_title("Two-state transition", fontsize=20, fontweight="bold", pad=35)
ax.set_xlabel("Time", fontsize=14)
ax.set_ylabel("Amplitude", fontsize=14)
ax.set_ylim(-1.28,1.3)
ax.grid(alpha=0.25)

# move legend above everything
ax.legend(
    frameon=False,
    ncol=3,
    loc="upper center",
    bbox_to_anchor=(0.5,1.28),
    fontsize=14
)

plt.tight_layout(rect=[0,0,1,0.88])

# save
out_path = Path("/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/template/two_state_transition_final.png")
out_path.parent.mkdir(parents=True, exist_ok=True)

plt.savefig(out_path, dpi=220, bbox_inches="tight")
plt.close()

print("Saved:", out_path)