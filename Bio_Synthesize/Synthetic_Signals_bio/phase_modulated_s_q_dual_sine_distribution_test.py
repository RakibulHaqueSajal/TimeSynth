#!/usr/bin/env python3
import numpy as np
import pandas as pd
import os
import hashlib
import itertools
import matplotlib.pyplot as plt

# ==============================#
#        Signal Definition      #
# ==============================#
def generate_twofreq_phase_modulated_signal(t, A0, f0, beta0, fmod0, A1, f1, beta1, fmod1, offset):
    s1 = A0 * np.sin(2 * np.pi * f0 * t + beta0 * np.sin(2 * np.pi * fmod0 * t))
    s2 = A1 * np.sin(2 * np.pi * f1 * t + beta1 * np.sin(2 * np.pi * fmod1 * t))
    return s1 + s2 + offset


# ==============================#
#          Hash helpers         #
# ==============================#
def param_hash_2f(A0, f0, beta0, fmod0, A1, f1, beta1, fmod1, offset, precision=6):
    key = "_".join([f"{x:.{precision}f}" for x in (A0, f0, beta0, fmod0, A1, f1, beta1, fmod1, offset)])
    return hashlib.md5(key.encode()).hexdigest()


# ==============================#
#       Bucket tag helpers      #
# ==============================#
def _range_tag(fr, label="f"):
    return f"{label}_{fr[0]:.2f}_{fr[1]:.2f}"

def _combo_tag(f0_range, f1_range):
    return f"{_range_tag(f0_range,'f0')}__{_range_tag(f1_range,'f1')}"


# ==============================#
#       Unique param sampler    #
# ==============================#
def sample_unique_param_sets_2f(
    n, bounds, existing_hashes, rng,
    f0_override_range=None, f1_override_range=None
):
    """
    If f0_override_range / f1_override_range are provided, those replace bounds['f_0']/['f_1'].
    """
    params = []
    while len(params) < n:
        A0   = rng.uniform(*bounds["A_0"])
        A1   = rng.uniform(*bounds["A_1"])
        f0   = rng.uniform(*(f0_override_range if f0_override_range else bounds["f_0"]))
        f1   = rng.uniform(*(f1_override_range if f1_override_range else bounds["f_1"]))
        b0   = rng.uniform(*bounds["beta_0"])
        b1   = rng.uniform(*bounds["beta_1"])
        fm0  = rng.uniform(*bounds["fmod_0"])
        fm1  = rng.uniform(*bounds["fmod_1"])
        offs = rng.uniform(*bounds["offset"])

        h = param_hash_2f(A0, f0, b0, fm0, A1, f1, b1, fm1, offs)
        if h not in existing_hashes:
            existing_hashes.add(h)
            params.append((A0, f0, b0, fm0, A1, f1, b1, fm1, offs))
    return params


# ==============================#
#         IO / Metadata         #
# ==============================#
def save_2f_signal_csv(t, sig, params, idx, base_dir, f0_range, f1_range):
    """
    Save under: <base_dir>/<f0_tag>__<f1_tag>/test/test_XXX_...csv
    """
    combo = _combo_tag(f0_range, f1_range)
    out_dir = os.path.join(base_dir, combo, "test")
    os.makedirs(out_dir, exist_ok=True)

    A0, f0, b0, fm0, A1, f1, b1, fm1, offset = params
    filename = (
        f"test_{idx:03d}"
        f"_A0_{A0:.4f}_f0_{f0:.4f}_beta0_{b0:.4f}_fmod0_{fm0:.4f}"
        f"_A1_{A1:.4f}_f1_{f1:.4f}_beta1_{b1:.4f}_fmod1_{fm1:.4f}"
        f"_offset_{offset:.4f}.csv"
    )
    fpath = os.path.join(out_dir, filename)
    pd.DataFrame({"Time": t, "Value": sig}).to_csv(fpath, index=False)
    return fpath


