import numpy as np
import pandas as pd
import os
import hashlib
import matplotlib.pyplot as plt
import os
import pandas as pd
import matplotlib.pyplot as plt

# ------------------ Signal Definition (Single-State) ------------------
def generate_phase_modulated_signal(t, A, f, beta, fmod, offset):
    """
    Single-state phase-modulated signal:
    x(t) = A * sin(2π f t + β sin(2π f_mod t)) + offset
    """
    return A * np.sin(2 * np.pi * f * t + beta * np.sin(2 * np.pi * fmod * t)) + offset

# ------------------ Unique Hash for Parameters (Single-State) ------------------
def param_hash_pm(A, f, beta, fmod, offset, precision=6):
    key = f"{A:.{precision}f}_{f:.{precision}f}_{beta:.{precision}f}_{fmod:.{precision}f}_{offset:.{precision}f}"
    return hashlib.md5(key.encode()).hexdigest()

# ------------------ Unique Parameter Sampler (Single-State) ------------------
def sample_unique_pm_param_sets(n, bounds, existing_hashes):
    params = []
    while len(params) < n:
        A = np.random.uniform(*bounds["A"])
        f = np.random.uniform(*bounds["f"])
        beta = np.random.uniform(*bounds["beta"])
        fmod = np.random.uniform(*bounds["fmod"])
        offset = np.random.uniform(*bounds["offset"])
        h = param_hash_pm(A, f, beta, fmod, offset)
        if h not in existing_hashes:
            existing_hashes.add(h)
            params.append((A, f, beta, fmod, offset))
    return params

# ------------------ Save to CSV (Single-State) ------------------
def save_pm_signal(t, signal, A, f, beta, fmod, offset, idx, mode, base_dir):
    split_dir = os.path.join(base_dir, mode)
    os.makedirs(split_dir, exist_ok=True)
    filename = (
        f"{mode}_{idx:03d}_A_{A:.4f}_f_{f:.4f}_beta_{beta:.4f}_"
        f"fmod_{fmod:.4f}_offset_{offset:.4f}.csv"
    )
    df = pd.DataFrame({"Time": t, "Value": signal})
    df.to_csv(os.path.join(split_dir, filename), index=False)

# ------------------ Dataset Generator (Single-State) ------------------
def generate_pm_signals(base_dir, bounds, n_train=70, n_val=10, n_test=20, fs=10, duration=300):
    t = np.linspace(0, duration, int(fs * duration))
    used_hashes = set()
    splits = {"train": n_train, "val": n_val, "test": n_test}

    for mode, count in splits.items():
        param_list = sample_unique_pm_param_sets(count, bounds, used_hashes)
        for idx, (A, f, beta, fmod, offset) in enumerate(param_list):
            signal = generate_phase_modulated_signal(t, A, f, beta, fmod, offset)
            save_pm_signal(t, signal, A, f, beta, fmod, offset, idx, mode, base_dir)
        print(f"[single-state] Saved {count} samples to {mode}/ in {base_dir}")

# ======================================================
#  TWO-STATE MARKOV SWITCHING VERSION (FREQUENCY ONLY)
#  + SMALL β SHIFT IN STATE 1
# ======================================================

# ----- 2-state Markov chain -----
def simulate_two_state_chain(T, p, start_state=0):
    """
    Symmetric 2-state Markov chain:
        P(switch) = p, P(stay) = 1 - p
    """
    states = np.zeros(T, dtype=int)
    states[0] = start_state
    for t in range(1, T):
        if np.random.rand() < p:
            states[t] = 1 - states[t-1]
        else:
            states[t] = states[t-1]
    return states

# ----- Better-separated frequency bands -----
def make_well_separated_freq_ranges(global_f_range):
    """
    Given (f_low, f_high), create two distinct bands for state 0 and state 1.
    Keeps realism but enhances visual + statistical separability.
    """
    f_low, f_high = global_f_range
    span = f_high - f_low

    # State 0: lower band
    f0_range = (f_low + 0.05 * span,
                f_low + 0.25 * span)

    # State 1: higher band
    f1_range = (f_low + 0.55 * span,
                f_low + 0.75 * span)
  
    return f0_range, f1_range

