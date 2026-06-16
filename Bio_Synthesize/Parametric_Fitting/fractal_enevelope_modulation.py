# Generate and plot Fractal Envelope Modulated Oscillation
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft import irfft, rfftfreq

# Generate fractal envelope using 1/f^alpha noise
def generate_fractal_envelope(N, dt=0.1, alpha=1.5, seed=None):
    if seed is not None:
        np.random.seed(seed)
    f = rfftfreq(N, d=dt)
    f[0] = 1e-6  # avoid division by zero
    amplitude = 1 / f**alpha
    phase = np.exp(1j * 2 * np.pi * np.random.rand(len(f)))
    spectrum = amplitude * phase
    envelope = irfft(spectrum, n=N)
    return (envelope - np.min(envelope)) / (np.max(envelope) - np.min(envelope))  # normalize to [0, 1]

# Generate modulated signal
def fractal_modulated_oscillation(t, f=0.2, alpha=1.5):
    A_t = generate_fractal_envelope(len(t), dt=t[1] - t[0], alpha=alpha)
    return A_t * np.sin(2 * np.pi * f * t)

# Time vector
fs = 40               # Fixed sampling rate (Hz)
duration = 300        # Adjust this for desired time length (seconds)
N = int(fs * duration)
t = np.linspace(0, duration, N)
# Parameters
f = 0.2       # carrier frequency
alpha = 1.5   # fractal exponent

# Generate signal
signal = fractal_modulated_oscillation(t, f=f, alpha=alpha)

# Plot
plt.figure(figsize=(12, 4))
plt.plot(t, signal, label="Fractal Envelope Modulated Oscillation")
plt.title(f"Fractal Envelope Modulated Oscillation: f={f}, α={alpha}")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
