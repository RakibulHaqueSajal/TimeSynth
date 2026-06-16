import numpy as np
import pandas as pd
import os
import hashlib
import matplotlib.pyplot as plt

# ------------------ Signal definition ------------------
def drift_modulated_harmonic(t, epsilon, f, phi, a):
    A_t = 1 + epsilon * t
    base = np.sin(2 * np.pi * f * t + phi)
    trend = a * t
    signal = A_t * base + trend
    # Normalize to [0, 1] for a consistent dynamic range before adding noise
    return (signal - np.min(signal)) / (np.max(signal) - np.min(signal) + 1e-12)

# ------------------ AWGN utilities ------------------
def add_awgn(signal, snr_db, rng):
    """
    Add white Gaussian noise to achieve target SNR (dB).
    SNR defined on the zero-mean signal to avoid offset inflation.
    """
    s0 = signal - np.mean(signal)
    sig_power = np.mean(s0**2) + 1e-12
    snr_lin = 10 ** (snr_db / 10.0)
    noise_power = sig_power / snr_lin
    noise_std = np.sqrt(noise_power)
    noise = rng.normal(0.0, noise_std, size=signal.shape)
    return signal + noise

# ------------------ Unique hash tracker ------------------
def param_hash(f, phi, a, precision=6):
    key = f"{f:.{precision}f}_{phi:.{precision}f}_{a:.{precision}e}"
    return hashlib.md5(key.encode()).hexdigest()

# ------------------ Generate unique parameter sets ------------------
def sample_unique_param_sets(n, f_range, phi_range, a_range, existing_hashes, rng):
    params = []
    while len(params) < n:
        f   = rng.uniform(*f_range)
        phi = rng.uniform(*phi_range)
        a   = rng.uniform(*a_range)
        h = param_hash(f, phi, a)
        if h not in existing_hashes:
            existing_hashes.add(h)
            params.append((f, phi, a))
    return params

# ------------------ Save signal ------------------
def save_signal(t, signal, epsilon, f, phi, a, idx, mode, base_dir, snr_tag=None):
    """
    snr_tag: None for clean, or integer level (1..4) to store under SNR_<tag>/
    """
    if snr_tag is None:
        split_dir = os.path.join(base_dir, "Clean", mode)
    else:
        split_dir = os.path.join(base_dir, f"SNR_{snr_tag}", mode)

    os.makedirs(split_dir, exist_ok=True)

    snr_suffix = "" if snr_tag is None else f"_SNR{snr_tag}"
    filename = (
        f"{mode}_{idx:03d}_epsilon_{epsilon:.4f}_f_{f:.4f}_phi_{phi:.4f}_a_{a:.8e}{snr_suffix}.csv"
    )
    df = pd.DataFrame({"Time": t, "Value": signal})
    df.to_csv(os.path.join(split_dir, filename), index=False)


# ------------------ Main generation with SNR folders ------------------
def generate_all_splits_with_snr(
    base_dir,
    n_train=70, n_val=10, n_test=20,
    fs=10, duration=300, epsilon=-0.05,
    f_range=(0.85, 1.10), phi_range=(-0.6, 0.75), a_range=(-6e-5, 8e-5),
    snr_levels=(1,2,3,4), snr_db_map=None, seed=1234
):
    """
    Creates a clean dataset AND SNR_1..SNR_4 datasets using the SAME parameter sets.
    Only the noise differs across SNR folders.
    """
    if snr_db_map is None:
        snr_db_map = {1: 40.0, 2: 30.0, 3: 20.0, 4: 10.0}

    t = np.linspace(0, duration, int(fs * duration))  # keep original endpoint behavior
    rng = np.random.default_rng(seed)

    # Sample unique params once for all SNR levels
    used = set()
    splits = {'train': n_train, 'val': n_val, 'test': n_test}
    split_params = {}
    for mode, count in splits.items():
        split_params[mode] = sample_unique_param_sets(count, f_range, phi_range, a_range, used, rng)

    # 1) Clean signals
    for mode, plist in split_params.items():
        for idx, (f, phi, a) in enumerate(plist):
            sig = drift_modulated_harmonic(t, epsilon, f, phi, a)
            save_signal(t, sig, epsilon, f, phi, a, idx, mode, base_dir, snr_tag=None)
    print("✓ Saved CLEAN signals")

    # 2) Noisy signals at each SNR (only noise changes)
    for lvl in snr_levels:
        snr_db = snr_db_map.get(lvl, 20.0)
        rng_lvl = np.random.default_rng(seed + lvl * 1000)
        for mode, plist in split_params.items():
            for idx, (f, phi, a) in enumerate(plist):
                clean = drift_modulated_harmonic(t, epsilon, f, phi, a)
                noisy = add_awgn(clean, snr_db, rng_lvl)
                save_signal(t, noisy, epsilon, f, phi, a, idx, mode, base_dir, snr_tag=lvl)
        print(f"✓ Saved NOISY signals @ SNR level {lvl} ({snr_db:.1f} dB)")

