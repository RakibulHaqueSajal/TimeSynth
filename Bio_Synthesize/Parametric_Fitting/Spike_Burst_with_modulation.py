# Generate and plot the Predictable Spike Bursts with Modulated Timing signal
import numpy as np
import matplotlib.pyplot as plt

# Define the spike burst signal
def predictable_spike_bursts(t, T=5, A_mod=1.0, omega=0.4, sigma=0.5):
    signal = np.zeros_like(t)
    k = 0
    while True:
        tk = k * T + A_mod * np.sin(omega * k)
        if tk > t[-1]:
            break
        amp = 1 + 0.5 * np.sin(0.02 * tk)
        signal += amp * np.exp(-0.5 * ((t - tk) / sigma)**2)
        k += 1
    return signal

# Time vector
fs = 10                # Sampling rate in Hz
duration = 300         # Duration in seconds (change as needed)
dt = 1 / fs            # Time step
N = int(fs * duration) # Number of samples
t = np.linspace(0, duration, N)

# Parameters
T_spike = 5
A_mod = 1.0
omega = 0.4
sigma = 0.5

# Generate the signal
signal = predictable_spike_bursts(t, T=T_spike, A_mod=A_mod, omega=omega, sigma=sigma)

# Plot
plt.figure(figsize=(12, 4))
plt.plot(t, signal, label="Predictable Spike Bursts")
plt.title(f"Predictable Spike Bursts: T={T_spike}, A={A_mod}, ω={omega}, σ={sigma}")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
