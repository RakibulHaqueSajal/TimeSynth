#!/usr/bin/env python3
"""
P1.2 / P1.3: preprocess the raw real recordings into the loader's CSV layout and
write subject-level splits.

Matched-cycles principle: the synthetic benchmark is 50 samples of history and
100 of horizon at 10 Hz for ~1 Hz rhythms. Real data are resampled so that the
same window holds about the same number of dominant cycles.

Track A (rhythm band):   bandpass around the dominant rhythm, resample
    PPG  0.5-4 Hz  -> 10 Hz        ECG 0.5-3 Hz -> 10 Hz        EEG 1-30 Hz -> 100 Hz
Track B (morphology, ECG and PPG only):  lowpass 20 Hz -> 50 Hz (windows 250 / 500, D5)

Artifact handling: the resampled recording is scanned in 5 s segments; segments
that are flat, contain non-finite values, or exceed 6 robust SDs (MAD) are
marked bad, and the recording is cut into contiguous clean chunks of at least
one window length. Each chunk becomes one CSV ``<subject>__<record>__c<k>.csv``
with columns ``Time`` (s) and ``Value``.

Normalization: z-score per recording with mean and SD of the first 20 % of the
recording (a calibration segment that would be available at deployment); no
statistics from the forecast targets of other subjects are used.

Splits (P1.3): by subject, 70/10/20 with a fixed seed, saved to
``RealData/splits/<dataset>.json``. Test windows are made non-overlapping by the
loader (eval_stride = seq_len + pred_len) and capped per file (max_windows_per_file).

Natural events (activity changes, AF onsets, sleep-stage changes) are written per
chunk as ``<chunk>.events.json`` in resampled seconds, for tagging in analysis.

Usage: python RealData/preprocess.py --dataset bidmc --track A [--root ...]
"""
from __future__ import annotations

import argparse
import json
import os
from fractions import Fraction

import numpy as np
import pandas as pd
from scipy.signal import butter, resample_poly, sosfiltfilt

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.environ.get(
    "TIMESYNTH_REAL", "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_real")

MODALITY = {"bidmc": "ppg", "dalia": "ppg", "nsrdb": "ecg", "afdb": "ecg", "sleepedfx": "eeg"}
TRACKS = {
    ("ppg", "A"): dict(band=(0.5, 4.0), fs_out=10.0, seq_len=50, pred_len=100),
    ("ecg", "A"): dict(band=(0.5, 3.0), fs_out=10.0, seq_len=50, pred_len=100),
    ("eeg", "A"): dict(band=(1.0, 30.0), fs_out=100.0, seq_len=50, pred_len=100),
    ("ppg", "B"): dict(band=(0.3, 20.0), fs_out=50.0, seq_len=250, pred_len=500),
    ("ecg", "B"): dict(band=(0.5, 20.0), fs_out=50.0, seq_len=250, pred_len=500),
}
SPLIT_FRACS = (0.7, 0.1, 0.2)
SEED = 0


# ---------------------------------------------------------------------------
def bandpass(x, fs, lo, hi, order=4):
    nyq = fs / 2.0
    hi = min(hi, 0.95 * nyq)
    sos = butter(order, [lo / nyq, hi / nyq], btype="band", output="sos")
    return sosfiltfilt(sos, x.astype(np.float64))


def resample(x, fs_in, fs_out):
    fr = Fraction(fs_out / fs_in).limit_denominator(1000)
    return resample_poly(x, fr.numerator, fr.denominator)


def bad_segments(x, fs, seg_s=5.0, z_thresh=6.0):
    """Boolean mask over samples: True where the 5 s segment is an artifact."""
    n = int(seg_s * fs)
    med = np.median(x)
    mad = np.median(np.abs(x - med)) * 1.4826 + 1e-12
    bad = np.zeros(x.size, bool)
    for s in range(0, x.size, n):
        seg = x[s:s + n]
        if seg.size < n // 2:
            bad[s:] = True
            break
        if (not np.all(np.isfinite(seg))) or seg.std() < 1e-6 * (mad + 1e-12) \
                or np.max(np.abs(seg - med)) > z_thresh * mad:
            bad[s:s + n] = True
    return bad


def clean_chunks(x, bad, min_len):
    """Contiguous runs of clean samples of at least min_len."""
    out = []
    i = 0
    n = x.size
    while i < n:
        if bad[i]:
            i += 1
            continue
        j = i
        while j < n and not bad[j]:
            j += 1
        if j - i >= min_len:
            out.append((i, j))
        i = j
    return out


def make_windows(signal, fs, seq_len, pred_len, stride):
    """Shared window enumerator (also used by Tier 2 tests): returns start indices."""
    L = seq_len + pred_len
    return np.arange(0, signal.size - L + 1, stride, dtype=int)


