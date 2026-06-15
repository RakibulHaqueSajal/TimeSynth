#!/usr/bin/env python3
"""
Single-state-transition statistical tests (tag-wise, paired within tag) + adaptation tests.

Assumptions (matches what you said):
- For a FIXED tag, the SAME sequences are evaluated for ALL models (pairing is valid).
- Different tags can have different N (that's fine).
- Some metrics (freq/phase) can produce NaNs per-sequence; we handle that by intersecting
  finite entries per (tag, model vs baseline).

What this script outputs (per metric):
1) Tag-wise paired tests vs baseline (Wilcoxon signed-rank; normal approx w/ tie correction)
   - one CSV per metric: tag | model | n_used | median_model | median_baseline | median_delta | p | p_holm
2) Adaptation tests across HIST tags:
   - per model: slope of (median error) vs distance for hist_dXX
   - bootstrap CI + p-value for slope difference vs baseline
   - one CSV per metric: model | slope | ci_lo | ci_hi | delta_vs_base | p | p_holm

You can run all families at once.
"""

import os
import math
import json
import csv
from typing import Dict, List, Tuple, Optional, Any

import numpy as np
import pandas as pd


# -------------------------
# Basic utils
# -------------------------
def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)


def _tag_distance(tag: str):
    # returns (kind, dist) where kind in {"hist","fut","none"}
    if tag.startswith("hist_d"):
        return "hist", int(tag.split("hist_d")[1])
    if tag.startswith("fut_d"):
        return "fut", int(tag.split("fut_d")[1])
    return "none", None


def holm_adjust(pvals: np.ndarray) -> np.ndarray:
    """Holm-Bonferroni adjustment."""
    pvals = np.asarray(pvals, float)
    m = pvals.size
    order = np.argsort(pvals)
    adj = np.empty(m, float)
    prev = 0.0
    for k, idx in enumerate(order):
        mult = (m - k)
        val = min(1.0, mult * pvals[idx])
        val = max(val, prev)
        adj[idx] = val
        prev = val
    return adj


def _norm_cdf(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2)))


# -------------------------
# Tag-wise file loading
# -------------------------
def _resolve_tag_file(model_path: str, tag: str, kind: str) -> str:
    """
    kind: "true_with_history" or "pred_with_history"
    Tries:
      tag_{tag}_{kind}.npy
      tag_{tag}__{kind}.npy  (double underscore)
    """
    cands = [
        os.path.join(model_path, f"tag_{tag}_{kind}.npy"),
        os.path.join(model_path, f"tag_{tag}__{kind}.npy"),
    ]
    for fp in cands:
        if os.path.exists(fp):
            return fp
    raise FileNotFoundError(
        f"Missing tag files for tag={tag} in {model_path}.\nTried:\n  " + "\n  ".join(cands)
    )


def _load_true_pred_with_history(model_path: str, split: str, tag: Optional[str]):
    if tag is None:
        true_fp = os.path.join(model_path, f"{split}_true_with_history.npy")
        pred_fp = os.path.join(model_path, f"{split}_pred_with_history.npy")
        if (not os.path.exists(true_fp)) or (not os.path.exists(pred_fp)):
            raise FileNotFoundError(f"Missing split files: {true_fp} or {pred_fp}")
    else:
        true_fp = _resolve_tag_file(model_path, tag, "true_with_history")
        pred_fp = _resolve_tag_file(model_path, tag, "pred_with_history")

    true = np.load(true_fp)
    pred = np.load(pred_fp)

    if true.ndim == 3:
        true = true.squeeze(-1)
    if pred.ndim == 3:
        pred = pred.squeeze(-1)
    return true, pred


# -------------------------
# Metrics (per-sequence, tag-aware)
# -------------------------
def per_series_mae(model_path: str, history_len: int, tag: str, split="test") -> np.ndarray:
    true, pred = _load_true_pred_with_history(model_path, split=split, tag=tag)
    Y = true[:, history_len:]
    YH = pred[:, history_len:]
    return np.mean(np.abs(YH - Y), axis=1)


