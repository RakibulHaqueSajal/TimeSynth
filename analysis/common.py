"""
Shared loader for the revision result layout (results/{paradigm}/{signal}/{model}/seed{k}/).

``load_paradigm`` returns one DataFrame with a row per test window and columns:
    paradigm, condition, signal, model, seed, file_id, file_name, window_start, unit,
    mae, mse, a_rms, phase, freq, [band_power, xcorr_lag, peak_timing, peak_amp, peak_f1, rr_err,
    crps], plus paradigm-specific tags:
    - state_transition: t_star (samples), tag in {H_dk, F_dk, none}: transition inside the history
      (d samples before the forecast boundary) or inside the horizon (d samples after it)
    - markov_dwell: D (dwell time, from the file name)
    - real_*: subject (unit), natural-event tag: event label inside the horizon, if any
    - tier2_*: exact ground-truth peak indices are used for the peak metrics
Everything is cached as parquet under analysis/cache/.
"""
from __future__ import annotations

import glob
import json
import os
import re
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys  # noqa: E402
sys.path.insert(0, REPO)
from utils import fidelity as F                     # noqa: E402
from utils.config import DEFAULT_DATA_ROOT, DEFAULT_REAL_ROOT, load_bias_groups, load_yaml, paradigm_config_path  # noqa: E402
from utils.results_io import load_result             # noqa: E402

RESULTS_ROOT = os.environ.get("TIMESYNTH_RESULTS",
                              "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/results")
CACHE = os.path.join(REPO, "analysis", "cache")
BAND = {"ppg": (0.5, 4.0), "ecg": (0.5, 3.0), "eeg": (1.0, 30.0)}


def bias() -> Dict:
    return load_bias_groups()


def _events_sidecar(paradigm: str, signal: str, condition: Optional[str], file_name: str) -> Optional[dict]:
    """Locate <file>.events.json next to the test CSV that produced a window."""
    cfg = load_yaml(paradigm_config_path(paradigm.split("__")[0]))
    root = cfg.get("data_root")
    if root:
        from utils.config import _expand
        root = _expand(root)
    else:
        root = DEFAULT_DATA_ROOT
    base = os.path.join(root, cfg.get("data_root_rel", ""))
    sub = cfg["signals"][signal]
    if condition:
        spec = cfg.get("conditions", {}).get(condition)
        sub = spec[signal] if isinstance(spec, dict) else spec.format(signal=sub)
    fp = os.path.join(base, sub, "test", file_name[:-4] + ".events.json")
    return json.load(open(fp)) if os.path.exists(fp) else None


def _transition_table(paradigm: str, signal: str) -> Optional[pd.DataFrame]:
    cfg = load_yaml(paradigm_config_path(paradigm))
    d = os.path.join(DEFAULT_DATA_ROOT, cfg.get("data_root_rel", ""), cfg["signals"][signal])
    fp = os.path.join(d, "test_transitions.csv")
    return pd.read_csv(fp) if os.path.exists(fp) else None


def window_metrics(hist, true, pred, fs: float, meta: pd.DataFrame, samples=None,
                   peak_truth: Optional[List[np.ndarray]] = None, band=None, do_peaks=False) -> pd.DataFrame:
    tc = true - true.mean(axis=1, keepdims=True)
    out = pd.DataFrame({
        "mae": F.mae(pred, true), "mse": F.mse(pred, true),
        "a_rms": np.sqrt(np.mean(tc ** 2, axis=1)),
        "phase": F.phase_error_deg(pred, true), "freq": F.freq_error(pred, true, fs=fs),
    })
    if band is not None:
        out["band_power"] = F.band_power_error(pred, true, fs, band)
        out["xcorr_lag"] = F.xcorr_lag(pred, true, fs, max_lag_s=2.0)
    if do_peaks:
        kw = dict(true_peaks=peak_truth) if peak_truth is not None else {}
        det = dict(min_dist_s=0.3, prominence_frac=0.3)
        out["peak_timing"] = F.peak_timing_error(pred, true, fs, tol_s=0.05, detector_kwargs=det, **kw)
        out["peak_amp"] = F.peak_amplitude_error(pred, true, fs, tol_s=0.05, detector_kwargs=det, **kw)
        out["peak_f1"] = F.peak_detection_f1(pred, true, fs, tol_s=0.05, detector_kwargs=det, **kw)
        out["rr_err"] = F.rr_interval_error(pred, true, fs, detector_kwargs=det, **kw)
    if samples is not None:
        out["crps"] = F.crps_empirical(samples, true)
    return out


