import os
import pandas as pd
import matplotlib.pyplot as plt
import re

def extract_phase_mod_params(filename):
    """Extract A, f, beta, and f_mod from the filename."""
    base = os.path.splitext(filename)[0]
    match = re.search(
        r'A_([0-9.-]+)-([0-9.-]+)-([0-9.-]+)_f_([0-9.]+)-([0-9.]+)-([0-9.]+)_b_([0-9.]+)-([0-9.]+)-([0-9.]+)_fm_([0-9.]+)-([0-9.]+)-([0-9.]+)', base)
    if match:
        A = list(map(float, match.group(1, 2, 3)))
        f_i = list(map(float, match.group(4, 5, 6)))
        beta = list(map(float, match.group(7, 8, 9)))
        f_mod = list(map(float, match.group(10, 11, 12)))
        return A, f_i, beta, f_mod
    return None, None, None, None

def visualize_phase_mod_signals(base_dir, num_samples=5):
    splits = ['train', 'val', 'test']
    fig, axes = plt.subplots(len(splits), num_samples, figsize=(4 * num_samples, 3 * len(splits)), sharex=True)

    for row_idx, split in enumerate(splits):
        split_dir = os.path.join(base_dir, split)
        files = sorted(os.listdir(split_dir))[:num_samples]

        for col_idx, file in enumerate(files):
            df = pd.read_csv(os.path.join(split_dir, file))
            A, f_i, beta, f_mod = extract_phase_mod_params(file)
            ax = axes[row_idx, col_idx] if num_samples > 1 else axes[row_idx]

            ax.plot(df["Time"], df["Value"])
            ax.set_title(f"{split.capitalize()} Sample {col_idx+1}\nA={A}, f={f_i}, β={beta}, fₘ={f_mod}", fontsize=8)
            ax.set_xlabel("Time")
            ax.set_ylabel("Value")
            ax.grid(True)

    plt.tight_layout()
    plt.show()

# Example usage:
visualize_phase_mod_signals('/scratch_nvme/Time_Series/Bio-Synthesize/Generated_Datasets/Phase_Mod_Multi_Sine/Modulation', num_samples=5)