def calib_zscore(x, frac=0.2):
    n = max(int(frac * x.size), 10)
    mu, sd = float(np.mean(x[:n])), float(np.std(x[:n]))
    if sd < 1e-8:
        sd = float(np.std(x)) + 1e-8
    return (x - mu) / sd, mu, sd


# ---------------------------------------------------------------------------
def load_raw(root, dataset):
    d = os.path.join(root, "raw", dataset)
    files = sorted(f for f in os.listdir(d) if f.endswith(".npz"))
    for f in files:
        z = np.load(os.path.join(d, f), allow_pickle=False)
        yield f[:-4], z


def subjects_of(dataset, records):
    subs = {}
    for rec, z in records:
        subs.setdefault(str(z["subject"]), []).append(rec)
    return subs


def make_splits(dataset, subject_list, seed=SEED):
    rng = np.random.default_rng(seed)
    subs = sorted(subject_list)
    perm = list(rng.permutation(subs))
    n = len(perm)
    n_train = int(round(SPLIT_FRACS[0] * n))
    n_val = max(1, int(round(SPLIT_FRACS[1] * n)))
    n_test = n - n_train - n_val
    if n_test < 1:
        n_test, n_train = 1, n_train - 1
    return {"seed": seed, "fractions": SPLIT_FRACS,
            "train": perm[:n_train], "val": perm[n_train:n_train + n_val], "test": perm[n_train + n_val:]}


def process(root, dataset, track):
    mod = MODALITY[dataset]
    if (mod, track) not in TRACKS:
        raise SystemExit(f"no track {track} for {mod}")
    cfg = TRACKS[(mod, track)]
    fs_out, L = cfg["fs_out"], cfg["seq_len"] + cfg["pred_len"]
    out_root = os.path.join(root, "processed", f"{dataset}_{track}")
    records = list(load_raw(root, dataset))
    subs = subjects_of(dataset, records)

    split_fp = os.path.join(HERE, "splits", f"{dataset}.json")
    os.makedirs(os.path.dirname(split_fp), exist_ok=True)
    if os.path.exists(split_fp):
        splits = json.load(open(split_fp))
    else:
        splits = make_splits(dataset, list(subs))
        json.dump(splits, open(split_fp, "w"), indent=1)
    sub2split = {s: k for k in ("train", "val", "test") for s in splits[k]}

    stats = []
    for rec, z in records:
        x, fs = z["x"].astype(np.float64), float(z["fs"])
        subj = str(z["subject"])
        split = sub2split.get(subj)
        if split is None:
            continue
        y = bandpass(x, fs, *cfg["band"])
        y = resample(y, fs, fs_out)
        y, mu, sd = calib_zscore(y)
        bad = bad_segments(y, fs_out)
        chunks = clean_chunks(y, bad, min_len=L)
        events = z["events"] if "events" in z.files else None
        split_dir = os.path.join(out_root, split)
        os.makedirs(split_dir, exist_ok=True)
        for k, (a, b) in enumerate(chunks):
            name = f"{subj}__{rec}__c{k}"
            t = np.arange(b - a) / fs_out
            pd.DataFrame({"Time": t, "Value": y[a:b].astype(np.float32)}).to_csv(
                os.path.join(split_dir, name + ".csv"), index=False)
            ev = []
            if events is not None and len(events):
                for e in events:
                    te = float(e["t"]) - a / fs_out
                    if 0 <= te <= (b - a) / fs_out:
                        ev.append({"t": te, "label": str(e["label"])})
            json.dump({"subject": subj, "record": rec, "chunk": k, "fs": fs_out,
                       "chunk_start_s": a / fs_out, "events": ev, "calib_mean": mu, "calib_sd": sd},
                      open(os.path.join(split_dir, name + ".events.json"), "w"))
        stats.append(dict(record=rec, subject=subj, split=split, fs_in=fs, fs_out=fs_out,
                          n_in=x.size, n_out=y.size, bad_frac=float(bad.mean()), n_chunks=len(chunks),
                          n_windows_nonoverlap=int(sum((b - a) // L for a, b in chunks))))
        print(f"{dataset}/{track} {rec} [{split}] chunks={len(chunks)} bad={bad.mean():.1%}", flush=True)
    df = pd.DataFrame(stats)
    df.to_csv(os.path.join(out_root, "preprocess_stats.csv"), index=False)
    print(df.groupby("split")[["n_chunks", "n_windows_nonoverlap"]].sum())
    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True, choices=list(MODALITY) + ["all"])
    ap.add_argument("--track", default="A", choices=["A", "B"])
    ap.add_argument("--root", default=DEFAULT_ROOT)
    a = ap.parse_args()
    ds = list(MODALITY) if a.dataset == "all" else [a.dataset]
    for d in ds:
        if (MODALITY[d], a.track) in TRACKS:
            process(a.root, d, a.track)


if __name__ == "__main__":
    main()
