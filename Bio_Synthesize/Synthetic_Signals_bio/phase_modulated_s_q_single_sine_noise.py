import numpy as np
import pandas as pd
import os
import hashlib
import matplotlib.pyplot as plt

# ------------------ Signal Definition ------------------
def generate_phase_modulated_signal(t, A, f, beta, fmod, offset):
    return A * np.sin(2 * np.pi * f * t + beta * np.sin(2 * np.pi * fmod * t)) + offset

# ------------------ Noise Utilities ------------------
def add_awgn(signal, snr_db, rng):
    """
    Add white Gaussian noise to achieve target SNR in dB.
    SNR = signal_power / noise_power (power ratio, not dB).
    """
    # Use zero-mean version to estimate signal power robustly (offset shouldn't dominate)
    sig_zero_mean = signal - np.mean(signal)
    sig_power = np.mean(sig_zero_mean ** 2) + 1e-12  # avoid 0

    snr_lin = 10 ** (snr_db / 10.0)
    noise_power = sig_power / snr_lin
    noise_std = np.sqrt(noise_power)

    noise = rng.normal(loc=0.0, scale=noise_std, size=signal.shape)
    return signal + noise

# ------------------ Unique Hash for Parameters ------------------
def param_hash_pm(A, f, beta, fmod, offset, precision=6):
    key = f"{A:.{precision}f}_{f:.{precision}f}_{beta:.{precision}f}_{fmod:.{precision}f}_{offset:.{precision}f}"
    return hashlib.md5(key.encode()).hexdigest()

# ------------------ Unique Parameter Sampler ------------------
def sample_unique_pm_param_sets(n, bounds, existing_hashes, rng):
    params = []
    while len(params) < n:
        A = rng.uniform(*bounds["A"])
        f = rng.uniform(*bounds["f"])
        beta = rng.uniform(*bounds["beta"])
        fmod = rng.uniform(*bounds["fmod"])
        offset = rng.uniform(*bounds["offset"])
        h = param_hash_pm(A, f, beta, fmod, offset)
        if h not in existing_hashes:
            existing_hashes.add(h)
            params.append((A, f, beta, fmod, offset))
    return params

# ------------------ Save to CSV ------------------
def save_pm_signal(t, signal, A, f, beta, fmod, offset, idx, mode, base_dir, snr_tag=None):
    """
    Save one signal CSV.

    Parameters
    ----------
    t : np.ndarray
        Time vector.
    signal : np.ndarray
        Signal values (clean or noisy).
    A, f, beta, fmod, offset : float
        Parameters used to generate the signal.
    idx : int
        Sample index within the split.
    mode : str
        One of {'train','val','test'}.
    base_dir : str
        Root directory for this dataset (parent of 'clean' and 'SNR_k').
    snr_tag : int | None
        None  -> save under base_dir/clean/<mode>/
        int k -> save under base_dir/SNR_k/<mode>/
    """
    # Route to 'clean/' or 'SNR_k/'
    if snr_tag is None:
        split_dir = os.path.join(base_dir, "clean", mode)
        snr_suffix = ""
    else:
        split_dir = os.path.join(base_dir, f"SNR_{snr_tag}", mode)
        snr_suffix = f"_SNR{snr_tag}"

    os.makedirs(split_dir, exist_ok=True)

    # File name encodes parameters (and SNR if present)
    filename = (
        f"{mode}_{idx:03d}"
        f"_A_{A:.4f}_f_{f:.4f}_beta_{beta:.4f}_fmod_{fmod:.4f}_offset_{offset:.4f}"
        f"{snr_suffix}.csv"
    )

    df = pd.DataFrame({"Time": t, "Value": signal})
    df.to_csv(os.path.join(split_dir, filename), index=False)


# ------------------ Dataset Generator (CLEAN + SNR folders) ------------------
def generate_pm_signals_with_snr(
    base_dir,
    bounds,
    snr_levels=(1, 2, 3, 4),
    snr_db_map=None,
    n_train=70,
    n_val=10,
    n_test=20,
    fs=10,
    duration=300,
    seed=42,
):
    """
    Generates:
      - Clean set (no noise) at base_dir (optional: comment out if not needed)
      - Noisy sets at base_dir/SNR_k/ for each k in snr_levels
    Uses the same parameter sets for all SNR folders.
    """
    if snr_db_map is None:
        # Default mapping: higher level = lower SNR (noisier)
        snr_db_map = {1: 40.0, 2: 30.0, 3: 20.0, 4: 10.0, 5:5.0, 6:1.0}

    # Time axis
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)

    # Sample unique parameter sets ONCE for all SNR folders
    rng = np.random.default_rng(seed)
    used_hashes = set()
    splits = {"train": n_train, "val": n_val, "test": n_test}
    split_params = {}

    for mode, count in splits.items():
        split_params[mode] = sample_unique_pm_param_sets(count, bounds, used_hashes, rng)

    # 1) Save CLEAN signals (optional; comment this block if you don't want clean)
    for mode, plist in split_params.items():
        for idx, (A, f, beta, fmod, offset) in enumerate(plist):
            clean = generate_phase_modulated_signal(t, A, f, beta, fmod, offset)
            save_pm_signal(t, clean, A, f, beta, fmod, offset, idx, mode, base_dir, snr_tag=None)
    print("✓ Saved CLEAN signals")

    # 2) Save NOISY signals for each SNR level (same parameters, new noise per level)
    for lvl in snr_levels:
        snr_db = snr_db_map.get(lvl, 20.0)  # fallback to 20 dB if not in map
        # fresh RNG per level for reproducibility but different noise draws
        rng_lvl = np.random.default_rng(seed + int(lvl) * 1000)

        for mode, plist in split_params.items():
            for idx, (A, f, beta, fmod, offset) in enumerate(plist):
                clean = generate_phase_modulated_signal(t, A, f, beta, fmod, offset)
                noisy = add_awgn(clean, snr_db, rng_lvl)
                save_pm_signal(t, noisy, A, f, beta, fmod, offset, idx, mode, base_dir, snr_tag=lvl)
        print(f"✓ Saved NOISY signals @ SNR level {lvl} ({snr_db:.1f} dB)")

