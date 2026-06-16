import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def _shade_states(ax, time, state, alpha=0.15):
    """
    Shade background regions on `ax` according to the binary `state` sequence.
    state == 0 -> one color, state == 1 -> another color.
    """
    if len(time) != len(state):
        raise ValueError("time and state must have same length")

    # Find contiguous segments of constant state
    current_state = state[0]
    start_t = time[0]

    for i in range(1, len(state)):
        if state[i] != current_state:
            end_t = time[i]
            color = "tab:blue" if current_state == 0 else "tab:orange"
            ax.axvspan(start_t, end_t, color=color, alpha=alpha, linewidth=0)
            current_state = state[i]
            start_t = time[i]

    # Last segment
    end_t = time[-1]
    color = "tab:blue" if current_state == 0 else "tab:orange"
    ax.axvspan(start_t, end_t, color=color, alpha=alpha, linewidth=0)


def visualize_two_state_pm_signals(
    base_dir,
    p,
    split="train",
    num_samples=3,
    max_rows=None,
    save_path=None,
):
    """
    Visualize two-state phase-modulated signals in a structured way.

    Assumes files are stored as:
        base_dir / f"p_{p:.5f}" / split / *.csv
    Each CSV has columns: Time, Value, State.

    Args:
        base_dir    : root folder for the two-state dataset.
        p           : transition probability (float).
        split       : "train", "val", or "test".
        num_samples : how many signals to plot from this split.
        max_rows    : if not None, truncate each signal to first max_rows samples.
        save_path   : if not None, path to save figure (PDF/PNG). If None, just show.
    """
    p_folder = f"p_{p:.5f}"
    split_dir = os.path.join(base_dir, p_folder, split)

    if not os.path.isdir(split_dir):
        raise FileNotFoundError(f"Split directory not found: {split_dir}")

    files = sorted([f for f in os.listdir(split_dir) if f.endswith(".csv")])
    if len(files) == 0:
        raise RuntimeError(f"No CSV files found in {split_dir}")

    files = files[:num_samples]

    # 2 rows per sample: [signal, state]
    nrows = num_samples * 2
    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=1,
        figsize=(12, 3 * num_samples),
        sharex=True,
        gridspec_kw={"hspace": 0.25},
    )

    # Ensure axes is indexable
    if nrows == 1:
        axes = [axes]

    for sample_idx, fname in enumerate(files):
        df = pd.read_csv(os.path.join(split_dir, fname))

        if max_rows is not None:
            df = df.iloc[:max_rows]

        time = df["Time"].values
        value = df["Value"].values
        state = df["State"].values.astype(int)

        ax_signal = axes[2 * sample_idx]
        ax_state = axes[2 * sample_idx + 1]

        # ---- Signal plot with shaded states ----
        ax_signal.plot(time, value, linewidth=1.2)
        _shade_states(ax_signal, time, state, alpha=0.15)

        # Clean title from filename (optional)
        ax_signal.set_title(
            f"Sample {sample_idx + 1}  |  p = {p:.5f}  |  file: {fname}",
            fontsize=12,
            fontweight="bold",
        )
        ax_signal.set_ylabel("Amplitude", fontsize=11, fontweight="bold")
        ax_signal.tick_params(axis="both", labelsize=9, width=1.2)
        for label in ax_signal.get_yticklabels():
            label.set_fontweight("bold")

        # Legend for states (just once)
        if sample_idx == 0:
            custom_lines = [
                plt.Line2D([0], [0], color="tab:blue", lw=6, alpha=0.4),
                plt.Line2D([0], [0], color="tab:orange", lw=6, alpha=0.4),
            ]
            ax_signal.legend(
                custom_lines,
                ["State 0", "State 1"],
                loc="upper right",
                fontsize=9,
            )

        # ---- State plot as step function ----
        ax_state.step(time, state, where="post", linewidth=1.0)
        ax_state.set_yticks([0, 1])
        ax_state.set_yticklabels(["0", "1"])
        ax_state.set_ylabel("State", fontsize=11, fontweight="bold")
        ax_state.tick_params(axis="both", labelsize=9, width=1.2)
        for label in ax_state.get_yticklabels():
            label.set_fontweight("bold")

        if sample_idx == num_samples - 1:
            ax_state.set_xlabel("Time (s)", fontsize=11, fontweight="bold")
        else:
            # Hide x-axis label for intermediate rows
            ax_state.set_xlabel("")

    # Make x tick labels bold on the bottom axis
    for label in axes[-1].get_xticklabels():
        label.set_fontweight("bold")

    fig.suptitle(
        f"Two-State Phase-Modulated Signals  |  split = {split}  |  p = {p:.5f}",
        fontsize=14,
        fontweight="bold",
    )

    plt.tight_layout(rect=[0, 0.02, 1, 0.96])

    if save_path is not None:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300)
        plt.close(fig)
    else:
        plt.show()


# ---------------- Example usage ----------------
if __name__ == "__main__":
    base_dir = (
        "/scratch_nvme/Time_Series/Bio-Synthesize/"
        "Generation_Synthesized_Bio_Signals/PhaseMod_Single_Freq_TwoState_Modulation_Change"
    )
    p=1.0
    # Example: visualize 4 train samples for p = 0.1, first 2000 points
    visualize_two_state_pm_signals(
        base_dir=base_dir,
        p=p,
        split="train",
        num_samples=4,
        max_rows=300,
        save_path=(
            f"/scratch_nvme/Time_Series/Bio-Synthesize/"
            "Visualization_Scripts/PhaseMod_TwoState_Carrier_Freqeuncy_Change_Modulation_Change_p_1.0_train.png"
        ),
    )
