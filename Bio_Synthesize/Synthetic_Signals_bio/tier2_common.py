"""
Shared pieces of the Tier 2 (transient-rich) generators, P3.

* ``rr_process``: beat-to-beat interval series with McSharry-style bimodal RR
  variability (Mayer-wave band around 0.1 Hz and respiratory band around 0.25 Hz),
  parameterized by mean RR and RR standard deviation.
* ``beat_phases``: continuous beat phase theta(t) in [-pi, pi) from RR intervals,
  so a beat waveform defined in phase coordinates can be sampled at any fs.
* ``write_dataset``: hash-unique parameter sampling, 70/10/20 split, CSVs in the
  loader's ``Time,Value`` format, one ground-truth sidecar ``<file>.events.json``
  per signal with exact event times and amplitudes (peak metrics are then exact,
  not detector-dependent), and a noise variant folder per SNR level (Tier 1 SNR
  table: 40, 30, 20, 10, 5, 1 dB) for the test split.
"""
from __future__ import annotations

import hashlib
import json
import os

import numpy as np
import pandas as pd

SNR_LEVELS_DB = {1: 40, 2: 30, 3: 20, 4: 10, 5: 5, 6: 1}


def rr_process(n_beats, rr_mean, rr_sd, rng, f_lf=0.1, f_hf=0.25, c_lf=0.01, c_hf=0.01, lf_hf_ratio=0.5):
    """
    RR intervals (s) with the bimodal spectrum of McSharry et al. 2003: the RR
    time series is generated from a power spectrum made of two Gaussians (LF and
    HF), scaled to the requested standard deviation and shifted to the mean.
    """
    n = int(2 ** np.ceil(np.log2(max(n_beats, 64) * 4)))
    fs_rr = 1.0 / rr_mean                       # one sample per mean beat
    f = np.fft.rfftfreq(n, d=1.0 / fs_rr)
    S = lf_hf_ratio * np.exp(-(f - f_lf) ** 2 / (2 * c_lf ** 2)) + np.exp(-(f - f_hf) ** 2 / (2 * c_hf ** 2))
    S[0] = 0.0
    phase = rng.uniform(0, 2 * np.pi, f.size)
    spec = np.sqrt(S) * np.exp(1j * phase)
    x = np.fft.irfft(spec, n=n)
    x = (x - x.mean()) / (x.std() + 1e-12)
    rr = rr_mean + rr_sd * x[:n_beats]
    return np.clip(rr, 0.3, 2.5)


def beat_phases(rr, fs, duration):
    """
    theta(t) for t in [0, duration): linear from -pi at one beat's start to +pi at
    the next R, R peaks at theta = 0 in the middle of each RR... Convention: each
    beat k occupies [t_k, t_k + rr_k) with theta rising from -pi to pi, so the R
    peak (theta = 0) is at t_k + rr_k / 2. Returns theta [T], R-peak times, beat index [T].
    """
    T = int(round(fs * duration))
    t = np.arange(T) / fs
    starts = np.concatenate([[0.0], np.cumsum(rr)])
    k = np.searchsorted(starts, t, side="right") - 1
    k = np.clip(k, 0, rr.size - 1)
    frac = (t - starts[k]) / rr[k]
    theta = -np.pi + 2 * np.pi * np.clip(frac, 0, 1)
    r_times = starts[:-1] + rr / 2.0
    r_times = r_times[r_times < duration]
    return theta, r_times, k


def add_noise_snr(x, snr_db, rng):
    p_sig = np.mean((x - x.mean()) ** 2)
    p_noise = p_sig / (10 ** (snr_db / 10))
    return x + rng.normal(0, np.sqrt(p_noise), x.shape)


def write_dataset(out_dir, sample_fn, n_train, n_val, n_test, fs, duration, seed, tag,
                  snr_levels=SNR_LEVELS_DB):
    """
    ``sample_fn(rng) -> (params: dict, x: np.ndarray, events: dict)``; ``events``
    holds JSON-serializable ground truth (peak times in seconds, amplitudes, ...).
    """
    rng = np.random.default_rng(seed)
    used = set()
    manifest = []
    for mode, n in [("train", n_train), ("val", n_val), ("test", n_test)]:
        d = os.path.join(out_dir, mode)
        os.makedirs(d, exist_ok=True)
        idx = 0
        while idx < n:
            params, x, events = sample_fn(rng)
            h = hashlib.md5(json.dumps(params, sort_keys=True).encode()).hexdigest()
            if h in used:
                continue
            used.add(h)
            name = f"{mode}_{idx:03d}_{tag}_{h[:10]}"
            t = np.arange(x.size) / fs
            pd.DataFrame({"Time": t, "Value": x.astype(np.float32)}).to_csv(os.path.join(d, name + ".csv"), index=False)
            json.dump({"params": params, "fs": fs, **events}, open(os.path.join(d, name + ".events.json"), "w"))
            if mode == "test":
                for lvl, db in snr_levels.items():
                    dn = os.path.join(out_dir, f"noise_SNR_{lvl}", "test")
                    os.makedirs(dn, exist_ok=True)
                    xn = add_noise_snr(x, db, rng)
                    pd.DataFrame({"Time": t, "Value": xn.astype(np.float32)}).to_csv(os.path.join(dn, name + ".csv"), index=False)
                    json.dump({"params": params, "fs": fs, "snr_db": db, **events},
                              open(os.path.join(dn, name + ".events.json"), "w"))
            manifest.append(dict(mode=mode, file=name + ".csv", **{k: v for k, v in params.items() if np.isscalar(v)}))
            idx += 1
    pd.DataFrame(manifest).to_csv(os.path.join(out_dir, "manifest.csv"), index=False)
    return manifest
