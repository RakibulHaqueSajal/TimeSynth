import numpy as np
import pandas as pd
import os
import hashlib
import matplotlib.pyplot as plt

# ------------------ Signal Definition (CLEAN ONLY) ------------------
def generate_phase_modulated_signal(t, A, f, beta, fmod, offset):
    """
    Single-frequency phase-modulated sine:
      s(t) = A * sin(2π f t + beta * sin(2π fmod t)) + offset
    """
    return A * np.sin(2 * np.pi * f * t + beta * np.sin(2 * np.pi * fmod * t)) + offset


# ------------------ Unique Hash for Parameters ------------------
def param_hash_pm(A, f, beta, fmod, offset, precision=6):
    key = f"{A:.{precision}f}_{f:.{precision}f}_{beta:.{precision}f}_{fmod:.{precision}f}_{offset:.{precision}f}"
    return hashlib.md5(key.encode()).hexdigest()


# ------------------ Unique Parameter Sampler ------------------
def sample_unique_pm_param_sets(n, bounds, existing_hashes, rng, f_override_range=None):
    """
    If f_override_range is provided, 'f' is sampled from that instead of bounds['f'].
    """
    params = []
    while len(params) < n:
        A     = rng.uniform(*bounds["A"])
        f     = rng.uniform(*(f_override_range if f_override_range else bounds["f"]))
        beta  = rng.uniform(*bounds["beta"])
        fmod  = rng.uniform(*bounds["fmod"])
        offset= rng.uniform(*bounds["offset"])
        h = param_hash_pm(A, f, beta, fmod, offset)
        if h not in existing_hashes:
            existing_hashes.add(h)
            params.append((A, f, beta, fmod, offset))
    return params


# ------------------ Path & Metadata Helpers ------------------
def _range_tag(fr):
    return f"f_{fr[0]:.3f}_{fr[1]:.3f}"

def save_pm_signal_csv(t, signal, A, f, beta, fmod, offset, idx, base_dir, f_range):
    """
    Save under: <base_dir>/<f_low_f_high>/test/<filename.csv>
    """
    split_dir = os.path.join(base_dir, _range_tag(f_range), "test")
    os.makedirs(split_dir, exist_ok=True)
    filename = (
        f"test_{idx:03d}"
        f"_A_{A:.4f}_f_{f:.4f}_beta_{beta:.4f}_fmod_{fmod:.4f}_offset_{offset:.4f}.csv"
    )
    df = pd.DataFrame({"Time": t, "Value": signal})
    out = os.path.join(split_dir, filename)
    df.to_csv(out, index=False)
    return out

def append_metadata_row(meta_rows, filepath, A, f, beta, fmod, offset, fs, duration, seed, f_low, f_high):
    meta_rows.append({
        "filepath": filepath,
        "A": A, "f": f, "beta": beta, "fmod": fmod, "offset": offset,
        "fs": fs, "duration": duration, "seed": seed,
        "f_low": f_low, "f_high": f_high, "bucket_tag": _range_tag((f_low, f_high))
    })

def write_metadata_csv(meta_rows, base_dir, f_range):
    test_dir = os.path.join(base_dir, _range_tag(f_range), "test")
    os.makedirs(test_dir, exist_ok=True)
    meta_path = os.path.join(test_dir, "metadata_test.csv")
    pd.DataFrame(meta_rows).to_csv(meta_path, index=False)


# ------------------ Frequency Range Builder (OOD buckets) ------------------
def make_shifted_ranges(train_f=(0.68, 1.41), n_below=2, n_above=2, digits=2):
    f_low, f_high = train_f
    width = f_high - f_low

    buckets = []

    # Split [0, f_low) into n_below equal slices
    span_below = f_low
    step_below = span_below / n_below
    start = 0.0
    for _ in range(n_below):
        buckets.append((round(start, digits), round(start + step_below, digits)))
        start += step_below

    # Training bucket
    buckets.append((round(f_low, digits), round(f_high, digits)))

    # Step above by multiples of train width
    lo, hi = f_low, f_high
    for _ in range(n_above):
        lo += width
        hi += width
        buckets.append((round(lo, digits), round(hi, digits)))

    return buckets


# ------------------ Main Generator (CLEAN OOD buckets) ------------------
def generate_pm_clean_ood(
    base_dir,
    bounds,
    f_distributions,   # list of (f_low, f_high)
    n_test=20,
    fs=10,
    duration=300,
    seed=42,
):
    """
    For each frequency bucket in f_distributions, generate n_test CLEAN signals.
    Saves per-sample CSVs + per-bucket metadata_test.csv.
    """
    # Exact sampling at fs
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)

    rng = np.random.default_rng(seed)
    used_hashes = set()  # ensure global uniqueness across ALL buckets

    for f_range in f_distributions:
        test_params = sample_unique_pm_param_sets(
            n=n_test,
            bounds=bounds,
            existing_hashes=used_hashes,
            rng=rng,
            f_override_range=f_range,
        )
        meta_rows = []
        for idx, (A, f, beta, fmod, offset) in enumerate(test_params):
            sig = generate_phase_modulated_signal(t, A, f, beta, fmod, offset)
            fpath = save_pm_signal_csv(t, sig, A, f, beta, fmod, offset, idx, base_dir, f_range)
            append_metadata_row(meta_rows, fpath, A, f, beta, fmod, offset, fs, duration, seed, f_range[0], f_range[1])

        write_metadata_csv(meta_rows, base_dir, f_range)
        print(f"✓ Generated CLEAN test set for f_range={f_range} at {os.path.join(base_dir, _range_tag(f_range), 'test')}")


# ------------------ Visualization Across Buckets ------------------
def visualize_buckets(base_dir, f_distributions, num_samples=3, max_timesteps=300, random_pick=False):
    """
    For each bucket, plot up to 'num_samples' test CSVs (first max_timesteps points).
    """
    for f_range in f_distributions:
        split_dir = os.path.join(base_dir, _range_tag(f_range), "test")
        if not os.path.isdir(split_dir):
            print(f"(!) Missing directory: {split_dir}")
            continue

        files = sorted([f for f in os.listdir(split_dir) if f.endswith(".csv") and f.startswith("test_")])
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
        plt.suptitle(f"Bucket {_range_tag(f_range)} – CLEAN test samples", fontsize=13)
        plt.tight_layout(rect=[0, 0, 1, 0.94])
        plt.show()


# ------------------ Main ------------------
if __name__ == "__main__":
    # Parameter bounds (edit as needed)
    param_bounds = {
        "A": (0.1, 0.1227),
        "f": (0.6782, 1.4112),   # used only if you generate a non-bucketed set; buckets override this
        "beta": (0.01, 0.3),
        "fmod": (0.01, 0.1),
        "offset": (0.1937, 0.7418),
    }

    # Training frequency range and OOD buckets
    train_f_range = (0.6782, 1.4112)
    f_buckets = make_shifted_ranges(train_f=train_f_range, n_below=2, n_above=2)

    print(f_buckets)


    base_dir = "/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq"

    # Generate CLEAN OOD-only sets (per bucket)
    generate_pm_clean_ood(
        base_dir=base_dir,
        bounds=param_bounds,
        f_distributions=f_buckets,
        n_test=20,
        fs=10,
        duration=300,
        seed=42,
    )

    # Visualize a few examples per bucket
    visualize_buckets(base_dir, f_buckets, num_samples=3, max_timesteps=300, random_pick=False)