def _peak_freq_rfft_with_confidence(
    x,
    fs: float,
    drop_dc: bool = True,
    parabolic: bool = True,
    peak_frac_thresh: float = 0.1,
    power_thresh: float = 1e-8,
):
    x = np.asarray(x, float)
    x = x - x.mean()
    n = len(x)
    if n <= 2:
        return 0.0, False
    X = np.fft.rfft(x, n=n)
    P = (np.abs(X) ** 2).astype(float)
    f = np.fft.rfftfreq(n, d=1.0 / fs)

    start = 1 if drop_dc else 0
    total_power = P[start:].sum()
    if total_power <= power_thresh:
        return 0.0, False

    k = start + int(np.argmax(P[start:]))

    if (not parabolic) or k == 0 or k == len(P) - 1:
        f_est = f[k]
    else:
        denom = (P[k - 1] - 2 * P[k] + P[k + 1])
        delta = 0.0 if abs(denom) < 1e-12 else 0.5 * (P[k - 1] - P[k + 1]) / denom
        f_est = (k + delta) * (fs / n)

    peak_power = P[k]
    frac = peak_power / total_power if total_power > 0 else 0.0
    reliable = frac >= peak_frac_thresh
    return float(f_est), bool(reliable)


def per_series_freq_error(
    model_path: str,
    history_len: int,
    fs: float,
    tag: str,
    split="test",
    peak_frac_thresh=0.1,
    power_thresh=1e-8,
) -> np.ndarray:
    true, pred = _load_true_pred_with_history(model_path, split=split, tag=tag)
    Y = true[:, history_len:]
    YH = pred[:, history_len:]
    N = Y.shape[0]
    out = np.full(N, np.nan, float)
    for i in range(N):
        f_t, ok_t = _peak_freq_rfft_with_confidence(
            Y[i], fs=fs, peak_frac_thresh=peak_frac_thresh, power_thresh=power_thresh
        )
        f_p, ok_p = _peak_freq_rfft_with_confidence(
            YH[i], fs=fs, peak_frac_thresh=peak_frac_thresh, power_thresh=power_thresh
        )
        if ok_t and ok_p:
            out[i] = abs(f_p - f_t)
    return out


