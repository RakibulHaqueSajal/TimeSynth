import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from tqdm import tqdm
# import pmdarima as pm
import threading
from sklearn.ensemble import GradientBoostingRegressor
import numpy as np
import torch
import torch.nn as nn
import pandas as pd

from darts import TimeSeries
from darts.models import KalmanForecaster as DartsKalman
from darts.utils.timeseries_generation import datetime_attribute_timeseries

import numpy as np
import torch
import torch.nn as nn
import pandas as pd

from darts import TimeSeries
from darts.models import ARIMA as DartsARIMA
from darts.utils.timeseries_generation import datetime_attribute_timeseries

from statsmodels.tsa.arima.model import ARIMA as SM_ARIMA


from statsmodels.tsa.statespace.sarimax import SARIMAX


from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA



# class Naive_repeat(nn.Module):
#     """
#     Naive baseline: repeat last observed value for all forecast steps.
#     Input:  x [B, L, D] (torch.Tensor or np.ndarray)
#     Output: [B, pred_len, D] (np.ndarray)
#     """
#     def __init__(self, configs):
#         super(Naive_repeat, self).__init__()
#         self.pred_len = configs.pred_len

#     def forward(self, x):
#         # Accept both torch.Tensor and numpy
#         if isinstance(x, torch.Tensor):
#             x_np = x.detach().cpu().numpy()
#         else:
#             x_np = np.asarray(x)

#         B, L, D = x_np.shape
#         last = x_np[:, -1:, :]               # [B, 1, D]
#         result = np.repeat(last, self.pred_len, axis=1)  # [B, pred_len, D]
#         return result


# class Naive_thread(threading.Thread):
#     """
#     Simple wrapper to run a function in a separate thread and
#     retrieve its result later.
#     """
#     def __init__(self, func, args=()):
#         super(Naive_thread, self).__init__()
#         self.func = func
#         self.args = args
#         self.results = None

#     def run(self):
#         self.results = self.func(*self.args)

#     def return_result(self):
#         threading.Thread.join(self)
#         return self.results


# import numpy as np
# import torch
# import torch.nn as nn
# from statsforecast.models import AutoARIMA


# import numpy as np
# import torch
# import torch.nn as nn
# from statsforecast.models import AutoARIMA


# class Arima(nn.Module):
#     """
#     AutoARIMA baseline using the *new* statsforecast API:

#         arima = AutoARIMA(season_length=4)
#         arima = arima.fit(y=ap)
#         y_hat_dict = arima.predict(h=4, level=[80])

#     Input : x [B, L, D] (torch.Tensor or np.ndarray, float)
#     Output: [B, pred_len, D] (np.ndarray, float32)

#     configs:
#         pred_len                : forecast horizon (required)
#         seq_len                 : expected input length L (optional sanity check)
#         arima_season_length     : season_length for AutoARIMA (default 1)
#         arima_min_len           : minimum length to fit ARIMA (default season_length + 5)
#         autoarima_kwargs        : extra scalar kwargs passed to AutoARIMA(...)
#                                   (e.g. {'d': None, 'seasonal': True})
#     """

#     def __init__(self, configs):
#         super().__init__()
#         self.pred_len = configs.pred_len
#         self.seq_len = getattr(configs, "seq_len", None)

#         self.season_length = 10
#         self.min_len = getattr(configs, "arima_min_len", self.season_length + 5)

#         raw_kwargs = getattr(configs, "autoarima_kwargs", {})
#         self.auto_kwargs =dict(
#             seasonal=True,
#             stationary=False,
#             stepwise=False,
#         )

#     # ---------------------------------------------------------
#     # Helpers
#     # ---------------------------------------------------------
#     @staticmethod
#     def _safe_autoarima_kwargs(kwargs):
#         """
#         AutoARIMA only expects scalar-like kwargs (int/float/bool/None).
#         Drop dicts, lists, etc. so we don't blow up inside the library.
#         """
#         safe = {}
#         for k, v in kwargs.items():
#             if isinstance(v, (int, float, bool)) or v is None:
#                 safe[k] = v
#             else:
#                 print(f"[Arima] Ignoring AutoARIMA kwarg '{k}' of type {type(v)}")
#         return safe

#     @staticmethod
#     def _clean_series(y):
#         """
#         y: 1D np.ndarray (float)
#         Replace NaN/inf with last finite (or 0 if none).
#         """
#         y = np.asarray(y, dtype=np.float64)

#         if not np.isfinite(y).all():
#             finite = np.isfinite(y)
#             if finite.any():
#                 last_val = y[finite][-1]
#             else:
#                 last_val = 0.0
#             y = np.where(finite, y, last_val)

#         return y

#     def _forecast_one(self, y):
#         """
#         Fit AutoARIMA on 1D series y and forecast pred_len.
#         Uses new API: fit(y=...) then predict(h=...).

#         Returns: np.ndarray [pred_len] float32
#         """
#         y = self._clean_series(y)

#         # too short or almost constant → naive
#         if y.shape[0] < self.min_len or np.allclose(y, y[0]):
#             return np.full(self.pred_len, y[-1], dtype=np.float32)

#         try:
#             # Instantiate model
#             model = AutoARIMA(
#                 season_length=self.season_length,
#                 **self.auto_kwargs,
#             )

#             # NEW API: fit(y=...)
#             model = model.fit(y=y)

#             # NEW API: predict(h=..., level=...) returns a dict
#             # We only care about the mean forecast.
#             res = model.predict(h=self.pred_len)  # e.g. {'mean': np.array, ...}

#             if isinstance(res, dict):
#                 if "mean" not in res:
#                     raise RuntimeError(f"AutoARIMA.predict returned dict without 'mean' key: {res.keys()}")
#                 fcst = np.asarray(res["mean"], dtype=np.float32).reshape(-1)
#             else:
#                 # Just in case some version returns an array directly
#                 fcst = np.asarray(res, dtype=np.float32).reshape(-1)

#             # pad / crop as safety
#             if fcst.shape[0] < self.pred_len:
#                 pad_val = fcst[-1] if fcst.size > 0 else 0.0
#                 pad = np.full(self.pred_len - fcst.shape[0], pad_val, dtype=np.float32)
#                 fcst = np.concatenate([fcst, pad])
#             elif fcst.shape[0] > self.pred_len:
#                 fcst = fcst[: self.pred_len]

