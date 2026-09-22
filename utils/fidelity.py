"""
Unified temporal-fidelity metrics for TimeSynth (P0.1 of REVISION_PLAN.md).

One implementation of every metric used in the paper and in the revision.
The phase and frequency code was extracted from Statistical_Test/shift.py and
Statistical_Test/state_transition.py without changing behavior (verified by
tests/test_fidelity.py::test_regression_against_saved_predictions).

Conventions
-----------
* Per-sequence functions take ``pred`` and ``true`` arrays of shape ``[N, H]``
  (a trailing channel axis of size 1 is squeezed) and return one value per
  sequence, shape ``[N]``.  NaN marks a sequence where the metric is undefined
  (unreliable spectrum, no valid phase samples, no detected peaks, ...).
* ``fs`` is the sampling rate in Hz.  Times are in seconds, phases in degrees
  unless ``unit="rad"`` is given.
* Nothing here reads files.  Loading helpers live in ``utils/results_io.py``.
"""
from __future__ import annotations

from typing import Optional, Sequence, Tuple

import numpy as np

__all__ = [
    "mae", "mse",
    "freq_error", "phase_error_deg",
    "band_power_error", "xcorr_lag",
    "detect_peaks", "peak_timing_error", "peak_amplitude_error",
    "peak_detection_f1", "rr_interval_error",
    "crps_empirical",
    "peak_freq_rfft_with_confidence", "analytic_signal_fft", "wrap_to_pi",
    "peak_freq_batch", "analytic_signal_batch",
    "transition_matrix", "stationary_distribution", "transition_kl_rate", "mean_dwell_from_matrix",
]


# ---------------------------------------------------------------------------
# Shape helpers
# ---------------------------------------------------------------------------
def _as_2d(x) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    if x.ndim == 3 and x.shape[-1] == 1:
        x = x[..., 0]
    if x.ndim == 1:
        x = x[None, :]
    if x.ndim != 2:
        raise ValueError(f"expected [N, H] or [N, H, 1], got shape {x.shape}")
    return x


def _pair(pred, true) -> Tuple[np.ndarray, np.ndarray]:
    P, T = _as_2d(pred), _as_2d(true)
    if P.shape != T.shape:
        raise ValueError(f"pred {P.shape} and true {T.shape} differ in shape")
    return P, T


# ---------------------------------------------------------------------------
# Pointwise
# ---------------------------------------------------------------------------
def mae(pred, true) -> np.ndarray:
    """Per-sequence mean absolute error over the horizon. Shape [N]."""
    P, T = _pair(pred, true)
    return np.mean(np.abs(P - T), axis=1)


def mse(pred, true) -> np.ndarray:
    """Per-sequence mean squared error over the horizon. Shape [N]."""
    P, T = _pair(pred, true)
    return np.mean((P - T) ** 2, axis=1)


