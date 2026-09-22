#!/usr/bin/env python3
"""
P3.3: Tier 2 synthetic EEG: narrowband dual phase-modulated background (the Tier 1
DPM form, carriers in the theta and alpha bands) plus transients: biphasic spikes
(difference of two Gaussians, 20-70 ms), sharp waves (70-200 ms) and optional
spike-and-slow-wave complexes (spike followed by a 200-400 ms slow wave). Event
times follow a Poisson process with a sampled rate; polarity is random.

fs = 100 Hz (stated deviation from D5: 20 ms spikes need >= 100 Hz), 60 s per signal,
so windows are 500 / 1000 samples (5 s / 10 s as elsewhere). Ground truth: event
times, type, polarity, amplitude.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tier2_common import write_dataset  # noqa: E402

DATA_ROOT = os.environ.get("TIMESYNTH_DATA_ROOT",
                           "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_data/Generation_Synthesized_Bio_Signals")
FS, DURATION = 100.0, 60.0
BOUNDS = dict(A1=(0.6, 1.0), f1=(8.0, 12.0), beta1=(0.05, 0.3), fmod1=(0.05, 0.2),
              A2=(0.3, 0.6), f2=(4.0, 7.0), beta2=(0.05, 0.3), fmod2=(0.05, 0.2),
              rate_hz=(0.1, 1.0), spike_amp=(2.0, 5.0), p_sharp=(0.2, 0.5), p_complex=(0.1, 0.4))


def transient(t_rel, kind, amp, polarity, dur, rng):
    """Waveform on t_rel (s, relative to event onset)."""
    if kind == "spike":                       # biphasic: difference of two Gaussians
        s1, s2 = dur / 6.0, dur / 3.0
        w = np.exp(-(t_rel - dur / 3) ** 2 / (2 * s1 ** 2)) - 0.6 * np.exp(-(t_rel - 2 * dur / 3) ** 2 / (2 * s2 ** 2))
    elif kind == "sharp":                     # single asymmetric bump
        s = dur / 4.0
        w = np.exp(-(t_rel - dur / 2) ** 2 / (2 * s ** 2))
    else:                                     # spike followed by a slow wave
        sd = 0.04
        w = np.exp(-(t_rel - 0.03) ** 2 / (2 * (sd / 3) ** 2))
        slow = 0.25 * dur
        w -= 0.5 * np.exp(-(t_rel - 0.06 - slow) ** 2 / (2 * (slow / 2.5) ** 2))
    w = np.where((t_rel >= 0) & (t_rel <= dur + (0.5 if kind == "complex" else 0.0)), w, 0.0)
    return polarity * amp * w


def sample(rng, fs=FS, duration=DURATION):
    p = {k: float(rng.uniform(*v)) for k, v in BOUNDS.items()}
    T = int(fs * duration)
    t = np.arange(T) / fs
    x = (p["A1"] * np.sin(2 * np.pi * p["f1"] * t + p["beta1"] * np.sin(2 * np.pi * p["fmod1"] * t))
         + p["A2"] * np.sin(2 * np.pi * p["f2"] * t + p["beta2"] * np.sin(2 * np.pi * p["fmod2"] * t)))
    n_ev = rng.poisson(p["rate_hz"] * duration)
    times = np.sort(rng.uniform(0.5, duration - 0.8, n_ev))
    events = []
    for te in times:
        u = rng.random()
        if u < p["p_complex"]:
            kind, dur = "complex", float(rng.uniform(0.2, 0.4))
        elif u < p["p_complex"] + p["p_sharp"]:
            kind, dur = "sharp", float(rng.uniform(0.07, 0.2))
        else:
            kind, dur = "spike", float(rng.uniform(0.02, 0.07))
        pol = float(rng.choice([-1.0, 1.0]))
        amp = float(rng.uniform(0.7, 1.0) * p["spike_amp"])
        w = transient(t - te, kind, amp, pol, dur, rng)
        x += w
        peak_i = int(np.argmax(np.abs(w)))
        events.append(dict(t_onset=round(te, 4), t_peak=round(peak_i / fs, 4), kind=kind, polarity=pol,
                           amplitude=round(float(w[peak_i]), 4), duration=round(dur, 4)))
    params = {k: round(v, 5) for k, v in p.items()}
    return params, x, dict(events=events, peak_times=[e["t_peak"] for e in events],
                           peak_amplitudes=[e["amplitude"] for e in events])


if __name__ == "__main__":
    out = os.path.join(DATA_ROOT, "Tier2_EEG")
    m = write_dataset(out, sample, 70, 10, 20, FS, DURATION, seed=2021, tag="eeg")
    print(len(m), "signals ->", out)
