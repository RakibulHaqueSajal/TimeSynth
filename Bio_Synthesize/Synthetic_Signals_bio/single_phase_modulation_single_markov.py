import numpy as np
import pandas as pd
import os
import hashlib

# ------------------ Single-state PM (unchanged) ------------------
def generate_phase_modulated_signal(t, A, f, beta, fmod, offset):
    return A * np.sin(2 * np.pi * f * t + beta * np.sin(2 * np.pi * fmod * t)) + offset


# ======================================================
#  ONE-CHANGEPOINT TWO-STATE VERSION (A, f, β, fmod CHANGE ONCE)
# ======================================================

def make_well_separated_freq_ranges(global_f_range):
    f_low, f_high = global_f_range
    span = f_high - f_low
    f0_range = (f_low + 0.05 * span, f_low + 0.25 * span)
    f1_range = (f_low + 0.55 * span, f_low + 0.75 * span)
    return f0_range, f1_range

def make_well_separated_fmod_ranges(global_fmod_range):
    fmod_low, fmod_high = global_fmod_range
    span = fmod_high - fmod_low
    fmod0_range = (fmod_low + 0.05 * span, fmod_low + 0.30 * span)
    fmod1_range = (fmod_low + 0.55 * span, fmod_low + 0.90 * span)
    return fmod0_range, fmod1_range

def param_hash_one_cp(A0, A1, f0, f1, beta0, beta1, fmod0, fmod1, offset, t_star, precision=6):
    key = (
        f"{A0:.{precision}f}_{A1:.{precision}f}_"
        f"{f0:.{precision}f}_{f1:.{precision}f}_"
        f"{beta0:.{precision}f}_{beta1:.{precision}f}_"
        f"{fmod0:.{precision}f}_{fmod1:.{precision}f}_"
        f"{offset:.{precision}f}_"
        f"{int(t_star)}"
    )
    return hashlib.md5(key.encode()).hexdigest()

def generate_one_changepoint_pm_signal(
    T,
    fs,
    A0, A1,
    f0, f1,
    beta0, beta1,
    fmod0, fmod1,
    offset,
    t_star,            # index where state flips: state=0 for t < t_star, state=1 for t >= t_star
    start_state=0,     # typically 0
):
    """
    One changepoint at index t_star.
    State:
        S_k = start_state for k < t_star
        S_k = 1-start_state for k >= t_star

    Carrier phase recursion uses f_t to maintain continuity:
        phase[k] = phase[k-1] + 2π f_t[k-1] dt

    Signal:
        x_k = A_t * sin(phase[k] + beta_t * sin(2π fmod_t * t_k)) + offset
    """
    dt = 1.0 / fs
    t = np.arange(T) * dt

    states = np.zeros(T, dtype=int)
    states[:t_star] = start_state
    states[t_star:] = 1 - start_state

    A_t    = np.where(states == 0, A0,    A1)
    f_t    = np.where(states == 0, f0,    f1)
    beta_t = np.where(states == 0, beta0, beta1)
    fmod_t = np.where(states == 0, fmod0, fmod1)

    phase = np.zeros(T, dtype=float)
    for k in range(1, T):
        phase[k] = phase[k-1] + 2 * np.pi * f_t[k-1] * dt

    phase_mod = beta_t * np.sin(2 * np.pi * fmod_t * t)
    signal = A_t * np.sin(phase + phase_mod) + offset
    return t, signal, states

def save_one_cp_signal_csv(base_dir, mode, idx, t, signal, states,
                           A0, A1, f0, f1, beta0, beta1, fmod0, fmod1, offset, t_star):
    split_dir = os.path.join(base_dir, mode)
    os.makedirs(split_dir, exist_ok=True)

    filename = (
        f"{mode}_{idx:05d}_"
        f"tstar_{t_star:04d}_"
        f"A0_{A0:.4f}_A1_{A1:.4f}_"
        f"f0_{f0:.4f}_f1_{f1:.4f}_"
        f"beta0_{beta0:.4f}_beta1_{beta1:.4f}_"
        f"fmod0_{fmod0:.4f}_fmod1_{fmod1:.4f}_"
        f"offset_{offset:.4f}.csv"
    )

    df = pd.DataFrame({"Time": t, "Value": signal, "State": states})
    out_path = os.path.join(split_dir, filename)
    df.to_csv(out_path, index=False)
    return out_path, filename

