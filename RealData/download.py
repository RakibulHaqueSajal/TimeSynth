#!/usr/bin/env python3
"""
P1.1: download the real biosignal datasets (decision D1: all three modalities).

Every record is stored as one ``.npz`` under ``$TIMESYNTH_REAL/raw/<dataset>/``
with keys ``x`` (float32 signal), ``fs`` (Hz), ``channel`` and, where the source
provides them, ``events`` (structured array of natural events: activity changes,
AF onsets, sleep-stage changes) and ``beats`` (annotated beat sample indices).
``RealData/MANIFEST.md`` records the source, version, record list and SHA-256 of
each saved file.

Datasets (PhysioNet unless noted):
  bidmc      BIDMC PPG and Respiration, v1.0.0, 53 x 8 min, 125 Hz, PLETH channel
  nsrdb      MIT-BIH Normal Sinus Rhythm, v1.0.0, 18 x 24 h, 128 Hz, ECG1; first 45 min kept
  afdb       MIT-BIH Atrial Fibrillation, v1.0.0, 23 x 10 h, 250 Hz, ECG1; stable-N head
             plus +-150 s around each N -> AFIB onset
  sleepedfx  Sleep-EDF Expanded, v1.0.0, sleep-cassette, 100 Hz, Fpz-Cz; first night of the
             first 20 subjects, 2.5 h starting 15 min before sleep onset, hypnogram events
  dalia      PPG-DaLiA (UCI repository), 15 subjects, wrist BVP at 64 Hz, activity labels

Usage:  python RealData/download.py --datasets all [--root /path]
"""
from __future__ import annotations

import argparse
import hashlib
import io
import os
import pickle
import sys
import zipfile
from datetime import datetime

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.environ.get(
    "TIMESYNTH_REAL", "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_real")

