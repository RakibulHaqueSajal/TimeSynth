import numpy as np
import pandas as pd
import os
import hashlib
import matplotlib.pyplot as plt

# ------------------ Dual PM Signal ------------------
def generate_twofreq_phase_modulated_signal(t, A0, f0, beta0, fmod0,
                                            A1, f1, beta1, fmod1, offset):
    s1 = A0 * np.sin(2 * np.pi * f0 * t + beta0 * np.sin(2 * np.pi * fmod0 * t))
    s2 = A1 * np.sin(2 * np.pi * f1 * t + beta1 * np.sin(2 * np.pi * fmod1 * t))
    return s1 + s2 + offset

# ------------------ Noise Utilities ------------------
def add_awgn(signal, snr_db, rng):
    """
    Add white Gaussian noise achieving target SNR (in dB).
    SNR computed on zero-mean signal to avoid offset influencing power.
    """
    sig_zero_mean = signal - np.mean(signal)
    sig_power = np.mean(sig_zero_mean ** 2) + 1e-12
    snr_lin = 10.0 ** (snr_db / 10.0)
    noise_power = sig_power / snr_lin
    noise_std = np.sqrt(noise_power)
    noise = rng.normal(loc=0.0, scale=noise_std, size=signal.shape)
    return signal + noise

# ------------------ Unique Hash / Params ------------------
def param_hash_2f(A0, f0, beta0, fmod0, A1, f1, beta1, fmod1, offset, precision=6):
    key = "_".join([f"{x:.{precision}f}" for x in
                    (A0, f0, beta0, fmod0, A1, f1, beta1, fmod1, offset)])
    return hashlib.md5(key.encode()).hexdigest()

def sample_unique_param_sets_2f(n, bounds, existing_hashes, rng):
    params = []
    while len(params) < n:
        A0   = rng.uniform(*bounds["A_0"])
        A1   = rng.uniform(*bounds["A_1"])
        f0   = rng.uniform(*bounds["f_0"])
        f1   = rng.uniform(*bounds["f_1"])
        b0   = rng.uniform(*bounds["beta_0"])
        b1   = rng.uniform(*bounds["beta_1"])
        fm0  = rng.uniform(*bounds["fmod_0"])
        fm1  = rng.uniform(*bounds["fmod_1"])
        off  = rng.uniform(*bounds["offset"])
        h = param_hash_2f(A0, f0, b0, fm0, A1, f1, b1, fm1, off)
        if h not in existing_hashes:
            existing_hashes.add(h)
            params.append((A0, f0, b0, fm0, A1, f1, b1, fm1, off))
    return params

# ------------------ Save to CSV ------------------
def save_2f_signal(t, signal, params, idx, mode, base_dir, snr_tag=None):
    """
    Save one signal to CSV.
      - clean: base_dir/clean/<mode>/
      - noisy: base_dir/SNR_k/<mode>/
    """
    A0, f0, b0, fm0, A1, f1, b1, fm1, offset = params
    if snr_tag is None:
        split_dir = os.path.join(base_dir, "clean", mode)
        snr_suffix = ""
    else:
        split_dir = os.path.join(base_dir, f"SNR_{snr_tag}", mode)
        snr_suffix = f"_SNR{snr_tag}"
    os.makedirs(split_dir, exist_ok=True)

    filename = (
        f"{mode}_{idx:03d}"
        f"_A0_{A0:.4f}_f0_{f0:.4f}_b0_{b0:.4f}_fm0_{fm0:.4f}"
        f"_A1_{A1:.4f}_f1_{f1:.4f}_b1_{b1:.4f}_fm1_{fm1:.4f}"
        f"_offset_{offset:.4f}{snr_suffix}.csv"
    )
    df = pd.DataFrame({"Time": t, "Value": signal})
    df.to_csv(os.path.join(split_dir, filename), index=False)