def generate_one_changepoint_dataset(
    base_dir,
    param_bounds,
    n_train=500,
    n_val=100,
    n_test=200,
    fs=10,
    duration=20.0,           # SHORTER signals (seconds). With fs=10, duration=20 -> T=200
    # transition placement control:
    tstar_min_frac=0.25,     # transition not too close to start
    tstar_max_frac=0.75,     # transition not too close to end
    # optionally make carrier/mod bands separated:
    f0_range=None,
    f1_range=None,
    fmod0_range=None,
    fmod1_range=None,
    start_state=0,
    seed=123,
):
    """
    Generates many SHORT signals. Each signal has ONE changepoint t_star.
    Saves:
      - CSV per sample: Time, Value, State
      - metadata CSV per split: idx, filename, t_star_idx, t_star_time_sec, and parameters
    """
    rng = np.random.default_rng(seed)

    T = int(fs * duration)

    # default separated ranges
    if f0_range is None or f1_range is None:
        f0_range, f1_range = make_well_separated_freq_ranges(param_bounds["f"])
    if fmod0_range is None or fmod1_range is None:
        fmod0_range, fmod1_range = make_well_separated_fmod_ranges(param_bounds["fmod"])

    splits = {"train": n_train, "val": n_val, "test": n_test}
    used_hashes = set()

    for mode, count in splits.items():
        rows = []
        idx_local = 0

        tstar_min = int(np.floor(tstar_min_frac * T))
        tstar_max = int(np.ceil(tstar_max_frac * T))
        tstar_max = max(tstar_min + 1, min(tstar_max, T - 1))

        while idx_local < count:
            # sample changepoint (ONE transition)
            t_star = int(rng.integers(tstar_min, tstar_max))

            # shared offset
            offset = float(rng.uniform(*param_bounds["offset"]))

            # amplitude: subtle jump
            A_base = float(rng.uniform(*param_bounds["A"]))
            delta_A = float(rng.uniform(0.01, 0.03))
            A0, A1 = A_base, A_base + delta_A

            # carrier frequency (separated)
            f0 = float(rng.uniform(*f0_range))
            f1 = float(rng.uniform(*f1_range))

            # modulation depth: subtle jump
            beta_base = float(rng.uniform(*param_bounds["beta"]))
            delta_beta = float(rng.uniform(0.02, 0.04))
            beta0, beta1 = beta_base, beta_base + delta_beta

            # modulation frequency (separated)
            fmod0 = float(rng.uniform(*fmod0_range))
            fmod1 = float(rng.uniform(*fmod1_range))

            h = param_hash_one_cp(A0, A1, f0, f1, beta0, beta1, fmod0, fmod1, offset, t_star)
            if h in used_hashes:
                continue
            used_hashes.add(h)

            t, signal, states = generate_one_changepoint_pm_signal(
                T=T, fs=fs,
                A0=A0, A1=A1,
                f0=f0, f1=f1,
                beta0=beta0, beta1=beta1,
                fmod0=fmod0, fmod1=fmod1,
                offset=offset,
                t_star=t_star,
                start_state=start_state
            )

            out_path, fname = save_one_cp_signal_csv(
                base_dir=base_dir, mode=mode, idx=idx_local,
                t=t, signal=signal, states=states,
                A0=A0, A1=A1, f0=f0, f1=f1,
                beta0=beta0, beta1=beta1,
                fmod0=fmod0, fmod1=fmod1,
                offset=offset,
                t_star=t_star
            )

            rows.append({
                "split": mode,
                "idx": idx_local,
                "filename": fname,
                "filepath": out_path,
                "t_star_idx": t_star,
                "t_star_time_sec": t_star / fs,
                "A0": A0, "A1": A1,
                "f0": f0, "f1": f1,
                "beta0": beta0, "beta1": beta1,
                "fmod0": fmod0, "fmod1": fmod1,
                "offset": offset,
                "fs": fs,
                "T": T,
                "duration_sec": duration,
            })

            idx_local += 1

        # save metadata CSV for this split
        meta_path = os.path.join(base_dir, f"{mode}_transitions.csv")
        pd.DataFrame(rows).to_csv(meta_path, index=False)
        print(f"[one-change] Saved {count} samples to {mode}/")
        print(f"[one-change] Wrote metadata: {meta_path}")


# ------------------ Main ------------------
if __name__ == "__main__":
    param_bounds = {
        "A": (0.1, 0.1227),
        "f": (0.6782, 1.4112),
        "beta": (0.01, 0.3),
        "fmod": (0.01, 0.1),
        "offset": (0.1937, 0.7418),
    }

    out_dir = (
        "/scratch_nvme/Time_Series/Bio-Synthesize/"
        "Generation_Synthesized_Bio_Signals/PhaseMod_OneState_Change_Trial"
    )

    generate_one_changepoint_dataset(
        base_dir=out_dir,
        param_bounds=param_bounds,
        n_train=600,     # many short signals
        n_val=100,
        n_test=200,
        fs=10,
        duration=30.0,    # short (T=200)
        tstar_min_frac=0.25,
        tstar_max_frac=0.75,
        seed=123
    )