def append_metadata_row(meta_rows, filepath, params, fs, duration, seed, f0_range, f1_range):
    A0, f0, b0, fm0, A1, f1, b1, fm1, offset = params
    meta_rows.append({
        "filepath": filepath,
        "A0": A0, "f0": f0, "beta0": b0, "fmod0": fm0,
        "A1": A1, "f1": f1, "beta1": b1, "fmod1": fm1,
        "offset": offset,
        "fs": fs, "duration": duration, "seed": seed,
        "f0_low": f0_range[0], "f0_high": f0_range[1],
        "f1_low": f1_range[0], "f1_high": f1_range[1],
        "bucket_tag": _combo_tag(f0_range, f1_range),
    })


def write_metadata_csv(meta_rows, base_dir, f0_range, f1_range):
    combo = _combo_tag(f0_range, f1_range)
    out_dir = os.path.join(base_dir, combo, "test")
    os.makedirs(out_dir, exist_ok=True)
    meta_path = os.path.join(out_dir, "metadata_test.csv")
    pd.DataFrame(meta_rows).to_csv(meta_path, index=False)


# ==============================#
#     Frequency bucket maker    #
# ==============================#
def make_shifted_ranges(train_f=(0.68, 1.41), n_below=2, n_above=2, digits=2):
    """
    Splits [0, f_low) into n_below equal buckets, includes the train bucket,
    then steps above by train-width n_above times. Values rounded to 'digits'.
    """
    f_low, f_high = train_f
    width = f_high - f_low

    buckets = []
    # below
    span_below = max(f_low, 0.0)
    step_below = span_below / max(n_below, 1)
    start = 0.0
    for _ in range(n_below):
        buckets.append((round(start, digits), round(start + step_below, digits)))
        start += step_below

    # train
    buckets.append((round(f_low, digits), round(f_high, digits)))

    # above
    lo, hi = f_low, f_high
    for _ in range(n_above):
        lo += width
        hi += width
        buckets.append((round(lo, digits), round(hi, digits)))

    return buckets


# ==============================#
#          Generators           #
# ==============================#

def generate_twofreq_clean_ood(
    base_dir,
    bounds,
    f0_distributions,     # list of (low, high)
    f1_distributions,     # list of (low, high)
    n_test=20,
    fs=10,
    duration=300,
    seed=42,
    mode="grid",          # "grid" | "f0_only" | "f1_only" | "lockstep"
    train_f0=None,        # needed for f1_only
    train_f1=None,        # needed for f0_only
):
    """
    mode:
      - "grid":     iterate over all (f0_range, f1_range) pairs (Cartesian product).
      - "f0_only":  vary f0 over f0_distributions, keep f1 in 'train_f1'.
      - "f1_only":  vary f1 over f1_distributions, keep f0 in 'train_f0'.
      - "lockstep": pair f0_distributions[i] with f1_distributions[i] (same index shift).
    """
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    rng = np.random.default_rng(seed)
    used_hashes = set()

    if mode == "grid":
        pairs = list(itertools.product(f0_distributions, f1_distributions))
    elif mode == "f0_only":
        assert train_f1 is not None, "Provide train_f1=(low, high) for mode='f0_only'."
        pairs = [(f0r, train_f1) for f0r in f0_distributions]
    elif mode == "f1_only":
        assert train_f0 is not None, "Provide train_f0=(low, high) for mode='f1_only'."
        pairs = [(train_f0, f1r) for f1r in f1_distributions]
    elif mode == "lockstep":
        assert len(f0_distributions) == len(f1_distributions), \
            "For lockstep, f0_distributions and f1_distributions must be the same length."
        pairs = list(zip(f0_distributions, f1_distributions))
    else:
        raise ValueError("mode must be one of {'grid','f0_only','f1_only','lockstep'}")

    for (f0_range, f1_range) in pairs:
        params_list = sample_unique_param_sets_2f(
            n=n_test,
            bounds=bounds,
            existing_hashes=used_hashes,
            rng=rng,
            f0_override_range=f0_range,
            f1_override_range=f1_range,
        )
        meta_rows = []
        for idx, params in enumerate(params_list):
            sig = generate_twofreq_phase_modulated_signal(t, *params)
            fpath = save_2f_signal_csv(t, sig, params, idx, base_dir, f0_range, f1_range)
            append_metadata_row(meta_rows, fpath, params, fs, duration, seed, f0_range, f1_range)

        write_metadata_csv(meta_rows, base_dir, f0_range, f1_range)
        print(f"✓ Generated CLEAN test set for {_combo_tag(f0_range, f1_range)}")


