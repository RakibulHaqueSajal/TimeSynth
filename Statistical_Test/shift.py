#!/usr/bin/env python3
import os
import re
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
from matplotlib.patches import Patch
from typing import List, Dict, Any
import json 
import csv

import math
import pandas as pd


# -------------------------
# Helpers
# -------------------------
def _parse_family(model_name: str):
    """
    Extract a model family token from the display name (before first '-' if present).
    Examples: 'Linear-4' -> 'Linear', 'PatchTST' -> 'PatchTST'
    """
    return model_name.split('-', 1)[0]


def _extract_level(name: str, path: str, tag: str = "Shift"):
    """
    Return an integer 'level' for a given tag (default: Shift).
    Priority:
      1) Look for '...<tag>[-_ ]<digits>' in the NAME
      2) Look for '_<tag>_<digits>' in the PATH
      3) Fall back to hyphen pattern 'Family-<digits>' at end of NAME
      4) Default 0
    """
    m = re.search(rf"{tag}[-_ ]?(\d+)", name, flags=re.IGNORECASE)
    if m:
        return int(m.group(1))
    m = re.search(rf"[_/]{tag}[_-](\d+)", path, flags=re.IGNORECASE)
    if m:
        return int(m.group(1))
    m = re.search(r"-([0-9]+)$", name)
    if m:
        return int(m.group(1))
    return 0


# Keep only Shift-0 (clean)
def filter_to_levels(models, tag="Shift", allowed_levels={0}):
    out = []
    for name, path in models:
        if _extract_level(name, path, tag=tag) in allowed_levels:
            out.append((name, path))
    if not out:
        raise ValueError(f"No models remain after filtering to levels={allowed_levels}.")
    return out


def gather_models(REG, signal, families):
    if signal not in REG:
        raise KeyError(f"Unknown signal: {signal}")
    missing = [f for f in families if f not in REG[signal]]
    if missing:
        print(f"[WARN] Missing families for signal={signal}: {missing}")
    out = []
    for fam in families:
        out.extend(REG[signal].get(fam, []))
    if not out:
        raise ValueError(f"No models found for signal={signal} families={families}")
    return out


def build_clean_models_by_signal(REGISTRY, signals, families, tag="Shift"):
    """Returns dict: signal -> [(name, path) ...] filtered to Shift-0"""
    out = {}
    for sig in signals:
        models = gather_models(REGISTRY, sig, families)
        out[sig] = filter_to_levels(models, tag=tag, allowed_levels={0})
    return out


def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)


def add_family(
    REG: Dict[str, Dict[str, List[Tuple[str, str]]]],
    signal: str,
    family: str,
    models: List[Tuple[str, str]],
):
    REG.setdefault(signal, {}).setdefault(family, []).extend(models)


def add_family_from_fmt(
    REG: Dict[str, Dict[str, List[Tuple[str, str]]]],
    signal: str,
    family: str,
    name_fmt: str,   # e.g., "Linear-{k}"
    path_fmt: str,   # e.g., "..._Shift_{k}"
    k_values=(0, 1, 2, 3, 4),
):
    REG.setdefault(signal, {}).setdefault(family, [])
    for k in k_values:
        REG[signal][family].append((name_fmt.format(k=k), path_fmt.format(k=k)))