# ----- Hash for 2-state parameters -----
def param_hash_pm_two_state(A, f0, f1, beta, fmod, offset, p, precision=6):
    key = (
        f"{A:.{precision}f}_"
        f"{f0:.{precision}f}_"
        f"{f1:.{precision}f}_"
        f"{beta:.{precision}f}_"
        f"{fmod:.{precision}f}_"
        f"{offset:.{precision}f}_"
        f"{p:.{precision}e}"
    )
    return hashlib.md5(key.encode()).hexdigest()

# ----- Two-state phase-modulated signal -----
def generate_two_state_pm_signal(
    T,
    fs,
    A,
    f0,
    f1,
    beta,
    fmod,
    offset,
    p,
    start_state=0,
):
    """
    Phase-modulated signal with carrier frequency switching between two states.

    States:
        S_t in {0,1}, symmetric Markov chain with P(switch) = p.

    Carrier phase is updated recursively for continuity:
        θ_{k+1} = θ_k + 2π f_{S_k} Δt

    Modulation is applied as a state-dependent phase term:
        beta_0 = beta
        beta_1 = beta + Δβ   (small positive offset)
        x_k = A * sin(θ_k + β_t sin(2π f_mod t_k)) + offset
    """
    dt = 1.0 / fs
    t = np.arange(T) * dt

    # Hidden state sequence
    states = simulate_two_state_chain(T, p, start_state=start_state)

    # State-dependent carrier frequency
    f_t = np.where(states == 0, f0, f1)

    # Carrier phase recursion
    phase = np.zeros(T, dtype=float)
    phase[0] = 0.0
    for k in range(1, T):
        phase[k] = phase[k-1] + 2 * np.pi * f_t[k-1] * dt

    # Small β offset for state 1 (keeps realism, increases separability)
    delta_beta = np.random.uniform(0.02, 0.04)
    beta0 = beta
    beta1 = beta + delta_beta
    beta_t = np.where(states == 0, beta0, beta1)

    # Phase modulation term (state-dependent β)
    phase_mod = beta_t * np.sin(2 * np.pi * fmod * t)

    # Final signal
    signal = A * np.sin(phase + phase_mod) + offset

    return t, signal, states

# ----- Save 2-state PM signal -----
def save_two_state_pm_signal(
    t,
    signal,
    states,
    A,
    f0,
    f1,
    beta,
    fmod,
    offset,
    p,
    idx,
    mode,
    base_dir
):
    """
    Save 2-state PM signal and its state sequence.
    Folder structure: base_dir/p_<p>/mode/*.csv
    """
    p_folder = f"p_{p:.5f}"
    split_dir = os.path.join(base_dir, p_folder, mode)
    os.makedirs(split_dir, exist_ok=True)

    filename = (
        f"{mode}_{idx:03d}_A_{A:.4f}_f0_{f0:.4f}_f1_{f1:.4f}_"
        f"beta_{beta:.4f}_fmod_{fmod:.4f}_offset_{offset:.4f}_p_{p:.5e}.csv"
    )
    df = pd.DataFrame(
        {
            "Time": t,
            "Value": signal,
            "State": states,
        }
    )
    df.to_csv(os.path.join(split_dir, filename), index=False)