#             return fcst

#         except Exception as e:
#             print(f"[Arima/AutoARIMA] Failed on series: {repr(e)} → Naive_repeat")
#             return np.full(self.pred_len, y[-1], dtype=np.float32)

#     # ---------------------------------------------------------
#     # Forward
#     # ---------------------------------------------------------
#     def forward(self, x):
#         """
#         x: [B, L, D] float tensor or np.ndarray
#         """
#         if isinstance(x, torch.Tensor):
#             x_np = x.detach().cpu().numpy().astype(np.float64)
#         else:
#             x_np = np.asarray(x, dtype=np.float64)

#         B, L, D = x_np.shape

#         if self.seq_len is not None and L != self.seq_len:
#             raise ValueError(f"Arima: seq_len mismatch (got L={L}, expected {self.seq_len})")

#         out = np.zeros((B, self.pred_len, D), dtype=np.float32)

#         for b in range(B):
#             for d in range(D):
#                 series_1d = x_np[b, :, d]  # [L]
#                 out[b, :, d] = self._forecast_one(series_1d)

#         return out  # [B, pred_len, D]


# # -------------------------------------------------------------------
# # ARIMA (auto_arima) – very slow, use small sample
# # -------------------------------------------------------------------

# # def _arima(seq, pred_len, bt, i):
# #     """
# #     Helper for ARIMA: fit auto_arima on 1D seq and predict pred_len.
# #     seq: 1D np.ndarray
# #     Returns forecasts, batch index, feature index.
# #     """
# #     try:
# #         model = pm.auto_arima(seq, error_action='ignore', suppress_warnings=True)
# #         forecasts = model.predict(pred_len)
# #         forecasts = np.asarray(forecasts, dtype=float).reshape(-1)
# #     except Exception:
# #         last = seq[-1]
# #         forecasts = np.full(pred_len, last, dtype=float)
# #     return forecasts, bt, i


# # class Arima(nn.Module):
# #     """
# #     ARIMA baseline using pmdarima.auto_arima.
# #     Extremely slow – use args.sample << 1.
# #     Input:  x [B, L, D] (torch.Tensor or np.ndarray)
# #     Output: [B, pred_len, D] (np.ndarray)
# #     """
# #     def __init__(self, configs):
# #         super(Arima, self).__init__()
# #         self.pred_len = configs.pred_len

# #     def forward(self, x):
# #         # Accept both torch.Tensor and numpy
# #         if isinstance(x, torch.Tensor):
# #             x_np = x.detach().cpu().numpy()
# #         else:
# #             x_np = np.asarray(x)

# #         B, L, D = x_np.shape
# #         result = np.zeros((B, self.pred_len, D), dtype=float)
# #         threads = []

# #         for bt, seqs in tqdm(enumerate(x_np), total=B, desc="ARIMA fitting"):
# #             for i in range(D):
# #                 seq = seqs[:, i]
# #                 one_seq = Naive_thread(
# #                     func=_arima,
# #                     args=(seq, self.pred_len, bt, i)
# #                 )
# #                 threads.append(one_seq)
# #                 one_seq.start()

# #         for every_thread in tqdm(threads, desc="ARIMA collecting"):
# #             forecast, bt, i = every_thread.return_result()
# #             result[bt, :, i] = forecast

# #         return result  # [B, pred_len, D]


# # -------------------------------------------------------------------
# # Seasonal ARIMA (SARIMA) – auto_arima with seasonal=True
# # -------------------------------------------------------------------

# def _sarima(season, seq, pred_len, bt, i):
#     """
#     Helper for SARIMA: seasonal auto_arima with period m=season.
#     """
#     try:
#         model = pm.auto_arima(
#             seq,
#             seasonal=True,
#             m=season,
#             error_action='ignore',
#             suppress_warnings=True
#         )
#         forecasts = model.predict(pred_len)
#         forecasts = np.asarray(forecasts, dtype=float).reshape(-1)
#     except Exception:
#         last = seq[-1]
#         forecasts = np.full(pred_len, last, dtype=float)
#     return forecasts, bt, i


# class SArima(nn.Module):
#     """
#     Seasonal ARIMA baseline.
#     Extremely extremely slow, use args.sample << 1.
#     Season is inferred heuristically from dataset name.
#     """
#     def __init__(self, configs):
#         super(SArima, self).__init__()
#         self.pred_len = configs.pred_len
#         self.seq_len = configs.seq_len

#         # crude heuristic for seasonality (consistent with some LTSF repos)
#         season = 24
#         if hasattr(configs, "data_path"):
#             if 'Ettm' in configs.data_path:
#                 season = 12
#             elif 'ILI' in configs.data_path:
#                 season = 1
#         if season >= self.seq_len:
#             season = 1
#         self.season = season

#     def forward(self, x):
#         if isinstance(x, torch.Tensor):
#             x_np = x.detach().cpu().numpy()
#         else:
#             x_np = np.asarray(x)

#         B, L, D = x_np.shape
#         result = np.zeros((B, self.pred_len, D), dtype=float)
#         threads = []

#         for bt, seqs in tqdm(enumerate(x_np), total=B, desc="SARIMA fitting"):
#             for i in range(D):
#                 seq = seqs[:, i]
#                 one_seq = Naive_thread(
#                     func=_sarima,
#                     args=(self.season, seq, self.pred_len, bt, i)
#                 )
#                 threads.append(one_seq)
#                 one_seq.start()

#         for every_thread in tqdm(threads, desc="SARIMA collecting"):
#             forecast, bt, i = every_thread.return_result()
#             result[bt, :, i] = forecast

#         return result  # [B, pred_len, D]


# # -------------------------------------------------------------------
# # Gradient Boosting Regression Trees (GBRT) on time index
# # -------------------------------------------------------------------

# def _gbrt(seq, seq_len, pred_len, bt, i):
#     """
#     Fit GradientBoostingRegressor on (time_index -> value).
#     """
#     x_idx = np.arange(seq_len).reshape(-1, 1)
#     y_val = seq.reshape(-1, 1)

