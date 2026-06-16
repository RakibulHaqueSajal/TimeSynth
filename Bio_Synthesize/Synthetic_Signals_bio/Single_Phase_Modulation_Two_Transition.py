#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Two-transition (two changepoint) phase-modulated dataset generator.

Goal:
- Each sequence has TWO transitions between two states A(0) and B(1):
    ABA: 0 -> 1 -> 0   (A->B then B->A)
    BAB: 1 -> 0 -> 1   (B->A then A->B)

- Transitions can occur:
    HH: both in history      (t2 < H)
    HF: one in hist, one fut (t1 < H <= t2)
    FF: both in future       (H <= t1)

You control regime probabilities per split (train/val/test) via `regime_probs_by_split`.

Outputs:
  <base_dir>/<split>/*.csv
  <base_dir>/<split>_transitions.csv  (metadata)
"""

import os
import hashlib
import numpy as np
import pandas as pd
from typing import Dict, Tuple, Optional


# ======================================================
# Ranges (well-separated parameter bands)
# ======================================================

def make_well_separated_freq_ranges(global_f_range: Tuple[float, float]):
    f_low, f_high = global_f_range
    span = f_high - f_low
    f0_range = (f_low + 0.05 * span, f_low + 0.25 * span)   # state 0
    f1_range = (f_low + 0.55 * span, f_low + 0.75 * span)   # state 1
    return f0_range, f1_range


def make_well_separated_fmod_ranges(global_fmod_range: Tuple[float, float]):
    fmod_low, fmod_high = global_fmod_range
    span = fmod_high - fmod_low
    fmod0_range = (fmod_low + 0.05 * span, fmod_low + 0.30 * span)  # state 0
    fmod1_range = (fmod_low + 0.55 * span, fmod_low + 0.90 * span)  # state 1
    return fmod0_range, fmod1_range


# ======================================================
# Hash helpers (avoid duplicates across splits)
# ======================================================

def param_hash_two_cp(
    A0, A1, f0, f1, beta0, beta1, fmod0, fmod1,
    offset, t1, t2, motif, precision=6
):
    key = (
        f"{motif}_"
        f"{A0:.{precision}f}_{A1:.{precision}f}_"
        f"{f0:.{precision}f}_{f1:.{precision}f}_"
        f"{beta0:.{precision}f}_{beta1:.{precision}f}_"
        f"{fmod0:.{precision}f}_{fmod1:.{precision}f}_"
        f"{offset:.{precision}f}_"
        f"{int(t1)}_{int(t2)}"
    )
    return hashlib.md5(key.encode()).hexdigest()


def param_hash_no_transition(A, f, beta, fmod, offset, state_id, precision=6):
    key = (
        f"NO_TRANS_{int(state_id)}_"
        f"{A:.{precision}f}_{f:.{precision}f}_"
        f"{beta:.{precision}f}_{fmod:.{precision}f}_"
        f"{offset:.{precision}f}"
    )
    return hashlib.md5(key.encode()).hexdigest()


# ======================================================
# Two-CP placement logic: HH/HF/FF regimes
# ======================================================

def pick_regime(rng: np.random.Generator, regime_probs: Dict[str, float]) -> str:
    """
    regime_probs keys: "HH","HF","FF"
    values sum to ~1.0
    """
    pHH = float(regime_probs.get("HH", 0.0))
    pHF = float(regime_probs.get("HF", 0.0))
    pFF = float(regime_probs.get("FF", 0.0))
    s = pHH + pHF + pFF
    if s <= 0:
        raise ValueError("regime_probs must have positive mass.")
    # normalize
    pHH, pHF, pFF = pHH / s, pHF / s, pFF / s
    r = rng.random()
    if r < pHH:
        return "HH"
    elif r < pHH + pHF:
        return "HF"
    else:
        return "FF"


def sample_two_cps_by_regime(
    rng: np.random.Generator,
    T: int,
    H: int,
    min_dwell: int,
    max_dwell: Optional[int],
    regime: str,
    t1_min_abs: int = 1,
    t2_max_abs: Optional[int] = None,
) -> Tuple[int, int]:
    """
    Sample (t1, t2) with t1 < t2 under a placement regime relative to boundary H.

    Regimes:
      HH: t2 < H
      HF: t1 < H <= t2
      FF: H <= t1
    """
    assert 0 < H < T
    assert regime in ("HH", "HF", "FF")

    if t2_max_abs is None:
        t2_max_abs = T - 1

    # clamp feasible global bounds
    t1_min_abs = max(1, min(int(t1_min_abs), T - 3))
    t2_max_abs = max(t1_min_abs + 2, min(int(t2_max_abs), T - 1))

    if max_dwell is None:
        max_dwell = (t2_max_abs - t1_min_abs)
    max_dwell = int(max_dwell)
    min_dwell = int(min_dwell)

    for _ in range(300):
        dwell = int(rng.integers(min_dwell, max_dwell + 1))

        if regime == "HH":
            # need t2 <= H-1
            t2_hi = min(H - 1, t2_max_abs)
            t1_hi = t2_hi - dwell
            if t1_hi <= t1_min_abs:
                continue
            t1 = int(rng.integers(t1_min_abs, t1_hi + 1))
            t2 = int(t1 + dwell)
            if 0 < t1 < t2 < H:
                return t1, t2

        elif regime == "HF":
            # need t1 < H and t2 >= H
            t1_hi = min(H - 1, t2_max_abs - dwell)
            if t1_hi <= t1_min_abs:
                continue
            t1 = int(rng.integers(t1_min_abs, t1_hi + 1))
            t2 = int(t1 + dwell)
            if t1 < H <= t2 < T:
                return t1, t2

        else:  # FF
            # need t1 >= H
            t1_lo = max(H, t1_min_abs)
            t1_hi = min(t2_max_abs - dwell, T - 2)
            if t1_hi <= t1_lo:
                continue
            t1 = int(rng.integers(t1_lo, t1_hi + 1))
            t2 = int(t1 + dwell)
            if H <= t1 < t2 < T:
                return t1, t2

    raise RuntimeError(
        f"Could not sample (t1,t2) for regime={regime} with constraints "
        f"T={T}, H={H}, min_dwell={min_dwell}, max_dwell={max_dwell}."
    )


# ======================================================
# Signal generators
# ======================================================

def generate_two_changepoint_pm_signal(
    T: int,
    fs: float,
    A0: float, A1: float,
    f0: float, f1: float,
    beta0: float, beta1: float,
    fmod0: float, fmod1: float,
    offset: float,
    t1: int, t2: int,
    motif: str = "ABA",
):
    """
    Two transitions, two states (0 and 1).
    Motif:
      - ABA: 0 -> 1 -> 0
      - BAB: 1 -> 0 -> 1

    Phase recursion keeps continuity when f changes by state.
    """
    assert 0 < t1 < t2 < T
    assert motif in ("ABA", "BAB")

    dt = 1.0 / float(fs)
    t = np.arange(T) * dt

    states = np.zeros(T, dtype=int)
    if motif == "ABA":
        states[:t1] = 0
        states[t1:t2] = 1
        states[t2:] = 0
    else:  # BAB
        states[:t1] = 1
        states[t1:t2] = 0
        states[t2:] = 1

    A_t    = np.where(states == 0, A0,    A1)
    f_t    = np.where(states == 0, f0,    f1)
    beta_t = np.where(states == 0, beta0, beta1)
    fmod_t = np.where(states == 0, fmod0, fmod1)

    # carrier phase recursion for continuity
    phase = np.zeros(T, dtype=float)
    for k in range(1, T):
        phase[k] = phase[k - 1] + 2 * np.pi * f_t[k - 1] * dt

    phase_mod = beta_t * np.sin(2 * np.pi * fmod_t * t)
    signal = A_t * np.sin(phase + phase_mod) + offset
    return t, signal, states


def generate_no_transition_pm_signal(
    T: int, fs: float,
    A: float, f: float, beta: float, fmod: float, offset: float,
    state_id: int = 0
):
    dt = 1.0 / float(fs)
    t = np.arange(T) * dt

    phase = np.zeros(T, dtype=float)
    for k in range(1, T):
        phase[k] = phase[k - 1] + 2 * np.pi * f * dt

    phase_mod = beta * np.sin(2 * np.pi * fmod * t)
    signal = A * np.sin(phase + phase_mod) + offset
    states = np.full(T, int(state_id), dtype=int)
    return t, signal, states


# ======================================================
# Save helpers
# ======================================================

def save_two_cp_signal_csv(
    base_dir: str,
    split: str,
    idx: int,
    t: np.ndarray,
    signal: np.ndarray,
    states: np.ndarray,
    motif: str,
    t1: int,
    t2: int,
    A0: float, A1: float,
    f0: float, f1: float,
    beta0: float, beta1: float,
    fmod0: float, fmod1: float,
    offset: float
):
    split_dir = os.path.join(base_dir, split)
    os.makedirs(split_dir, exist_ok=True)

    dwell = int(t2 - t1)
    filename = (
        f"{split}_{idx:05d}_"
        f"motif_{motif}_"
        f"t1_{t1:04d}_t2_{t2:04d}_dwell_{dwell:04d}_"
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


def save_no_transition_csv(
    base_dir: str,
    split: str,
    idx: int,
    t: np.ndarray,
    signal: np.ndarray,
    states: np.ndarray,
    state_id: int,
    A: float, f: float, beta: float, fmod: float, offset: float
):
    split_dir = os.path.join(base_dir, split)
    os.makedirs(split_dir, exist_ok=True)

    filename = (
        f"{split}_{idx:05d}_"
        f"motif_NO_TRANS_state_{int(state_id)}_"
        f"A_{A:.4f}_f_{f:.4f}_beta_{beta:.4f}_fmod_{fmod:.4f}_"
        f"offset_{offset:.4f}.csv"
    )

    df = pd.DataFrame({"Time": t, "Value": signal, "State": states})
    out_path = os.path.join(split_dir, filename)
    df.to_csv(out_path, index=False)
    return out_path, filename


# ======================================================
# Dataset generator
# ======================================================

def generate_two_changepoint_dataset(
    base_dir: str,
    param_bounds: Dict[str, Tuple[float, float]],

    n_train: int = 600,
    n_val: int = 100,
    n_test: int = 400,

    # optional no-transition baselines (added to test)
    n_test_no_transition: int = 0,

    fs: float = 10,
    H: int = 50,
    P: int = 100,
    extra_context: int = 0,

    # dwell bounds
    min_dwell: int = 5,
    max_dwell: Optional[int] = None,

    # optional override separated bands
    f0_range: Optional[Tuple[float, float]] = None,
    f1_range: Optional[Tuple[float, float]] = None,
    fmod0_range: Optional[Tuple[float, float]] = None,
    fmod1_range: Optional[Tuple[float, float]] = None,

    # regime probabilities per split
    # keys: "HH","HF","FF"
    regime_probs_by_split: Optional[Dict[str, Dict[str, float]]] = None,

    # balancing
    force_balanced_motifs: bool = True,
    force_balanced_no_transition_AB: bool = True,

    seed: int = 123,
):
    """
    Generate train/val/test, each sample has exactly two transitions (ABA or BAB)
    with placements governed by HH/HF/FF regime probabilities.

    Metadata includes regime and placement flags.
    """
    rng = np.random.default_rng(seed)

    T = int(H + P + extra_context)
    duration = T / fs

    # separated ranges (defaults from global bounds)
    if f0_range is None or f1_range is None:
        f0_range, f1_range = make_well_separated_freq_ranges(param_bounds["f"])
    if fmod0_range is None or fmod1_range is None:
        fmod0_range, fmod1_range = make_well_separated_fmod_ranges(param_bounds["fmod"])

    # default regime probabilities
    if regime_probs_by_split is None:
        regime_probs_by_split = {
            "train": {"HH": 0.34, "HF": 0.33, "FF": 0.33},
            "val":   {"HH": 0.34, "HF": 0.33, "FF": 0.33},
            "test":  {"HH": 0.34, "HF": 0.33, "FF": 0.33},
        }

    used_hashes = set()
    splits = {"train": int(n_train), "val": int(n_val), "test": int(n_test)}

    for split, count in splits.items():
        rows = []
        idx_local = 0

        # motif list (balanced)
        if force_balanced_motifs:
            motifs = (["ABA"] * (count // 2)) + (["BAB"] * (count - count // 2))
            rng.shuffle(motifs)
        else:
            motifs = None

        regime_probs = regime_probs_by_split.get(split, {"HH": 0.34, "HF": 0.33, "FF": 0.33})

        while idx_local < count:
            motif = motifs[idx_local] if motifs is not None else ("ABA" if rng.random() < 0.5 else "BAB")
            regime = pick_regime(rng, regime_probs)

            # sample changepoints according to regime
            t1, t2 = sample_two_cps_by_regime(
                rng=rng,
                T=T,
                H=H,
                min_dwell=min_dwell,
                max_dwell=max_dwell,
                regime=regime,
                t1_min_abs=1,
                t2_max_abs=T - 1
            )

            # params
            offset = float(rng.uniform(*param_bounds["offset"]))

            A_base = float(rng.uniform(*param_bounds["A"]))
            delta_A = float(rng.uniform(0.01, 0.03))
            A0, A1 = A_base, A_base + delta_A

            f0 = float(rng.uniform(*f0_range))
            f1 = float(rng.uniform(*f1_range))

            beta_base = float(rng.uniform(*param_bounds["beta"]))
            delta_beta = float(rng.uniform(0.02, 0.04))
            beta0, beta1 = beta_base, beta_base + delta_beta

            fmod0 = float(rng.uniform(*fmod0_range))
            fmod1 = float(rng.uniform(*fmod1_range))

            h = param_hash_two_cp(A0, A1, f0, f1, beta0, beta1, fmod0, fmod1, offset, t1, t2, motif)
            if h in used_hashes:
                continue
            used_hashes.add(h)

            t, signal, states = generate_two_changepoint_pm_signal(
                T=T, fs=fs,
                A0=A0, A1=A1,
                f0=f0, f1=f1,
                beta0=beta0, beta1=beta1,
                fmod0=fmod0, fmod1=fmod1,
                offset=offset,
                t1=t1, t2=t2,
                motif=motif
            )

            out_path, fname = save_two_cp_signal_csv(
                base_dir=base_dir, split=split, idx=idx_local,
                t=t, signal=signal, states=states,
                motif=motif, t1=t1, t2=t2,
                A0=A0, A1=A1,
                f0=f0, f1=f1,
                beta0=beta0, beta1=beta1,
                fmod0=fmod0, fmod1=fmod1,
                offset=offset
            )

            rows.append({
                "split": split,
                "idx": idx_local,
                "motif": motif,
                "regime": regime,
                "filename": fname,
                "filepath": out_path,

                "t1_idx": int(t1),
                "t2_idx": int(t2),
                "dwell_idx": int(t2 - t1),

                "t1_time_sec": float(t1 / fs),
                "t2_time_sec": float(t2 / fs),
                "dwell_time_sec": float((t2 - t1) / fs),

                "A0": A0, "A1": A1,
                "f0": f0, "f1": f1,
                "beta0": beta0, "beta1": beta1,
                "fmod0": fmod0, "fmod1": fmod1,
                "offset": offset,

                "fs": fs,
                "H": H,
                "P": P,
                "T": T,
                "duration_sec": duration,
                "extra_context": int(extra_context),

                "both_transitions_in_history": int(t2 < H),
                "one_in_hist_one_in_future": int(t1 < H <= t2),
                "both_transitions_in_future": int(t1 >= H),
                "no_transition": 0,
                "const_state_id": -1,
            })

            idx_local += 1

        # optional no-transition baselines (test only)
        if split == "test" and int(n_test_no_transition) > 0:
            n_no = int(n_test_no_transition)

            if force_balanced_no_transition_AB:
                state_ids = ([0] * (n_no // 2)) + ([1] * (n_no - n_no // 2))
                rng.shuffle(state_ids)
            else:
                state_ids = [0 if rng.random() < 0.5 else 1 for _ in range(n_no)]

            for j in range(n_no):
                state_id = int(state_ids[j])

                offset = float(rng.uniform(*param_bounds["offset"]))
                A = float(rng.uniform(*param_bounds["A"]))
                beta = float(rng.uniform(*param_bounds["beta"]))

                f = float(rng.uniform(*f0_range)) if state_id == 0 else float(rng.uniform(*f1_range))
                fmod = float(rng.uniform(*fmod0_range)) if state_id == 0 else float(rng.uniform(*fmod1_range))

                h = param_hash_no_transition(A, f, beta, fmod, offset, state_id)
                if h in used_hashes:
                    continue
                used_hashes.add(h)

                t, signal, states = generate_no_transition_pm_signal(
                    T=T, fs=fs, A=A, f=f, beta=beta, fmod=fmod, offset=offset, state_id=state_id
                )

                out_path, fname = save_no_transition_csv(
                    base_dir=base_dir, split=split, idx=idx_local,
                    t=t, signal=signal, states=states,
                    state_id=state_id, A=A, f=f, beta=beta, fmod=fmod, offset=offset
                )

                rows.append({
                    "split": split,
                    "idx": idx_local,
                    "motif": "NO_TRANS",
                    "regime": "NONE",
                    "filename": fname,
                    "filepath": out_path,

                    "t1_idx": -1,
                    "t2_idx": -1,
                    "dwell_idx": 0,

                    "t1_time_sec": np.nan,
                    "t2_time_sec": np.nan,
                    "dwell_time_sec": 0.0,

                    "A0": A, "A1": A,
                    "f0": f, "f1": f,
                    "beta0": beta, "beta1": beta,
                    "fmod0": fmod, "fmod1": fmod,
                    "offset": offset,

                    "fs": fs,
                    "H": H,
                    "P": P,
                    "T": T,
                    "duration_sec": duration,
                    "extra_context": int(extra_context),

                    "both_transitions_in_history": 0,
                    "one_in_hist_one_in_future": 0,
                    "both_transitions_in_future": 0,
                    "no_transition": 1,
                    "const_state_id": int(state_id),
                })

                idx_local += 1

        meta_path = os.path.join(base_dir, f"{split}_transitions.csv")
        pd.DataFrame(rows).to_csv(meta_path, index=False)

        print(f"[two-change] Saved {count} two-transition samples to {split}/")
        print(f"[two-change] Regime probs for {split}: {regime_probs}")
        if split == "test" and int(n_test_no_transition) > 0:
            print(f"[two-change] Added {int(n_test_no_transition)} no-transition baselines to test/")
        print(f"[two-change] Wrote metadata: {meta_path}")


# ======================================================
# Main
# ======================================================

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
        "Generation_Synthesized_Bio_Signals/PhaseMod_TwoTransition_Mixed"
    )

    # Example: emphasize HF (one transition in history, one in future)
    regime_probs_by_split = {
        "train": {"HH": 0.25, "HF": 0.50, "FF": 0.25},
        "val":   {"HH": 0.25, "HF": 0.50, "FF": 0.25},
        "test":  {"HH": 0.33, "HF": 0.34, "FF": 0.33},
    }

    generate_two_changepoint_dataset(
        base_dir=out_dir,
        param_bounds=param_bounds,

        n_train=600,
        n_val=100,
        n_test=400,

        # optional baselines in test
        n_test_no_transition=50,

        fs=10,
        H=150,
        P=100,
        extra_context=150,

        min_dwell=5,
        max_dwell=None,

        regime_probs_by_split=regime_probs_by_split,

        seed=123,
        force_balanced_motifs=True,
        force_balanced_no_transition_AB=True,
    )
