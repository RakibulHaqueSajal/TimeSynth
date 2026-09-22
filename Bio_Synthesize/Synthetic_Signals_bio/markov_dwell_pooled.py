#!/usr/bin/env python3
"""
Phase 4 (P4.1, P4.2, P4.4): redesigned two-state Markov switching paradigm.

Changes with respect to ``single_phase_modulation_markov.py`` (the paper's generator):

* Dwell-time parameterization (P4.1). The chain is still symmetric with a per-sample
  switching probability, but ``p = 1 / (fs * D)`` is derived from an expected dwell
  time ``D`` in seconds (decision D8: D in {2, 5, 10} s). At fs = 10 Hz this gives
  mean dwells of 20, 50 and 100 samples, i.e. 2 to 10 carrier cycles per state, and
  about 5, 2 and 1 expected switches inside the 10 s horizon.
* Pooled training (P4.2). All dwell times go into one ``train`` and one ``val`` folder,
  so the model must infer the switching statistics from the history. ``test`` is split
  per dwell time (``test_D2``, ``test_D5``, ``test_D10``) so results are reported per D;
  a pooled ``test`` folder is also written for convenience.
* Multiple futures (P4.4). For every test signal the chain state and carrier phase at
  every forecast boundary are recoverable from the saved ``State`` column and the
  parameters in the file name, so ``continue_from`` can simulate K independent
  continuations of any window. ``alt_futures.npy`` is written for a fixed set of
  window starts per test file (every seq_len + pred_len samples), shape
  [n_windows, K, pred_len], with a JSON index.
* Frequency bands: unchanged (Eq. A7 via ``make_well_separated_freq_ranges``).
* Same hash-based uniqueness and 70/10/20 signals per dwell time as Tier 1.

Output layout (default under $TIMESYNTH_DATA_ROOT):
    PhaseMod_Markov_Dwell/
        train/*.csv   val/*.csv   test/*.csv        (pooled; file names carry D)
        by_dwell/D2/test  by_dwell/D5/test  by_dwell/D10/test   (per-D copies of the test files)
        alt_futures/<test file>.npy + .json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from single_phase_modulation_markov import make_well_separated_freq_ranges  # noqa: E402

PARAM_BOUNDS = {          # identical to the paper's generator __main__
    "A": (0.1, 0.1227),
    "f": (0.6782, 1.4112),
    "beta": (0.01, 0.3),
    "fmod": (0.01, 0.1),
    "offset": (0.1937, 0.7418),
}
DEFAULT_OUT = os.path.join(
    os.environ.get("TIMESYNTH_DATA_ROOT",
                   "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_data/Generation_Synthesized_Bio_Signals"),
    "PhaseMod_Markov_Dwell")


def p_from_dwell(D_s: float, fs: float) -> float:
    return 1.0 / (fs * D_s)


def simulate_chain(T, p, rng, start_state=0):
    switch = rng.random(T) < p
    switch[0] = False
    return (start_state + np.cumsum(switch)) % 2


def synthesize(states, fs, A, f0, f1, beta, delta_beta, fmod, offset, phase0=0.0, t0=0.0):
    """Deterministic given states: carrier phase recursion + state-dependent PM."""
    T = states.size
    dt = 1.0 / fs
    t = t0 + np.arange(T) * dt
    f_t = np.where(states == 0, f0, f1)
    phase = phase0 + np.concatenate([[0.0], np.cumsum(2 * np.pi * f_t[:-1] * dt)])
    beta_t = np.where(states == 0, beta, beta + delta_beta)
    x = A * np.sin(phase + beta_t * np.sin(2 * np.pi * fmod * t)) + offset
    return t, x, phase


def param_hash(*vals, precision=6):
    return hashlib.md5("_".join(f"{v:.{precision}e}" for v in vals).encode()).hexdigest()


def file_name(mode, idx, D, A, f0, f1, beta, delta_beta, fmod, offset):
    return (f"{mode}_{idx:03d}_D_{D:g}_A_{A:.4f}_f0_{f0:.4f}_f1_{f1:.4f}_beta_{beta:.4f}_"
            f"dbeta_{delta_beta:.4f}_fmod_{fmod:.4f}_offset_{offset:.4f}.csv")


def parse_params(name):
    import re
    keys = ["D", "A", "f0", "f1", "beta", "dbeta", "fmod", "offset"]
    out = {}
    for k in keys:
        m = re.search(rf"_{k}_(-?\d+(?:\.\d+)?(?:e-?\d+)?)", name)
        out[k] = float(m.group(1))
    return out


def continue_from(df: pd.DataFrame, start: int, seq_len: int, pred_len: int, K: int, fs: float,
                  params: dict, rng) -> np.ndarray:
    """
    K independent continuations of the window starting at ``start``: same history
    (rows start .. start+seq_len), fresh chain draws for the horizon with the same p,
    starting from the true state and carrier phase at the boundary. Returns [K, pred_len].
    """
    st = df["State"].values.astype(int)
    b = start + seq_len
    p = p_from_dwell(params["D"], fs)
    # carrier phase at the boundary, reconstructed from the true states
    f_t = np.where(st[:b] == 0, params["f0"], params["f1"])
    phase_b = np.sum(2 * np.pi * f_t / fs)          # phase index b
    out = np.empty((K, pred_len))
    for k in range(K):
        s_fut = simulate_chain(pred_len + 1, p, rng, start_state=st[b - 1])[1:]
        # phase recursion starts from the phase at index b (which uses state b-1)
        _, x, _ = synthesize(s_fut, fs, params["A"], params["f0"], params["f1"], params["beta"],
                             params["dbeta"], params["fmod"], params["offset"],
                             phase0=phase_b, t0=b / fs)
        out[k] = x
    return out


def generate(out_dir=DEFAULT_OUT, dwell_s=(2.0, 5.0, 10.0), n_train=70, n_val=10, n_test=20,
             fs=10.0, duration=300.0, seed=2021, seq_len=50, pred_len=100, K_alt=20):
    rng = np.random.default_rng(seed)
    T = int(fs * duration)
    f0_range, f1_range = make_well_separated_freq_ranges(PARAM_BOUNDS["f"])
    used = set()
    for mode in ["train", "val", "test"]:
        os.makedirs(os.path.join(out_dir, mode), exist_ok=True)
    for D in dwell_s:
        os.makedirs(os.path.join(out_dir, "by_dwell", f"D{D:g}", "test"), exist_ok=True)
    os.makedirs(os.path.join(out_dir, "alt_futures"), exist_ok=True)

    manifest = []
    for D in dwell_s:
        p = p_from_dwell(D, fs)
        for mode, n in [("train", n_train), ("val", n_val), ("test", n_test)]:
            idx = 0
            while idx < n:
                A = rng.uniform(*PARAM_BOUNDS["A"])
                beta = rng.uniform(*PARAM_BOUNDS["beta"])
                fmod = rng.uniform(*PARAM_BOUNDS["fmod"])
                offset = rng.uniform(*PARAM_BOUNDS["offset"])
                f0 = rng.uniform(*f0_range)
                f1 = rng.uniform(*f1_range)
                delta_beta = rng.uniform(0.02, 0.04)
                h = param_hash(A, f0, f1, beta, delta_beta, fmod, offset, p)
                if h in used:
                    continue
                used.add(h)
                states = simulate_chain(T, p, rng, start_state=int(rng.integers(0, 2)))
                t, x, _ = synthesize(states, fs, A, f0, f1, beta, delta_beta, fmod, offset)
                name = file_name(mode, idx, D, A, f0, f1, beta, delta_beta, fmod, offset)
                df = pd.DataFrame({"Time": t, "Value": x, "State": states})
                fp = os.path.join(out_dir, mode, name)
                df.to_csv(fp, index=False)
                if mode == "test":
                    shutil.copy(fp, os.path.join(out_dir, "by_dwell", f"D{D:g}", "test", name))
                    starts = np.arange(0, T - seq_len - pred_len + 1, seq_len + pred_len)
                    params = parse_params(name)
                    alt = np.stack([continue_from(df, s, seq_len, pred_len, K_alt, fs, params, rng) for s in starts])
                    np.save(os.path.join(out_dir, "alt_futures", name[:-4] + ".npy"), alt.astype(np.float32))
                    json.dump({"file": name, "window_starts": starts.tolist(), "K": K_alt,
                               "seq_len": seq_len, "pred_len": pred_len, "fs": fs, "D": D, "p": p},
                              open(os.path.join(out_dir, "alt_futures", name[:-4] + ".json"), "w"))
                n_sw = int(np.sum(np.diff(states) != 0))
                manifest.append(dict(mode=mode, D=D, p=p, file=name, n_switches=n_sw,
                                     mean_dwell_s=(T / max(n_sw, 1)) / fs))
                idx += 1
        print(f"D={D:g}s p={p:.4f}: done", flush=True)
    pd.DataFrame(manifest).to_csv(os.path.join(out_dir, "manifest.csv"), index=False)
    json.dump({"dwell_s": list(dwell_s), "fs": fs, "duration_s": duration, "seed": seed,
               "f0_range": f0_range, "f1_range": f1_range, "param_bounds": PARAM_BOUNDS,
               "p_per_dwell": {f"{D:g}": p_from_dwell(D, fs) for D in dwell_s}},
              open(os.path.join(out_dir, "generation_config.json"), "w"), indent=1)
    print(pd.DataFrame(manifest).groupby(["D", "mode"]).agg(n=("file", "size"), mean_dwell_s=("mean_dwell_s", "mean")))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--dwell", type=float, nargs="+", default=[2.0, 5.0, 10.0])
    ap.add_argument("--seed", type=int, default=2021)
    a = ap.parse_args()
    generate(out_dir=a.out, dwell_s=tuple(a.dwell), seed=a.seed)