# ---------------------------------------------------------------------------
# Frequency (Methods Eq. 5)
# ---------------------------------------------------------------------------
def peak_freq_rfft_with_confidence(
    x,
    fs: float = 1.0,
    drop_dc: bool = True,
    parabolic: bool = True,
    peak_frac_thresh: float = 0.1,
    power_thresh: float = 1e-8,
) -> Tuple[float, bool]:
    """
    Dominant frequency of one sequence via one-sided rFFT, plus a reliability flag.

    Identical to ``_peak_freq_rfft_with_confidence`` in the Statistical_Test
    scripts: DC removal, argmax of the power spectrum (excluding the DC bin),
    parabolic interpolation of the peak, and ``reliable = False`` when the peak
    explains less than ``peak_frac_thresh`` of the total (non-DC) power or the
    total power is below ``power_thresh``.
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
        delta = 0.0 if abs(denom) < 1e-12 else 0.5 * (P[k - 1] - P[k + 1]) / denom
        f_est = (k + delta) * (fs / n)

    peak_power = P[k]
    frac = peak_power / total_power if total_power > 0 else 0.0
    reliable = frac >= peak_frac_thresh
    return float(f_est), bool(reliable)


def peak_freq_batch(X, fs: float, peak_frac_thresh: float = 0.1,
                    power_thresh: float = 1e-8) -> Tuple[np.ndarray, np.ndarray]:
    """
    Vectorized ``peak_freq_rfft_with_confidence`` over rows of ``X`` [N, H]
    (DC dropped, parabolic refinement). Returns (f_est [N], reliable [N]).
    Numerically identical to the per-row function.
    """
    X = np.asarray(X, float)
    N, n = X.shape
    if n <= 2:
        return np.zeros(N), np.zeros(N, bool)
    X = X - X.mean(axis=1, keepdims=True)
    P = np.abs(np.fft.rfft(X, n=n, axis=1)) ** 2
    total = P[:, 1:].sum(axis=1)
    k = 1 + np.argmax(P[:, 1:], axis=1)
    rows = np.arange(N)
    f_est = k * (fs / n)
    interior = (k > 0) & (k < P.shape[1] - 1)
    ki = np.where(interior, k, 1)
    denom = P[rows, ki - 1] - 2 * P[rows, ki] + P[rows, ki + 1]
    num = 0.5 * (P[rows, ki - 1] - P[rows, ki + 1])
    with np.errstate(divide="ignore", invalid="ignore"):
        delta = np.where(np.abs(denom) < 1e-12, 0.0, num / denom)
    f_est = np.where(interior, (k + delta) * (fs / n), f_est)
    with np.errstate(divide="ignore", invalid="ignore"):
        frac = np.where(total > 0, P[rows, k] / total, 0.0)
    reliable = (total > power_thresh) & (frac >= peak_frac_thresh)
    f_est = np.where(total > power_thresh, f_est, 0.0)
    return f_est.astype(float), reliable


def freq_error(
    pred,
    true,
    fs: float,
    peak_frac_thresh: float = 0.1,
    power_thresh: float = 1e-8,
) -> np.ndarray:
    """
    Per-sequence |f_pred - f_true| in Hz on the dominant spectral peak.

    NaN where either spectrum fails the reliability filter. Shape [N].
    """
    P, T = _pair(pred, true)
    f_t, ok_t = peak_freq_batch(T, fs, peak_frac_thresh, power_thresh)
    f_p, ok_p = peak_freq_batch(P, fs, peak_frac_thresh, power_thresh)
    out = np.full(T.shape[0], np.nan, float)
    ok = ok_t & ok_p
    out[ok] = np.abs(f_p[ok] - f_t[ok])
    return out


# ---------------------------------------------------------------------------
# Phase (Methods Eq. 6)
# ---------------------------------------------------------------------------
def analytic_signal_fft(x, pad_factor: int = 2) -> np.ndarray:
    """
    Analytic signal z = x + jH{x} via a frequency-domain Hilbert transform with
    zero-padding by ``pad_factor``, cropped back to the input length. The mean is
    removed first. Identical to ``_analytic_signal_fft`` in the Statistical_Test
    scripts (the optional ``smooth_win`` of shift.py was never used).
    """
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


def wrap_to_pi(ang) -> np.ndarray:
    """Unwrap for temporal continuity, then wrap to (-pi, pi]."""
    ang = np.asarray(ang, float)
    ang_unwrapped = np.unwrap(ang)
    return (ang_unwrapped + np.pi) % (2 * np.pi) - np.pi


def phase_error_deg(
    pred,
    true,
    unit: str = "deg",
    amp_frac_thresh: float = 0.2,
    pad_factor: int = 2,
) -> np.ndarray:
    """
    Per-sequence mean |phase_pred - phase_true| from the Hilbert analytic signal.

    Phase is evaluated only where the TRUE analytic amplitude exceeds
    ``amp_frac_thresh`` times its median, which avoids spurious phase in
    low-amplitude regions. NaN where no valid samples exist. Shape [N].
    """
    P, T = _pair(pred, true)
    N, n = T.shape
    scale = 1.0 if unit == "rad" else (180.0 / np.pi)

    zt = analytic_signal_batch(T, pad_factor=pad_factor)
    zp = analytic_signal_batch(P, pad_factor=pad_factor)
    At = np.abs(zt)
    med = np.median(At, axis=1)
    valid_row = np.isfinite(med) & (med != 0)
    mask = At > (amp_frac_thresh * med)[:, None]
    mask &= valid_row[:, None]

    phi_t = np.unwrap(np.angle(zt), axis=1)
    phi_p = np.unwrap(np.angle(zp), axis=1)
    d = phi_p - phi_t
    d = np.unwrap(d, axis=1)                       # wrap_to_pi: unwrap ...
    d = (d + np.pi) % (2 * np.pi) - np.pi          # ... then wrap to (-pi, pi]
    cnt = mask.sum(axis=1)
    out = np.full(N, np.nan, float)
    ok = cnt > 0
    out[ok] = (np.abs(d) * mask).sum(axis=1)[ok] / cnt[ok] * scale
    return out


def analytic_signal_batch(X, pad_factor: int = 2) -> np.ndarray:
    """Row-wise ``analytic_signal_fft`` for X [N, n]. Identical numerics."""
    X = np.asarray(X, float)
    N, n = X.shape
    X = X - X.mean(axis=1, keepdims=True)
    pad_factor = 1 if (pad_factor is None or pad_factor < 1) else int(pad_factor)
    n_fft = int(pad_factor * n)
    F_ = np.fft.fft(X, n=n_fft, axis=1)
    H = np.zeros(n_fft, float)
    if n_fft % 2 == 0:
        H[0] = 1.0
        H[n_fft // 2] = 1.0
        H[1:n_fft // 2] = 2.0
    else:
        H[0] = 1.0
        H[1:(n_fft + 1) // 2] = 2.0
    return np.fft.ifft(F_ * H[None, :], n=n_fft, axis=1)[:, :n]


# ---------------------------------------------------------------------------
# Real-data metrics
# ---------------------------------------------------------------------------
def band_power_error(
    pred,
    true,
    fs: float,
    band: Tuple[float, float],
    relative: bool = True,
) -> np.ndarray:
    """
    Per-sequence error of power inside ``band = (f_lo, f_hi)`` Hz.

    ``relative=True`` returns |P_pred - P_true| / P_true (NaN if P_true == 0);
    otherwise the absolute difference. Power is the rFFT periodogram sum over
    bins with f_lo <= f <= f_hi after mean removal. Shape [N].
    """
    P, T = _pair(pred, true)
    n = T.shape[1]
    f = np.fft.rfftfreq(n, d=1.0 / fs)
    sel = (f >= band[0]) & (f <= band[1])
    if not np.any(sel):
        raise ValueError(f"band {band} contains no FFT bins at fs={fs}, n={n}")

    def _bp(x):
        x = x - x.mean(axis=1, keepdims=True)
        S = np.abs(np.fft.rfft(x, axis=1)) ** 2
        return S[:, sel].sum(axis=1)

    bp_t, bp_p = _bp(T), _bp(P)
    diff = np.abs(bp_p - bp_t)
    if not relative:
        return diff
    out = np.full(T.shape[0], np.nan)
    ok = bp_t > 0
    out[ok] = diff[ok] / bp_t[ok]
    return out


def xcorr_lag(pred, true, fs: float, max_lag_s: Optional[float] = None) -> np.ndarray:
    """
    Per-sequence lag (seconds) of the normalized cross-correlation peak between
    prediction and truth. Positive means the prediction LAGS the truth
    (pred(t) ~ true(t - lag)). Both are mean-removed. Restricted to
    |lag| <= max_lag_s if given. NaN if either sequence is constant. Shape [N].
    """
    P, T = _pair(pred, true)
    N, H = T.shape
    out = np.full(N, np.nan)
    lags = np.arange(-(H - 1), H)
    if max_lag_s is not None:
        keep = np.abs(lags) <= int(round(max_lag_s * fs))
    else:
        keep = np.ones_like(lags, dtype=bool)
    for i in range(N):
        t = T[i] - T[i].mean()
        p = P[i] - P[i].mean()
        st, sp = np.linalg.norm(t), np.linalg.norm(p)
        if st == 0 or sp == 0:
            continue
        # np.correlate(p, t, "full")[k] = sum_m p[m + k - (H-1)] t[m]
        # so the argmax lag k0 satisfies p(t) ~ t(t - k0).
        c = np.correlate(p, t, mode="full") / (st * sp)
        c = np.where(keep, c, -np.inf)
        out[i] = lags[int(np.argmax(c))] / fs
    return out


# ---------------------------------------------------------------------------
# Peak / beat metrics (Tier 2 and real ECG / PPG)
# ---------------------------------------------------------------------------
def detect_peaks(
    x,
    fs: float,
    min_dist_s: float = 0.3,
    prominence_frac: float = 0.3,
) -> np.ndarray:
    """
    Simple prominence-based peak detector applied identically to prediction and
    truth. Returns sample indices of peaks. ``prominence_frac`` is relative to
    the peak-to-peak range of the mean-removed sequence; ``min_dist_s`` is the
    refractory period. Uses scipy.signal.find_peaks.
    """
    from scipy.signal import find_peaks

    x = np.asarray(x, float)
    x = x - x.mean()
    rng = np.ptp(x)
    if rng == 0:
        return np.array([], dtype=int)
    idx, _ = find_peaks(
        x,
        distance=max(1, int(round(min_dist_s * fs))),
        prominence=prominence_frac * rng,
    )
    return idx.astype(int)


def _match_peaks(p_idx: np.ndarray, t_idx: np.ndarray, tol: int):
    """
    Greedy one-to-one matching of predicted to true peak indices within
    ``tol`` samples, in order of increasing distance. Returns (pairs, n_fp, n_fn)
    where pairs is a list of (p, t) index pairs.
    """
    if p_idx.size == 0 or t_idx.size == 0:
        return [], int(p_idx.size), int(t_idx.size)
    d = np.abs(p_idx[:, None] - t_idx[None, :])
    cand = np.argwhere(d <= tol)
    order = np.argsort(d[cand[:, 0], cand[:, 1]], kind="stable")
    used_p, used_t, pairs = set(), set(), []
    for k in order:
        a, b = cand[k]
        if a in used_p or b in used_t:
            continue
        used_p.add(a)
        used_t.add(b)
        pairs.append((int(p_idx[a]), int(t_idx[b])))
    return pairs, int(p_idx.size - len(pairs)), int(t_idx.size - len(pairs))


def _peaks_for(
    pred, true, fs, tol_s, true_peaks, pred_peaks, detector_kwargs,
):
    P, T = _pair(pred, true)
    N = T.shape[0]
    tol = int(round(tol_s * fs))
    kw = detector_kwargs or {}
    for i in range(N):
        t_idx = (np.asarray(true_peaks[i], int) if true_peaks is not None
                 else detect_peaks(T[i], fs, **kw))
        p_idx = (np.asarray(pred_peaks[i], int) if pred_peaks is not None
                 else detect_peaks(P[i], fs, **kw))
        yield i, P[i], T[i], p_idx, t_idx, _match_peaks(p_idx, t_idx, tol)


def peak_timing_error(
    pred, true, fs: float, tol_s: float = 0.05,
    true_peaks: Optional[Sequence] = None, pred_peaks: Optional[Sequence] = None,
    detector_kwargs: Optional[dict] = None,
) -> np.ndarray:
    """
    Per-sequence mean |t_peak_pred - t_peak_true| in SECONDS over matched
    peaks (within ``tol_s``). ``true_peaks`` may supply exact ground-truth
    indices per sequence (Tier 2 sidecar JSON); otherwise ``detect_peaks`` is
    used on both. NaN when no peaks match. Shape [N].
    """
    out = np.full(_as_2d(true).shape[0], np.nan)
    for i, _, _, _, _, (pairs, _, _) in _peaks_for(
            pred, true, fs, tol_s, true_peaks, pred_peaks, detector_kwargs):
        if pairs:
            out[i] = np.mean([abs(p - t) for p, t in pairs]) / fs
    return out


def peak_amplitude_error(
    pred, true, fs: float, tol_s: float = 0.05,
    true_peaks: Optional[Sequence] = None, pred_peaks: Optional[Sequence] = None,
    detector_kwargs: Optional[dict] = None,
) -> np.ndarray:
    """
    Per-sequence mean |A_pred - A_true| at matched peaks, in signal units.
    NaN when no peaks match. Shape [N].
    """
    out = np.full(_as_2d(true).shape[0], np.nan)
    for i, p, t, _, _, (pairs, _, _) in _peaks_for(
            pred, true, fs, tol_s, true_peaks, pred_peaks, detector_kwargs):
        if pairs:
            out[i] = np.mean([abs(p[a] - t[b]) for a, b in pairs])
    return out


def peak_detection_f1(
    pred, true, fs: float, tol_s: float = 0.05,
    true_peaks: Optional[Sequence] = None, pred_peaks: Optional[Sequence] = None,
    detector_kwargs: Optional[dict] = None,
) -> np.ndarray:
    """
    Per-sequence F1 of predicted peaks against true peaks within ``tol_s``.
    NaN when the truth has no peaks. Shape [N].
    """
    out = np.full(_as_2d(true).shape[0], np.nan)
    for i, _, _, _, t_idx, (pairs, n_fp, n_fn) in _peaks_for(
            pred, true, fs, tol_s, true_peaks, pred_peaks, detector_kwargs):
        if t_idx.size == 0:
            continue
        tp = len(pairs)
        denom = 2 * tp + n_fp + n_fn
        out[i] = (2 * tp / denom) if denom > 0 else 0.0
    return out


def rr_interval_error(
    pred, true, fs: float,
    true_peaks: Optional[Sequence] = None, pred_peaks: Optional[Sequence] = None,
    detector_kwargs: Optional[dict] = None,
) -> np.ndarray:
    """
    Per-sequence |mean RR_pred - mean RR_true| in seconds, where RR is the
    inter-peak interval. NaN when either side has fewer than two peaks.
    Shape [N].
    """
    P, T = _pair(pred, true)
    N = T.shape[0]
    out = np.full(N, np.nan)
    kw = detector_kwargs or {}
    for i in range(N):
        t_idx = (np.asarray(true_peaks[i], int) if true_peaks is not None
                 else detect_peaks(T[i], fs, **kw))
        p_idx = (np.asarray(pred_peaks[i], int) if pred_peaks is not None
                 else detect_peaks(P[i], fs, **kw))
        if t_idx.size < 2 or p_idx.size < 2:
            continue
        out[i] = abs(np.mean(np.diff(p_idx)) - np.mean(np.diff(t_idx))) / fs
    return out


# ---------------------------------------------------------------------------
# Probabilistic
# ---------------------------------------------------------------------------
def crps_empirical(samples, true) -> np.ndarray:
    """
    Per-sequence CRPS averaged over the horizon, from an empirical ensemble.

    ``samples`` has shape [S, N, H] (or [S, N, H, 1]); ``true`` has shape [N, H].
    Uses the energy form CRPS = E|X - y| - 0.5 E|X - X'| with the unbiased
    pairwise estimator over the S samples. Shape [N].
    """
    S = np.asarray(samples, float)
    if S.ndim == 4 and S.shape[-1] == 1:
        S = S[..., 0]
    if S.ndim != 3:
        raise ValueError(f"samples must be [S, N, H], got {S.shape}")
    T = _as_2d(true)
    if S.shape[1:] != T.shape:
        raise ValueError(f"samples {S.shape[1:]} and true {T.shape} differ")
    n_s = S.shape[0]
    term1 = np.mean(np.abs(S - T[None]), axis=0)            # [N, H]
    if n_s > 1:
        Ss = np.sort(S, axis=0)
        # sum_{i<j} |x_i - x_j| = sum_k (2k - n + 1) x_(k)   for sorted x
        k = np.arange(n_s, dtype=float)[:, None, None]
        pair_sum = np.sum((2 * k - n_s + 1) * Ss, axis=0)   # [N, H]
        term2 = pair_sum / (n_s * (n_s - 1))                # E|X - X'| / 2 (unbiased)
    else:
        term2 = 0.0
    return np.mean(term1 - term2, axis=1)


# ---------------------------------------------------------------------------
# Markov switching (P4.3)
# ---------------------------------------------------------------------------
def transition_matrix(states, n_states: int = 2, pseudo: float = 0.5) -> np.ndarray:
    """
    Row-stochastic transition matrix estimated from one or many state sequences
    (list of 1-D int arrays or a 2-D array [N, T]); additive smoothing ``pseudo``.
    """
    seqs = [np.asarray(s, int) for s in (states if isinstance(states, (list, tuple)) else np.atleast_2d(states))]
    C = np.full((n_states, n_states), pseudo, float)
    for s in seqs:
        if s.size < 2:
            continue
        np.add.at(C, (s[:-1], s[1:]), 1.0)
    return C / C.sum(axis=1, keepdims=True)


def stationary_distribution(P: np.ndarray) -> np.ndarray:
    w, v = np.linalg.eig(P.T)
    k = int(np.argmin(np.abs(w - 1.0)))
    pi = np.real(v[:, k])
    pi = np.abs(pi) / np.abs(pi).sum()
    return pi


def transition_kl_rate(P: np.ndarray, Q: np.ndarray, symmetric: bool = True) -> float:
    """
    KL divergence rate between two stationary Markov chains with transition
    matrices P (reference, e.g. fitted to the true futures) and Q (fitted to the
    predicted futures): sum_i pi_P(i) * KL(P[i, :] || Q[i, :]). With
    ``symmetric=True`` the two directions are averaged (each weighted by its own
    stationary distribution). Natural log; units nats per step.
    """
    P, Q = np.asarray(P, float), np.asarray(Q, float)

    def _one(A, B):
        pi = stationary_distribution(A)
        with np.errstate(divide="ignore", invalid="ignore"):
            terms = np.where(A > 0, A * np.log(A / B), 0.0)
        return float(np.sum(pi[:, None] * terms))

    return 0.5 * (_one(P, Q) + _one(Q, P)) if symmetric else _one(P, Q)


def mean_dwell_from_matrix(P: np.ndarray, fs: float) -> np.ndarray:
    """Expected dwell time per state in seconds: 1 / ((1 - P_ii) fs)."""
    P = np.asarray(P, float)
    stay = np.clip(np.diag(P), 0.0, 1.0 - 1e-12)
    return 1.0 / ((1.0 - stay) * fs)