# ----- Dataset generator for 2-state PM signals -----
def generate_two_state_pm_dataset(
    base_dir,
    param_bounds,
    transition_probs=(0,0.1, 0.5, 0.9, 0.9999),
    n_train=70,
    n_val=10,
    n_test=20,
    fs=10,
    duration=300,
    # optional: custom f ranges for the two states
    f0_range=None,
    f1_range=None,
):
    """
    Generate PM signals with a 2-state switching carrier frequency.

    param_bounds: dict with keys "A", "f", "beta", "fmod", "offset".
                  If f0_range/f1_range are None, we create well-separated
                  bands from param_bounds["f"].
    """
    T = int(fs * duration)
    used_hashes = set()
    splits = {"train": n_train, "val": n_val, "test": n_test}

    # Use better-separated frequency bands if not provided
    if f0_range is None or f1_range is None:
        f0_range, f1_range = make_well_separated_freq_ranges(param_bounds["f"])

    for p in transition_probs:
        print(f"\n=== Generating two-state PM signals for p = {p} ===")
        for mode, count in splits.items():
            idx_local = 0
            while idx_local < count:
                # Sample parameters
                A = np.random.uniform(*param_bounds["A"])
                beta = np.random.uniform(*param_bounds["beta"])
                fmod = np.random.uniform(*param_bounds["fmod"])
                offset = np.random.uniform(*param_bounds["offset"])
                f0 = np.random.uniform(*f0_range)
                f1 = np.random.uniform(*f1_range)

                h = param_hash_pm_two_state(A, f0, f1, beta, fmod, offset, p)
                if h in used_hashes:
                    continue
                used_hashes.add(h)

                t, signal, states = generate_two_state_pm_signal(
                    T=T,
                    fs=fs,
                    A=A,
                    f0=f0,
                    f1=f1,
                    beta=beta,
                    fmod=fmod,
                    offset=offset,
                    p=p,
                    start_state=0,
                )

                save_two_state_pm_signal(
                    t=t,
                    signal=signal,
                    states=states,
                    A=A,
                    f0=f0,
                    f1=f1,
                    beta=beta,
                    fmod=fmod,
                    offset=offset,
                    p=p,
                    idx=idx_local,
                    mode=mode,
                    base_dir=base_dir,
                )

                idx_local += 1
            print(f"[two-state, p={p}] Saved {count} samples to {mode}/ under p_{p:.5f}")

# ------------------ Simple Visualization (single folder) ------------------
def visualize_signals(base_dir, split="train", num_samples=3, max_rows=50):
    """
    Simple visualizer for single-state data (no State column).
    For two-state data, point this to one specific p-folder.
    """


    split_dir = os.path.join(base_dir, split)
    files = sorted([f for f in os.listdir(split_dir) if f.endswith(".csv")])[:num_samples]

    fig, axes = plt.subplots(1, num_samples, figsize=(4 * num_samples, 3), sharex=True)

    if num_samples == 1:
        axes = [axes]  # make iterable

    for col_idx, file in enumerate(files):
        df = pd.read_csv(os.path.join(split_dir, file))
        df = df.iloc[:max_rows]

        ax = axes[col_idx]
        ax.plot(df["Time"], df["Value"])
        ax.set_title(f'Sample {col_idx+1}', fontsize=14, weight='bold')

        # bold axis labels
        ax.set_xlabel("Time", fontsize=13, weight='bold')
        ax.set_ylabel("Amplitude", fontsize=13, weight='bold')

        # bold tick labels
        ax.tick_params(axis='both', which='major', labelsize=10, width=1.2)
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontweight('bold')

        ax.grid(False)

    plt.tight_layout()
    plt.savefig(
        '/scratch_nvme/Time_Series/Bio-Synthesize/Visualization_Scripts/SPM_Harmonic_Signals.pdf',
        dpi=800
    )
    plt.close()

# ------------------ Main Execution ------------------
if __name__ == "__main__":
    # Original single-state bounds
    param_bounds = {
        "A": (0.1, 0.1227),
        "f": (0.6782, 1.4112),
        "beta": (0.01, 0.3),
        "fmod": (0.01, 0.1),
        "offset": (0.1937, 0.7418),
    }

    # --- Single-state output directory (if you still want it) ---
    single_base_dir = (
        "/scratch_nvme/Time_Series/Bio-Synthesize/"
        "Generation_Synthesized_Bio_Signals/PhaseMod_SingleFreq/Visualization"
    )
    # generate_pm_signals(single_base_dir, param_bounds, n_train=70, n_val=10, n_test=20)

    # --- Two-state output directory ---
    two_state_base_dir = (
        "/scratch_nvme/Time_Series/Bio-Synthesize/"
        "Generation_Synthesized_Bio_Signals/PhaseMod_Single_Freq_TwoState_Extended"
    )

    # Generate two-state dataset with better-separated states
    # (uncomment to run)
    generate_two_state_pm_dataset(
        base_dir=two_state_base_dir,
        param_bounds=param_bounds,
        transition_probs=(0,0.1,0.5,0.9,1),
        n_train=70,
        n_val=10,
        n_test=20,
        fs=10,
        duration=300,
    )

    # Example: to quickly sanity-check one p:
    # visualize_signals(os.path.join(two_state_base_dir, "p_0.10000"), split="train", num_samples=3, max_rows=100)
