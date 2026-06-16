import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import irfft, rfftfreq

# --- Pink Noise Generator ---
def generate_pink_noise(N, dt=0.1, alpha=1.5, seed=None):
    if seed is not None:
        np.random.seed(seed)
    f = rfftfreq(N, d=dt)
    f[0] = 1e-6  # avoid division by zero
    amplitude = 1 / f**alpha
    phase = np.exp(1j * 2 * np.pi * np.random.rand(len(f)))
    noise = irfft(amplitude * phase, n=N)
    return (noise - np.mean(noise)) / np.std(noise)

# --- Parameters ---
fs = 10               # Sampling rate in Hz
duration = 300        # Duration in seconds (adjust as needed)
dt = 1 / fs           # Time step based on sampling rate
N = int(fs * duration)  # Total number of points
alpha = 1.5           # Fractal exponent
seed = 42             # For reproducibility

# --- Generate and Plot ---
t = np.linspace(0, duration, N)
pink_noise = generate_pink_noise(N, dt, alpha, seed)

plt.figure(figsize=(12, 4))
plt.plot(t, pink_noise, label=f"1/f Noise (α={alpha})")
plt.title(f"Generated 1/f Noise (α={alpha}, Duration={duration}s, fs={fs}Hz)")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
