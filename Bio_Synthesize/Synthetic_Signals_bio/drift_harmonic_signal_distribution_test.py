import numpy as np
import pandas as pd
import os
import hashlib

# -------------------------- Signal definition --------------------------
def drift_modulated_harmonic(t, epsilon, f, phi, a):
    A_t = 1 + epsilon * t
    base = np.sin(2 * np.pi * f * t + phi)
    trend = a * t
    signal = A_t * base + trend
    return (signal - np.min(signal)) / (np.max(signal) - np.min(signal) + 1e-12)

# -------------------------- Unique hash generator --------------------------
def param_hash(f, phi, a, precision=6):
    key = f"{f:.{precision}f}_{phi:.{precision}f}_{a:.{precision}e}"
    return hashlib.md5(key.encode()).hexdigest()

# -------------------------- Unique sampler --------------------------
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

# -------------------------- Save helpers --------------------------
def _range_tag(fr):
    return f"f_{fr[0]:.2f}_{fr[1]:.2f}"

def save_signal_csv(t, signal, epsilon, f, phi, a, idx, base_dir, f_range):
    # <base_dir>/<f_low_f_high>/test/<files.csv>
    split_dir = os.path.join(base_dir, _range_tag(f_range), "test")
    os.makedirs(split_dir, exist_ok=True)
    filename = f"test_{idx:03d}_epsilon_{epsilon:.4f}_f_{f:.4f}_phi_{phi:.4f}_a_{a:.8e}.csv"
    df = pd.DataFrame({"Time": t, "Value": signal})
    df.to_csv(os.path.join(split_dir, filename), index=False)
    return os.path.join(split_dir, filename)

def append_metadata_row(meta_rows, filepath, epsilon, f, phi, a, fs, duration, seed, f_low, f_high):
    meta_rows.append({
        "filepath": filepath,
        "epsilon": epsilon,
        "f": f,
        "phi": phi,
        "a": a,
        "fs": fs,
        "duration": duration,
        "seed": seed,
        "f_low": f_low,
        "f_high": f_high
    })

def write_metadata_csv(meta_rows, base_dir, f_range):
    # <base_dir>/<f_low_f_high>/test/metadata_test.csv
    test_dir = os.path.join(base_dir, _range_tag(f_range), "test")
    os.makedirs(test_dir, exist_ok=True)
    meta_path = os.path.join(test_dir, "metadata_test.csv")
    pd.DataFrame(meta_rows).to_csv(meta_path, index=False)

# -------------------------- Main generator --------------------------
def generate_test_dist_shift(
    base_dir,
    fs=10,
    duration=300,
    epsilon=-0.05,
    f_distributions=((0.5, 0.7), (0.85, 1.1), (1.2, 1.5)),
    n_test=20,
    phi_range=(-0.6, 0.75),
    a_range=(-6e-5, 8e-5),
    seed=42,
):
    t = np.linspace(0, duration, int(fs * duration))
    rng = np.random.default_rng(seed)
    used = set()

    for f_range in f_distributions:
        # ensure directory exists: <base_dir>/<f_low_f_high>/test
        test_dir = os.path.join(base_dir, _range_tag(f_range), "test")
        os.makedirs(test_dir, exist_ok=True)

        # sample and generate
        test_params = sample_unique_param_sets(n_test, f_range, phi_range, a_range, used, rng)
        meta_rows = []
        for idx, (f, phi, a) in enumerate(test_params):
            signal = drift_modulated_harmonic(t, epsilon, f, phi, a)
            fpath = save_signal_csv(t, signal, epsilon, f, phi, a, idx, base_dir, f_range)
            append_metadata_row(meta_rows, fpath, epsilon, f, phi, a, fs, duration, seed, f_range[0], f_range[1])

        write_metadata_csv(meta_rows, base_dir, f_range)
        print(f"✓ Generated test set for f_range = {f_range} at {test_dir}")

def make_shifted_ranges(f_train=(0.85, 1.10), n_steps=2):
    f_low, f_high = f_train
    width = f_high - f_low
    ranges = []
    # backward steps
    for k in range(n_steps, 0, -1):
        ranges.append((round(f_low - k*width, 3), round(f_high - k*width, 3)))
    # training
    ranges.append((f_low, f_high))
    # forward steps
    for k in range(1, n_steps+1):
        ranges.append((round(f_low + k*width, 3), round(f_high + k*width, 3)))
    return ranges



# -------------------------- Run --------------------------
if __name__ == "__main__":
    base_dir = "/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic"
    generate_test_dist_shift(
    base_dir=base_dir,
    fs=10,
    duration=300,
    epsilon=-0.05,
    f_distributions=make_shifted_ranges((0.85, 1.10), n_steps=2),
    n_test=20
)