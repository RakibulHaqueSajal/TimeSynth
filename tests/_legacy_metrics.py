"""Frozen copy of the paper-era metric code (git main, Statistical_Test/clean.py) used only for the regression test."""
import numpy as np
def _peak_freq_rfft_with_confidence(
    x,
    fs: float = 1.0,
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
    split="test",
    history_len=50,
    fs=10.0,
    peak_frac_thresh=0.1,
    power_thresh=1e-8,
) -> np.ndarray:
    true, pred = _load_true_pred(model_path, split=split)
    Y = true[:, history_len:]
    YH = pred[:, history_len:]

    N = Y.shape[0]
    out = np.full(N, np.nan, dtype=float)

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
    x = np.asarray(x, dtype=float)
    n = x.size
    x = x - x.mean()

    pad_factor = 1 if (pad_factor is None or pad_factor < 1) else int(pad_factor)
    n_fft = int(pad_factor * n)

    X = np.fft.fft(x, n=n_fft)

    H = np.zeros(n_fft, dtype=float)
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
    ang = np.asarray(ang, dtype=float)
    ang_unwrapped = np.unwrap(ang)
    return (ang_unwrapped + np.pi) % (2 * np.pi) - np.pi


def per_series_phase_error(
    model_path: str,
    split="test",
    history_len=50,
    unit="deg",
    amp_frac_thresh=0.2,
) -> np.ndarray:
    true, pred = _load_true_pred(model_path, split=split)
    Y = true[:, history_len:]
    YH = pred[:, history_len:]

    N = Y.shape[0]
    out = np.full(N, np.nan, dtype=float)
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


# -------------------------
# Core: build per-model vectors + valid mask
# -------------------------