#     try:
#         model = GradientBoostingRegressor()
#         model.fit(x_idx, y_val.ravel())
#         future_idx = np.arange(seq_len, seq_len + pred_len).reshape(-1, 1)
#         forecasts = model.predict(future_idx)
#         forecasts = np.asarray(forecasts, dtype=float).reshape(-1)
#     except Exception:
#         last = seq[-1]
#         forecasts = np.full(pred_len, last, dtype=float)

#     return forecasts, bt, i


# class GBRT(nn.Module):
#     """
#     GBRT baseline: regress value on time index and extrapolate.
#     Input:  x [B, L, D]
#     Output: [B, pred_len, D]
#     """
#     def __init__(self, configs):
#         super(GBRT, self).__init__()
#         self.seq_len = configs.seq_len
#         self.pred_len = configs.pred_len

#     def forward(self, x):
#         if isinstance(x, torch.Tensor):
#             x_np = x.detach().cpu().numpy()
#         else:
#             x_np = np.asarray(x)

#         B, L, D = x_np.shape
#         assert L == self.seq_len, "seq_len mismatch in GBRT"

#         result = np.zeros((B, self.pred_len, D), dtype=float)
#         threads = []

#         for bt, seqs in tqdm(enumerate(x_np), total=B, desc="GBRT fitting"):
#             for i in range(D):
#                 seq = seqs[:, i]
#                 one_seq = Naive_thread(
#                     func=_gbrt,
#                     args=(seq, self.seq_len, self.pred_len, bt, i)
#                 )
#                 threads.append(one_seq)
#                 one_seq.start()

#         for every_thread in tqdm(threads, desc="GBRT collecting"):
#             forecast, bt, i = every_thread.return_result()
#             result[bt, :, i] = forecast

#         return result  # [B, pred_len, D]

class KalmanForecaster(nn.Module):
    """
    Wrapper around Darts KalmanForecaster so it fits your Exp_Basic API.

    Input:  x [B, L, D]  (torch.Tensor or np.ndarray)
    Output: [B, pred_len, D] (np.ndarray)
    """
    def __init__(self, configs):
        super(KalmanForecaster, self).__init__()
        self.pred_len = configs.pred_len
        # latent state dimension of the Kalman filter
        self.dim_x = getattr(configs, "dim_x", 2)

        # optional knobs from args (if you want them)
        self.use_datetime_cov = getattr(configs, "kalman_use_cov", False)
        self.freq = getattr(configs, "kalman_freq", "S") # 'D', 'H', etc.

    def _make_series(self, values_2d):
        """
        values_2d: [L, D] numpy
        Returns a Darts TimeSeries with a dummy time index.
        """
        L = values_2d.shape[0]
        time_index = pd.date_range(start="2000-01-01", periods=L, freq=self.freq)
        return TimeSeries.from_times_and_values(time_index, values_2d)

    def forward(self, x):
        # Accept both torch.Tensor and numpy
        if isinstance(x, torch.Tensor):
            x_np = x.detach().cpu().numpy()
        else:
            x_np = np.asarray(x)

        B, L, D = x_np.shape
        out = np.zeros((B, self.pred_len, D), dtype=np.float32)

        for b in range(B):
            # build TimeSeries for this sample (multivariate if D > 1)
            series = self._make_series(x_np[b])  # [L, D] -> TimeSeries

            # optional future covariates (month as cyclic encoding)
            if self.use_datetime_cov:
                future_cov = datetime_attribute_timeseries(
                    series,
                    attribute="month",
                    cyclic=True,
                    add_length=self.pred_len,
                )
                model = DartsKalman(dim_x=self.dim_x)
                model.fit(series, future_covariates=future_cov)
                pred = model.predict(self.pred_len, future_covariates=future_cov)
            else:
                model = DartsKalman(dim_x=self.dim_x)
                model.fit(series)
                pred = model.predict(self.pred_len)

            # Darts returns a TimeSeries; convert to numpy
            # pred.values(): [pred_len, D]
            out[b] = pred.values().astype(np.float32)

        # shape: [B, pred_len, D]
        return out


import numpy as np
import torch
import torch.nn as nn
import math


def _aic_from_residuals(residuals, n_params):
    """
    AIC = 2k - 2 log L,   assuming Gaussian residuals.
    log L = -0.5 * n * [log(2π) + log(σ^2) + 1]
    """
    n = residuals.shape[0]
    if n <= 0:
        return np.inf

    sigma2 = float(np.mean(residuals ** 2))
    if sigma2 <= 0 or not np.isfinite(sigma2):
        return np.inf

    loglik = -0.5 * n * (math.log(2 * math.pi) + math.log(sigma2) + 1.0)
    return 2 * n_params - 2 * loglik


def _fit_ar_least_squares(series, p):
    """
    Fit AR(p) with intercept via least squares on 1D series.
    series: 1D np.ndarray
    Returns (intercept, phi, residuals, aic)
        intercept: float
        phi: np.ndarray of shape [p] (possibly length 0 if p=0)
    """
    series = np.asarray(series, dtype=float)
    n = series.shape[0]

    # Not enough data for this order
    if n <= p + 1:
        return None

    if p == 0:
        # Model: y_t = c + e_t
        c = float(series.mean())
        residuals = series - c
        aic = _aic_from_residuals(residuals, n_params=1)  # c only
        return c, np.zeros(0, dtype=float), residuals, aic

    # Build design matrix X and target y:
    # For t = p..n-1: y_t = c + sum_{k=1..p} phi_k * y_{t-k}
    y = series[p:]  # shape [n - p]
    T = y.shape[0]
    X = np.ones((T, p + 1), dtype=float)  # intercept + p lags

    for k in range(1, p + 1):
        # column k is y_{t-k}
        X[:, k] = series[p - k : n - k]

    # Solve least squares using torch for consistency
    X_t = torch.from_numpy(X).double()
    y_t = torch.from_numpy(y).double()

    # beta = (X^T X)^(-1) X^T y   via lstsq
    beta, *_ = torch.linalg.lstsq(X_t, y_t.unsqueeze(-1))
    beta = beta.squeeze(-1).cpu().numpy()  # shape [p+1]

    c = float(beta[0])
    phi = beta[1:].astype(float)  # shape [p]

    y_hat = X @ beta
    residuals = y - y_hat
    aic = _aic_from_residuals(residuals, n_params=(p + 1))  # c + p AR params

    return c, phi, residuals, aic


