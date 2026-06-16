import numpy as np
import matplotlib.pyplot as plt

# --- OU Process Generator ---
def generate_ou_process(t, theta=0.2, mu=0.0, sigma=0.5, x0=0.0):
    dt = t[1] - t[0]
    x = np.zeros_like(t)
    x[0] = x0
    for i in range(1, len(t)):
        dx = theta * (mu - x[i-1]) * dt + sigma * np.sqrt(dt) * np.random.normal()
        x[i] = x[i-1] + dx
    return x

# --- Oscillator + OU Noise Signal ---
def oscillator_plus_ou(t, f=0.1, theta=0.2, mu=0.0, sigma=0.5):
    oscillator = np.sin(2 * np.pi * f * t)
    ou_noise = generate_ou_process(t, theta=theta, mu=mu, sigma=sigma)
    return oscillator + ou_noise

# --- Generate and Plot ---
# Sampling rate and duration
fs = 10                # sampling rate in Hz (fixed)
duration = 200         # total duration in seconds (adjust freely)
T = int(fs * duration) # total number of samples
t = np.linspace(0, duration, T)

#signal parameter
theta, mu, sigma, f = 0.2, 0.0, 0.5, 0.1

signal = oscillator_plus_ou(t, f=f, theta=theta, mu=mu, sigma=sigma)

plt.figure(figsize=(12, 4))
plt.plot(t, signal, label="Oscillator + OU Noise")
plt.title(f"Oscillator + OU Noise: θ={theta}, μ={mu}, σ={sigma}, f={f}")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
