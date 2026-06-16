import numpy as np
import matplotlib.pyplot as plt

# Define the signal function
def phase_modulated_multisine(t, A, f_i, beta, f_mod):
    signal = np.zeros_like(t)
    for Ai, fi, bi, fmod in zip(A, f_i, beta, f_mod):
        mod_phase = bi * np.sin(2 * np.pi * fmod * t)
        signal += Ai * np.sin(2 * np.pi * fi * t + mod_phase)
    return signal

# Parameters
A = [0.7, 0.6, 0.8]
f_i = [0.1, 0.2, 0.05]
beta = [3, 1, 2]
f_mod = [0.01, 0.02, 0.022]

# Time vector
# Sampling rate and duration
fs = 10                # sampling rate in Hz (fixed)
duration = 200         # total duration in seconds (adjust freely)
T = int(fs * duration) # total number of samples
t = np.linspace(0, duration, T)
# Generate the signal
signal = phase_modulated_multisine(t, A, f_i, beta, f_mod)

# Plot with parameter summary
plt.figure(figsize=(12, 4))
plt.plot(t, signal, label="Phase-Modulated Multi-Sinewave")
param_str = f"A={A}, f_i={f_i}, β={beta}, f_mod={f_mod}"
plt.title(f"Phase-Modulated Multi-Sinewave\n{param_str}", fontsize=10)
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