def _auto_ar_for_diff_series(diff_series, max_p):
    """
    Given a differenced series (or original if d=0), select AR(p) by AIC.
    Returns (best_p, best_c, best_phi) or (None, None, None) if fail.
    """
    best_aic = np.inf
    best_p = None
    best_c = None
    best_phi = None

    for p in range(0, max_p + 1):
        res = _fit_ar_least_squares(diff_series, p)
        if res is None:
            continue
        c, phi, residuals, aic = res
        if aic < best_aic:
            best_aic = aic
            best_p = p
            best_c = c
            best_phi = phi

    return best_p, best_c, best_phi


def _forecast_ar(series, p, c, phi, pred_len):
    """
    AR(p) forecast on a *given* series (no differencing).
    series: 1D np.ndarray (training data)
    Returns forecast of length pred_len (np.ndarray).
    """
    series = list(np.asarray(series, dtype=float))
    forecasts = []

    for _ in range(pred_len):
        if p == 0:
            y_hat = c
        else:
            # y_hat = c + sum_{k=1..p} phi_k * y_{t-k}
            y_hat = c
            for k in range(1, p + 1):
                y_hat += phi[k - 1] * series[-k]
        series.append(float(y_hat))
        forecasts.append(float(y_hat))

    return np.asarray(forecasts, dtype=float)


def _forecast_arima_p_d_0(z, d, p, c, phi, pred_len):
    """
    Forecast ARIMA(p,d,0) by:
      1) Building the differenced series up to order d.
      2) Applying AR(p) on the highest-order difference.
      3) Integrating back to the original scale.

    z: original 1D np.ndarray
    d: 0, 1, or 2
    p, c, phi: AR model params on the d-th difference.
    """
    z = np.asarray(z, dtype=float)
    if z.ndim != 1:
        z = z.reshape(-1)

    if d == 0:
        # AR(p) directly on z
        return _forecast_ar(z, p, c, phi, pred_len)

    elif d == 1:
        # y^{(1)}_t = z_t - z_{t-1}
        y1 = np.diff(z)  # length n-1
        y1 = list(y1)
        z_last = float(z[-1])

        forecasts = []
        for _ in range(pred_len):
            if p == 0:
                diff_hat = c
            else:
                diff_hat = c
                for k in range(1, p + 1):
                    diff_hat += phi[k - 1] * y1[-k]
            y1.append(float(diff_hat))
            z_last = z_last + diff_hat
            forecasts.append(float(z_last))

        return np.asarray(forecasts, dtype=float)

    elif d == 2:
        # y^{(1)}_t = z_t - z_{t-1}
        # y^{(2)}_t = y^{(1)}_t - y^{(1)}_{t-1}
        y1 = np.diff(z)
        y2 = np.diff(y1)
        y2 = list(y2)

        y1_last = float(y1[-1])
        z_last = float(z[-1])

        forecasts = []
        for _ in range(pred_len):
            if p == 0:
                y2_hat = c
            else:
                y2_hat = c
                for k in range(1, p + 1):
                    y2_hat += phi[k - 1] * y2[-k]
            y2.append(float(y2_hat))

            # integrate y2 → y1 → z
            y1_last = y1_last + y2_hat
            z_last = z_last + y1_last
            forecasts.append(float(z_last))

        return np.asarray(forecasts, dtype=float)

    else:
        raise NotImplementedError("This implementation supports d in {0,1,2} only.")


def _auto_arima_p_d_0(z, max_p=3, max_d=2, min_length=10):
    """
    Restricted AutoARIMA: search over p in [0,max_p], d in [0,max_d], q=0.
    Selects (p,d) by AIC of AR(p) fit on d-th differenced series.
    Returns (best_d, best_p, best_c, best_phi).
    """
    z = np.asarray(z, dtype=float)
    if z.ndim != 1:
        z = z.reshape(-1)

    n = z.shape[0]
    if n < min_length:
        # fallback: constant forecast from mean
        mean_val = float(z.mean())
        return 0, 0, mean_val, np.zeros(0, dtype=float)

    best_aic = np.inf
    best_model = (0, 0, float(z.mean()), np.zeros(0, dtype=float))

    for d in range(0, max_d + 1):
        if d == 0:
            series_d = z
        elif d == 1:
            if n - 1 < min_length:
                continue
            series_d = np.diff(z)
        elif d == 2:
            if n - 2 < min_length:
                continue
            y1 = np.diff(z)
            series_d = np.diff(y1)
        else:
            # Not implemented
            continue

        # Fit AR on series_d
        p, c, phi = _auto_ar_for_diff_series(series_d, max_p=max_p)
        if p is None:
            continue

        # Compute residuals and AIC again (slight duplication, but fine)
        # For simplicity, re-run fit function
        c_, phi_, residuals, aic = _fit_ar_least_squares(series_d, p)
        if aic < best_aic:
            best_aic = aic
            best_model = (d, p, c, phi)

    return best_model  # (best_d, best_p, best_c, best_phi)


class ARIMA(nn.Module):
    """
    TorchAutoARIMA: restricted AutoARIMA(p,d,0) implemented in PyTorch/NumPy.

    - Input:  x [B, L, D]  (torch.Tensor or np.ndarray, float)
    - Output: [B, pred_len, D]  (np.ndarray, float32)
    - Per series (b, d): we run a small AutoARIMA search:
        d ∈ [0, max_d], p ∈ [0, max_p], q = 0
      using AIC to choose the best model.

    Notes:
      * This is NON-differentiable and intended as a classical baseline.
      * No seasonal part, no MA(q), no exogenous regressors.
      * All fitting is done on CPU.
    """

    def __init__(self, configs):
        super().__init__()
        self.pred_len = configs.pred_len
        self.max_p = getattr(configs, "arima_max_p", 2)
        self.max_d = getattr(configs, "arima_max_d", 2)
        self.min_length = getattr(configs, "arima_min_len", 10)

    def forward(self, x):
        """
        x: [B, L, D] torch.Tensor or np.ndarray
        returns: [B, pred_len, D] np.ndarray (float32)
        """
        # Convert to numpy
        if isinstance(x, torch.Tensor):
            x_np = x.detach().cpu().numpy()
        else:
            x_np = np.asarray(x, dtype=float)

        B, L, D = x_np.shape
        result = np.zeros((B, self.pred_len, D), dtype=np.float32)

        for b in range(B):
            for i in range(D):
                seq = x_np[b, :, i]  # 1D series

                # Auto-select (d, p) and AR params
                best_d, best_p, best_c, best_phi = _auto_arima_p_d_0(
                    seq,
                    max_p=self.max_p,
                    max_d=self.max_d,
                    min_length=self.min_length,
                )

                # Forecast
                forecast = _forecast_arima_p_d_0(
                    seq,
                    d=best_d,
                    p=best_p,
                    c=best_c,
                    phi=best_phi,
                    pred_len=self.pred_len,
                )

                result[b, :, i] = forecast.astype(np.float32)

        return result  # [B, pred_len, D]