# ==============================#
#     Visualization (optional)  #
# ==============================#
def visualize_bucket_pairs(base_dir, plot_dir, pairs, num_samples=3, max_timesteps=300, random_pick=False):
    for (f0_range, f1_range) in pairs:
        combo = _combo_tag(f0_range, f1_range)
        split_dir = os.path.join(base_dir, combo, "test")
        if not os.path.isdir(split_dir):
            print(f"(!) Missing: {split_dir}")
            continue

        files = sorted([f for f in os.listdir(split_dir) if f.endswith(".csv") and f.startswith("test_")])
        if not files:
            print(f"(!) No CSVs in {split_dir}")
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
            ax.grid(True)
        axes[0].set_ylabel("Value")
        plt.suptitle(f"Bucket {_combo_tag(f0_range, f1_range)} – CLEAN test samples", fontsize=13)
        plt.tight_layout(rect=[0, 0, 1, 0.94])
        plt.show()
        #plt.savefig(os.path.join(plot_dir,file.replace(".csv", "")))


# ==============================#
#              Main             #
# ==============================#
if __name__ == "__main__":
    # Parameter bounds (same as your dual-sine code)
    param_bounds = {
        "A_0": (0.1, 0.1227),
        "A_1": (0.1, 0.1227),
        "f_0": (0.6782, 1.4112),
        "f_1": (0.6782, 1.4112),
        "beta_0": (0.01, 0.3),
        "beta_1": (0.01, 0.3),
        "fmod_0": (0.01, 0.1),
        "fmod_1": (0.01, 0.1),
        "offset": (0.1937, 0.7418),
    }

    # Training ranges (used for building OOD buckets and for the fixed side in one-sided shifts)
    train_f0 = (0.6782, 1.4112)
    train_f1 = (0.6782, 1.4112)

    # Build OOD buckets for both carriers (2 below slices, train, 2 above steps) with two decimals
    f0_buckets = make_shifted_ranges(train_f=train_f0, n_below=2, n_above=2, digits=2)
    f1_buckets = make_shifted_ranges(train_f=train_f1, n_below=2, n_above=2, digits=2)

    print("f0 buckets:", f0_buckets)
    print("f1 buckets:", f1_buckets)

    base_dir = "/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq"
    plot_dir="/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/plots"

    # ========== Option A: Grid over both f0 and f1 ==========
    # generate_twofreq_clean_ood(
    #     base_dir=base_dir,
    #     bounds=param_bounds,
    #     f0_distributions=f0_buckets,
    #     f1_distributions=f1_buckets,
    #     n_test=20,
    #     fs=10,
    #     duration=300,
    #     seed=42,
    #     mode="grid",
    # )

    # # ========== Option B: Shift f0 only, keep f1 in-train ==========
    # generate_twofreq_clean_ood(
    #     base_dir=base_dir,
    #     bounds=param_bounds,
    #     f0_distributions=f0_buckets,
    #     f1_distributions=[],          # unused
    #     n_test=20,
    #     fs=10,
    #     duration=300,
    #     seed=42,
    #     mode="f0_only",
    #     train_f1=train_f1,
    # )

    # # ========== Option C: Shift f1 only, keep f0 in-train ==========
    # generate_twofreq_clean_ood(
    #     base_dir=base_dir,
    #     bounds=param_bounds,
    #     f0_distributions=[],          # unused
    #     f1_distributions=f1_buckets,
    #     n_test=20,
    #     fs=10,
    #     duration=300,
    #     seed=42,
    #     mode="f1_only",
    #     train_f0=train_f0,
    # )
    # ========== Option D: Shift f0 and f1 by the SAME bucket index (lockstep) ==========
    generate_twofreq_clean_ood(
        base_dir=base_dir,
        bounds=param_bounds,
        f0_distributions=f0_buckets,
        f1_distributions=f1_buckets,
        n_test=20,
        fs=10,
        duration=300,
        seed=42,
        mode="lockstep",
    )


    # Visualize a handful per a few bucket pairs (example: first 3 pairs)
    demo_pairs = list(itertools.product(f0_buckets[:3], f1_buckets[:3]))
    visualize_bucket_pairs(base_dir,plot_dir,demo_pairs, num_samples=3, max_timesteps=300, random_pick=False)
