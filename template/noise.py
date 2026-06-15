#!/usr/bin/env python3
import os
import numpy as np
import matplotlib.pyplot as plt

HISTORY_LEN = 50
FS = 10.0

# -------------------------
# choose one run
# -------------------------
MODEL_PATH = "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/long_term_forecast_PatchTST_50_100_PatchTST_Single_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_15_SNR_Level_6"   # e.g. Linear Drift Harmonic clean run
OUT_PNG = "noise_real_template_examples.png"

# -------------------------
# loading
# -------------------------
def load_true_pred(model_path, split="test"):
    true = np.load(os.path.join(model_path, f"{split}_true_with_history.npy"))
    pred = np.load(os.path.join(model_path, f"{split}_pred_with_history.npy"))
    if true.ndim == 3:
        true = true.squeeze(-1)
    if pred.ndim == 3:
        pred = pred.squeeze(-1)
    return true, pred

# -------------------------
# metrics copied from your logic
# -------------------------
def peak_freq_rfft_with_confidence(x, fs=1.0, drop_dc=True, parabolic=True,
                                   peak_frac_thresh=0.1, power_thresh=1e-8):
    x = np.asarray(x, float)
    x = x - x.mean()
    n = len(x)
    if n <= 2:
        return 0.0, False

    X = np.fft.rfft(x, n=n)
    P = (np.abs(X) ** 2).astype(float)
    f = np.fft.rfftfreq(n, d=1.0 / fs)

    start = 1 if drop_dc else 0
    total_power = P[start:].sum()
    if total_power <= power_thresh:
        return 0.0, False

    k = start + int(np.argmax(P[start:]))

    if (not parabolic) or k == 0 or k == len(P) - 1:
        f_est = f[k]
    else:
        denom = (P[k - 1] - 2 * P[k] + P[k + 1])
        delta = 0.0 if abs(denom) < 1e-12 else 0.5 * (P[k - 1] - P[k + 1]) / denom
        f_est = (k + delta) * (fs / n)

    peak_power = P[k]
    frac = peak_power / total_power if total_power > 0 else 0.0
    reliable = frac >= peak_frac_thresh
    return float(f_est), bool(reliable)

def analytic_signal_fft(x):
    x = np.asarray(x, dtype=float)
    n = x.size
    x = x - x.mean()
    X = np.fft.fft(x, n=n)

    H = np.zeros(n, dtype=float)
    if n % 2 == 0:
        H[0] = 1.0
        H[n // 2] = 1.0
        H[1:n // 2] = 2.0
    else:
        H[0] = 1.0
        H[1:(n + 1) // 2] = 2.0

    z = np.fft.ifft(X * H, n=n)
    return z

def wrap_to_pi(ang):
    ang = np.asarray(ang, dtype=float)
    ang_unwrapped = np.unwrap(ang)
    return (ang_unwrapped + np.pi) % (2 * np.pi) - np.pi

def per_seq_metrics(true, pred, history_len=50, fs=10.0):
    Y = true[:, history_len:]
    YH = pred[:, history_len:]

    N = Y.shape[0]
    mae = np.mean(np.abs(YH - Y), axis=1)

    freq_err = np.full(N, np.nan)
    phase_err = np.full(N, np.nan)

    for i in range(N):
        # frequency
        ft, okt = peak_freq_rfft_with_confidence(Y[i], fs=fs)
        fp, okp = peak_freq_rfft_with_confidence(YH[i], fs=fs)
        if okt and okp:
            freq_err[i] = abs(fp - ft)

        # phase
        y = Y[i] - Y[i].mean()
        yh = YH[i] - YH[i].mean()
        zt = analytic_signal_fft(y)
        zp = analytic_signal_fft(yh)

        At = np.abs(zt)
        med_amp = np.median(At)
        if np.isfinite(med_amp) and med_amp > 0:
            mask = At > (0.2 * med_amp)
            if np.any(mask):
                phi_t = np.unwrap(np.angle(zt))
                phi_p = np.unwrap(np.angle(zp))
                dphi = wrap_to_pi(phi_p - phi_t)
                sel = dphi[mask]
                if sel.size > 0:
                    phase_err[i] = np.mean(np.abs(np.degrees(sel)))

    return mae, freq_err, phase_err

# -------------------------
# example selection
# -------------------------
def pick_examples(mae, freq_err, phase_err):
    valid_f = np.isfinite(freq_err)
    valid_p = np.isfinite(phase_err)

    # representative forecast: median MAE
    idx_forecast = np.argsort(mae)[len(mae)//2]

    # amplitude-heavy: high MAE, but lower freq/phase than other high-MAE cases
    score_amp = mae.copy()
    if np.any(valid_f):
        score_amp -= 0.5 * np.nan_to_num(freq_err, nan=np.nanmedian(freq_err))
    if np.any(valid_p):
        score_amp -= 0.005 * np.nan_to_num(phase_err, nan=np.nanmedian(phase_err))
    idx_amp = np.nanargmax(score_amp)

    # strongest frequency mismatch
    idx_freq = np.nanargmax(freq_err)

    # strongest phase mismatch
    idx_phase = np.nanargmax(phase_err)

    return idx_forecast, idx_amp, idx_freq, idx_phase

# -------------------------
# plotting
# -------------------------
def plot_example(ax, true_seq, pred_seq, idx, title, history_len=50):
    T = len(true_seq)
    t = np.arange(T)

    ax.axvspan(0, history_len - 1, color="lightgray", alpha=0.35)
    ax.axvline(history_len - 1, color="k", linestyle="--", linewidth=1)

    ax.plot(t[:history_len], true_seq[:history_len], color="tab:blue", linewidth=2, label="History")
    ax.plot(t[history_len-1:], true_seq[history_len-1:], color="black", linewidth=2, label="Ground truth")
    ax.plot(t[history_len-1:], pred_seq[history_len-1:], color="tab:orange", linestyle="--", linewidth=2, label="Prediction")

    ax.set_title(f"{title} (seq {idx})", fontweight="bold")
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude")
    ax.grid(alpha=0.25)

true, pred = load_true_pred(MODEL_PATH)
mae, freq_err, phase_err = per_seq_metrics(true, pred, history_len=HISTORY_LEN, fs=FS)
idx_forecast, idx_amp, idx_freq, idx_phase = pick_examples(mae, freq_err, phase_err)

fig, axes = plt.subplots(2, 2, figsize=(12, 8), dpi=200)

plot_example(axes[0, 0], true[idx_forecast], pred[idx_forecast], idx_forecast, "Representative forecast", HISTORY_LEN)
plot_example(axes[0, 1], true[idx_amp], pred[idx_amp], idx_amp, "Amplitude mismatch", HISTORY_LEN)
plot_example(axes[1, 0], true[idx_freq], pred[idx_freq], idx_freq, "Frequency mismatch", HISTORY_LEN)
plot_example(axes[1, 1], true[idx_phase], pred[idx_phase], idx_phase, "Phase mismatch", HISTORY_LEN)

handles, labels = axes[0, 0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper center", ncol=3, frameon=False)
fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig(OUT_PNG, bbox_inches="tight")
print(f"saved to {OUT_PNG}")