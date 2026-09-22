#!/usr/bin/env python3
"""
P3.2: Tier 2 synthetic ECG from the McSharry et al. (2003) sum-of-Gaussians model,
with wave parameters sampled from ranges fitted to MIT-BIH NSR beats
(Bio_Synthesize/Parametric_Fitting/tier2_ecg_fit.json) and RR variability from the
bimodal RR spectrum. fs = 50 Hz, 120 s per signal (D5). Ground truth (R-peak times
and amplitudes, all wave positions) in the sidecar JSON.
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


def ecg_from_phase(theta, a, th0, b, z0=0.0):
    z = np.full(theta.shape, z0)
    for ai, ti, bi in zip(a, th0, b):
        d = np.angle(np.exp(1j * (theta - ti)))          # wrapped phase difference
        z += ai * np.exp(-d ** 2 / (2 * bi ** 2))
    return z


def sample(rng, fs=FS, duration=DURATION):
    r = FIT["ranges"]
    a_rel = rng.uniform(r["a_rel"]["min"], r["a_rel"]["max"])
    th0 = rng.uniform(r["theta"]["min"], r["theta"]["max"])
    b = rng.uniform(r["b"]["min"], r["b"]["max"])
    a_rel[2] = 1.0
    R_amp = rng.uniform(r["R_amp"]["min"], r["R_amp"]["max"])
    a = a_rel * R_amp
    rr_mean = rng.uniform(*FIT["rr"]["mean_s"])
    rr_sd = rng.uniform(*FIT["rr"]["sd_s"])
    # QRS widths: the 128 Hz fits allow sigmas of a few ms, below the 50 Hz sample spacing.
    # Clamp Q, R, S sigmas to >= 12 ms (in phase: 2 pi * 0.012 / RR) so every beat is resolved.
    b_min_qrs = 2 * np.pi * 0.012 / rr_mean
    b[1:4] = np.maximum(b[1:4], b_min_qrs)
    rr = rr_process(int(duration / 0.3) + 5, rr_mean, rr_sd, rng)
    theta, r_times, _ = beat_phases(rr, fs, duration)
    x = ecg_from_phase(theta, a, th0, b)
    # baseline wander (respiratory) as in ECGSYN: small, slow
    t = np.arange(x.size) / fs
    x += 0.05 * R_amp * np.sin(2 * np.pi * rng.uniform(0.15, 0.3) * t + rng.uniform(0, 2 * np.pi))
    # exact ground truth: analytic waveform value at theta = theta_R (independent of the grid)
    r_amp_true = float(ecg_from_phase(np.array([th0[2]]), a, th0, b)[0])
    params = dict(a=a.round(5).tolist(), theta=th0.round(5).tolist(), b=b.round(5).tolist(),
                  rr_mean=round(rr_mean, 4), rr_sd=round(rr_sd, 4), R_amp=round(R_amp, 4))
    # R occurs at theta = theta_R, i.e. RR * theta_R / (2 pi) after the mid-beat R reference
    r_times = r_times + np.diff(np.concatenate([[0.0], np.cumsum(rr)]))[:r_times.size] * th0[2] / (2 * np.pi)
    r_idx = np.clip(np.round(r_times * fs).astype(int), 0, x.size - 1)
    events = dict(r_peak_times=r_times.round(6).tolist(), r_peak_amplitudes=x[r_idx].round(5).tolist(),
                  r_peak_amplitude_analytic=round(r_amp_true, 5),
                  rr_intervals=np.diff(r_times).round(6).tolist())
    return params, x, events


if __name__ == "__main__":
    out = os.path.join(DATA_ROOT, "Tier2_ECG")
    m = write_dataset(out, sample, 70, 10, 20, FS, DURATION, seed=2021, tag="ecg")
    print(len(m), "signals ->", out)
