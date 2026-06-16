# Fix the regime switching signal to normalize each regime before concatenating
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import irfft, rfftfreq

# OU Process
def generate_ou_process(t, theta=0.2, mu=0.0, sigma=0.5, x0=0.0):
    dt = t[1] - t[0]
    x = np.zeros_like(t)
    x[0] = x0
    for i in range(1, len(t)):
        dx = theta * (mu - x[i-1]) * dt + sigma * np.sqrt(dt) * np.random.normal()
        x[i] = x[i-1] + dx
    return x

# 1/f Fractal Noise (normalize output)
def generate_pink_noise(t, alpha=1.5):
    f = rfftfreq(len(t), d=(t[1] - t[0]))
    f[0] = 1e-6
    amp = 1 / f**alpha
    phase = np.exp(1j * 2 * np.pi * np.random.rand(len(f)))
    noise = np.real(irfft(amp * phase, n=len(t)))
    return (noise - np.mean(noise)) / np.std(noise)

# Regime Switching Signal
def generate_regime_switching_signal(t):
    thirds = len(t) // 3
    sig = np.zeros_like(t)

    # Regime 1: Sine wave
    sig[:thirds] = np.sin(2 * np.pi * 0.1 * t[:thirds])

    # Regime 2: OU process
    
    ou_segment = generate_ou_process(t[thirds:2*thirds])
    ou_segment = (ou_segment - np.mean(ou_segment)) / np.std(ou_segment)
    sig[thirds:2*thirds] = ou_segment

    # Regime 3: 1/f noise
    pink_segment = generate_pink_noise(t[2*thirds:])
    sig[2*thirds:] = pink_segment

    return sig

# Time and Signal
# --- Adjustable Parameters ---
fs = 10               # Fixed sampling rate (Hz)
duration = 300        # Desired duration in seconds
T = int(fs * duration)
t = np.linspace(0, duration, T)
signal = generate_regime_switching_signal(t)

# Plot
plt.figure(figsize=(12, 4))
plt.plot(t, signal, label="Regime Switching Signal")
plt.axvline(t[T//3], color='r', linestyle='--', label="Regime Boundaries")
plt.axvline(t[2*T//3], color='r', linestyle='--')
plt.title("Regime Switching Signal: Sine → OU → 1/f")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
