import numpy as np
from scipy.signal import welch

# ----------------------------
# Config
# ----------------------------
FS = 10
SEQ_LEN = 50
PRED_LEN = 100

WIN = 16
STRIDE = 8
CENTER = WIN // 2

N_SUB = 2000  # set None to use all sequences (slower)

true_wh = np.load("/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/long_term_forecast_Linear_50_100_Linear_PhaseMod_Single_Freq_TwoState_p_0.30000_70_10_20_0.001_0.0001_16_Markov/test_true_with_history.npy")      # (N,150,1)
pred_wh = np.load("/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/long_term_forecast_Linear_50_100_Linear_PhaseMod_Single_Freq_TwoState_p_0.30000_70_10_20_0.001_0.0001_16_Markov/test_pred_with_history.npy")      # (N,150,1)
z_true  = np.load("/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/long_term_forecast_Linear_50_100_Linear_PhaseMod_Single_Freq_TwoState_p_0.30000_70_10_20_0.001_0.0001_16_Markov/test_true_state.npy")[:, :, 0].astype(int)  # (N,100)

y_true = true_wh[:, SEQ_LEN:, 0]  # (N,100)
y_pred = pred_wh[:, SEQ_LEN:, 0]  # (N,100)

N = y_true.shape[0]
idx = np.arange(N) if (N_SUB is None or N_SUB >= N) else np.random.choice(N, size=N_SUB, replace=False)

def dom_freq_welch(seg, fs, nperseg):
    nperseg = min(nperseg, len(seg))
    f, Pxx = welch(seg, fs=fs, nperseg=nperseg)
    return f[np.argmax(Pxx)]

def extract_fdom_and_labels(y, z=None):
    """
    y: (N,T) signal
    z: (N,T) optional true labels for alignment (uses CENTER index)
    Returns:
      fdom: (M,) dominant freq per window
      lab:  (M,) labels if z is provided else None
      win_id: (M,) which sequence each window came from (for per-seq transitions)
    """
    fdom = []
    lab = []
    win_id = []
    for ii, i in enumerate(idx):
        for s in range(0, PRED_LEN - WIN + 1, STRIDE):
            seg = y[i, s:s+WIN]
            f0 = dom_freq_welch(seg, FS, nperseg=WIN)
            fdom.append(f0)
            win_id.append(ii)  # local id 0..len(idx)-1
            if z is not None:
                lab.append(z[i, s + CENTER])
    fdom = np.array(fdom)
    win_id = np.array(win_id, dtype=int)
    if z is not None:
        lab = np.array(lab, dtype=int)
        return fdom, lab, win_id
    return fdom, None, win_id

# ----------------------------
# A) Build proxy classifier from TRUE waveform
# ----------------------------
fdom_true, lab_true, win_id_true = extract_fdom_and_labels(y_true, z_true)

m0 = fdom_true[lab_true == 0].mean()
m1 = fdom_true[lab_true == 1].mean()
thr = 0.5 * (m0 + m1)

zhat_true = (fdom_true > thr).astype(int)
acc_true = (zhat_true == lab_true).mean()

print("=== Spectral separability on TRUE ===")
print("mean dom freq state0:", m0)
print("mean dom freq state1:", m1)
print("sep:", abs(m1 - m0))
print("threshold:", thr)
print("proxy-state accuracy on TRUE windows:", acc_true)

# ----------------------------
# Helper: compute per-sequence proxy switch prob + transition matrix
# ----------------------------
def proxy_switch_stats(zhat, win_id):
    """
    zhat: (M,) proxy states per window
    win_id: (M,) sequence id for each window, windows are in time order by construction
    Returns mean/median switch rate per sequence, plus pooled transition matrix.
    """
    # per-seq switch rate
    rates = []
    C = np.zeros((2,2), dtype=np.int64)

    # iterate per sequence
    for s_id in np.unique(win_id):
        zseq = zhat[win_id == s_id]
        if len(zseq) < 2:
            continue
        rates.append((zseq[1:] != zseq[:-1]).mean())
        for a, b in zip(zseq[:-1], zseq[1:]):
            C[a, b] += 1

    rates = np.array(rates, dtype=float)
    P = C / C.sum(axis=1, keepdims=True)
    return float(rates.mean()), float(np.median(rates)), C, P

p_trueproxy_mean, p_trueproxy_med, C_trueproxy, P_trueproxy = proxy_switch_stats(zhat_true, win_id_true)

print("\n=== Proxy Markov stats (TRUE waveform) ===")
print("proxy switch prob mean:", p_trueproxy_mean, "median:", p_trueproxy_med)
print("Counts:\n", C_trueproxy)
print("P:\n", P_trueproxy)

# ----------------------------
# B) Apply same proxy to PRED waveform
# ----------------------------
fdom_pred, _, win_id_pred = extract_fdom_and_labels(y_pred, z=None)
zhat_pred = (fdom_pred > thr).astype(int)

p_predproxy_mean, p_predproxy_med, C_predproxy, P_predproxy = proxy_switch_stats(zhat_pred, win_id_pred)

print("\n=== Proxy Markov stats (PRED waveform) ===")
print("proxy switch prob mean:", p_predproxy_mean, "median:", p_predproxy_med)
print("Counts:\n", C_predproxy)
print("P:\n", P_predproxy)

# ----------------------------
# C) Ground truth switch prob from TRUE STATES (sample-level, not window-level)
# ----------------------------
z = z_true[idx]  # (Nsub,100)
p_state_true = (z[:,1:] != z[:,:-1]).mean()

print("\n=== Ground-truth switch prob from true_state.npy (sample-level) ===")
print("p_true_state (per-step):", float(p_state_true))

# ----------------------------
# D) Interpretation-friendly deltas
# ----------------------------
print("\n=== Key comparisons ===")
print("GT state p:", float(p_state_true))
print("TRUE proxy p (windowed):", p_trueproxy_mean, "(this includes window/stride bias)")
print("PRED proxy p (windowed):", p_predproxy_mean)
print("Delta (PRED proxy - TRUE proxy):", p_predproxy_mean - p_trueproxy_mean)