# ------------------ Dataset Generator (CLEAN + SNR folders) ------------------
def generate_twofreq_pm_with_snr(
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
    Creates:
      - base_dir/clean/<split>/ : noiseless signals
      - base_dir/SNR_k/<split>/ : noisy signals at different SNRs

    The same parameter sets are used across all SNR levels for comparability.
    """
    if snr_db_map is None:
        snr_db_map = {1: 40.0, 2: 30.0, 3: 20.0, 4: 10.0}

    # Time axis (avoid duplicating the last point)
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)

    rng = np.random.default_rng(seed)
    used_hashes = set()
    splits = {"train": n_train, "val": n_val, "test": n_test}
    split_params = {m: sample_unique_param_sets_2f(c, bounds, used_hashes, rng)
                    for m, c in splits.items()}

    # 1) CLEAN
    for mode, plist in split_params.items():
        for idx, params in enumerate(plist):
            clean = generate_twofreq_phase_modulated_signal(t, *params)
            save_2f_signal(t, clean, params, idx, mode, base_dir, snr_tag=None)
    print("✓ Saved CLEAN dual-PM signals")

    # 2) NOISY (repeat with same params; fresh noise per level)
    for lvl in snr_levels:
        snr_db = snr_db_map.get(lvl, 20.0)
        rng_lvl = np.random.default_rng(seed + int(lvl) * 1000)
        for mode, plist in split_params.items():
            for idx, params in enumerate(plist):
                clean = generate_twofreq_phase_modulated_signal(t, *params)
                noisy = add_awgn(clean, snr_db, rng_lvl)
                save_2f_signal(t, noisy, params, idx, mode, base_dir, snr_tag=lvl)
        print(f"✓ Saved NOISY dual-PM signals @ SNR level {lvl} ({snr_db:.1f} dB)")

# ------------------ Optional: Visualization ------------------
def visualize_signals(base_dir, which="clean", snr_level=None, splits=("train","val","test"),
                      num_samples=5, max_timesteps=200, random_pick=False):
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
            df = pd.read_csv(os.path.join(split_dir, file)).iloc[:max_timesteps]
            ax.plot(df["Time"], df["Value"])
            ax.set_title(file.replace(".csv", ""), fontsize=8)
            ax.set_xlabel("Time")
            ax.grid(False)
        axes[0].set_ylabel("Value")
        plt.suptitle(f"{title_prefix} – {split.capitalize()} Set", fontsize=13)
        plt.tight_layout(rect=[0, 0, 1, 0.94])
        plt.savefig(os.path.join(base_dir, f"{title_prefix}_{split}.png"), dpi=300) 
        plt.show()

# ------------------ Main ------------------
if __name__ == "__main__":
    # Bounds (same style as your dual code)
    param_bounds = {
        "A_0":    (0.1, 0.1227),
        "A_1":    (0.1, 0.1227),
        "f_0":    (0.6782, 1.4112),
        "f_1":    (0.6782, 1.4112),
        "beta_0": (0.01, 0.3),
        "beta_1": (0.01, 0.3),
        "fmod_0": (0.01, 0.1),
        "fmod_1": (0.01, 0.1),
        "offset": (0.1937, 0.7418)
    }

    base_dir = "/scratch_nvme/Time_Series/Bio-Synthesize/noisy signal generation/DPM_Harmonic_Signal"

    # Map SNR levels to dB (edit as needed)
    snr_db_map = {1: 40.0, 2: 30.0, 3: 20.0, 4: 10.0,5:5.0, 6:1.0}

    generate_twofreq_pm_with_snr(
        base_dir=base_dir,
        bounds=param_bounds,
        snr_levels=(1, 2, 3, 4,5,6),
        snr_db_map=snr_db_map,
        n_train=70, n_val=10, n_test=20,
        fs=10, duration=300,
        seed=42,
    )

    # Quick visual checks (optional)
    visualize_signals(base_dir, which="clean", num_samples=3, max_timesteps=300)
    visualize_signals(base_dir, which="snr", snr_level=1, num_samples=3, max_timesteps=300)
    visualize_signals(base_dir, which="snr", snr_level=2, num_samples=3, max_timesteps=300)
    visualize_signals(base_dir, which="snr", snr_level=3, num_samples=3, max_timesteps=300)
    visualize_signals(base_dir, which="snr", snr_level=4, num_samples=3, max_timesteps=300)
    visualize_signals(base_dir, which="snr", snr_level=5, num_samples=3, max_timesteps=300)
    visualize_signals(base_dir, which="snr", snr_level=6, num_samples=3, max_timesteps=300)