import numpy as np
import torch
import torch.nn as nn
import math


# -----------------------------
#  Differencing / Integration
# -----------------------------

def _difference_series(z, d):
    """
    Apply d-th order differencing to 1D series z.
    Returns (y, aux) where:
      y   : differenced series (np.ndarray, 1D)
      aux : dict with info needed to integrate back.
    """
    z = np.asarray(z, dtype=float).reshape(-1)
    aux = {"d": d}

    if d == 0:
        aux["z_last"] = float(z[-1])
        return z, aux

    if d == 1:
        y1 = np.diff(z)
        aux["z_last"] = float(z[-1])
        return y1, aux

    if d == 2:
        y1 = np.diff(z)
        y2 = np.diff(y1)
        aux["z_last"] = float(z[-1])
        aux["y1_last"] = float(y1[-1])
        return y2, aux

    # you can extend this, but let's cap at d<=2
    raise NotImplementedError("This implementation supports d in {0,1,2} only.")


def _integrate_forecast(y_forecast, aux):
    """
    Integrate forecasted differenced series back to original scale
    using metadata in aux returned by _difference_series().
    """
    d = aux["d"]
    y_forecast = np.asarray(y_forecast, dtype=float).reshape(-1)
    H = y_forecast.shape[0]

    if d == 0:
        # already on original scale
        return y_forecast

    if d == 1:
        z_last = aux["z_last"]
        out = []
        z_t = z_last
        for k in range(H):
            z_t = z_t + y_forecast[k]
            out.append(z_t)
        return np.asarray(out, dtype=float)

    if d == 2:
        z_last = aux["z_last"]
        y1_last = aux["y1_last"]
        out = []
        z_t = z_last
        y1_t = y1_last
        for k in range(H):
            # y2_hat = y_forecast[k]
            y1_t = y1_t + y_forecast[k]
            z_t = z_t + y1_t
            out.append(z_t)
        return np.asarray(out, dtype=float)

    raise NotImplementedError("Integration only implemented for d in {0,1,2}.")


# -----------------------------
#  ARMA(p,q) residuals + fit
# -----------------------------

def _arma_residuals_torch(y, p, q, params):
    """
    Compute conditional residuals for ARMA(p,q) on 1D tensor y.

    y: 1D torch tensor [T]
    params: 1 + p + q tensor [c, phi_1..phi_p, theta_1..theta_q]

    Returns residuals from t=max(p,q)..T-1 as 1D tensor, differentiable in params.
    """
    assert y.ndim == 1
    T = y.shape[0]
    max_lag = max(p, q)

    if T <= max_lag:
        return torch.zeros(0, dtype=y.dtype, device=y.device)

    c = params[0]
    phi = params[1:1 + p]
    theta = params[1 + p:1 + p + q]

    # innovations e_t, we maintain as we go
    e = torch.zeros(T, dtype=y.dtype, device=y.device)
    res_list = []

    for t in range(max_lag, T):
        ar_part = torch.zeros((), dtype=y.dtype, device=y.device)
        if p > 0:
            for i in range(1, p + 1):
                ar_part = ar_part + phi[i - 1] * y[t - i]

        ma_part = torch.zeros((), dtype=y.dtype, device=y.device)
        if q > 0:
            for j in range(1, q + 1):
                ma_part = ma_part + theta[j - 1] * e[t - j]

        y_hat = c + ar_part + ma_part
        e_t = y[t] - y_hat

        # avoid in-place on a tensor used in autograd graph by reassigning
        e = e.clone()
        e[t] = e_t

        res_list.append(e_t)

    if not res_list:
        return torch.zeros(0, dtype=y.dtype, device=y.device)

    return torch.stack(res_list)  # [T - max_lag]

def _fit_arma_css(y_np, p, q,
                  max_iter=60,
                  lr=0.05,
                  min_length=10):
    """
    Fit ARMA(p,q) on 1D numpy array y_np via conditional sum of squares (CSS)
    using PyTorch (Adam).

    Returns (c, phi, theta) as numpy arrays, or None if fail.
    """
    y_np = np.asarray(y_np, dtype=float).reshape(-1)
    T = y_np.shape[0]

    if T < max(min_length, max(p, q) + 2):
        return None

    # Torch tensor
    y = torch.tensor(y_np, dtype=torch.float64)

    # parameter vector: [c, phi_1..phi_p, theta_1..theta_q]
    param_dim = 1 + p + q
    params = torch.zeros(param_dim, dtype=torch.float64, requires_grad=True)

    # init intercept as mean of y
    with torch.no_grad():
        params[0] = y.mean()

    # Everything below must run with grad enabled,
    # even if caller wrapped forward() in torch.no_grad().
    with torch.enable_grad():
        # Sanity check: make sure we actually get some residuals
        test_res = _arma_residuals_torch(y, p, q, params)
        if test_res.numel() == 0:
            # cannot fit this combination of (p,q) on this series
            return None

        opt = torch.optim.Adam([params], lr=lr)

        for _ in range(max_iter):
            opt.zero_grad()
            res = _arma_residuals_torch(y, p, q, params)
            if res.numel() == 0:
                # something went degenerate during optimization – give up
                return None

            loss = (res ** 2).mean()
            loss.backward()
            opt.step()

    # After optimization we don't need grads any more
    with torch.no_grad():
        res = _arma_residuals_torch(y, p, q, params)
        if res.numel() == 0:
            return None

        c = float(params[0].item())
        phi = params[1:1 + p].cpu().numpy().astype(float)
        theta = params[1 + p:1 + p + q].cpu().numpy().astype(float)

    return c, phi, theta



