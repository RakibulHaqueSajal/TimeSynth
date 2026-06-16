#!/usr/bin/env python3
import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------- IO helpers ----------------------------
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


def _infer_fs_from_time(t):
    if len(t) < 2:
        return None
    dt = float(np.median(np.diff(t)))
    if dt <= 0:
        return None
    return 1.0 / dt


# ---------------------------- metadata loader ----------------------------
def _load_meta_map(root_dir, split):
    """
    Looks for metadata in common locations:
      - <root>/<split>_transitions.csv  (your new generator)
      - <root>/<split>_transitions_twoflip.csv
      - <root>/<split>_transitions_two_cp.csv

    Returns:
      meta_map[fname] = dict (row)
      meta_path
    """
    candidates = [
        os.path.join(root_dir, f"{split}_transitions.csv"),
        os.path.join(root_dir, f"{split}_transitions_twoflip.csv"),
        os.path.join(root_dir, f"{split}_transitions_two_cp.csv"),
    ]
    meta_path = next((p for p in candidates if os.path.exists(p)), None)
    if meta_path is None:
        return {}, None

    meta = pd.read_csv(meta_path)

    out = {}
    for _, row in meta.iterrows():
        fname = str(row["filename"])
        out[fname] = row.to_dict()
    return out, meta_path


# ---------------------------- transition inference fallback ----------------------------
def _infer_t1_t2_from_state(df):
    """
    Fallback if metadata missing:
      infer t1/t2 (seconds) from state changes.
    Works if State exists and has exactly two changes.
    """
    if "State" not in df.columns or "Time" not in df.columns:
        return None, None
    s = df["State"].to_numpy().astype(int)
    t = df["Time"].to_numpy()
    ch = np.where(np.diff(s) != 0)[0] + 1
    if len(ch) >= 1:
        t1 = float(t[ch[0]])
    else:
        t1 = None
    if len(ch) >= 2:
        t2 = float(t[ch[1]])
    else:
        t2 = None
    return t1, t2


def _get_transition_times(df, meta_row):
    """
    Prefer seconds from metadata if available,
    otherwise idx->time lookup, otherwise infer from State.
    """
    if meta_row is None:
        return _infer_t1_t2_from_state(df)

    t = df["Time"].to_numpy() if "Time" in df.columns else None

    def _get(col, default=None):
        v = meta_row.get(col, default)
        if v is None:
            return default
        if isinstance(v, float) and np.isnan(v):
            return default
        return v

    # new format (preferred)
    t1_sec = _get("t1_time_sec", None)
    t2_sec = _get("t2_time_sec", None)
    if t1_sec is not None or t2_sec is not None:
        return (float(t1_sec) if t1_sec is not None else None,
                float(t2_sec) if t2_sec is not None else None)

    # idx fallback
    t1_idx = _get("t1_idx", None)
    t2_idx = _get("t2_idx", None)

    t1 = None
    t2 = None
    if t is not None:
        if t1_idx is not None and 0 <= int(t1_idx) < len(t):
            t1 = float(t[int(t1_idx)])
        if t2_idx is not None and 0 <= int(t2_idx) < len(t):
            t2 = float(t[int(t2_idx)])

    if t1 is None and t2 is None:
        return _infer_t1_t2_from_state(df)
    return t1, t2


# ---------------------------- plotting helpers ----------------------------
def _shade_by_state(ax, t, s):
    # Shade contiguous state segments.
    if s is None or len(s) == 0:
        return
    changes = np.where(np.diff(s) != 0)[0] + 1
    starts = np.concatenate(([0], changes))
    ends = np.concatenate((changes, [len(s)]))
    for a, b in zip(starts, ends):
        ax.axvspan(t[a], t[b - 1], alpha=0.12)


def _draw_history_boundary(ax, t, H, fs, shade_history=True):
    """
    Draws forecast boundary at index H (history length).
    Optionally shades [0, H) region.
    """
    if fs is None or H is None:
        return
    if len(t) == 0:
        return
    # boundary time at t[H] if possible; else approximate by t[0] + H/fs
    if 0 <= H < len(t):
        tb = float(t[H])
    else:
        tb = float(t[0]) + (H / fs)

    if shade_history:
        ax.axvspan(float(t[0]), tb, alpha=0.06)
    ax.axvline(tb, linestyle=":", linewidth=1.3)