def _analytic_signal_fft(x, pad_factor=2, smooth_win=None):
    """
    Analytic signal via FFT (Hilbert transform without scipy), with a few
    stabilizing tricks for low-amplitude / noisy signals:

    - optional moving-average smoothing before Hilbert (smooth_win)
    - zero-padding in FFT (pad_factor) to reduce edge effects
    - mean removal to avoid DC dominating

    Parameters
    ----------
    x : array_like
        Real-valued input signal, shape (N,).
    pad_factor : int, optional
        Factor by which to zero-pad the FFT length. pad_factor=1 -> no padding.
        pad_factor=2 (default) often helps with smoother phase.
    smooth_win : int or None, optional
        If not None and >1, applies a simple moving-average of this window
        length before computing the analytic signal. This greatly stabilizes
        the Hilbert transform in low-SNR regions.

    Returns
    -------
    z : ndarray of complex
        Analytic signal z = x_smooth + j*H{x_smooth}, cropped to original length.
    """
    x = np.asarray(x, dtype=float)
    n = x.size

    # Remove mean to avoid large DC term dominating the Hilbert transform
    x = x - x.mean()

    # Optional smoothing to reduce high-frequency noise that blows up phase
    if smooth_win is not None and smooth_win > 1:
        # Simple moving average, zero-phase-ish via 'same' mode
        kernel = np.ones(int(smooth_win), dtype=float) / float(smooth_win)
        x = np.convolve(x, kernel, mode="same")

    # Zero-padding for more stable FFT-based Hilbert transform
    if pad_factor is None or pad_factor < 1:
        pad_factor = 1
    n_fft = int(pad_factor * n)

    X = np.fft.fft(x, n=n_fft)

    # Construct frequency-domain Hilbert transform multiplier
    H = np.zeros(n_fft, dtype=float)
    if n_fft % 2 == 0:
        # even length
        H[0] = 1.0
        H[n_fft // 2] = 1.0
        H[1:n_fft // 2] = 2.0
    else:
        # odd length
        H[0] = 1.0
        H[1:(n_fft + 1) // 2] = 2.0

    z_full = np.fft.ifft(X * H, n=n_fft)

    # Crop back to original length
    z = z_full[:n]
    return z


def _wrap_to_pi(ang):
    """
    Wrap angle array to (-pi, pi], but first enforce temporal continuity
    with np.unwrap to reduce spurious jumps in low-amplitude regions.

    This is helpful when you're computing instantaneous phase from a Hilbert
    transform and want a stable, smooth phase trajectory.
    """
    ang = np.asarray(ang, dtype=float)

    # First unwrap to make it continuous over time
    ang_unwrapped = np.unwrap(ang)

    # Then wrap back to (-pi, pi]
    return (ang_unwrapped + np.pi) % (2 * np.pi) - np.pi


def _per_series_phase_error_for_model(
    model_path,
    split: str = "test",
    history_len: int = 50,
    unit: str = "rad",
    amp_frac_thresh: float = 0.2,
):
    """
    Per-series mean |Δphase| with amplitude-thresholded masking.

    - Analytic signal via FFT Hilbert.
    - Phase is evaluated ONLY where the TRUE amplitude is reliable:
        A_true > amp_frac_thresh * median(A_true)
    - This avoids spurious phase spikes in low-amplitude regions.
    - If no valid region → NaN for that series.
    """

    true = np.load(os.path.join(model_path, f"{split}_true_with_history.npy"))
    pred = np.load(os.path.join(model_path, f"{split}_pred_with_history.npy"))
    if true.ndim == 3:
        true = true.squeeze(-1)
    if pred.ndim == 3:
        pred = pred.squeeze(-1)

    Y  = true[:, history_len:]     # (N, H)
    YH = pred[:, history_len:]     # (N, H)

    N, H = Y.shape
    errs = np.full(N, np.nan)

    to_unit = (lambda a: a) if unit == "rad" else (lambda a: np.degrees(a))

    for i in range(N):
        y  = Y[i]  - Y[i].mean()
        yh = YH[i] - YH[i].mean()

        # analytic signals
        zt = _analytic_signal_fft(y)
        zp = _analytic_signal_fft(yh)

        At = np.abs(zt)
        Ap = np.abs(zp)

        # amplitude threshold from TRUE signal only
        med_amp = np.median(At)
        if not np.isfinite(med_amp) or med_amp == 0:
            continue

        amp_thresh = amp_frac_thresh * med_amp
        mask = At > amp_thresh

        if not np.any(mask):
            continue

        # unwrap before difference
        phi_t = np.unwrap(np.angle(zt))
        phi_p = np.unwrap(np.angle(zp))

        # wrapped phase difference
        dphi = _wrap_to_pi(phi_p - phi_t)
        dphi_sel = dphi[mask]

        if dphi_sel.size == 0:
            continue

        errs[i] = np.mean(np.abs(to_unit(dphi_sel)))

    return errs


# -------------------------
# MAE / MSE metrics
# -------------------------
def _per_series_mae_for_model(model_path, split="test", history_len=50):
    """
    Returns array of per-series MAE averaged over the forecast horizon. Shape: (N_series,)
    """
    true = np.load(os.path.join(model_path, f"{split}_true_with_history.npy"))
    pred = np.load(os.path.join(model_path, f"{split}_pred_with_history.npy"))
    if true.ndim == 3:
        true = true.squeeze(-1)
    if pred.ndim == 3:
        pred = pred.squeeze(-1)
    Y = true[:, history_len:]   # (N, H)
    YH = pred[:, history_len:]  # (N, H)
    return np.mean(np.abs(YH - Y), axis=1)


def _per_series_mse_for_model(model_path, split="test", history_len=50):
    """
    Returns array of per-series MSE averaged over the forecast horizon. Shape: (N_series,)
    """
    true = np.load(os.path.join(model_path, f"{split}_true_with_history.npy"))
    pred = np.load(os.path.join(model_path, f"{split}_pred_with_history.npy"))
    if true.ndim == 3:
        true = true.squeeze(-1)
    if pred.ndim == 3:
        pred = pred.squeeze(-1)
    Y = true[:, history_len:]   # (N, H)
    YH = pred[:, history_len:]  # (N, H)
    return np.mean((YH - Y) ** 2, axis=1)


def _peak_freq_rfft_with_confidence(
    x,
    fs: float = 1.0,
    drop_dc: bool = True,
    parabolic: bool = True,
    peak_frac_thresh: float = 0.1,
    power_thresh: float = 1e-8,
):
    """
    Dominant frequency via one-sided rFFT, plus a reliability flag.

    Returns:
        (f_est, reliable) where:
          - f_est: estimated dominant frequency (same units as fs)
          - reliable: False if spectrum is too flat / low power.

    Criteria:
      - total spectral power (excluding DC if drop_dc) must exceed power_thresh
      - dominant peak must explain at least peak_frac_thresh of total power
    """
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
        if abs(denom) < 1e-12:
            delta = 0.0
        else:
            delta = 0.5 * (P[k - 1] - P[k + 1]) / denom
        f_est = (k + delta) * (fs / n)

    peak_power = P[k]
    frac = peak_power / total_power if total_power > 0 else 0.0
    reliable = frac >= peak_frac_thresh

    return float(f_est), bool(reliable)


def _per_series_freq_error_for_model(
    model_path,
    split: str = "test",
    history_len: int = 50,
    fs: float = 1.0,
    peak_frac_thresh: float = 0.1,
    power_thresh: float = 1e-8,
):
    """
    Robust per-series dominant-frequency error over the forecast horizon.

    Uses _peak_freq_rfft_with_confidence to detect 'tampered'/flat spectra.
    Returns:
        errs[N], with NaN where either true or pred spectrum is unreliable.
    """
    true = np.load(os.path.join(model_path, f"{split}_true_with_history.npy"))
    pred = np.load(os.path.join(model_path, f"{split}_pred_with_history.npy"))
    if true.ndim == 3:
        true = true.squeeze(-1)
    if pred.ndim == 3:
        pred = pred.squeeze(-1)

    Y = true[:, history_len:]   # (N, H)
    YH = pred[:, history_len:]  # (N, H)

    N = Y.shape[0]
    errs = np.full(N, np.nan, dtype=float)

    for i in range(N):
        f_t, ok_t = _peak_freq_rfft_with_confidence(
            Y[i],
            fs=fs,
            drop_dc=True,
            parabolic=True,
            peak_frac_thresh=peak_frac_thresh,
            power_thresh=power_thresh,
        )
        f_p, ok_p = _peak_freq_rfft_with_confidence(
            YH[i],
            fs=fs,
            drop_dc=True,
            parabolic=True,
            peak_frac_thresh=peak_frac_thresh,
            power_thresh=power_thresh,
        )

        if not (ok_t and ok_p):
            # mark as NaN -> filtered out in plotting
            continue

        errs[i] = abs(f_p - f_t)

    return errs



def build_models_by_shift_for_signal(
    REGISTRY: Dict[str, Dict[str, List[Tuple[str, str]]]],
    signal: str,
    families: List[str],
    levels: List[int],
    tag: str = "Shift",
) -> Dict[int, List[Tuple[str, str]]]:
    """
    Returns dict: level -> [(name, path), ...] for a single signal.

    `level` is an integer from `levels` (e.g., 1,2,0,3,4).
    For each (signal, family, level) we expect at most one run.
    """
    if signal not in REGISTRY:
        raise KeyError(f"Unknown signal: {signal}")

    by_shift: Dict[int, List[Tuple[str, str]]] = {}

    for lvl in levels:
        for fam in families:
            found = False
            for name, path in REGISTRY[signal].get(fam, []):
                if _extract_level(name, path, tag=tag) == lvl:
                    by_shift.setdefault(lvl, []).append((name, path))
                    found = True
                    break
            if not found:
                print(f"[WARN] Missing {fam} for {signal} at Shift-{lvl}")

    if not by_shift:
        raise ValueError(f"No models found for {signal} at levels={levels}")

    return by_shift


# -------------------------
# Color + plotting helpers
# -------------------------
def _build_colors(families):
    """Stable color per family."""
    base = [
        'tab:blue', 'tab:orange', 'tab:green', 'tab:red',
        'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray',
        'tab:olive', 'tab:cyan'
    ]
    return {fam: base[i % len(base)] for i, fam in enumerate(families)}


def _collect_metric_for_signals(
    models_by_signal: Dict[str, List[Tuple[str, str]]],
    families: List[str],
    signals_order: List[str],
    metric_fn,
    pass_signal: bool = False,
):
    """
    Collect per-series metric arrays for each (signal, family).

    metric_fn:
      - if pass_signal == False: metric_fn(path) -> 1D np.array
      - if pass_signal == True : metric_fn(path, sig) -> 1D np.array

    NaN / inf entries are dropped.

    NOTE: This no longer enforces Shift-0; caller is responsible for
    filtering models to desired levels.
    """
    per_sig_fam_vals = {
        sig: {fam: np.array([], float) for fam in families}
        for sig in signals_order
    }

    for sig in signals_order:
        chosen = {}
        for name, path in models_by_signal[sig]:
            fam = _parse_family(name)
            if fam in families:
                chosen[fam] = path  # last one wins if duplicates

        for fam in families:
            p = chosen.get(fam)
            if not p:
                continue
            try:
                if pass_signal:
                    vals = metric_fn(p, sig)
                else:
                    vals = metric_fn(p)

                vals = np.asarray(vals, float)
                vals = vals[np.isfinite(vals)]  # drop NaNs / infs
                per_sig_fam_vals[sig][fam] = vals
            except Exception:
                # If something goes wrong (missing file, etc.), leave empty
                pass

    return per_sig_fam_vals



def _plot_grouped_boxplot(
    per_sig_fam_vals: Dict[Any, Dict[str, np.ndarray]],
    families: List[str],
    signals_order: List[Any],
    fam_color: Dict[str, str],
    output_png: str,
    ylabel: str,
    base_font: int = 12,
    tick_font: int = 10,
    dpi: int = 400,
    box_width: float = 0.35,   # tighter by default
    group_gap: float = 0.20,   # much smaller gap between groups
    show_separators: bool = True,
    logy: bool = False,
    label_map: Dict[Any, str] = None,   # can be int->str or str->str
):
    """
    Generic grouped boxplot:
      - groups = signals (or shifts)
      - boxes = families
      - compact horizontal spacing
    """

    # Fonts
    plt.rcParams.update({
        "font.size": base_font,
        "font.weight": "bold",
        "axes.titlesize": base_font,
        "axes.labelsize": base_font,
        "xtick.labelsize": tick_font,
        "ytick.labelsize": tick_font,
    })

    F = len(families)
    L = len(signals_order)

    inner_gap = 0.06
    group_width = F * box_width + (F - 1) * inner_gap

    group_centers = []
    start = 0.0
    for _ in range(L):
        group_centers.append(start + group_width / 2.0)
        start += group_width + group_gap
    group_centers = np.asarray(group_centers)

    fam_offsets = np.linspace(
        -group_width / 2.0 + box_width / 2.0,
        +group_width / 2.0 - box_width / 2.0,
        F,
    )

    fig_width = max(4.0, 1.4 + 0.9 * L)
    fig, ax = plt.subplots(figsize=(fig_width, 3.4),
                           constrained_layout=False, dpi=dpi)

    positions, data, colors = [], [], []
    for gi, sig in enumerate(signals_order):
        center = group_centers[gi]
        for fi, fam in enumerate(families):
            vals = per_sig_fam_vals[sig][fam]
            positions.append(center + fam_offsets[fi])
            data.append(vals)
            colors.append(fam_color[fam])

    bp = ax.boxplot(
        data,
        positions=positions,
        widths=box_width,
        patch_artist=True,
        showfliers=True,
        flierprops=dict(markersize=2.5, alpha=0.6),
        medianprops=dict(lw=1.4),
        boxprops=dict(lw=1.0),
        whiskerprops=dict(lw=0.9),
        capprops=dict(lw=0.9),
        manage_ticks=False,
    )
    for patch, c in zip(bp["boxes"], colors):
        patch.set_facecolor(c)
        patch.set_alpha(0.65)

    # X labels
    if label_map is not None:
        # use custom labels (e.g. for shifts)
        sig_labels = [str(label_map.get(s, s)) for s in signals_order]
    else:
        # default: interpret as signal family names
        title_map = {
            "Drift_Harmonic": "Drift Harmonic",
            "Single_Phase_Modulation": "SPM-Harmonic",
            "Dual_Phase_Modulation": "DPM-Harmonic",
        }
        sig_labels = [str(title_map.get(s, s)) for s in signals_order]

    ax.set_xticks(group_centers)
    ax.set_xticklabels(sig_labels)

    ax.set_ylabel(ylabel)
    if logy:
        ax.set_yscale("log")

    ax.grid(True, axis="y", alpha=0.35, linestyle="--", linewidth=0.6)

    if len(positions) > 0:
        margin = 0.4 * box_width
        ax.set_xlim(group_centers[0] - group_width / 2.0 - margin,
                    group_centers[-1] + group_width / 2.0 + margin)

    if show_separators and L > 1:
        for gi in range(L - 1):
            x_sep = (group_centers[gi] + group_centers[gi + 1]) / 2.0
            ax.axvline(x_sep, color="0.85", lw=0.8, zorder=0)

    legend_patches = [Patch(facecolor=fam_color[f], alpha=0.65, label=f)
                      for f in families]
    fig.legend(
        handles=legend_patches,
        loc="upper center",
        ncol=min(F, 6),
        frameon=False,
        fontsize=base_font,
        borderaxespad=0.3,
        handlelength=1.4,
        columnspacing=1.1,
    )

    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.20, top=0.80)

    fig.savefig(output_png, dpi=dpi, bbox_inches="tight")
    fig.savefig(os.path.splitext(output_png)[0] + ".pdf",
                dpi=dpi, bbox_inches="tight")
    plt.close(fig)

    print(f"✓ Saved grouped boxplot: {output_png} and {os.path.splitext(output_png)[0] + '.pdf'}")

#Saving stats

def _summarize_grouped_vals(group_vals: Dict[Any, Dict[str, np.ndarray]]):
    """
    group_vals[group_key][family] -> 1D array
    Returns nested dict with n/mean/median/std/q25/q75/iqr/min/max.
    """
    out: Dict[Any, Dict[str, Dict[str, float]]] = {}
    for g, fam_dict in group_vals.items():
        out[g] = {}
        for fam, vals in fam_dict.items():
            vals = np.asarray(vals, float)
            vals = vals[np.isfinite(vals)]
            if vals.size == 0:
                out[g][fam] = dict(
                    n=0, mean=float("nan"), median=float("nan"), std=float("nan"),
                    q25=float("nan"), q75=float("nan"), iqr=float("nan"),
                    min=float("nan"), max=float("nan"),
                )
                continue

            q25, q75 = np.percentile(vals, [25, 75])
            out[g][fam] = dict(
                n=int(vals.size),
                mean=float(np.mean(vals)),
                median=float(np.median(vals)),
                std=float(np.std(vals, ddof=1)) if vals.size > 1 else 0.0,
                q25=float(q25),
                q75=float(q75),
                iqr=float(q75 - q25),
                min=float(np.min(vals)),
                max=float(np.max(vals)),
            )
    return out


def save_grouped_summary_stats(
    group_vals: Dict[Any, Dict[str, np.ndarray]],
    group_order: List[Any],
    families: List[str],
    out_path_base: str,
    metric_name: str,
    group_label: str = "level",
    label_map: Dict[Any, str] = None,
):
    """
    Saves:
      - <out_path_base>_<metric_name>_stats.csv
      - <out_path_base>_<metric_name>_stats.json
    """
    stats = _summarize_grouped_vals(group_vals)

    csv_path  = f"{out_path_base}_{metric_name}_stats.csv"
    json_path = f"{out_path_base}_{metric_name}_stats.json"

    # CSV
    fieldnames = [group_label, "group_name", "family",
                  "n", "mean", "median", "std", "q25", "q75", "iqr", "min", "max"]
    with open(csv_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for g in group_order:
            g_name = str(label_map.get(g, g)) if label_map else str(g)
            for fam in families:
                s = stats.get(g, {}).get(fam, {})
                row = {group_label: g, "group_name": g_name, "family": fam}
                row.update(s)
                w.writerow(row)

    # JSON
    payload = dict(
        metric=metric_name,
        group_label=group_label,
        group_order=[str(g) for g in group_order],
        group_names=[str(label_map.get(g, g)) if label_map else str(g) for g in group_order],
        families=families,
        stats={str(g): stats.get(g, {}) for g in group_order},
    )
    with open(json_path, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"✓ Saved stats: {csv_path}")
    print(f"✓ Saved stats: {json_path}")

##Generic boxplot Metric
def _boxplot_metric_across_shifts_for_signal(
    REGISTRY: Dict[str, Dict[str, List[Tuple[str, str]]]],
    signal: str,
    families: List[str],
    levels: List[int],
    output_png: str,
    metric_fn,
    ylabel: str,
    history_len: int = 50,
    base_font: int = 12,
    tick_font: int = 10,
    metric_name: str ="metric",
    tag: str ="Shift",
    dpi: int = 400,
    box_width: float = 0.5,
    group_gap: float = 0.9,
    show_separators: bool = True,
    logy: bool = False,
    label_map: Dict[Any, str] = None,   # <-- NEW
):
    """
    Generic grouped boxplot across *shifts* for a fixed signal.

    - groups = shift levels (e.g., 1,2,0,3,4)
    - boxes  = model families
    """
    # Reindex REGISTRY by shift level for this signal (keys are ints)
    models_by_shift = build_models_by_shift_for_signal(
        REGISTRY=REGISTRY,
        signal=signal,
        families=families,
        levels=levels,
        tag=tag,
    )    

    # Only keep levels that actually exist
    shifts_order = [lvl for lvl in levels if lvl in models_by_shift]

    fam_color = _build_colors(families)

    per_shift_fam_vals = _collect_metric_for_signals(
        models_by_signal=models_by_shift,
        families=families,
        signals_order=shifts_order,
        metric_fn=metric_fn,
    )
    # ---- SAVE SUMMARY (mean/median/etc.) ----
    out_base = os.path.splitext(output_png)[0]  # drop .png
    save_grouped_summary_stats(
        group_vals=per_shift_fam_vals,
        group_order=shifts_order,
        families=families,
        out_path_base=out_base,
        metric_name=metric_name,
        group_label=tag,       # e.g., "Shift" or "SNR_Level"
        label_map=label_map,
)


    _plot_grouped_boxplot(
        per_sig_fam_vals=per_shift_fam_vals,
        families=families,
        signals_order=shifts_order,
        fam_color=fam_color,
        output_png=output_png,
        ylabel=ylabel,
        base_font=base_font,
        tick_font=tick_font,
        dpi=dpi,
        box_width=box_width,
        group_gap=group_gap,
        show_separators=show_separators,
        logy=logy,
        label_map=label_map,   # <-- USE THE GLOBAL MAP HERE
    )


#AMPLITUDE ERROR METRIC
def boxplot_mae_across_shifts_for_signal(
    REGISTRY,
    signal: str,
    families: List[str],
    levels: List[int],
    output_png: str,
    history_len: int = 50,
    **kwargs,
):
    def mae_fn(path):
        return _per_series_mae_for_model(path, split="test", history_len=history_len)

    _boxplot_metric_across_shifts_for_signal(
        REGISTRY=REGISTRY,
        signal=signal,
        families=families,
        levels=levels,
        output_png=output_png,
        metric_fn=mae_fn,
        ylabel="Per-series average MAE",
        metric_name="mae",
        history_len=history_len,
        **kwargs,
    )


def boxplot_mse_across_shifts_for_signal(
    REGISTRY,
    signal: str,
    families: List[str],
    levels: List[int],
    output_png: str,
    history_len: int = 50,
    **kwargs,
):
    def mse_fn(path):
        return _per_series_mse_for_model(path, split="test", history_len=history_len)

    _boxplot_metric_across_shifts_for_signal(
        REGISTRY=REGISTRY,
        signal=signal,
        families=families,
        levels=levels,
        output_png=output_png,
        metric_fn=mse_fn,
        ylabel="Per-series average MSE",
        metric_name="mse",
        history_len=history_len,
        **kwargs,
    )

##Phase ERROR METRIC
def boxplot_phase_error_across_shifts_for_signal(
    REGISTRY,
    signal: str,
    families: List[str],
    levels: List[int],
    output_png: str,
    history_len: int = 50,
    unit: str = "deg",
    amp_frac_thresh: float = 0.2,
    **kwargs,
):
    def phase_fn(path):
        return _per_series_phase_error_for_model(
            path,
            split="test",
            history_len=history_len,
            unit=unit,
            amp_frac_thresh=amp_frac_thresh,
        )

    ylab = f"|Δphase| ({'radians' if unit == 'rad' else 'degrees'})"

    _boxplot_metric_across_shifts_for_signal(
        REGISTRY=REGISTRY,
        signal=signal,
        families=families,
        levels=levels,
        output_png=output_png,
        metric_fn=phase_fn,
        ylabel=ylab,
        metric_name=f"Phase_{unit}",
        history_len=history_len,
        **kwargs,
    )

##FREQUENCY ERROR METRIC
def boxplot_freq_error_across_shifts_for_signal(
    REGISTRY,
    signal: str,
    families: List[str],
    levels: List[int],
    output_png: str,
    history_len: int = 50,
    fs: float = 10.0,
    peak_frac_thresh: float = 0.1,
    power_thresh: float = 1e-8,
    **kwargs,
):
    def freq_fn(path):
        return _per_series_freq_error_for_model(
            path,
            split="test",
            history_len=history_len,
            fs=fs,
            peak_frac_thresh=peak_frac_thresh,
            power_thresh=power_thresh,
        )

    ylab = "|Δf| (Hz)"  # since we pass fs explicitly

    _boxplot_metric_across_shifts_for_signal(
        REGISTRY=REGISTRY,
        signal=signal,
        families=families,
        levels=levels,
        output_png=output_png,
        metric_fn=freq_fn,
        ylabel=ylab,
        metric_name="Freq",
        history_len=history_len,
        **kwargs,
    )




# -------------------------
# stats helpers
# -------------------------
def holm_adjust(pvals: np.ndarray) -> np.ndarray:
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

def paired_ttest_normal_approx(d: np.ndarray):
    d = np.asarray(d, float)
    d = d[np.isfinite(d)]
    n = d.size
    if n < 3:
        return np.nan, np.nan
    mu = d.mean()
    sd = d.std(ddof=1)
    if not np.isfinite(sd) or sd == 0:
        if mu == 0:
            return 0.0, 1.0
        return float(np.sign(mu) * np.inf), 0.0
    t = mu / (sd / math.sqrt(n))
    p = 2.0 * (1.0 - _norm_cdf(abs(t)))
    return float(t), float(p)

def mean_ci_95(d: np.ndarray):
    d = np.asarray(d, float)
    d = d[np.isfinite(d)]
    n = d.size
    if n == 0:
        return np.nan, np.nan, np.nan, np.nan
    mu = d.mean()
    sd = d.std(ddof=1) if n > 1 else 0.0
    se = sd / math.sqrt(n) if n > 1 else 0.0
    lo = mu - 1.96 * se
    hi = mu + 1.96 * se
    return float(mu), float(se), float(lo), float(hi)

# -------------------------
# registry lookup at (signal, family, shift_level)
# -------------------------
def get_paths_for_signal_level(REGISTRY, signal, families, level, tag="Shift"):
    out = {}
    missing = []
    for fam in families:
        found = None
        for name, path in REGISTRY[signal].get(fam, []):
            if _extract_level(name, path, tag=tag) == level:
                found = path
                break
        if found is None:
            missing.append(fam)
        else:
            out[fam] = found
    if missing:
        raise KeyError(f"[{signal}] missing families at {tag}={level}: {missing}")
    return out

# -------------------------
# metric dispatcher
# -------------------------
def metric_vector(metric: str, model_path: str, history_len: int, fs: float, phase_unit: str):
    if metric == "mae":
        return _per_series_mae_for_model(model_path, split="test", history_len=history_len)
    if metric == "freq":
        return _per_series_freq_error_for_model(model_path, split="test", history_len=history_len, fs=fs)
    if metric == "phase":
        return _per_series_phase_error_for_model(model_path, split="test", history_len=history_len, unit=phase_unit)
    raise ValueError(metric)

# ============================================================
# Option A: paired Δ vs Linear at each Shift level + Holm
# ============================================================
def shift_optionA_per_level(
    REGISTRY,
    signal: str,
    families: list,
    baseline: str,
    shift_levels: list,
    metric: str,
    history_len: int,
    fs: float = 10.0,
    phase_unit: str = "deg",
    tag: str = "Shift",
):
    rows = []
    for lvl in shift_levels:
        fam_to_path = get_paths_for_signal_level(REGISTRY, signal, families, lvl, tag=tag)

        vec = {fam: metric_vector(metric, path, history_len, fs, phase_unit)
               for fam, path in fam_to_path.items()}

        if baseline not in vec:
            raise RuntimeError(f"[{signal}] baseline '{baseline}' missing at {tag}={lvl}")

        N = vec[baseline].shape[0]

        # valid mask: freq/phase must be finite for ALL models at this level
        if metric in ("freq", "phase"):
            valid = np.ones(N, bool)
            for fam in families:
                valid &= np.isfinite(vec[fam])
        else:
            valid = np.isfinite(vec[baseline])

        idx = np.where(valid)[0]
        # baseline row
        rows.append(dict(signal=signal, metric=metric, shift=lvl, model=baseline,
                         n_paired=int(idx.size), delta_vs_linear=0.0,
                         ci_lo=0.0, ci_hi=0.0, t_approx=np.nan, p_value=np.nan, p_holm=np.nan))

        tmp, pvals = [], []
        base = vec[baseline]
        for fam in families:
            if fam == baseline:
                continue
            d = vec[fam][idx] - base[idx]
            mu, se, lo, hi = mean_ci_95(d)
            t, p = paired_ttest_normal_approx(d)
            tmp.append(dict(signal=signal, metric=metric, shift=lvl, model=fam,
                            n_paired=int(idx.size), delta_vs_linear=mu,
                            ci_lo=lo, ci_hi=hi, t_approx=t, p_value=p))
            pvals.append(p)

        pvals = np.asarray(pvals, float)
        p_holm = holm_adjust(pvals) if pvals.size else np.array([])
        for r, ph in zip(tmp, p_holm):
            r["p_holm"] = float(ph)
            rows.append(r)

    df = pd.DataFrame(rows).sort_values(["shift", "delta_vs_linear"], ascending=[True, True]).reset_index(drop=True)
    return df

# ============================================================
# Option B1: AUC degradation vs shift (relative to shift=0)
# ============================================================
def shift_optionB_auc(
    REGISTRY,
    signal: str,
    families: list,
    baseline: str,
    shift_levels: list,        # must include 0
    metric: str,
    history_len: int,
    fs: float = 10.0,
    phase_unit: str = "deg",
    tag: str = "Shift",
    require_all_finite: bool = True,
):
    if 0 not in shift_levels:
        raise ValueError("shift_levels must include 0 (No Shift) for AUC degradation")

    vec_by_lvl = {}
    for lvl in shift_levels:
        fam_to_path = get_paths_for_signal_level(REGISTRY, signal, families, lvl, tag=tag)
        vec_by_lvl[lvl] = {fam: metric_vector(metric, p, history_len, fs, phase_unit) for fam, p in fam_to_path.items()}

    N = vec_by_lvl[0][baseline].shape[0]

    # AUC per family per sequence
    ks = [k for k in shift_levels if k != 0]
    auc = {fam: np.full(N, np.nan, float) for fam in families}
    for fam in families:
        x0 = vec_by_lvl[0][fam]
        D = np.vstack([vec_by_lvl[k][fam] - x0 for k in ks])  # (K, N)
        auc[fam] = np.nanmean(D, axis=0)

    base_auc = auc[baseline]
    rows = [dict(signal=signal, metric=metric, model=baseline,
                 n_paired=np.nan, delta_auc_vs_linear=0.0,
                 ci_lo=0.0, ci_hi=0.0, t_approx=np.nan, p_value=np.nan, p_holm=np.nan)]

    tmp, pvals = [], []

    if metric in ("freq", "phase") and require_all_finite:
        valid = np.isfinite(base_auc)
        for fam in families:
            valid &= np.isfinite(auc[fam])
        idx = np.where(valid)[0]

        for fam in families:
            if fam == baseline:
                continue
            d = auc[fam][idx] - base_auc[idx]
            mu, se, lo, hi = mean_ci_95(d)
            t, p = paired_ttest_normal_approx(d)
            tmp.append(dict(signal=signal, metric=metric, model=fam,
                            n_paired=int(idx.size), delta_auc_vs_linear=mu,
                            ci_lo=lo, ci_hi=hi, t_approx=t, p_value=p))
            pvals.append(p)
    else:
        for fam in families:
            if fam == baseline:
                continue
            valid = np.isfinite(base_auc) & np.isfinite(auc[fam])
            idx = np.where(valid)[0]
            d = auc[fam][idx] - base_auc[idx]
            mu, se, lo, hi = mean_ci_95(d)
            t, p = paired_ttest_normal_approx(d)
            tmp.append(dict(signal=signal, metric=metric, model=fam,
                            n_paired=int(idx.size), delta_auc_vs_linear=mu,
                            ci_lo=lo, ci_hi=hi, t_approx=t, p_value=p))
            pvals.append(p)

    pvals = np.asarray(pvals, float)
    p_holm = holm_adjust(pvals) if pvals.size else np.array([])
    for r, ph in zip(tmp, p_holm):
        r["p_holm"] = float(ph)
        rows.append(r)

    df = pd.DataFrame(rows).sort_values("delta_auc_vs_linear", ascending=True).reset_index(drop=True)
    return df

# ============================================================
# Option B2: slope vs shift-x per sequence (relative to shift=0)
# ============================================================
def shift_optionB_slope(
    REGISTRY,
    signal: str,
    families: list,
    baseline: str,
    shift_levels: list,           # e.g. [1,2,0,3,4]
    shift_x: dict,                # e.g. {1:-2, 2:-1, 0:0, 3:+1, 4:+2}
    metric: str,
    history_len: int,
    fs: float = 10.0,
    phase_unit: str = "deg",
    tag: str = "Shift",
    require_all_finite: bool = True,
):
    xs = np.array([shift_x[l] for l in shift_levels], float)
    if len(np.unique(xs)) < 2:
        raise ValueError("Need at least 2 distinct shift_x values to fit slope.")

    vec_by_lvl = {}
    for lvl in shift_levels:
        fam_to_path = get_paths_for_signal_level(REGISTRY, signal, families, lvl, tag=tag)
        vec_by_lvl[lvl] = {fam: metric_vector(metric, p, history_len, fs, phase_unit) for fam, p in fam_to_path.items()}

    N = vec_by_lvl[shift_levels[0]][baseline].shape[0]

    def fit_slope(y_mat, xs):
        # y_mat: (L, N), xs: (L,)
        x = xs.reshape(-1, 1)  # (L,1)
        x_mean = x.mean()
        xc = x - x_mean
        denom = float((xc**2).sum())
        if denom == 0:
            return np.full(y_mat.shape[1], np.nan, float)
        y_mean = np.nanmean(y_mat, axis=0, keepdims=True)
        yc = y_mat - y_mean
        num = np.nansum(yc * xc, axis=0)
        return num / denom

    # build slopes
    slope = {fam: np.full(N, np.nan, float) for fam in families}
    for fam in families:
        Y = np.vstack([vec_by_lvl[lvl][fam] for lvl in shift_levels])  # (L, N)
        slope[fam] = fit_slope(Y, xs)

    base_slope = slope[baseline]
    rows = [dict(signal=signal, metric=metric, model=baseline,
                 n_paired=np.nan, delta_slope_vs_linear=0.0,
                 ci_lo=0.0, ci_hi=0.0, t_approx=np.nan, p_value=np.nan, p_holm=np.nan)]

    tmp, pvals = [], []

    if metric in ("freq", "phase") and require_all_finite:
        valid = np.isfinite(base_slope)
        for fam in families:
            valid &= np.isfinite(slope[fam])
        idx = np.where(valid)[0]
        for fam in families:
            if fam == baseline:
                continue
            d = slope[fam][idx] - base_slope[idx]
            mu, se, lo, hi = mean_ci_95(d)
            t, p = paired_ttest_normal_approx(d)
            tmp.append(dict(signal=signal, metric=metric, model=fam,
                            n_paired=int(idx.size), delta_slope_vs_linear=mu,
                            ci_lo=lo, ci_hi=hi, t_approx=t, p_value=p))
            pvals.append(p)
    else:
        for fam in families:
            if fam == baseline:
                continue
            valid = np.isfinite(base_slope) & np.isfinite(slope[fam])
            idx = np.where(valid)[0]
            d = slope[fam][idx] - base_slope[idx]
            mu, se, lo, hi = mean_ci_95(d)
            t, p = paired_ttest_normal_approx(d)
            tmp.append(dict(signal=signal, metric=metric, model=fam,
                            n_paired=int(idx.size), delta_slope_vs_linear=mu,
                            ci_lo=lo, ci_hi=hi, t_approx=t, p_value=p))
            pvals.append(p)

    pvals = np.asarray(pvals, float)
    p_holm = holm_adjust(pvals) if pvals.size else np.array([])
    for r, ph in zip(tmp, p_holm):
        r["p_holm"] = float(ph)
        rows.append(r)

    df = pd.DataFrame(rows).sort_values("delta_slope_vs_linear", ascending=True).reset_index(drop=True)
    return df
#Statistical test  across shifts for a single signal and metric

# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":

    # -------------------------
    # 1) Build a unified REGISTRY
    # -------------------------
    REGISTRY: Dict[str, Dict[str, List[Tuple[str, str]]]] = {}

    # === Drift_Harmonic ===
    add_family_from_fmt(
        REGISTRY, "Drift_Harmonic", "Linear",
        name_fmt="Linear-{k}",
        path_fmt="/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
                 "long_term_forecast_Linear_50_100_Linear_Drift_Harmonic_Clean_70_10_20_0.001_0.0001_16_Shift_{k}",
    )

    add_family_from_fmt(REGISTRY, "Drift_Harmonic", "NBeats",
        "NBeats-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_NBeats_50_100_Nbeats_Drift_Harmonic_Clean_70_10_20_0.0001_0.0001_16_Shift_{k}",
    )

    add_family_from_fmt(REGISTRY, "Drift_Harmonic", "FreMLP",
        "FreMLP-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_FreMLP_50_100_FreMLP__Drift_Harmonic_Clean_70_10_20_0.0001_0.0001_16_Shift_{k}",
    )

    add_family_from_fmt(REGISTRY, "Drift_Harmonic", "ModernTCN",
        "ModernTCN-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_ModernTCN_50_100_ModernTCN_Drift_Harmonic_Clean_70_10_20_0.0_0.001_16_Shift_{k}",
    )

    add_family_from_fmt(REGISTRY, "Drift_Harmonic", "MICN_Regre",
        "MICN_Regre-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_MICN_50_100_MICN_Regre_Drift_Harmonic_Clean_70_10_20_0.0001_0.0001_16_Shift_{k}",
    )

    add_family_from_fmt(REGISTRY, "Drift_Harmonic", "MICN_Mean",
        "MICN_Mean-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_MICN_50_100_MICN_Mean_Drift_Harmonic_Clean_70_10_20_0.0001_0.0001_16_Shift_{k}",
    )

    add_family_from_fmt(REGISTRY, "Drift_Harmonic", "PatchTST",
        "PatchTST-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_PatchTST_50_100_PatchTST_Drift_Harmonic_Clean_70_10_20_0.0001_0.0001_15_Shift_{k}",
    )

    add_family_from_fmt(REGISTRY, "Drift_Harmonic", "Transformer",
        "Transformer-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_Transformer_50_100_Transformer_Drift_Harmonic_Clean_70_10_20_0.0001_0.0001_16_Shift_{k}",
    )

    add_family_from_fmt(REGISTRY, "Drift_Harmonic", "Autoformer",
        "Autoformer-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_Autoformer_50_100_Autoformer_Drift_Harmonic_Clean_70_10_20_0.0001_0.0001_16_Shift_{k}",
    )

    add_family_from_fmt(REGISTRY, "Drift_Harmonic", "MLinear",
        "MLinear-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_MLinear_50_100_MLinear_Drift_Harmonic_Clean_70_10_20_0.0001_0.0001_16_Shift_{k}",
    )

    add_family_from_fmt(REGISTRY, "Drift_Harmonic", "DLinear",
        "DLinear-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_DLinear_50_100_DLinear_Drift_Harmonic_Clean_70_10_20_0.001_0.0001_16_Shift_{k}",
    )

    add_family_from_fmt(REGISTRY, "Drift_Harmonic", "FITS",
        "FITS-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_FITS_50_100_FITS_Single_Phase_Modulation_Clean_70_10_20_0.001_0.0001_16_Shift_{k}",
    )

    # === Single_Phase_Modulation ===
    add_family_from_fmt(REGISTRY, "Single_Phase_Modulation", "Linear",
        "Linear-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_Linear_50_100_Linear_Single_Phase_Modulation_Clean_70_10_20_0.001_0.0001_16_Shift_{k}",
    )
    add_family_from_fmt(REGISTRY, "Single_Phase_Modulation", "DLinear",
        "DLinear-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_DLinear_50_100_DLinear_Single_Phase_Modulation_Clean_70_10_20_0.001_0.0001_16_Shift_{k}",
    )
    add_family_from_fmt(REGISTRY, "Single_Phase_Modulation", "FITS",
        "FITS-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_FITS_50_100_FITS_Single_Phase_Modulation_Clean_70_10_20_0.001_0.0001_16_Shift_{k}",
    )
    add_family_from_fmt(REGISTRY, "Single_Phase_Modulation", "MLinear",
        "MLinear-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_MLinear_50_100_MLinear_Single_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_{k}",
    )
    add_family_from_fmt(REGISTRY, "Single_Phase_Modulation", "NBeats",
        "NBeats-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_NBeats_50_100_Nbeats_Single_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_{k}",
    )
    add_family_from_fmt(REGISTRY, "Single_Phase_Modulation", "FreMLP",
        "FreMLP-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_FreMLP_50_100_FreMLP__Single_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_{k}",
    )
    add_family_from_fmt(REGISTRY, "Single_Phase_Modulation", "ModernTCN",
        "ModernTCN-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_ModernTCN_50_100_ModernTCN_Single_Phase_Modulation_Clean_70_10_20_0.0_0.001_16_Shift_{k}",
    )
    add_family_from_fmt(REGISTRY, "Single_Phase_Modulation", "MICN_Regre",
        "MICN_Regre-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_MICN_50_100_MICN_Regre_Single_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_{k}",
    )
    add_family_from_fmt(REGISTRY, "Single_Phase_Modulation", "MICN_Mean",
        "MICN_Mean-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_MICN_50_100_MICN_Mean_Single_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_{k}",
    )
    add_family_from_fmt(REGISTRY, "Single_Phase_Modulation", "Transformer",
        "Transformer-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_Transformer_50_100_Transformer_Single_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_{k}",
    )
    add_family_from_fmt(REGISTRY, "Single_Phase_Modulation", "Autoformer",
        "Autoformer-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_Autoformer_50_100_Autoformer_Single_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_{k}",
    )
    add_family_from_fmt(REGISTRY, "Single_Phase_Modulation", "PatchTST",
        "PatchTST-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_PatchTST_50_100_PatchTST_Single_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_15_Shift_{k}",
    )

    # === Dual_Phase_Modulation ===
    add_family_from_fmt(REGISTRY, "Dual_Phase_Modulation", "Linear",
        "Linear-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_Linear_50_100_Linear_Dual_Phase_Modulation_Clean_70_10_20_0.001_0.0001_16_Shift_{k}",
    )
    add_family_from_fmt(REGISTRY, "Dual_Phase_Modulation", "DLinear",
        "DLinear-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_DLinear_50_100_DLinear_Dual_Phase_Modulation_Clean_70_10_20_0.001_0.0001_16_Shift_{k}",
    )
    add_family_from_fmt(REGISTRY, "Dual_Phase_Modulation", "FITS",
        "FITS-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_FITS_50_100_FITS_Dual_Phase_Modulation_Clean_70_10_20_0.001_0.0001_16_Shift_{k}",
    )
    add_family_from_fmt(REGISTRY, "Dual_Phase_Modulation", "MLinear",
        "MLinear-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_MLinear_50_100_MLinear_Dual_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_{k}",
    )
    add_family_from_fmt(REGISTRY, "Dual_Phase_Modulation", "NBeats",
        "NBeats-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_NBeats_50_100_Nbeats_Dual_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_{k}",
    )
    add_family_from_fmt(REGISTRY, "Dual_Phase_Modulation", "FreMLP",
        "FreMLP-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_FreMLP_50_100_FreMLP__Dual_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_{k}",
    )
    add_family_from_fmt(REGISTRY, "Dual_Phase_Modulation", "ModernTCN",
        "ModernTCN-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_ModernTCN_50_100_ModernTCN_Dual_Phase_Modulation_Clean_70_10_20_0.0_0.001_16_Shift_{k}",
    )
    add_family_from_fmt(REGISTRY, "Dual_Phase_Modulation", "MICN_Mean",
        "MICN_Mean-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_MICN_50_100_MICN_Mean_Dual_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_{k}",
    )
    add_family_from_fmt(REGISTRY, "Dual_Phase_Modulation", "MICN_Regre",
        "MICN_Regre-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_MICN_50_100_MICN_Regre_Dual_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_{k}",
    )
    add_family_from_fmt(REGISTRY, "Dual_Phase_Modulation", "Transformer",
        "Transformer-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_Transformer_50_100_Transformer_Dual_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_{k}",
    )
    add_family_from_fmt(REGISTRY, "Dual_Phase_Modulation", "Autoformer",
        "Autoformer-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_Autoformer_50_100_Autoformer_Dual_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_16_Shift_{k}",
    )
    add_family_from_fmt(REGISTRY, "Dual_Phase_Modulation", "PatchTST",
        "PatchTST-{k}",
        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
        "long_term_forecast_PatchTST_50_100_PatchTST_Dual_Phase_Modulation_Clean_70_10_20_0.0001_0.0001_15_Shift_{k}",
    )

    # -------------------------
    # 2) Family groups (pick what to compare)
    # -------------------------
    # FAMILY_GROUPS = {
    # "Linear":              ["Linear", "DLinear", "FITS"],
    # "MLinear":             ["MLinear", "NBeats", "FreMLP"],
    # "CNN":                 ["ModernTCN", "MICN_Mean", "MICN_Regre"],
    # "Transformer":         ["PatchTST", "Transformer", "Autoformer"],
    # "Best_Models":         ["Linear", "PatchTST", "NBeats", "MICN_Mean"],
    # "Best_Exclude_Linear": ["PatchTST", "NBeats", "MICN_Mean"],
    # }

    # -------------------------
    # 3) Orchestrate all runs
    # -------------------------
    SIGNALS      = ["Drift_Harmonic", "Single_Phase_Modulation", "Dual_Phase_Modulation"]
    OUT_ROOT     = "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Model_Comparison/Statistical/Shift_Dir"
    OUT_PHASE_ROOT = os.path.join(OUT_ROOT, "phase_error")
    OUT_FREQ_ROOT  = os.path.join(OUT_ROOT, "freq_error")
    OUT_AMP_ROOT   = os.path.join(OUT_ROOT, "amp_error")

    HISTORY_LEN  = 50
    SHIFT_LEVELS = [1, 2, 0, 3, 4]   # Shift-1, Shift-2, No Shift, Shift-3, Shift-4
    SHIFT_LABEL_MAP = {
        1: "Shift -2",
        2: "Shift -1",
        0: "No Shift",
        3: "Shift +1",
        4: "Shift +2",
    }
    for root in [OUT_PHASE_ROOT, OUT_FREQ_ROOT, OUT_AMP_ROOT]:
        ensure_dir(root)
 
    # for group_name, families in FAMILY_GROUPS.items():
    #     # First: CLEAN paradigm, across signals
    #     try:
    #         models_by_signal = build_clean_models_by_signal(
    #             REGISTRY, SIGNALS, families, tag="Shift"
    #         )
    #     except Exception as e:
    #         print(f"[SKIP] clean-across-signals {group_name}: {e}")
    #         continue

    SHIFT_LEVELS = [1, 2, 0, 3, 4]
    SHIFT_X = {1:-2, 2:-1, 0:0, 3:+1, 4:+2}  # critical for slope meaning
    BASELINE = "Linear"
    FAMILIES = ["Linear", "PatchTST", "NBeats", "MICN_Mean",  "MICN_Regre", "FreMLP", "Transformer","Autoformer", "MLinear",  "DLinear", "FITS"]  # example
    METRICS  = ["mae","freq","phase"]

    # for metric in METRICS:
    #     dfA = shift_optionA_per_level(REGISTRY, "Drift_Harmonic", FAMILIES, BASELINE,
    #                                 SHIFT_LEVELS, metric, history_len=50, fs=10.0, phase_unit="deg")
    #     dfA.to_csv(f"Shift_OptionA_Drift_Harmonic_{metric}.csv", index=False)

    #     dfB_auc = shift_optionB_auc(REGISTRY, "Drift_Harmonic", FAMILIES, BASELINE,
    #                                 SHIFT_LEVELS, metric, history_len=50, fs=10.0, phase_unit="deg")
    #     dfB_auc.to_csv(f"Shift_OptionB_AUC_Drift_Harmonic_{metric}.csv", index=False)

    #     dfB_slope = shift_optionB_slope(REGISTRY, "Drift_Harmonic", FAMILIES, BASELINE,
    #                                     SHIFT_LEVELS, SHIFT_X, metric, history_len=50, fs=10.0, phase_unit="deg")
    #     dfB_slope.to_csv(f"Shift_OptionB_Slope_Drift_Harmonic_{metric}.csv", index=False)
    for signal in SIGNALS:
        print(f"\n=== Processing signal: {signal} ===")
        for metric in METRICS:
            dfA = shift_optionA_per_level(REGISTRY, signal, FAMILIES, BASELINE,
                                        SHIFT_LEVELS, metric, history_len=50, fs=10.0, phase_unit="deg")
            dfA.to_csv(os.path.join(OUT_ROOT, f"Shift_OptionA_{signal}_{metric}.csv"), index=False)

            dfB_auc = shift_optionB_auc(REGISTRY, signal, FAMILIES, BASELINE,
                                        SHIFT_LEVELS, metric, history_len=50, fs=10.0, phase_unit="deg")
            dfB_auc.to_csv(os.path.join(OUT_ROOT, f"Shift_OptionB_AUC_{signal}_{metric}.csv"), index=False)

            dfB_slope = shift_optionB_slope(REGISTRY, signal, FAMILIES, BASELINE,
                                            SHIFT_LEVELS, SHIFT_X, metric, history_len=50, fs=10.0, phase_unit="deg")
            dfB_slope.to_csv(os.path.join(OUT_ROOT, f"Shift_OptionB_Slope_{signal}_{metric}.csv"), index=False)

    print("All done.")