def _peak_truth_for(meta: pd.DataFrame, paradigm: str, signal: str, condition: Optional[str], fs: float) -> Optional[List[np.ndarray]]:
    """Exact peak indices per window from Tier 2 sidecars (r_peak_times / peak_times), horizon-relative."""
    cache = {}
    out = []
    L = int(meta.seq_len.iloc[0])
    for fn, ws in zip(meta.file_name, meta.window_start):
        if fn not in cache:
            ev = _events_sidecar(paradigm, signal, condition, fn)
            times = None
            if ev is not None:
                times = ev.get("r_peak_times") or ev.get("peak_times")
            cache[fn] = np.asarray(times, float) if times is not None else None
        t = cache[fn]
        if t is None:
            return None
        idx = np.round(t * fs).astype(int) - (ws + L)
        out.append(idx[(idx >= 0) & (idx < int(meta.pred_len.iloc[0]))])
    return out


def _tag_state_transition(meta: pd.DataFrame, tt: pd.DataFrame) -> pd.DataFrame:
    tstar = dict(zip(tt.filename, tt.t_star_idx))
    L, H = int(meta.seq_len.iloc[0]), int(meta.pred_len.iloc[0])
    ts = meta.file_name.map(tstar)
    rel = ts - (meta.window_start + L)                 # samples after the forecast boundary
    tag = np.where((rel > -L) & (rel <= 0), "H_d" + (-rel).astype("Int64").astype(str),
                   np.where((rel > 0) & (rel <= H), "F_d" + rel.astype("Int64").astype(str), "none"))
    meta = meta.copy()
    meta["t_star"] = ts.values
    meta["rel_transition"] = rel.values
    meta["tag"] = tag
    return meta


def _tag_real_events(meta: pd.DataFrame, paradigm: str, signal: str, condition: Optional[str], fs: float) -> pd.DataFrame:
    meta = meta.copy()
    meta["subject"] = meta.file_name.str.split("__").str[0]
    meta["unit"] = meta["subject"]
    L, H = int(meta.seq_len.iloc[0]), int(meta.pred_len.iloc[0])
    cache, tags = {}, []
    for fn, ws in zip(meta.file_name, meta.window_start):
        if fn not in cache:
            ev = _events_sidecar(paradigm, signal, condition, fn)
            cache[fn] = ev["events"] if ev else []
        t0, t1 = (ws + L) / fs, (ws + L + H) / fs
        lab = [e["label"] for e in cache[fn] if t0 <= e["t"] < t1]
        tags.append(lab[0] if lab else "")
    meta["event_in_horizon"] = tags
    return meta


def load_paradigm(paradigm: str, results_root: str = RESULTS_ROOT, force: bool = False) -> pd.DataFrame:
    """All results under results/<paradigm>[__cond]/*/*/seed*/ as one per-window table."""
    os.makedirs(CACHE, exist_ok=True)
    frames = []
    for run in sorted(glob.glob(os.path.join(results_root, paradigm + "*", "*", "*", "seed*"))):
        if not os.path.exists(os.path.join(run, "pred.npy")):
            continue
        rel = os.path.relpath(run, results_root).split(os.sep)
        pname, signal, model, seed_s = rel
        condition = pname.split("__")[1] if "__" in pname else None
        cp = os.path.join(CACHE, f"{pname}_{signal}_{model}_{seed_s}.parquet")
        if os.path.exists(cp) and not force and os.path.getmtime(cp) > os.path.getmtime(os.path.join(run, "pred.npy")):
            frames.append(pd.read_parquet(cp))
            continue
        res = load_result(run)
        hist, true, pred, meta = res[:4]
        samples = res[4] if len(res) > 4 else None
        fs = float(meta.fs.iloc[0])
        base = paradigm.split("__")[0]
        is_real, is_tier2 = base.startswith("real_"), base.startswith("tier2_")
        band = BAND[base.split("_")[1]] if is_real else None
        peak_truth = _peak_truth_for(meta, base, signal, condition, fs) if is_tier2 else None
        do_peaks = is_tier2 or (is_real and base.split("_")[1] in ("ppg", "ecg"))
        met = window_metrics(hist, true, pred, fs, meta, samples, peak_truth, band, do_peaks)
        df = pd.concat([meta.reset_index(drop=True), met], axis=1)
        df["paradigm"], df["condition"], df["signal"], df["model"], df["seed"] = base, condition or "", signal, model, int(seed_s[4:])
        df["unit"] = df["file_id"]
        if base == "state_transition":
            tt = _transition_table(base, signal)
            if tt is not None:
                df = _tag_state_transition(df, tt)
        if base == "markov_dwell":
            df["D"] = df.file_name.str.extract(r"_D_([0-9.]+)_")[0].astype(float)
        if is_real:
            df = _tag_real_events(df, base, signal, condition, fs)
        df.to_parquet(cp, index=False)
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)