# ------------------ Optional: Visualization ------------------
def visualize_signals(base_dir, which="clean", snr_level=None, splits=("train","val","test"),
                      num_samples=5, max_timesteps=200, random_pick=False):
    """
    Visualize a few signals from 'clean/' or 'SNR_k/' folders.

    Parameters
    ----------
    base_dir : str
        Root directory (parent of 'clean' and 'SNR_k').
    which : {'clean', 'snr'}
        'clean' -> show from base_dir/clean/<split>/
        'snr'   -> show from base_dir/SNR_<snr_level>/<split>/
    snr_level : int | None
        Required if which=='snr'; ignored for 'clean'.
    splits : tuple[str, ...]
        Splits to visualize (default: ('train','val','test')).
    num_samples : int
        Number of files per split to plot (columns).
    max_timesteps : int
        Plot only the first `max_timesteps` points for readability.
    random_pick : bool
        If True, randomly pick files (when many). Otherwise take the first N.
    """
    if which not in {"clean", "snr"}:
        raise ValueError("`which` must be 'clean' or 'snr'.")

    if which == "clean":
        root = os.path.join(base_dir, "clean")
        title_prefix = "Clean"
    else:
        if snr_level is None:
            raise ValueError("Provide `snr_level` when which='snr'.")
        root = os.path.join(base_dir, f"SNR_{snr_level}")
        title_prefix = f"SNR {snr_level}"

    for split in splits:
        split_dir = os.path.join(root, split)
        if not os.path.isdir(split_dir):
            print(f"(!) Missing directory: {split_dir}")
            continue

        files = sorted([f for f in os.listdir(split_dir) if f.endswith(".csv")])
        if not files:
            print(f"(!) No CSV files found in {split_dir}")
            continue

        if random_pick and len(files) > num_samples:
            rng = np.random.default_rng(123)
            files = list(rng.choice(files, size=num_samples, replace=False))
        else:
            files = files[:num_samples]

        fig, axes = plt.subplots(1, len(files), figsize=(4 * len(files), 3), sharey=True)
        if len(files) == 1:
            axes = [axes]

        for ax, file in zip(axes, files):
            df = pd.read_csv(os.path.join(split_dir, file))
            df = df.iloc[:max_timesteps]
            ax.plot(df["Time"], df["Value"])
            ax.set_title(file.replace(".csv", ""), fontsize=8)
            ax.set_xlabel("Time")
            ax.grid(True)

        axes[0].set_ylabel("Value")
        plt.suptitle(f"{title_prefix} – {split.capitalize()} Set", fontsize=13)
        plt.tight_layout(rect=[0, 0, 1, 0.94])
        plt.show()
        plt.savefig(os.path.join(split_dir, f"{title_prefix}_{split}_set.png"))


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

    # Output directory (parent for clean + SNR subfolders)
    base_dir = "/scratch_nvme/Time_Series/Bio-Synthesize/noisy signal generation/SPM_Harmonic"

    # Map SNR levels to dB (edit as you like)
    snr_db_map = {1: 40.0, 2: 30.0, 3: 20.0, 4: 10.0,5:5.0, 6:1.0}

    # Generate datasets (clean + SNR_1..4)
    generate_pm_signals_with_snr(
        base_dir=base_dir,
        bounds=param_bounds,
        snr_levels=(1, 2, 3, 4,5,6),
        snr_db_map=snr_db_map,
        n_train=70, n_val=10, n_test=20,
        fs=10, duration=300,
        seed=42,
    )

    # Quick visual check (optional)
    visualize_signals(base_dir, num_samples=3, max_timesteps=300, snr_level=None)  # clean
    visualize_signals(base_dir, num_samples=3, which="snr",max_timesteps=300, snr_level=1)
    visualize_signals(base_dir, num_samples=3, which="snr",max_timesteps=300, snr_level=2)
    visualize_signals(base_dir, num_samples=3, which="snr",max_timesteps=300, snr_level=3)
    visualize_signals(base_dir, num_samples=3, which="snr",max_timesteps=300, snr_level=4)
    visualize_signals(base_dir, num_samples=3, which="snr",max_timesteps=300, snr_level=5)
    visualize_signals(base_dir, num_samples=3, which="snr",max_timesteps=300, snr_level=6)
