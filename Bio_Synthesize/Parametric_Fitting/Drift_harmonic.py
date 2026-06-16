# Re-import and plot the drift-modulated harmonic signal with parameters shown in title
import numpy as np
import matplotlib.pyplot as plt

# Define the signal
def drift_modulated_harmonic(t, epsilon=0.005, f=0.1, phi=0, a=0.01):
    A_t = 1 + epsilon * t
    base = np.sin(2 * np.pi * f * t + phi)
    trend = a * t
    return A_t * base + trend

# Time and signal
duration = 200     # seconds (adjust as needed)
fs = 10            # sampling rate in Hz
epsilon = 0.001
f = 0.1
phi = 0
a = 0.01

# --- Time vector ---
T = int(fs * duration)       # total samples
t = np.linspace(0, duration, T)

#Signal Parameters
epsilon, f, phi, a = 0.001, 0.1, 0, 0.01
signal = drift_modulated_harmonic(t, epsilon, f, phi, a)

# Plot with parameters in title
plt.figure(figsize=(12, 4))
plt.plot(t, signal, label="Drift-Modulated Harmonic Signal")
plt.title(f"Drift-Modulated Harmonic: ε={epsilon}, f={f}, ϕ={phi}, a={a}")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
