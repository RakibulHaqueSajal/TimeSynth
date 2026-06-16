import numpy as np
import pandas as pd
import os
import hashlib
import matplotlib.pyplot as plt

# Signal definition
def drift_modulated_harmonic(t, epsilon, f, phi, a):
    A_t = 1 + epsilon * t
    base = np.sin(2 * np.pi * f * t + phi)
    trend = a * t
    signal = A_t * base + trend
    return (signal - np.min(signal)) / (np.max(signal) - np.min(signal))

# Unique hash tracker
def param_hash(f, phi, a, precision=6):
    key = f"{f:.{precision}f}_{phi:.{precision}f}_{a:.{precision}e}"
    return hashlib.md5(key.encode()).hexdigest()

# Generate unique parameter sets
def sample_unique_param_sets(n, f_range, phi_range, a_range, existing_hashes):
    params = []
    while len(params) < n:
        f = np.random.uniform(*f_range)
        phi = np.random.uniform(*phi_range)
        a = np.random.uniform(*a_range)
        h = param_hash(f, phi, a)
        if h not in existing_hashes:
            existing_hashes.add(h)
            params.append((f, phi, a))
    return params

# Save signal
def save_signal(t, signal, epsilon, f, phi, a, idx, mode, base_dir):
    split_dir = os.path.join(base_dir, mode)
    os.makedirs(split_dir, exist_ok=True)
    filename = f"{mode}_{idx:03d}_epsilon_{epsilon:.4f}_f_{f:.4f}_phi_{phi:.4f}_a_{a:.8f}.csv"
    df = pd.DataFrame({"Time": t, "Value": signal})
    df.to_csv(os.path.join(split_dir, filename), index=False)

# Main generation
def generate_all_splits(base_dir, n_train=70, n_val=10, n_test=20, fs=10, duration=300):
    t = np.linspace(0, duration, int(fs * duration))
    epsilon = -0.05
    f_range = (0.85, 1.10)
    phi_range = (-0.6, 0.75)
    a_range = (-6e-5, 8e-5)

    used_hashes = set()

    splits = {
        'train': n_train,
        'val': n_val,
        'test': n_test
    }

    for mode, count in splits.items():
        param_list = sample_unique_param_sets(count, f_range, phi_range, a_range, used_hashes)
        for idx, (f, phi, a) in enumerate(param_list):
            signal = drift_modulated_harmonic(t, epsilon, f, phi, a)
            save_signal(t, signal, epsilon, f, phi, a, idx, mode, base_dir)
        print(f"Saved {count} samples to {mode}/")

# Visualization (optional)
def visualize_signals(base_dir, num_samples=3, max_rows=100):
    import os
    import pandas as pd
    import matplotlib.pyplot as plt

    split = "train"
    split_dir = os.path.join(base_dir, split)
    files = sorted([f for f in os.listdir(split_dir) if f.endswith(".csv")])[:num_samples]

    fig, axes = plt.subplots(1, num_samples, figsize=(4 * num_samples, 3), sharex=True)

    if num_samples == 1:
        axes = [axes]  # make iterable

    for col_idx, file in enumerate(files):
        df = pd.read_csv(os.path.join(split_dir, file))

        # take only first `max_rows` rows
        df = df.iloc[:max_rows]

        ax = axes[col_idx]
        ax.plot(df["Time"], df["Value"])
        ax.set_title(f'Sample {col_idx + 1}',fontsize=14, weight='bold')

        # bold axis labels
        ax.set_xlabel("Time", fontsize=13, weight='bold')
        ax.set_ylabel("Amplitude", fontsize=13, weight='bold')

        # bold tick labels
        ax.tick_params(axis='both', which='major', labelsize=10, width=1.2)
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontweight('bold')

        ax.grid(False)

    plt.tight_layout()
    plt.savefig(
        '/scratch_nvme/Time_Series/Bio-Synthesize/Visualization_Scripts/Drift_Harmonic_Signals.pdf',
        dpi=800
    )
    # plt.show()
    plt.close()


# Run everything
base_dir = "/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Drift_Harmonic_Test_Visulaization"
generate_all_splits(base_dir, n_train=70, n_val=10, n_test=20)
visualize_signals(base_dir, num_samples=3)
