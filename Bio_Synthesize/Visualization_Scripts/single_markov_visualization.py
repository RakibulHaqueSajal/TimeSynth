#!/usr/bin/env python3
import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def _list_csv(root_dir, split):
    split_dir = os.path.join(root_dir, split)
    files = sorted(glob.glob(os.path.join(split_dir, "*.csv")))
    if not files:
        raise FileNotFoundError(f"No CSV files found in {split_dir}")
    return files


def _pick_n(files, n=4, seed=0):
    if n >= len(files):
        return files
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(files), size=n, replace=False)
    return [files[i] for i in sorted(idx)]


def _load_transition_map(root_dir, split):
    """
    Reads: <root_dir>/<split>_transitions.csv
    Expected columns:
      - filename
      - t_star_idx (optional)
      - t_star_time_sec (optional)
    Returns dict: filename -> (t_star_idx or None, t_star_time_sec or None)
    """
    meta_path = os.path.join(root_dir, f"{split}_transitions.csv")
    if not os.path.exists(meta_path):
        return {}

    meta = pd.read_csv(meta_path)
    out = {}
    for _, row in meta.iterrows():
        fname = str(row["filename"])
        t_idx = int(row["t_star_idx"]) if "t_star_idx" in meta.columns and not pd.isna(row.get("t_star_idx", np.nan)) else None
        t_sec = float(row["t_star_time_sec"]) if "t_star_time_sec" in meta.columns and not pd.isna(row.get("t_star_time_sec", np.nan)) else None
        out[fname] = (t_idx, t_sec)
    return out


def _shade_by_state(ax, t, s):
    # Shade contiguous state segments (keeps your “like this” look).
    changes = np.where(np.diff(s) != 0)[0] + 1
    starts = np.concatenate(([0], changes))
    ends = np.concatenate((changes, [len(s)]))
    for a, b in zip(starts, ends):
        ax.axvspan(t[a], t[b - 1], alpha=0.12)


def visualize_like_example_for_split(
    root_dir,
    split="train",
    n_samples=4,
    seed=0,
    max_seconds=30,      # matches your screenshot
    save_dir=None,       # if None: saves into root_dir/visualizations/
):
    """
    Creates a figure like your screenshot:
      For each sample:
        - top axis: signal
        - bottom axis: state (0/1)
      Repeats vertically for n_samples
    """
    files = _pick_n(_list_csv(root_dir, split), n=n_samples, seed=seed)
    trans_map = _load_transition_map(root_dir, split)

    # layout: 2 rows per sample
    fig, axes = plt.subplots(
        nrows=2 * len(files),
        ncols=1,
        figsize=(12, 2.6 * len(files)),
        sharex=True
    )
    if len(files) == 1:
        axes = np.array([axes]).reshape(2, 1)
    else:
        axes = np.array(axes).reshape(2 * len(files), 1)

    fig.suptitle(f"Two-State Phase-Modulated Signals  |  split = {split}", fontsize=18, fontweight="bold", y=0.995)

    for i, fpath in enumerate(files):
        df = pd.read_csv(fpath)

        # Optional time window (0..max_seconds)
        if max_seconds is not None and "Time" in df.columns:
            df = df[df["Time"] <= max_seconds].copy()

        t = df["Time"].to_numpy()
        y = df["Value"].to_numpy()
        has_state = "State" in df.columns
        s = df["State"].to_numpy().astype(int) if has_state else None

        ax_sig = axes[2 * i, 0]
        ax_state = axes[2 * i + 1, 0]

        # Light background shading by state (like your example)
        if has_state:
            _shade_by_state(ax_sig, t, s)

        ax_sig.plot(t, y, linewidth=1.6)
        ax_sig.set_ylabel("Amplitude", fontsize=12, fontweight="bold")
        ax_sig.tick_params(axis="y", labelsize=10, width=1.2)
        for lab in ax_sig.get_yticklabels():
            lab.set_fontweight("bold")

        # Title line per sample with filename (like your example)
        fname = os.path.basename(fpath)
        ax_sig.set_title(f"Sample {i+1}  |  file: {fname}", fontsize=11, fontweight="bold", loc="left")

        # State subplot
        if has_state:
            ax_state.step(t, s, where="post", linewidth=1.6)
            ax_state.set_ylim(-0.1, 1.1)
        else:
            ax_state.text(0.02, 0.5, "No 'State' column found", transform=ax_state.transAxes,
                          fontsize=11, fontweight="bold", va="center")
            ax_state.set_ylim(0, 1)

        ax_state.set_ylabel("State", fontsize=12, fontweight="bold")
        ax_state.tick_params(axis="y", labelsize=10, width=1.2)
        ax_state.set_yticks([0, 1])
        for lab in ax_state.get_yticklabels():
            lab.set_fontweight("bold")

        # Optional: transition marker if metadata exists
        if fname in trans_map:
            t_idx, t_sec = trans_map[fname]
            t_star = None
            if t_sec is not None:
                t_star = t_sec
            elif t_idx is not None and t_idx < len(t):
                t_star = float(t[t_idx])
            if t_star is not None:
                ax_sig.axvline(t_star, linestyle="--", linewidth=1.4)
                ax_state.axvline(t_star, linestyle="--", linewidth=1.4)

        # Clean look like your screenshot
        ax_sig.grid(False)
        ax_state.grid(False)

    axes[-1, 0].set_xlabel("Time (s)", fontsize=12, fontweight="bold")
    axes[-1, 0].tick_params(axis="x", labelsize=10, width=1.2)
    for lab in axes[-1, 0].get_xticklabels():
        lab.set_fontweight("bold")

    plt.tight_layout(rect=[0, 0, 1, 0.97])

    if save_dir is None:
        save_dir = os.path.join(root_dir, "visualizations")
    os.makedirs(save_dir, exist_ok=True)

    out_path = os.path.join(save_dir, f"{split}_signals_like_example.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out_path}")


def visualize_all_splits_like_example(
    root_dir,
    splits=("train", "val", "test"),
    n_samples=4,
    seed=0,
    max_seconds=30,
):
    for sp in splits:
        visualize_like_example_for_split(
            root_dir=root_dir,
            split=sp,
            n_samples=n_samples,
            seed=seed,
            max_seconds=max_seconds,
        )


if __name__ == "__main__":
    root_dir = (
        "/scratch_nvme/Time_Series/Bio-Synthesize/"
        "Generation_Synthesized_Bio_Signals/PhaseMod_OneState_Change"
    )
    visualize_all_splits_like_example(
        root_dir=root_dir,
        splits=("train", "val", "test"),
        n_samples=4,
        seed=1,
        max_seconds=30,
    )