# ---------------------------- main visualization ----------------------------
def visualize_two_transition_dataset(
    root_dir,
    split="test",
    n_samples=4,
    seed=0,
    max_seconds=None,
    save_dir=None,
    history_len=50,
    future_len=100,
    shade_by_state=True,
    show_history_boundary=True,
):
    """
    2 rows per sample (signal + state), with:
      - motif + dwell shown in title if available
      - vertical lines at t1,t2
      - optional history/future boundary at H
    """
    files = _pick_n(_list_csv(root_dir, split), n=n_samples, seed=seed)
    meta_map, meta_path = _load_meta_map(root_dir, split)

    fig, axes = plt.subplots(
        nrows=2 * len(files),
        ncols=1,
        figsize=(12, 2.8 * len(files)),
        sharex=True
    )
    if len(files) == 1:
        axes = np.array([axes]).reshape(2, 1)
    else:
        axes = np.array(axes).reshape(2 * len(files), 1)

    title_extra = f" | meta: {os.path.basename(meta_path)}" if meta_path else " | meta: (none)"
    fig.suptitle(
        f"Two-Transition Two-State PM Signals | split={split}{title_extra}",
        fontsize=18, fontweight="bold", y=0.995
    )

    for i, fpath in enumerate(files):
        df = pd.read_csv(fpath)

        # Optional time window
        if max_seconds is not None and "Time" in df.columns:
            df = df[df["Time"] <= max_seconds].copy()

        t = df["Time"].to_numpy()
        y = df["Value"].to_numpy()
        s = df["State"].to_numpy().astype(int) if "State" in df.columns else None
        fs = _infer_fs_from_time(t)

        ax_sig = axes[2 * i, 0]
        ax_state = axes[2 * i + 1, 0]

        fname = os.path.basename(fpath)
        meta_row = meta_map.get(fname, None)

        motif = meta_row.get("motif", None) if meta_row else None
        dwell = meta_row.get("dwell_idx", None) if meta_row else None
        t1, t2 = _get_transition_times(df, meta_row if meta_row else {})

        # background shading by state
        if shade_by_state and s is not None:
            _shade_by_state(ax_sig, t, s)

        # history boundary
        if show_history_boundary and fs is not None:
            _draw_history_boundary(ax_sig, t, history_len, fs, shade_history=True)
            _draw_history_boundary(ax_state, t, history_len, fs, shade_history=False)

        # signal plot
        ax_sig.plot(t, y, linewidth=1.6)
        ax_sig.set_ylabel("Amplitude", fontsize=12, fontweight="bold")
        ax_sig.tick_params(axis="y", labelsize=10, width=1.2)
        for lab in ax_sig.get_yticklabels():
            lab.set_fontweight("bold")

        # title
        extra = []
        if motif is not None:
            extra.append(f"motif={motif}")
        if dwell is not None and not (isinstance(dwell, float) and np.isnan(dwell)):
            extra.append(f"dwell={int(dwell)}")
        extra_str = (" | " + ", ".join(extra)) if extra else ""
        ax_sig.set_title(f"Sample {i+1} | file: {fname}{extra_str}",
                         fontsize=11, fontweight="bold", loc="left")

        # transition lines
        if t1 is not None:
            ax_sig.axvline(t1, linestyle="--", linewidth=1.4)
            ax_state.axvline(t1, linestyle="--", linewidth=1.4)
        if t2 is not None:
            ax_sig.axvline(t2, linestyle="--", linewidth=1.4)
            ax_state.axvline(t2, linestyle="--", linewidth=1.4)

        # state plot
        if s is not None:
            ax_state.step(t, s, where="post", linewidth=1.6)
            uniq = sorted(np.unique(s).tolist())
            ax_state.set_yticks(uniq)
            ymin = min(uniq) - 0.2
            ymax = max(uniq) + 0.2
            ax_state.set_ylim(ymin, ymax)
        else:
            ax_state.text(0.02, 0.5, "No 'State' column found", transform=ax_state.transAxes,
                          fontsize=11, fontweight="bold", va="center")
            ax_state.set_ylim(0, 1)

        ax_state.set_ylabel("State", fontsize=12, fontweight="bold")
        ax_state.tick_params(axis="y", labelsize=10, width=1.2)
        for lab in ax_state.get_yticklabels():
            lab.set_fontweight("bold")

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

    out_path = os.path.join(save_dir, f"{split}_signals_two_transition_like_example.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out_path}")


def visualize_all_splits(
    root_dir,
    splits=("train", "val", "test"),
    n_samples=4,
    seed=0,
    max_seconds=None,
    history_len=50,
    future_len=100,
    shade_by_state=True,
    show_history_boundary=True,
):
    for sp in splits:
        visualize_two_transition_dataset(
            root_dir=root_dir,
            split=sp,
            n_samples=n_samples,
            seed=seed,
            max_seconds=max_seconds,
            history_len=history_len,
            future_len=future_len,
            shade_by_state=shade_by_state,
            show_history_boundary=show_history_boundary,
        )


if __name__ == "__main__":
    root_dir = (
        "/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/PhaseMod_TwoTransition_Mixed"
    )

    visualize_all_splits(
        root_dir=root_dir,
        splits=("train", "val", "test"),
        n_samples=4,
        seed=1,
        max_seconds=30,
        history_len=50,
        future_len=100,
        shade_by_state=True,
        show_history_boundary=True,
    )
