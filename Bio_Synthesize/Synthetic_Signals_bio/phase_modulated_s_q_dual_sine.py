import numpy as np
import pandas as pd
import os
import hashlib
import matplotlib.pyplot as plt

# ------------------ Signal Definition ------------------
def generate_twofreq_phase_modulated_signal(t, A0, f0, beta0, fmod0, A1, f1, beta1, fmod1, offset):
    s1 = A0 * np.sin(2 * np.pi * f0 * t + beta0 * np.sin(2 * np.pi * fmod0 * t))
    s2 = A1 * np.sin(2 * np.pi * f1 * t + beta1 * np.sin(2 * np.pi * fmod1 * t))
    return s1 + s2 + offset

# ------------------ Unique Hash Function ------------------
def param_hash_2f(*args, precision=6):
    key = "_".join([f"{x:.{precision}f}" for x in args])
    return hashlib.md5(key.encode()).hexdigest()

# ------------------ Save Signal to CSV ------------------
def save_2f_signal(t, signal, params, idx, mode, base_dir):
    split_dir = os.path.join(base_dir, mode)
    os.makedirs(split_dir, exist_ok=True)
    A0, f0, beta0, fmod0, A1, f1, beta1, fmod1, offset = params
    filename = (
        f"{mode}_{idx:03d}_A0_{A0:.3f}_f0_{f0:.3f}_b0_{beta0:.3f}_fm0_{fmod0:.3f}"
        f"_A1_{A1:.3f}_f1_{f1:.3f}_b1_{beta1:.3f}_fm1_{fmod1:.3f}_offset_{offset:.3f}.csv"
    )
    df = pd.DataFrame({"Time": t, "Value": signal})
    df.to_csv(os.path.join(split_dir, filename), index=False)

# ------------------ Sample Unique Parameters ------------------
def sample_unique_param_sets_2f(n, bounds, existing_hashes):
    params = []
    while len(params) < n:
        A0 = np.random.uniform(*bounds["A_0"])
        A1 = np.random.uniform(*bounds["A_1"])
        f0 = np.random.uniform(*bounds["f_0"])
        f1 = np.random.uniform(*bounds["f_1"])
        b0 = np.random.uniform(*bounds["beta_0"])
        b1 = np.random.uniform(*bounds["beta_1"])
        fm0 = np.random.uniform(*bounds["fmod_0"])
        fm1 = np.random.uniform(*bounds["fmod_1"])
        offset = np.random.uniform(*bounds["offset"])
        h = param_hash_2f(A0, f0, b0, fm0, A1, f1, b1, fm1, offset)
        if h not in existing_hashes:
            existing_hashes.add(h)
            params.append((A0, f0, b0, fm0, A1, f1, b1, fm1, offset))
    return params

# ------------------ Generate All Splits ------------------
def generate_twofreq_pm_from_bounds(bounds, base_dir, n_train=70, n_val=10, n_test=20, fs=10, duration=300):
    t = np.linspace(0, duration, int(fs * duration))
    used_hashes = set()

    splits = {
        "train": n_train,
        "val": n_val,
        "test": n_test
    }

    for mode, count in splits.items():
        param_list = sample_unique_param_sets_2f(count, bounds, used_hashes)
        for idx, params in enumerate(param_list):
            signal = generate_twofreq_phase_modulated_signal(t, *params)
            save_2f_signal(t, signal, params, idx, mode, base_dir)
        print(f"Saved {count} samples to {mode}/")

# ------------------ Visualization ------------------
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
        ax.set_title(f'Sample {col_idx + 1}', fontsize=14, weight='bold')

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
        '/scratch_nvme/Time_Series/Bio-Synthesize/Visualization_Scripts/DPM_Harmonic_Signals.pdf',
        dpi=800
    )
    # plt.show()
    plt.close()


# ------------------ Main Execution ------------------
if __name__ == "__main__":
    # Define bounds based on your earlier dataset
    param_bounds = {
        "A_0": (0.1, 0.1227),
        "A_1": (0.1, 0.1227),
        "f_0": (0.6782, 1.4112),
        "f_1": (0.6782, 1.4112),
        "beta_0": (0.01, 0.3),
        "beta_1": (0.01, 0.3),
        "fmod_0": (0.01, 0.1),
        "fmod_1": (0.01, 0.1),
        "offset": (0.1937, 0.7418)
    }

    # Output directory
    base_dir = "/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/PhaseMod_TwoFreq"

    # Generate signals from bounds
    generate_twofreq_pm_from_bounds(param_bounds, base_dir, n_train=70, n_val=10, n_test=20)

    # Visualize a few samples
    visualize_signals(base_dir, num_samples=3, max_rows=100)
