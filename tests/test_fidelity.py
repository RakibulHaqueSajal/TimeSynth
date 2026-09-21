"""
Acceptance tests for utils/fidelity.py (REVISION_PLAN.md P0.1).

Run:  python -m pytest tests/test_fidelity.py -q
"""
import os
import sys

import numpy as np
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from utils import fidelity as F  # noqa: E402

FS = 10.0
H = 100
t = np.arange(H) / FS


def _sine(f, phi_deg=0.0, A=1.0):
    return A * np.sin(2 * np.pi * f * t + np.deg2rad(phi_deg))


# ---------------------------------------------------------------- pointwise
def test_mae_mse_shapes_and_values():
    true = np.stack([_sine(1.0), _sine(1.2)])
    pred = true + 0.1
    assert np.allclose(F.mae(pred, true), 0.1)
    assert np.allclose(F.mse(pred, true), 0.01)
    # 3D input with trailing channel is accepted
    assert F.mae(pred[..., None], true[..., None]).shape == (2,)


# -------------------------------------------------------------------- phase
def test_phase_shift_30deg_recovered():
    true = _sine(1.0)[None]
    pred = _sine(1.0, phi_deg=30.0)[None]
    err = F.phase_error_deg(pred, true)
    assert abs(err[0] - 30.0) < 0.5


def test_phase_error_zero_for_identical():
    x = _sine(1.3)[None]
    assert F.phase_error_deg(x, x)[0] < 1e-9


def test_phase_nan_on_flat_true():
    true = np.zeros((1, H))
    pred = _sine(1.0)[None]
    assert np.isnan(F.phase_error_deg(pred, true)[0])


# ---------------------------------------------------------------- frequency
def test_freq_offset_recovered_within_resolution():
    # 0.05 Hz offset at a 0.1 Hz bin spacing must be resolved after parabolic interpolation
    true = _sine(1.00)[None]
    pred = _sine(1.05)[None]
    err = F.freq_error(pred, true, fs=FS)
    assert abs(err[0] - 0.05) < 0.02


def test_freq_error_unreliable_gives_nan():
    rng = np.random.default_rng(0)
    true = _sine(1.0)[None]
    pred = rng.normal(size=(1, H))  # flat spectrum -> unreliable
    assert np.isnan(F.freq_error(pred, true, fs=FS)[0])


# ------------------------------------------------------------- band / xcorr
def test_band_power_error_zero_and_scaled():
    true = _sine(1.0)[None]
    assert F.band_power_error(true, true, FS, (0.8, 1.2))[0] == 0.0
    pred = 2.0 * true  # power x4 -> relative error 3
    assert abs(F.band_power_error(pred, true, FS, (0.8, 1.2))[0] - 3.0) < 1e-9


def test_xcorr_lag_sign_and_value():
    fs = 100.0
    n = 400
    tt = np.arange(n) / fs
    true = np.exp(-((tt - 2.0) ** 2) / 0.02)[None]
    pred = np.exp(-((tt - 2.2) ** 2) / 0.02)[None]  # prediction is 0.2 s late
    lag = F.xcorr_lag(pred, true, fs)
    assert abs(lag[0] - 0.2) < 1e-9


# ------------------------------------------------------------------- peaks
def _peak_train(fs, n, times, width=0.02, amp=1.0):
    tt = np.arange(n) / fs
    x = np.zeros(n)
    for tc in times:
        x += amp * np.exp(-((tt - tc) ** 2) / (2 * width ** 2))
    return x


def test_peak_timing_error_40ms():
    fs = 250.0
    n = 2500
    true_t = np.arange(0.5, 9.5, 1.0)
    true = _peak_train(fs, n, true_t)[None]
    pred = _peak_train(fs, n, true_t + 0.040)[None]
    err = F.peak_timing_error(pred, true, fs, tol_s=0.1)
    assert abs(err[0] - 0.040) < 1.0 / fs + 1e-12
    assert F.peak_detection_f1(pred, true, fs, tol_s=0.1)[0] == 1.0
    assert F.rr_interval_error(pred, true, fs)[0] < 1.0 / fs + 1e-12


def test_peak_amplitude_and_f1_with_missing_peak():
    fs = 250.0
    n = 2500
    true_t = np.arange(0.5, 9.5, 1.0)          # 9 peaks
    true = _peak_train(fs, n, true_t)[None]
    pred = _peak_train(fs, n, true_t[:-1], amp=0.8)[None]  # 8 peaks, 80 % amplitude
    assert abs(F.peak_amplitude_error(pred, true, fs)[0] - 0.2) < 1e-6
    f1 = F.peak_detection_f1(pred, true, fs)[0]
    assert abs(f1 - (2 * 8) / (2 * 8 + 0 + 1)) < 1e-9


def test_peak_metrics_accept_ground_truth_indices():
    fs = 250.0
    n = 2500
    true_t = np.arange(0.5, 9.5, 1.0)
    true = _peak_train(fs, n, true_t)[None]
    gt_idx = [np.round(true_t * fs).astype(int)]
    err = F.peak_timing_error(true, true, fs, true_peaks=gt_idx)
    assert err[0] < 1.0 / fs + 1e-12


# -------------------------------------------------------------------- CRPS
def test_crps_reduces_to_mae_for_point_forecast():
    true = _sine(1.0)[None]
    pred = true + 0.3
    crps = F.crps_empirical(pred[None], true)  # S = 1
    assert np.allclose(crps, F.mae(pred, true))


