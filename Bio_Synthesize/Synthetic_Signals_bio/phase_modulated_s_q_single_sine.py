import numpy as np
import pandas as pd
import os
import hashlib
import matplotlib.pyplot as plt

# ------------------ Signal Definition ------------------
def generate_phase_modulated_signal(t, A, f, beta, fmod, offset):
    return A * np.sin(2 * np.pi * f * t + beta * np.sin(2 * np.pi * fmod * t)) + offset

# ------------------ Unique Hash for Parameters ------------------
def param_hash_pm(A, f, beta, fmod, offset, precision=6):
    key = f"{A:.{precision}f}_{f:.{precision}f}_{beta:.{precision}f}_{fmod:.{precision}f}_{offset:.{precision}f}"
    return hashlib.md5(key.encode()).hexdigest()

# ------------------ Unique Parameter Sampler ------------------
def sample_unique_pm_param_sets(n, bounds, existing_hashes):
    params = []
    while len(params) < n:
        A = np.random.uniform(*bounds["A"])
        f = np.random.uniform(*bounds["f"])
        beta = np.random.uniform(*bounds["beta"])
        fmod = np.random.uniform(*bounds["fmod"])
        offset = np.random.uniform(*bounds["offset"])
        h = param_hash_pm(A, f, beta, fmod, offset)
        if h not in existing_hashes:
            existing_hashes.add(h)
            params.append((A, f, beta, fmod, offset))
    return params

# ------------------ Save to CSV ------------------
def save_pm_signal(t, signal, A, f, beta, fmod, offset, idx, mode, base_dir):
    split_dir = os.path.join(base_dir, mode)
    os.makedirs(split_dir, exist_ok=True)
    filename = f"{mode}_{idx:03d}_A_{A:.4f}_f_{f:.4f}_beta_{beta:.4f}_fmod_{fmod:.4f}_offset_{offset:.4f}.csv"
    df = pd.DataFrame({"Time": t, "Value": signal})
    df.to_csv(os.path.join(split_dir, filename), index=False)

# ------------------ Dataset Generator ------------------
def generate_pm_signals(base_dir, bounds, n_train=70, n_val=10, n_test=20, fs=10, duration=300):
    t = np.linspace(0, duration, int(fs * duration))
    used_hashes = set()
    splits = {"train": n_train, "val": n_val, "test": n_test}

    for mode, count in splits.items():
        param_list = sample_unique_pm_param_sets(count, bounds, used_hashes)
        for idx, (A, f, beta, fmod, offset) in enumerate(param_list):
            signal = generate_phase_modulated_signal(t, A, f, beta, fmod, offset)
            save_pm_signal(t, signal, A, f, beta, fmod, offset, idx, mode, base_dir)
        print(f"Saved {count} samples to {mode}/")

# ------------------ Optional: Visualization ------------------def visualize_signals(base_dir, num_samples=3, max_rows=50):
def visualize_signals(base_dir, num_samples=3, max_rows=50):
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
        ax.set_title(f'Sample {col_idx+1}', fontsize=14, weight='bold')

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
        '/scratch_nvme/Time_Series/Bio-Synthesize/Visualization_Scripts/SPM_Harmonic_Signals.pdf',
        dpi=800
    )
    # plt.show()
    plt.close()
# ------------------ Main Execution ------------------
if __name__ == "__main__":
    # Define bounds based on your dataset
    param_bounds = {
        "A": (0.1, 0.1227),
        "f": (0.6782, 1.4112),
        "beta": (0.01, 0.3),
        "fmod": (0.01, 0.1),
        "offset": (0.1937, 0.7418)
    }

    # Output directory
    base_dir = "/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/PhaseMod_SingleFreq/Visualization"

    # Generate signals
    generate_pm_signals(base_dir, param_bounds, n_train=70, n_val=10, n_test=20)

    # Visualize few samples
    visualize_signals(base_dir, num_samples=3,max_rows=100)