# ------------------ Visualization (optional) ------------------
def visualize_signals(base_dir, num_samples=5, max_timesteps=200, snr_tag=None):
    """
    Visualize first `max_timesteps` of a few signals.

    snr_tag:
        None  -> read from base_dir/Clean/<split>/
        int k -> read from base_dir/SNR_k/<split>/
        str s -> if you pass 'Clean' or 'SNR_3' explicitly, it's used as-is.
    """
    # resolve root folder for this view
    if isinstance(snr_tag, str):
        root = os.path.join(base_dir, snr_tag)
        title_prefix = snr_tag
    elif snr_tag is None:
        root = os.path.join(base_dir, "Clean")
        title_prefix = "Clean"
    else:
        root = os.path.join(base_dir, f"SNR_{snr_tag}")
        title_prefix = f"SNR {snr_tag}"

    splits = ['train', 'val', 'test']
    for split in splits:
        split_dir = os.path.join(root, split)
        if not os.path.isdir(split_dir):
            print(f"(!) Missing directory: {split_dir}")
            continue

        files = sorted([f for f in os.listdir(split_dir) if f.endswith(".csv")])[:num_samples]
        if len(files) == 0:
            print(f"(!) No CSV files found in {split_dir}")
            continue

        fig, axes = plt.subplots(1, num_samples, figsize=(4 * num_samples, 3), sharey=True)
        if num_samples == 1:
            axes = [axes]

        for col_idx, file in enumerate(files):
            df = pd.read_csv(os.path.join(split_dir, file))
            df = df.iloc[:max_timesteps]
            ax = axes[col_idx]
            ax.plot(df["Time"], df["Value"])
            ax.set_title(file.replace(".csv", ""), fontsize=8)
            ax.set_xlabel("Time")
            if col_idx == 0:
                ax.set_ylabel("Value")
            ax.grid(True)

        plt.suptitle(f"{title_prefix} – {split.capitalize()} Set", fontsize=13)
        plt.tight_layout(rect=[0, 0, 1, 0.94])
        plt.savefig(os.path.join(root, f"{split}.png"), dpi=300)
        plt.show()


# ------------------ Run everything ------------------
if __name__ == "__main__":
    base_dir = "/scratch_nvme/Time_Series/Bio-Synthesize/noisy signal generation/drift_harmonic_signal"

    generate_all_splits_with_snr(
        base_dir=base_dir,
        n_train=70, n_val=10, n_test=20,
        fs=10, duration=300,
        epsilon=-0.05,
        f_range=(0.85, 1.10),
        phi_range=(-0.6, 0.75),
        a_range=(-6e-5, 8e-5),
        snr_levels=(1,2,3,4,5,6),
        snr_db_map={1:40.0, 2:30.0, 3:20.0, 4:10.0, 4:5.0, 6:1.0},
        seed=42
    )

    # Optional quick checks:
    visualize_signals(base_dir, num_samples=3, max_timesteps=200, snr_tag=None)  # clean
    visualize_signals(base_dir, num_samples=3, max_timesteps=200, snr_tag=1)    # noisy
    visualize_signals(base_dir, num_samples=3, max_timesteps=200, snr_tag=2)    # noisy
    visualize_signals(base_dir, num_samples=3, max_timesteps=200, snr_tag=3)    # noisy
    visualize_signals(base_dir, num_samples=3, max_timesteps=200, snr_tag=4)    # noisy
    visualize_signals(base_dir, num_samples=3, max_timesteps=200, snr_tag=5)    # noisy
    visualize_signals(base_dir, num_samples=3, max_timesteps=200, snr_tag=6)    # noisy
 