def test_crps_gaussian_closed_form():
    # For X ~ N(mu, s^2), CRPS(y) = s * [ z(2Phi(z)-1) + 2 phi(z) - 1/sqrt(pi) ], z=(y-mu)/s
    from scipy.stats import norm
    rng = np.random.default_rng(1)
    S, N, Hh = 4000, 1, 5
    mu, s = 0.0, 1.0
    y = np.array([[0.0, 0.5, 1.0, -1.0, 2.0]])
    samples = rng.normal(mu, s, size=(S, N, Hh))
    est = F.crps_empirical(samples, y)[0]
    z = (y[0] - mu) / s
    exact = s * (z * (2 * norm.cdf(z) - 1) + 2 * norm.pdf(z) - 1 / np.sqrt(np.pi))
    assert abs(est - exact.mean()) < 0.02


# ------------------------------------------------------------- regression
LEGACY = os.path.join(
    ROOT, "Train_Test_Validation",
    "long_term_forecast_Linear_50_100_Linear_Drift_Harmonic_Clean_70_10_20_0.001_0.0001_16_Shift_0")


@pytest.mark.skipif(not os.path.isdir(LEGACY), reason="paper predictions not on disk")
def test_regression_against_saved_predictions():
    """
    The unified module must reproduce the paper's per-series phase and
    frequency errors to 1e-6 on a saved pred/true pair.
    """
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import _legacy_metrics as legacy_clean  # frozen copy of the paper-era code
    from utils.results_io import load_legacy

    hist, true, pred = load_legacy(LEGACY, history_len=50)
    n = 2000  # subset for speed; stride-1 windows are highly redundant anyway
    true, pred = true[:n], pred[:n]

    new_phase = F.phase_error_deg(pred, true, unit="deg")
    new_freq = F.freq_error(pred, true, fs=10.0)

    old_phase = np.array([
        _old_phase_one(legacy_clean, pred[i], true[i]) for i in range(n)])
    old_freq = np.array([
        _old_freq_one(legacy_clean, pred[i], true[i]) for i in range(n)])

    assert np.array_equal(np.isnan(new_phase), np.isnan(old_phase))
    assert np.array_equal(np.isnan(new_freq), np.isnan(old_freq))
    m = ~np.isnan(new_phase)
    assert np.max(np.abs(new_phase[m] - old_phase[m])) < 1e-6
    m = ~np.isnan(new_freq)
    assert np.max(np.abs(new_freq[m] - old_freq[m])) < 1e-6


def _old_phase_one(mod, yh, y, amp_frac_thresh=0.2):
    # verbatim copy of the loop body of Statistical_Test/clean.py::per_series_phase_error
    y = y - y.mean()
    yh = yh - yh.mean()
    zt = mod._analytic_signal_fft(y)
    zp = mod._analytic_signal_fft(yh)
    At = np.abs(zt)
    med_amp = np.median(At)
    if not np.isfinite(med_amp) or med_amp == 0:
        return np.nan
    mask = At > (amp_frac_thresh * med_amp)
    if not np.any(mask):
        return np.nan
    phi_t = np.unwrap(np.angle(zt))
    phi_p = np.unwrap(np.angle(zp))
    dphi = mod._wrap_to_pi(phi_p - phi_t)
    sel = dphi[mask]
    if sel.size == 0:
        return np.nan
    return float(np.mean(np.abs(np.degrees(sel))))


def _old_freq_one(mod, yh, y, fs=10.0):
    f_t, ok_t = mod._peak_freq_rfft_with_confidence(y, fs=fs)
    f_p, ok_p = mod._peak_freq_rfft_with_confidence(yh, fs=fs)
    return abs(f_p - f_t) if (ok_t and ok_p) else np.nan


# ---------------------------------------------------- vectorized == loop
def test_vectorized_matches_reference_loop():
    """The batched phase/frequency code must equal the per-row reference to 1e-9."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import _legacy_metrics as L
    rng = np.random.default_rng(3)
    N = 300
    f = rng.uniform(0.6, 1.4, N)
    ph = rng.uniform(-np.pi, np.pi, N)
    true = np.sin(2 * np.pi * f[:, None] * t + ph[:, None]) + 0.05 * rng.normal(size=(N, H))
    pred = np.sin(2 * np.pi * (f + rng.normal(0, 0.05, N))[:, None] * t + (ph + 0.3)[:, None]) \
        + 0.3 * rng.normal(size=(N, H))
    pred[:5] = 0.0                     # flat predictions -> unreliable spectrum
    true[5:8] = 0.0                    # flat truth -> NaN phase
    ref_ph = np.array([_old_phase_one(L, pred[i], true[i]) for i in range(N)])
    ref_fr = np.array([_old_freq_one(L, pred[i], true[i]) for i in range(N)])
    new_ph = F.phase_error_deg(pred, true)
    new_fr = F.freq_error(pred, true, fs=FS)
    assert np.array_equal(np.isnan(ref_ph), np.isnan(new_ph))
    assert np.array_equal(np.isnan(ref_fr), np.isnan(new_fr))
    m = ~np.isnan(ref_ph)
    assert np.max(np.abs(ref_ph[m] - new_ph[m])) < 1e-9
    m = ~np.isnan(ref_fr)
    assert np.max(np.abs(ref_fr[m] - new_fr[m])) < 1e-9
