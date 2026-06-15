import numpy as np
from scipy.signal import welch

FS = 10
SEQ_LEN = 50
PRED_LEN = 100

true_wh = np.load("/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/long_term_forecast_Linear_50_100_Linear_PhaseMod_Single_Freq_TwoState_p_0.70000_70_10_20_0.001_0.0001_16_Markov/test_true_with_history.npy")      # (N,150,1)
z_true  = np.load("/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/long_term_forecast_Linear_50_100_Linear_PhaseMod_Single_Freq_TwoState_p_0.70000_70_10_20_0.001_0.0001_16_Markov/test_true_state.npy")             # (N,100,1)

# FIX: squeeze state to (N,100)
z_true = z_true[:, :, 0].astype(int)

y_true = true_wh[:, SEQ_LEN:, 0]                     # (N,100)

def dom_freq_welch(x, fs, nperseg=64):
    nperseg = min(nperseg, len(x))
    f, Pxx = welch(x, fs=fs, nperseg=nperseg)
    return f[np.argmax(Pxx)]

WIN = 16
STRIDE = 8
CENTER = WIN // 2

idx = np.random.choice(len(y_true), size=min(2000, len(y_true)), replace=False)

fdom = []
zlab = []

for i in idx:
    for s in range(0, PRED_LEN - WIN + 1, STRIDE):
        seg = y_true[i, s:s+WIN]
        fdom.append(dom_freq_welch(seg, FS, nperseg=WIN))
        zlab.append(z_true[i, s + CENTER])   # now scalar

fdom = np.array(fdom)
zlab = np.array(zlab)

print("fdom shape:", fdom.shape)
print("zlab shape:", zlab.shape)

m0 = fdom[zlab == 0].mean()
m1 = fdom[zlab == 1].mean()

print("mean dom freq state0:", m0)
print("mean dom freq state1:", m1)
print("sep:", abs(m1 - m0))