def _arma_forecast_mean(y_np, p, q, c, phi, theta, pred_len):
    """
    ARMA(p,q) mean forecast given fitted params.

    y_np: training series for differenced process (1D)
    c, phi, theta: fitted parameters
    pred_len: forecast horizon

    Uses E[e_future]=0 for future innovations.
    """
    y_np = np.asarray(y_np, dtype=float).reshape(-1)
    T = y_np.shape[0]
    max_lag = max(p, q)

    # We need historical innovations as well; recompute them once
    # so we can propagate MA part correctly up to current time.
    #
    # This duplicates some work but is cleaner than returning e_t from the fit.

    # Rebuild residuals (innovations) for t< T
    e_hist = np.zeros(T, dtype=float)

    for t in range(max_lag, T):
        ar_part = 0.0
        if p > 0:
            for i in range(1, p + 1):
                ar_part += phi[i - 1] * y_np[t - i]
        ma_part = 0.0
        if q > 0:
            for j in range(1, q + 1):
                ma_part += theta[j - 1] * e_hist[t - j]
        y_hat = c + ar_part + ma_part
        e_hist[t] = y_np[t] - y_hat

    # Now simulate forward:
    y_ext = list(y_np)
    e_ext = list(e_hist)

    forecasts = []
    for _ in range(pred_len):
        t = len(y_ext)  # next time index

        ar_part = 0.0
        if p > 0:
            for i in range(1, p + 1):
                ar_part += phi[i - 1] * y_ext[t - i]

        ma_part = 0.0
        if q > 0:
            # future innovations assumed zero mean -> only past e's matter
            for j in range(1, q + 1):
                ma_part += theta[j - 1] * e_ext[t - j]

        y_hat = c + ar_part + ma_part

        # For mean forecast we set future e_t = 0
        y_ext.append(float(y_hat))
        e_ext.append(0.0)

        forecasts.append(float(y_hat))

    return np.asarray(forecasts, dtype=float)


# -----------------------------
#  Full ARIMA(p,d,q) module
# -----------------------------

class FullARIMA(nn.Module):
    """
    Full ARIMA(p,d,q) baseline with fixed orders (p,d,q), fit per series via CSS.

    - Input:  x [B, L, D] (torch.Tensor or np.ndarray, float)
    - Output: [B, pred_len, D] (np.ndarray, float32)

    configs must provide:
        arima_p, arima_d, arima_q
    optional:
        arima_max_iter   (default 60)
        arima_lr         (default 0.05)
        arima_min_len    (default 10)
    """

    def __init__(self, configs):
        super().__init__()
        self.pred_len = configs.pred_len
        self.p = getattr(configs, "arima_p", 1)
        self.d = getattr(configs, "arima_d", 0)
        self.q = getattr(configs, "arima_q", 1)

        self.max_iter = getattr(configs, "arima_max_iter", 60)
        self.lr = getattr(configs, "arima_lr", 0.05)
        self.min_len = getattr(configs, "arima_min_len", 10)

    def _fit_and_forecast_one(self, z):
        """
        Fit ARIMA(p,d,q) on a single 1D numpy series z, return forecast [pred_len].
        """
        z = np.asarray(z, dtype=float).reshape(-1)

        # Short fallback: repeat last value
        if z.shape[0] < self.min_len:
            return np.full(self.pred_len, float(z[-1]), dtype=float)

        # 1) Difference
        y, aux = _difference_series(z, self.d)

        # In practice, if differencing kills length, bail out
        if y.shape[0] < self.min_len:
            return np.full(self.pred_len, float(z[-1]), dtype=float)

        # 2) Fit ARMA(p,q) on y
        fit = _fit_arma_css(
            y,
            self.p,
            self.q,
            max_iter=self.max_iter,
            lr=self.lr,
            min_length=self.min_len,
        )

        if fit is None:
            # fallback
            return np.full(self.pred_len, float(z[-1]), dtype=float)

        c, phi, theta = fit

        # 3) Forecast differenced process y
        y_forecast = _arma_forecast_mean(
            y, self.p, self.q, c, phi, theta, self.pred_len
        )

        # 4) Integrate back to original scale
        z_forecast = _integrate_forecast(y_forecast, aux)
        return z_forecast.astype(float)

    def forward(self, x):
        """
        x: [B, L, D] torch.Tensor or np.ndarray
        returns: [B, pred_len, D] np.ndarray (float32)
        """
        if isinstance(x, torch.Tensor):
            x_np = x.detach().cpu().numpy()
        else:
            x_np = np.asarray(x, dtype=float)

        B, L, D = x_np.shape
        out = np.zeros((B, self.pred_len, D), dtype=np.float32)

        for b in range(B):
            for i in range(D):
                series = x_np[b, :, i]
                forecast = self._fit_and_forecast_one(series)
                out[b, :, i] = forecast.astype(np.float32)

        return out  # [B, pred_len, D]




import numpy as np
import torch
import torch.nn as nn


def _estimate_dominant_omega_torch(series_t: torch.Tensor) -> torch.Tensor:
    """
    Estimate dominant angular frequency omega from a 1D torch tensor using rFFT.
    Assumes dt = 1.0 (discrete steps).
    series_t: 1D tensor [T]
    Returns: scalar tensor omega (radians per step)
    """
    # remove mean
    y = series_t - series_t.mean()
    T = y.shape[0]

    if T < 4:
        return torch.tensor(0.0, dtype=y.dtype, device=y.device)

    # FFT
    yf = torch.fft.rfft(y)
    freqs = torch.fft.rfftfreq(T, d=1.0).to(y.device)  # cycles per step

    if freqs.numel() <= 1:
        return torch.tensor(0.0, dtype=y.dtype, device=y.device)

    mag = torch.abs(yf)

    # ignore DC component at index 0
    mag_no_dc = mag[1:]
    if mag_no_dc.numel() == 0:
        return torch.tensor(0.0, dtype=y.dtype, device=y.device)

    idx_rel = torch.argmax(mag_no_dc)
    idx = idx_rel + 1

    f_dom = freqs[idx]                  # cycles/step
    omega = 2.0 * torch.pi * f_dom      # radians/step
    return omega