def _analytic_signal_fft(x, pad_factor=2):
    x = np.asarray(x, float)
    n = x.size
    x = x - x.mean()
    pad_factor = 1 if (pad_factor is None or pad_factor < 1) else int(pad_factor)
    n_fft = int(pad_factor * n)
    X = np.fft.fft(x, n=n_fft)
    H = np.zeros(n_fft, float)
    if n_fft % 2 == 0:
        H[0] = 1.0
        H[n_fft // 2] = 1.0
        H[1:n_fft // 2] = 2.0
    else:
        H[0] = 1.0
        H[1:(n_fft + 1) // 2] = 2.0
    z_full = np.fft.ifft(X * H, n=n_fft)
    return z_full[:n]


def _wrap_to_pi(ang):
    ang = np.asarray(ang, float)
    ang_unwrapped = np.unwrap(ang)
    return (ang_unwrapped + np.pi) % (2 * np.pi) - np.pi


def per_series_phase_error(
    model_path: str,
    history_len: int,
    tag: str,
    unit: str = "deg",
    split="test",
    amp_frac_thresh: float = 0.2,
) -> np.ndarray:
    true, pred = _load_true_pred_with_history(model_path, split=split, tag=tag)
    Y = true[:, history_len:]
    YH = pred[:, history_len:]
    N = Y.shape[0]
    out = np.full(N, np.nan, float)
    to_unit = (lambda a: a) if unit == "rad" else (lambda a: np.degrees(a))

    for i in range(N):
        y = Y[i] - Y[i].mean()
        yh = YH[i] - YH[i].mean()
        zt = _analytic_signal_fft(y)
        zp = _analytic_signal_fft(yh)

        At = np.abs(zt)
        med_amp = np.median(At)
        if not np.isfinite(med_amp) or med_amp == 0:
            continue

        mask = At > (amp_frac_thresh * med_amp)
        if not np.any(mask):
            continue

        phi_t = np.unwrap(np.angle(zt))
        phi_p = np.unwrap(np.angle(zp))
        dphi = _wrap_to_pi(phi_p - phi_t)

        sel = dphi[mask]
        if sel.size == 0:
            continue

        out[i] = float(np.mean(np.abs(to_unit(sel))))
    return out


def compute_metric_vector(
    metric: str,
    model_path: str,
    history_len: int,
    fs: float,
    phase_unit: str,
    tag: str,
) -> np.ndarray:
    if metric == "mae":
        return per_series_mae(model_path, history_len=history_len, tag=tag)
    if metric == "freq":
        return per_series_freq_error(model_path, history_len=history_len, fs=fs, tag=tag)
    if metric == "phase":
        return per_series_phase_error(model_path, history_len=history_len, tag=tag, unit=phase_unit)
    raise ValueError(metric)


# -------------------------
# Registry helper
# -------------------------
def build_models_for_signal(
    REGISTRY: Dict[str, Dict[str, List[Tuple[str, str]]]],
    signal: str,
    families: List[str],
) -> Dict[str, str]:
    """
    Return {family: path} for a single signal. Picks the first entry per family.
    """
    if signal not in REGISTRY:
        raise KeyError(f"signal not in REGISTRY: {signal}")
    fam_to_path = {}
    for fam in families:
        runs = REGISTRY[signal].get(fam, [])
        if not runs:
            continue
        fam_to_path[fam] = runs[0][1]
    return fam_to_path


# -------------------------
# Paired Wilcoxon signed-rank (normal approximation)
# -------------------------
def _rankdata_average_ties(x: np.ndarray) -> np.ndarray:
    """
    Ranks (1..n) with average ranks for ties. Pure numpy.
    """
    x = np.asarray(x, float)
    n = x.size
    order = np.argsort(x, kind="mergesort")
    ranks = np.empty(n, float)

    i = 0
    while i < n:
        j = i
        while j + 1 < n and x[order[j + 1]] == x[order[i]]:
            j += 1
        # average rank in [i+1, j+1]
        r = 0.5 * ((i + 1) + (j + 1))
        ranks[order[i : j + 1]] = r
        i = j + 1
    return ranks


def wilcoxon_signed_rank_normal(d: np.ndarray) -> Tuple[float, float]:
    """
    Two-sided Wilcoxon signed-rank test (paired) using normal approximation with tie correction.

    Input:
      d = (x - y) differences

    Returns:
      z, p_value

    Notes:
    - Removes zeros.
    - Uses W+ (sum of ranks of positive diffs).
    - Tie correction on variance by counting ties in |d|.
    """
    d = np.asarray(d, float)
    d = d[np.isfinite(d)]
    if d.size == 0:
        return np.nan, np.nan

    # remove zeros
    d = d[d != 0]
    n = d.size
    if n < 5:
        # too small: return NaNs (or you can still do exact, but we keep it simple)
        return np.nan, np.nan

    absd = np.abs(d)
    ranks = _rankdata_average_ties(absd)

    Wpos = float(np.sum(ranks[d > 0]))
    # mean / var under H0
    mu = n * (n + 1) / 4.0

    # tie correction for variance
    # var = n(n+1)(2n+1)/24 - sum(t^3 - t)/48 over tie groups in absd
    var = n * (n + 1) * (2 * n + 1) / 24.0

    # compute tie groups sizes in absd
    abs_sorted = np.sort(absd)
    tie_sum = 0.0
    i = 0
    while i < n:
        j = i
        while j + 1 < n and abs_sorted[j + 1] == abs_sorted[i]:
            j += 1
        t = (j - i + 1)
        if t > 1:
            tie_sum += (t**3 - t)
        i = j + 1

    var -= tie_sum / 48.0
    if var <= 0 or not np.isfinite(var):
        return np.nan, np.nan

    # continuity correction (optional)
    cc = 0.5 * np.sign(Wpos - mu)
    z = (Wpos - mu - cc) / math.sqrt(var)
    p = 2.0 * (1.0 - _norm_cdf(abs(z)))
    return float(z), float(p)


# -------------------------
# Tag-wise paired tests vs baseline
# -------------------------
def run_tagwise_paired_tests(
    REGISTRY: Dict[str, Dict[str, List[Tuple[str, str]]]],
    signal: str,
    families: List[str],
    baseline: str,
    tags: List[str],
    metric: str,
    history_len: int,
    fs: float,
    phase_unit: str,
    out_csv: str,
    out_json: str,
    require_common_valid: bool = True,
):
    """
    For each tag:
      - compute per-seq metric vectors for baseline + each model
      - paired test across sequences (Wilcoxon signed-rank) on d = model - baseline
      - Holm correction across models WITHIN THAT TAG

    require_common_valid=True:
      - use intersection of finite indices for (baseline, model) within each tag.
      - (recommended) ensures valid pairing.
    """
    fam_to_path = build_models_for_signal(REGISTRY, signal, families)
    if baseline not in fam_to_path:
        raise RuntimeError(f"Baseline '{baseline}' missing. Available: {sorted(fam_to_path.keys())}")

    ensure_dir(os.path.dirname(out_csv))

    all_rows = []
    summary = {
        "signal": signal,
        "metric": metric,
        "baseline": baseline,
        "tags": tags,
        "models": [f for f in families if f in fam_to_path],
        "require_common_valid": require_common_valid,
    }

    for tag in tags:
        # baseline vector
        b = compute_metric_vector(metric, fam_to_path[baseline], history_len, fs, phase_unit, tag)
        b = np.asarray(b, float)

        tmp_rows = []
        pvals = []
        models_in_tag = []

        for fam in families:
            if fam == baseline:
                continue
            if fam not in fam_to_path:
                continue

            x = compute_metric_vector(metric, fam_to_path[fam], history_len, fs, phase_unit, tag)
            x = np.asarray(x, float)

            # If N differs, that's not "pairing". You said they match, so treat as error.
            if x.shape[0] != b.shape[0]:
                raise RuntimeError(
                    f"N mismatch in tag={tag}: baseline {b.shape[0]} vs {fam} {x.shape[0]}"
                )

            if require_common_valid:
                ok = np.isfinite(b) & np.isfinite(x)
                bb = b[ok]
                xx = x[ok]
            else:
                bb = b[np.isfinite(b)]
                xx = x[np.isfinite(x)]
                # not paired anymore -> not what you want; keep common_valid=True.

            n_used = int(bb.size)
            if n_used < 5:
                z, p = np.nan, np.nan
                med_delta = np.nan
            else:
                d = xx - bb
                med_delta = float(np.median(d))
                z, p = wilcoxon_signed_rank_normal(d)

            row = dict(
                tag=tag,
                model=fam,
                baseline=baseline,
                n_used=n_used,
                median_model=float(np.nanmedian(xx)) if n_used else np.nan,
                median_baseline=float(np.nanmedian(bb)) if n_used else np.nan,
                median_delta=med_delta,
                z_wilcoxon=z,
                p_value=p,
            )
            tmp_rows.append(row)
            pvals.append(p)
            models_in_tag.append(fam)

        # Holm within this tag
        pvals = np.asarray(pvals, float)
        pholm = np.full_like(pvals, np.nan)
        finite = np.isfinite(pvals)
        if np.any(finite):
            pholm[finite] = holm_adjust(pvals[finite])

        for r, ph in zip(tmp_rows, pholm):
            r["p_holm"] = float(ph) if np.isfinite(ph) else np.nan
            all_rows.append(r)

        # add baseline reference row (optional)
        base_ok = np.isfinite(b)
        all_rows.append(dict(
            tag=tag,
            model=baseline,
            baseline=baseline,
            n_used=int(np.sum(base_ok)),
            median_model=float(np.nanmedian(b[base_ok])) if np.any(base_ok) else np.nan,
            median_baseline=float(np.nanmedian(b[base_ok])) if np.any(base_ok) else np.nan,
            median_delta=0.0,
            z_wilcoxon=np.nan,
            p_value=np.nan,
            p_holm=np.nan,
        ))

    df = pd.DataFrame(all_rows)
    df.to_csv(out_csv, index=False)
    with open(out_json, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"✓ wrote tag-wise paired-test CSV: {out_csv}")
    print(f"✓ wrote tag-wise config JSON:    {out_json}")


# -------------------------
# Adaptation test across HIST tags (bootstrap on medians per tag)
# -------------------------
def _fit_slope(xs: np.ndarray, ys: np.ndarray) -> float:
    xs = np.asarray(xs, float)
    ys = np.asarray(ys, float)
    ok = np.isfinite(xs) & np.isfinite(ys)
    xs, ys = xs[ok], ys[ok]
    if xs.size < 2:
        return np.nan
    x0 = xs.mean()
    y0 = ys.mean()
    denom = np.sum((xs - x0) ** 2)
    if denom <= 0:
        return np.nan
    return float(np.sum((xs - x0) * (ys - y0)) / denom)


def run_hist_adaptation_slope_bootstrap(
    REGISTRY: Dict[str, Dict[str, List[Tuple[str, str]]]],
    signal: str,
    families: List[str],
    baseline: str,
    tags: List[str],
    metric: str,
    history_len: int,
    fs: float,
    phase_unit: str,
    out_csv: str,
    out_json: str,
    B: int = 2000,
    seed: int = 0,
    require_common_valid_per_tag: bool = True,
):
    """
    Build adaptation slope per model using HIST tags only:
      slope_m = slope( median(error_m,tag) vs distance(tag) )

    Bootstrap:
      For each bootstrap replicate:
        - for each hist tag:
            resample sequence errors WITH replacement (within that tag)
            compute median
        - compute slope replicate
      Compare delta slope (model - baseline) distribution to get:
        - 95% CI on slope
        - p-value for delta vs 0 (two-sided)

    Note:
    - Tags can have different N; bootstrap is performed within each tag separately.
    - If freq/phase have NaNs, we intersect finite per (tag, model vs baseline)
      so comparisons remain fair.
    """
    rng = np.random.default_rng(seed)
    fam_to_path = build_models_for_signal(REGISTRY, signal, families)
    if baseline not in fam_to_path:
        raise RuntimeError(f"Baseline '{baseline}' missing. Available: {sorted(fam_to_path.keys())}")

    hist_tags = [t for t in tags if _tag_distance(t)[0] == "hist"]
    if len(hist_tags) < 2:
        raise ValueError("Need at least 2 hist_dXX tags to fit slope.")

    xs = np.array([_tag_distance(t)[1] for t in hist_tags], float)

    # Preload per-tag arrays for baseline and each model
    # data[fam][k] = vector of per-seq errors for hist_tags[k] (paired subset if requested)
    data: Dict[str, List[np.ndarray]] = {}

    # load baseline first
    base_vecs = []
    for t in hist_tags:
        b = compute_metric_vector(metric, fam_to_path[baseline], history_len, fs, phase_unit, t)
        base_vecs.append(np.asarray(b, float))
    data[baseline] = base_vecs

    # load each model and (optionally) pair mask per tag with baseline
    for fam in families:
        if fam not in fam_to_path:
            continue
        vecs = []
        for k, t in enumerate(hist_tags):
            x = compute_metric_vector(metric, fam_to_path[fam], history_len, fs, phase_unit, t)
            x = np.asarray(x, float)

            b = data[baseline][k]
            if x.shape[0] != b.shape[0]:
                raise RuntimeError(f"N mismatch in hist tag={t}: baseline {b.shape[0]} vs {fam} {x.shape[0]}")

            if require_common_valid_per_tag:
                ok = np.isfinite(b) & np.isfinite(x)
                # keep paired subset (same indices) for BOTH
                vecs.append(x[ok])
            else:
                vecs.append(x[np.isfinite(x)])
        data[fam] = vecs

    # helper: compute slope from these vectors (median per tag)
    def slope_from_vecs(vecs: List[np.ndarray]) -> float:
        meds = []
        for v in vecs:
            v = np.asarray(v, float)
            v = v[np.isfinite(v)]
            meds.append(float(np.median(v)) if v.size else np.nan)
        return _fit_slope(xs, np.array(meds, float))

    # point estimates
    slope_hat = {fam: slope_from_vecs(data[fam]) for fam in data.keys()}

    # bootstrap slopes
    boot = {fam: np.full(B, np.nan, float) for fam in data.keys()}
    for bidx in range(B):
        for fam in data.keys():
            meds = []
            for v in data[fam]:
                v = np.asarray(v, float)
                v = v[np.isfinite(v)]
                if v.size == 0:
                    meds.append(np.nan)
                    continue
                ii = rng.integers(0, v.size, size=v.size)
                meds.append(float(np.median(v[ii])))
            boot[fam][bidx] = _fit_slope(xs, np.array(meds, float))

    # slope CI and delta tests vs baseline
    rows = []
    pvals = []
    models = []

    base_boot = boot[baseline]
    for fam in families:
        if fam not in slope_hat:
            continue
        s = slope_hat[fam]
        sb = boot[fam]
        sb = sb[np.isfinite(sb)]
        if sb.size == 0 or not np.isfinite(s):
            ci_lo, ci_hi = np.nan, np.nan
        else:
            ci_lo, ci_hi = np.percentile(sb, [2.5, 97.5])

        if fam == baseline:
            delta = 0.0
            p = np.nan
            pvals.append(np.nan)
        else:
            # delta distribution
            d = boot[fam] - base_boot
            d = d[np.isfinite(d)]
            if d.size == 0:
                delta, p = np.nan, np.nan
            else:
                delta = float(slope_hat[fam] - slope_hat[baseline])
                # two-sided bootstrap p-value
                p_pos = float(np.mean(d >= 0.0))
                p_neg = float(np.mean(d <= 0.0))
                p = 2.0 * min(p_pos, p_neg)
                p = min(1.0, p)
            pvals.append(p)
            models.append(fam)

        rows.append(dict(
            model=fam,
            baseline=baseline,
            metric=metric,
            slope=float(s) if np.isfinite(s) else np.nan,
            ci_lo=float(ci_lo) if np.isfinite(ci_lo) else np.nan,
            ci_hi=float(ci_hi) if np.isfinite(ci_hi) else np.nan,
            delta_vs_baseline=float(delta) if np.isfinite(delta) else np.nan,
            p_value=float(p) if np.isfinite(p) else np.nan,
            p_holm=np.nan,
            B=int(B),
        ))

    # Holm across non-baseline models only
    pvals_arr = np.asarray([r["p_value"] for r in rows if r["model"] != baseline], float)
    finite = np.isfinite(pvals_arr)
    pholm = np.full_like(pvals_arr, np.nan)
    if np.any(finite):
        pholm[finite] = holm_adjust(pvals_arr[finite])

    j = 0
    for r in rows:
        if r["model"] == baseline:
            continue
        r["p_holm"] = float(pholm[j]) if np.isfinite(pholm[j]) else np.nan
        j += 1

    df = pd.DataFrame(rows)
    ensure_dir(os.path.dirname(out_csv))
    df.to_csv(out_csv, index=False)

    meta = dict(
        signal=signal,
        metric=metric,
        baseline=baseline,
        hist_tags=hist_tags,
        hist_distances=[int(_tag_distance(t)[1]) for t in hist_tags],
        bootstrap_B=int(B),
        seed=int(seed),
        require_common_valid_per_tag=bool(require_common_valid_per_tag),
    )
    with open(out_json, "w") as f:
        json.dump(meta, f, indent=2)

    print(f"✓ wrote HIST-slope bootstrap CSV: {out_csv}")
    print(f"✓ wrote HIST-slope meta JSON:     {out_json}")


# -------------------------
# MAIN (plug your REGISTRY here)
# -------------------------
if __name__ == "__main__":
    SIGNAL = "Single_State_Change"
    BASELINE = "Linear"
    HISTORY_LEN = 50
    FS = 10.0
    PHASE_UNIT = "deg"
    SPLIT = "test"

    TAGS = [
        "win_no_transition_A",
        "fut_d02", "fut_d04", "fut_d06", "fut_d10", "fut_d12", "fut_d15", "fut_d20", "fut_d30", "fut_d40",
        "hist_d02", "hist_d04", "hist_d06", "hist_d10", "hist_d12", "hist_d15", "hist_d20", "hist_d30", "hist_d40",
        "win_no_transition_B",
    ]

    # Compare ALL families at once
    FAMILIES_ALL = [
        "Linear", "DLinear", "FITS",
        "MLinear", "NBeats", "FreMLP",
        "ModernTCN", "MICN_Mean",
        "PatchTST", "Transformer", "Autoformer",
    ]

    OUT_ROOT = (
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/"
        "Model_Comparison/Statistical/Single_State_Change/"
    )
    OUT_TAGWISE = os.path.join(OUT_ROOT, "tagwise_paired_tests")
    OUT_ADAPT = os.path.join(OUT_ROOT, "hist_adaptation_slope_bootstrap")
    ensure_dir(OUT_TAGWISE)
    ensure_dir(OUT_ADAPT)

    # -------------------------
    # REGISTRY
    # REGISTRY[signal][family] = [(name, path)]
    # -------------------------
    REGISTRY: Dict[str, Dict[str, List[Tuple[str, str]]]] = {}

    def add_family(reg, signal, family, runs):
        reg.setdefault(signal, {})
        reg[signal].setdefault(family, [])
        for name, path in runs:
            reg[signal][family].append((name, path))

    # ---- your model folders ----
    add_family(REGISTRY, SIGNAL, "Linear", [(
        "Linear",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_Linear_50_100_Linear_Markov_Single_State_Change_600_100_200_0.001_0.0001_16_Markov",
    )])

    add_family(REGISTRY, SIGNAL, "DLinear", [(
        "DLinear",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_DLinear_50_100_DLinear_Markov_Single_State_Change_600_100_200_0.001_0.0001_16_Markov",
    )])

    add_family(REGISTRY, SIGNAL, "FITS", [(
        "FITS",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_FITS_50_100_FITS_Markov_Single_State_Change_600_100_200_0.001_0.0001_16_Markov",
    )])

    add_family(REGISTRY, SIGNAL, "MLinear", [(
        "MLinear",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_MLinear_50_100_MLinear_Markov_Single_State_Change_600_100_200_0.0001_0.0001_16_Markov",
    )])

    add_family(REGISTRY, SIGNAL, "NBeats", [(
        "NBeats",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_NBeats_50_100_Nbeats_Markov_Single_State_Change_600_100_200_0.0001_0.0001_16_Markov",
    )])

    add_family(REGISTRY, SIGNAL, "FreMLP", [(
        "FreMLP",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_FreMLP_50_100_FreMLP_Markov_Single_State_Change_600_100_200_0.0001_0.0001_16_Markov",
    )])

    add_family(REGISTRY, SIGNAL, "ModernTCN", [(
        "ModernTCN",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_ModernTCN_50_100_ModernTCN_Markov_Single_State_Change_600_100_200_0.0_0.001_16_Markov",
    )])

    add_family(REGISTRY, SIGNAL, "MICN_Mean", [(
        "MICN_Mean",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_MICN_50_100_MICN_Mean_Markov_Single_State_Change_600_100_200_0.0001_0.0001_16_Markov",
    )])

    add_family(REGISTRY, SIGNAL, "MICN_Regre", [(
        "MICN_Regre",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_MICN_Regere_50_100_MICN_Regre_Markov_Single_State_Change_600_100_200_0.0001_0.0001_16_Markov",
    )])

    add_family(REGISTRY, SIGNAL, "PatchTST", [(
        "PatchTST",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_PatchTST_50_100_PatchTST_Markov_Single_State_Change_600_100_200_0.0001_0.0001_15_Markov",
    )])

    add_family(REGISTRY, SIGNAL, "Transformer", [(
        "Transformer",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_Transformer_50_100_Transformer_Markov_Single_State_Change_600_100_200_0.0001_0.0001_16_Markov",
    )])

    add_family(REGISTRY, SIGNAL, "Autoformer", [(
        "Autoformer",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_Autoformer_50_100_Autoformer_Markov_Single_State_Change_600_100_200_0.0001_0.0001_16_Markov",
    )])

    METRICS = ["mae", "freq", "phase"]

    # -------------------------
    # 1) Tag-wise paired tests
    # -------------------------
    for metric in METRICS:
        out_csv = os.path.join(OUT_TAGWISE, f"tagwise_vs_{BASELINE}_{metric}.csv")
        out_json = os.path.join(OUT_TAGWISE, f"tagwise_vs_{BASELINE}_{metric}.json")
        run_tagwise_paired_tests(
            REGISTRY=REGISTRY,
            signal=SIGNAL,
            families=FAMILIES_ALL,
            baseline=BASELINE,
            tags=TAGS,
            metric=metric,
            history_len=HISTORY_LEN,
            fs=FS,
            phase_unit=PHASE_UNIT,
            out_csv=out_csv,
            out_json=out_json,
            require_common_valid=True,
        )

    # -------------------------
    # 2) HIST adaptation slope test (bootstrap)
    # -------------------------
    for metric in METRICS:
        out_csv = os.path.join(OUT_ADAPT, f"hist_slope_bootstrap_vs_{BASELINE}_{metric}.csv")
        out_json = os.path.join(OUT_ADAPT, f"hist_slope_bootstrap_vs_{BASELINE}_{metric}.json")
        run_hist_adaptation_slope_bootstrap(
            REGISTRY=REGISTRY,
            signal=SIGNAL,
            families=FAMILIES_ALL,
            baseline=BASELINE,
            tags=TAGS,
            metric=metric,
            history_len=HISTORY_LEN,
            fs=FS,
            phase_unit=PHASE_UNIT,
            out_csv=out_csv,
            out_json=out_json,
            B=2000,
            seed=0,
            require_common_valid_per_tag=True,
        )

    print("All done.")