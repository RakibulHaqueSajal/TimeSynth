#!/usr/bin/env python3
"""
P3.4: Tier 2 synthetic PPG (decision D7): two Gaussians per beat in phase
coordinates (systolic peak and dicrotic wave) driven by the same RR process as the
ECG generator. fs = 50 Hz, 120 s. Ground truth: systolic peak times and amplitudes.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tier2_common import beat_phases, rr_process, write_dataset  # noqa: E402

FIT = json.load(open(os.path.join(HERE, "..", "Parametric_Fitting", "tier2_ecg_fit.json")))
DATA_ROOT = os.environ.get("TIMESYNTH_DATA_ROOT",
                           "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_data/Generation_Synthesized_Bio_Signals")
FS, DURATION = 50.0, 120.0
BOUNDS = dict(A_sys=(0.8, 1.2), A_dic=(0.2, 0.55), th_sys=(-1.2, -0.6), th_dic=(0.3, 1.1),
              b_sys=(0.45, 0.75), b_dic=(0.5, 0.9), baseline=(0.2, 0.6))


def ppg_from_phase(theta, p):
    x = np.full(theta.shape, p["baseline"])
    for A, th, b in [(p["A_sys"], p["th_sys"], p["b_sys"]), (p["A_dic"], p["th_dic"], p["b_dic"])]:
        d = np.angle(np.exp(1j * (theta - th)))
        x += A * np.exp(-d ** 2 / (2 * b ** 2))
    return x


def sample(rng, fs=FS, duration=DURATION):
    p = {k: float(rng.uniform(*v)) for k, v in BOUNDS.items()}
    rr_mean = rng.uniform(*FIT["rr"]["mean_s"])
    rr_sd = rng.uniform(*FIT["rr"]["sd_s"])
    rr = rr_process(int(duration / 0.3) + 5, rr_mean, rr_sd, rng)
    theta, r_times, k = beat_phases(rr, fs, duration)
    x = ppg_from_phase(theta, p)
    # systolic peak of beat k is at theta = th_sys, i.e. at t_k + rr_k (th_sys + pi) / (2 pi)
    starts = np.concatenate([[0.0], np.cumsum(rr)])
    sys_times = starts[:-1] + rr * (p["th_sys"] + np.pi) / (2 * np.pi)
    sys_times = sys_times[sys_times < duration]
    s_idx = np.round(sys_times * fs).astype(int)
    s_idx = s_idx[s_idx < x.size]
    params = {**{k_: round(v, 5) for k_, v in p.items()}, "rr_mean": round(rr_mean, 4), "rr_sd": round(rr_sd, 4)}
    events = dict(peak_times=sys_times.round(6).tolist(), peak_amplitudes=x[s_idx].round(5).tolist(),
                  rr_intervals=np.diff(sys_times).round(6).tolist())
    return params, x, events


if __name__ == "__main__":
    out = os.path.join(DATA_ROOT, "Tier2_PPG")
    m = write_dataset(out, sample, 70, 10, 20, FS, DURATION, seed=2021, tag="ppg")
    print(len(m), "signals ->", out)