def _kalman_harmonic_forecast_torch(
    series_np,
    pred_len: int,
    q_scale: float = 0.01,
    r_scale: float = 0.1,
    min_length: int = 5,
    device: str = "cpu",
    dtype: torch.dtype = torch.float32,
):
    """
    One-step-ahead harmonic Kalman filter for a single 1D series, then roll out pred_len steps.

    Model:
        x_{t+1} = F x_t + w_t
        y_t     = H x_t + v_t
    with F a rotation matrix at frequency omega, H = [1, 0].

    series_np : 1D np.ndarray or list
    returns: forecast (np.ndarray of shape [pred_len], dtype float32)
    """
    with torch.no_grad():
        y = torch.as_tensor(series_np, dtype=dtype, device=device).reshape(-1)
        T = y.shape[0]

        # Fallback: too short or almost constant -> repeat last value
        if T < min_length or torch.var(y) < 1e-10:
            return np.full(pred_len, float(y[-1].item()), dtype=np.float32)

        # 1) Estimate dominant frequency
        omega = _estimate_dominant_omega_torch(y)
        if not torch.isfinite(omega) or torch.abs(omega) < 1e-8:
            # cannot estimate meaningful harmonic, fallback
            return np.full(pred_len, float(y[-1].item()), dtype=np.float32)

        cosw = torch.cos(omega)
        sinw = torch.sin(omega)

        # State transition matrix F (2x2), observation H (1x2)
        F = torch.stack([
            torch.stack([cosw, -sinw]),
            torch.stack([sinw,  cosw]),
        ], dim=0)  # [2,2]
        H = torch.tensor([[1.0, 0.0]], dtype=dtype, device=device)  # [1,2]
        HT = H.t()  # [2,1]

        # Noise covariances
        var_y = torch.var(y)
        if not torch.isfinite(var_y) or var_y <= 0:
            var_y = torch.tensor(1.0, dtype=dtype, device=device)

        Q = q_scale * var_y * torch.eye(2, dtype=dtype, device=device)   # process noise
        R = r_scale * var_y                                              # scalar obs noise

        # Initial state and covariance
        x = torch.tensor([y[0].item(), 0.0], dtype=dtype, device=device)  # [2]
        P = var_y * torch.eye(2, dtype=dtype, device=device)              # [2,2]
        I2 = torch.eye(2, dtype=dtype, device=device)

        # 2) Kalman filter through history
        for t in range(T):
            # Predict
            x = F @ x                # [2]
            P = F @ P @ F.t() + Q    # [2,2]

            yt = y[t]
            y_pred = (H @ x).squeeze()       # scalar
            S = (H @ P @ HT).squeeze() + R   # scalar

            if not torch.isfinite(S) or S <= 0:
                continue

            K = (P @ HT) / S  # [2,1]
            innovation = yt - y_pred
            x = x + (K[:, 0] * innovation)
            P = (I2 - K @ H) @ P

        # 3) Roll forward without further updates
        forecasts = []
        for _ in range(pred_len):
            x = F @ x
            P = F @ P @ F.t() + Q
            y_hat = (H @ x).squeeze()
            forecasts.append(float(y_hat.item()))

        forecast = np.asarray(forecasts, dtype=np.float32)

        # ---- ENFORCE CONTINUITY: match first forecast to last observed ----
        last_obs = float(series_np[-1])
        delta = last_obs - forecast[0]
        forecast = forecast + delta

        return forecast
    



class KalmanHarmonic(nn.Module):
    """
    Kalman harmonic forecaster implemented fully in PyTorch.

    - Input:  x [B, L, D] (torch.Tensor or np.ndarray, float)
    - Output: [B, pred_len, D] (np.ndarray, float32)

    For each univariate series (b, d):
        1) Estimate dominant frequency via torch FFT.
        2) Build a 2D harmonic state model with rotation F(omega).
        3) Run Kalman filter over the history.
        4) Roll forward pred_len steps and output y-hat.

    This is a classical baseline: no parameters, no backprop through it.
    """

    def __init__(self, configs):
        super().__init__()
        self.pred_len = configs.pred_len

        # Hyperparameters you can control via argparse
        self.q_scale = getattr(configs, "kalman_q_scale", 0.03)
        self.r_scale = getattr(configs, "kalman_r_scale", 2)
        self.min_length = getattr(configs, "kalman_min_len", 50)

    def forward(self, x):
        """
        x: [B, L, D] torch.Tensor or np.ndarray
        returns: [B, pred_len, D] np.ndarray (float32)
        """
        # Accept both torch and numpy input
        if isinstance(x, torch.Tensor):
            device = x.device
            x_np = x.detach().cpu().numpy()
        else:
            device = "cpu"
            x_np = np.asarray(x, dtype=float)

        B, L, D = x_np.shape
        out = np.zeros((B, self.pred_len, D), dtype=np.float32)

        for b in range(B):
            for d in range(D):
                series = x_np[b, :, d]
                forecast = _kalman_harmonic_forecast_torch(
                    series_np=series,
                    pred_len=self.pred_len,
                    q_scale=self.q_scale,
                    r_scale=self.r_scale,
                    min_length=self.min_length,
                    device=device,
                    dtype=torch.float32,
                )
                out[b, :, d] = forecast

        return out  # [B, pred_len, D]



import numpy as np
import torch
import torch.nn as nn