VERSIONS = {"bidmc": "bidmc/1.0.0", "nsrdb": "nsrdb/1.0.0", "afdb": "afdb/1.0.0",
            "sleepedfx": "sleep-edfx/1.0.0", "dalia": "UCI ML repository id 495 (ppg+dalia.zip)"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def save(root, dataset, rec, **arrays):
    d = os.path.join(root, "raw", dataset)
    os.makedirs(d, exist_ok=True)
    fp = os.path.join(d, f"{rec}.npz")
    np.savez_compressed(fp, **arrays)
    return fp


def events_array(times_s, labels):
    return np.array(list(zip(times_s, labels)), dtype=[("t", "f8"), ("label", "U16")])


# ---------------------------------------------------------------------------
def dl_bidmc(root):
    import wfdb
    out = []
    for i in range(1, 54):
        rec = f"bidmc{i:02d}"
        fp = os.path.join(root, "raw", "bidmc", f"{rec}.npz")
        if os.path.exists(fp):
            out.append(fp); continue
        r = wfdb.rdrecord(rec, pn_dir=VERSIONS["bidmc"])
        names = [n.strip(", ") for n in r.sig_name]          # header has trailing commas
        ch = names.index("PLETH")
        x = r.p_signal[:, ch].astype(np.float32)
        ecg = r.p_signal[:, names.index("II")].astype(np.float32) if "II" in names else None
        arrays = dict(x=x, fs=float(r.fs), channel="PLETH", subject=rec)
        if ecg is not None:
            arrays["ecg_ii"] = ecg
        out.append(save(root, "bidmc", rec, **arrays))
        print("bidmc", rec, x.shape, r.fs, flush=True)
    return out


def dl_nsrdb(root, minutes=45):
    import wfdb
    recs = wfdb.get_record_list("nsrdb")
    out = []
    for rec in recs:
        fp = os.path.join(root, "raw", "nsrdb", f"{rec}.npz")
        if os.path.exists(fp):
            out.append(fp); continue
        n = int(128 * 60 * minutes)
        r = wfdb.rdrecord(rec, pn_dir=VERSIONS["nsrdb"], sampto=n)
        ann = wfdb.rdann(rec, "atr", pn_dir=VERSIONS["nsrdb"], sampto=n)
        x = r.p_signal[:, 0].astype(np.float32)
        beats = ann.sample[np.isin(ann.symbol, ["N", "L", "R", "A", "V", "F", "j", "e", "J", "S"])]
        out.append(save(root, "nsrdb", rec, x=x, fs=float(r.fs), channel=r.sig_name[0],
                        subject=rec, beats=beats.astype(np.int64)))
        print("nsrdb", rec, x.shape, r.fs, "beats", beats.size, flush=True)
    return out


def dl_afdb(root, head_minutes=20, half_window_s=150, max_onsets=5):
    import wfdb
    recs = wfdb.get_record_list("afdb")
    out = []
    for rec in recs:
        fp = os.path.join(root, "raw", "afdb", f"{rec}.npz")
        if os.path.exists(fp):
            out.append(fp); continue
        try:
            r = wfdb.rdrecord(rec, pn_dir=VERSIONS["afdb"])
        except Exception as e:      # 00735 and 03665 have no signal files
            print("afdb", rec, "skipped:", e, flush=True)
            continue
        ann = wfdb.rdann(rec, "atr", pn_dir=VERSIONS["afdb"])
        fs = float(r.fs)
        x = r.p_signal[:, 0].astype(np.float32)
        rhythm = [(s, a.strip("(")) for s, a in zip(ann.sample, ann.aux_note) if a.startswith("(")]
        # segments: stable head + windows around N -> AFIB onsets
        segs = []
        head = int(head_minutes * 60 * fs)
        first_af = next((s for s, a in rhythm if a == "AFIB"), None)
        head_end = min(head, first_af if first_af is not None else head)
        if head_end > int(60 * fs):
            segs.append(("head", 0, head_end, None))
        n_on = 0
        for k in range(1, len(rhythm)):
            if rhythm[k][1] == "AFIB" and rhythm[k - 1][1] == "N":
                s = rhythm[k][0]
                a, b = max(0, s - int(half_window_s * fs)), min(len(x), s + int(half_window_s * fs))
                if b - a >= int(2 * half_window_s * fs) - 1:
                    segs.append((f"onset{n_on}", a, b, s - a))
                    n_on += 1
                if n_on >= max_onsets:
                    break
        for name, a, b, onset in segs:
            ev = events_array([onset / fs], ["AF_onset"]) if onset is not None else events_array([], [])
            fpk = save(root, "afdb", f"{rec}_{name}", x=x[a:b], fs=fs, channel=r.sig_name[0],
                       subject=rec, events=ev, segment_start_sample=a)
            out.append(fpk)
        print("afdb", rec, "segments", [s[0] for s in segs], flush=True)
    return out


def dl_sleepedfx(root, n_subjects=20, hours=2.5, pre_onset_min=15):
    import mne
    import urllib.request
    base = "https://physionet.org/files/sleep-edfx/1.0.0/sleep-cassette/"
    listing = urllib.request.urlopen(base).read().decode()
    import re
    psg = sorted(set(re.findall(r"SC4(\d{2})1E0-PSG\.edf", listing)))[:n_subjects]   # first night (1) only
    out = []
    tmp = os.path.join(root, "raw", "sleepedfx", "_edf")
    os.makedirs(tmp, exist_ok=True)
    for ss in psg:
        rec = f"SC4{ss}1E0"
        fp = os.path.join(root, "raw", "sleepedfx", f"{rec}.npz")
        if os.path.exists(fp):
            out.append(fp); continue
        hyp_name = re.findall(rf"(SC4{ss}1E[A-Z]-Hypnogram\.edf)", listing)
        if not hyp_name:
            print("sleepedfx", rec, "no hypnogram", flush=True); continue
        p_psg, p_hyp = os.path.join(tmp, f"{rec}-PSG.edf"), os.path.join(tmp, hyp_name[0])
        for name, path in [(f"{rec}-PSG.edf", p_psg), (hyp_name[0], p_hyp)]:
            if not os.path.exists(path):
                urllib.request.urlretrieve(base + name, path)
        raw = mne.io.read_raw_edf(p_psg, include=["EEG Fpz-Cz"], preload=False, verbose="ERROR")
        ann = mne.read_annotations(p_hyp)
        fs = float(raw.info["sfreq"])
        # sleep onset = first epoch that is not W / ? / movement
        stages = [(a["onset"], a["duration"], a["description"].replace("Sleep stage ", "")) for a in ann]
        onset = next((t for t, d, s in stages if s in ("1", "2", "3", "4", "R")), None)
        if onset is None:
            print("sleepedfx", rec, "no sleep found", flush=True); continue
        t0 = max(0.0, onset - pre_onset_min * 60)
        t1 = min(raw.times[-1], t0 + hours * 3600)
        raw.crop(tmin=t0, tmax=t1).load_data(verbose="ERROR")
        x = raw.get_data()[0].astype(np.float32) * 1e6          # volts -> microvolts
        # stage-change events relative to the crop
        ev_t, ev_l, last = [], [], None
        for t, d, s in stages:
            if t0 <= t <= t1 and s != last:
                ev_t.append(t - t0); ev_l.append(f"stage_{s}"); last = s
        out.append(save(root, "sleepedfx", rec, x=x, fs=fs, channel="EEG Fpz-Cz", subject=f"SC4{ss}",
                        events=events_array(ev_t, ev_l), crop_start_s=t0))
        print("sleepedfx", rec, x.shape, fs, "stage changes", len(ev_t), flush=True)
    return out


def dl_dalia(root):
    import urllib.request
    url = "https://archive.ics.uci.edu/static/public/495/ppg+dalia.zip"
    zpath = os.path.join(root, "raw", "dalia", "ppg+dalia.zip")
    os.makedirs(os.path.dirname(zpath), exist_ok=True)
    if not os.path.exists(zpath):
        print("downloading PPG-DaLiA zip ...", flush=True)
        urllib.request.urlretrieve(url, zpath)
    out = []
    with zipfile.ZipFile(zpath) as z:
        names = [n for n in z.namelist() if n.endswith(".pkl")]
        inner = [n for n in z.namelist() if n.endswith(".zip")]
        if not names and inner:          # nested zip
            data = z.read(inner[0])
            z2 = zipfile.ZipFile(io.BytesIO(data))
            names, z = [n for n in z2.namelist() if n.endswith(".pkl")], z2
        for n in sorted(names):
            subj = os.path.basename(n).replace(".pkl", "")
            fp = os.path.join(root, "raw", "dalia", f"{subj}.npz")
            if os.path.exists(fp):
                out.append(fp); continue
            d = pickle.loads(z.read(n), encoding="latin1")
            bvp = np.asarray(d["signal"]["wrist"]["BVP"]).astype(np.float32).ravel()
            act = np.asarray(d["activity"]).ravel()
            # activity labels are given at 4 Hz; record change points in seconds
            act_fs = 4.0
            ch = np.flatnonzero(np.diff(act) != 0) + 1
            ev = events_array(ch / act_fs, [f"activity_{int(act[i])}" for i in ch])
            out.append(save(root, "dalia", subj, x=bvp, fs=64.0, channel="wrist_BVP", subject=subj,
                            events=ev, activity=act.astype(np.int16), activity_fs=act_fs))
            print("dalia", subj, bvp.shape, "activity changes", len(ch), flush=True)
    return out


DOWNLOADERS = {"bidmc": dl_bidmc, "nsrdb": dl_nsrdb, "afdb": dl_afdb, "sleepedfx": dl_sleepedfx, "dalia": dl_dalia}


def write_manifest(root, results):
    fp = os.path.join(HERE, "MANIFEST.md")
    lines = ["# Real-data manifest (P1.1)", "",
             f"Root: `{root}/raw/`. Generated {datetime.now():%Y-%m-%d %H:%M} by `RealData/download.py`.", ""]
    for ds, files in results.items():
        lines += [f"## {ds}", "", f"Source/version: `{VERSIONS[ds]}`  ", f"Records: {len(files)}", "",
                  "| file | samples | fs | sha256 |", "|---|---|---|---|"]
        for f in files:
            z = np.load(f, allow_pickle=False)
            lines.append(f"| {os.path.basename(f)} | {z['x'].shape[0]} | {float(z['fs']):g} | `{sha256(f)[:16]}` |")
        lines.append("")
    with open(fp, "w") as f:
        f.write("\n".join(lines))
    print("wrote", fp)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--datasets", nargs="+", default=["all"])
    ap.add_argument("--root", default=DEFAULT_ROOT)
    a = ap.parse_args()
    ds = list(DOWNLOADERS) if a.datasets == ["all"] else a.datasets
    results = {}
    for d in ds:
        results[d] = DOWNLOADERS[d](a.root)
    write_manifest(a.root, results)


if __name__ == "__main__":
    main()