def _estimate_dominant_omega_torch(series_t: torch.Tensor) -> torch.Tensor:
    """
    Estimate dominant angular frequency omega from a 1D torch tensor using rFFT.
    Assumes dt = 1.0 (discrete steps).
    series_t: 1D tensor [T]
    Returns: scalar tensor omega (radians per step)
    """
    y = series_t - series_t.mean()
    T = y.shape[0]

    if T < 4:
        return torch.tensor(0.0, dtype=y.dtype, device=y.device)

    yf = torch.fft.rfft(y)
    freqs = torch.fft.rfftfreq(T, d=1.0).to(y.device)  # cycles per step

    if freqs.numel() <= 1:
        return torch.tensor(0.0, dtype=y.dtype, device=y.device)

    mag = torch.abs(yf)

    # ignore DC component at index 0
    mag_no_dc = mag[1:]
    if mag_no_dc.numel() == 0:
        return torch.tensor(0.0, dtype=y.dtype, device=y.device)

    idx_rel = torch.argmax(mag_no_dc)
    idx = idx_rel + 1

    f_dom = freqs[idx]                  # cycles/step
    omega = 2.0 * torch.pi * f_dom      # radians/step
    return omega


def _kalman_3state_drift_forecast_torch(
    series_np,
    pred_len: int,
    q_osc_scale: float = 1e-3,
    q_base_scale: float = 1e-3,
    r_scale: float = 1e-4,
    min_length: int = 50,
    device: str = "cpu",
    dtype: torch.dtype = torch.float32,
):
    """
    3-state Kalman filter forecaster for a single 1D series:

        x_t = [c_t, s_t, b_t]^T
        F  = [[cosw, -sinw, 0],
              [sinw,  cosw, 0],
              [  0 ,    0 , 1]]

        y_t = [1, 0, 1] x_t + v_t

    series_np : 1D np.ndarray or list
    returns: forecast (np.ndarray of shape [pred_len], dtype float32)

    This follows standard KF (no post-hoc shifts or clipping).
    """
    with torch.no_grad():
        y = torch.as_tensor(series_np, dtype=dtype, device=device).reshape(-1)
        T = y.shape[0]

        # Fallback: not enough data or almost constant -> repeat last value
        if T < min_length or torch.var(y) < 1e-10:
            return np.full(pred_len, float(y[-1].item()), dtype=np.float32)

        # 1) Estimate dominant frequency
        omega = _estimate_dominant_omega_torch(y)
        if not torch.isfinite(omega) or torch.abs(omega) < 1e-8:
            return np.full(pred_len, float(y[-1].item()), dtype=np.float32)

        cosw = torch.cos(omega)
        sinw = torch.sin(omega)

        # 2) State transition F (3x3) and observation H (1x3)
        F = torch.stack([
            torch.stack([cosw, -sinw, torch.tensor(0.0, dtype=dtype, device=device)]),
            torch.stack([sinw,  cosw, torch.tensor(0.0, dtype=dtype, device=device)]),
            torch.stack([torch.tensor(0.0, dtype=dtype, device=device),
                         torch.tensor(0.0, dtype=dtype, device=device),
                         torch.tensor(1.0, dtype=dtype, device=device)]),
        ], dim=0)  # [3,3]

        H = torch.tensor([[1.0, 0.0, 1.0]], dtype=dtype, device=device)  # [1,3]
        HT = H.t()  # [3,1]

        # 3) Noise covariances
        var_y = torch.var(y)
        if not torch.isfinite(var_y) or var_y <= 0:
            var_y = torch.tensor(1.0, dtype=dtype, device=device)

        Q = var_y * torch.diag(torch.tensor(
            [q_osc_scale, q_osc_scale, q_base_scale],
            dtype=dtype,
            device=device,
        ))  # [3,3]

        R = r_scale * var_y  # scalar

        # 4) Initial state and covariance
        # crude init: c_0 = y0, s_0 = 0, b_0 = 0
        x = torch.tensor(
            [y[0].item(), 0.0, 0.0],
            dtype=dtype,
            device=device,
        )  # [3]
        P = var_y * torch.eye(3, dtype=dtype, device=device)  # [3,3]
        I3 = torch.eye(3, dtype=dtype, device=device)

        # 5) Kalman filter over history
        for t in range(T):
            # Predict
            x = F @ x
            P = F @ P @ F.t() + Q

            yt = y[t]
            y_pred = (H @ x).squeeze()        # scalar
            S = (H @ P @ HT).squeeze() + R    # scalar

            if not torch.isfinite(S) or S <= 0:
                continue

            K = (P @ HT) / S  # [3,1]
            innovation = yt - y_pred
            x = x + (K[:, 0] * innovation)
            P = (I3 - K @ H) @ P

        # 6) Roll forward predictions (no more updates)
        forecasts = []
        for _ in range(pred_len):
            x = F @ x
            P = F @ P @ F.t() + Q
            y_hat = (H @ x).squeeze()
            forecasts.append(float(y_hat.item()))

        forecast = np.asarray(forecasts, dtype=np.float32)
        return forecast
class Kalman3StateDrift(nn.Module):
    """
    3-state Kalman drift-harmonic forecaster (pure KF, no post-shift).

    State:
        x_t = [c_t, s_t, b_t]^T

    - Input:  x [B, L, D] (torch.Tensor or np.ndarray, float)
    - Output: [B, pred_len, D] (np.ndarray, float32)
    """

    def __init__(self, configs):
        super().__init__()
        self.pred_len = configs.pred_len

        # Hyperparameters (you can expose via argparse)
        self.q_osc_scale = getattr(configs, "kalman_q_osc_scale", 1e-3)
        self.q_base_scale = getattr(configs, "kalman_q_base_scale", 1e-3)
        self.r_scale = getattr(configs, "kalman_r_scale", 1e-4)
        self.min_length = getattr(configs, "kalman_min_len", 50)

    def forward(self, x):
        # Accept both torch and numpy input
        if isinstance(x, torch.Tensor):
            device = x.device
            x_np = x.detach().cpu().numpy()
        else:
            device = "cpu"
            x_np = np.asarray(x, dtype=float)

        B, L, D = x_np.shape
        out = np.zeros((B, self.pred_len, D), dtype=np.float32)

        for b in range(B):
            for d in range(D):
                series = x_np[b, :, d]
                forecast = _kalman_3state_drift_forecast_torch(
                    series_np=series,
                    pred_len=self.pred_len,
                    q_osc_scale=self.q_osc_scale,
                    q_base_scale=self.q_base_scale,
                    r_scale=self.r_scale,
                    min_length=self.min_length,
                    device=device,
                    dtype=torch.float32,
                )
                out[b, :, d] = forecast

        return out  # [B, pred_len, D]
