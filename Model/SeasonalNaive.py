"""
Seasonal-naive floor (REVISION_PLAN.md P2.4).

No learning. For each window the dominant period ``P`` of the history is
estimated from the rFFT peak (parabolic refinement, same estimator as
``utils.fidelity.peak_freq_batch``), and the forecast repeats the last ``P``
samples of the history periodically over the horizon. If the spectrum is flat
or the period is longer than the history, the forecast falls back to the last
value (plain naive). A fractional period is honored by linear interpolation of
the last cycle, which keeps the phase continuous at the forecast boundary.

Registered as a regular ``Model`` so the runner can train and test it like any
other model; training is a no-op because the module has no parameters
(``main.py`` skips the optimizer loop when ``--train_epochs 0`` is used, see
configs/models/SeasonalNaive.yaml).
"""
import torch
import torch.nn as nn


class Model(nn.Module):
    def __init__(self, configs):
        super().__init__()
        self.seq_len = configs.seq_len
        self.pred_len = configs.pred_len
        self.peak_frac_thresh = getattr(configs, "naive_peak_frac", 0.1)
        # a dummy parameter so optimizers and state_dict saving do not choke
        self.register_buffer("_dummy", torch.zeros(1))

    @torch.no_grad()
    def _period(self, x):
        # x: [B, L] -> period in samples [B] (float), reliable mask [B]
        B, L = x.shape
        xc = x - x.mean(dim=1, keepdim=True)
        P = torch.fft.rfft(xc, dim=1).abs() ** 2
        P[:, 0] = 0.0
        total = P.sum(dim=1)
        k = torch.argmax(P, dim=1)
        rows = torch.arange(B, device=x.device)
        kc = k.clamp(1, P.shape[1] - 2)
        denom = P[rows, kc - 1] - 2 * P[rows, kc] + P[rows, kc + 1]
        num = 0.5 * (P[rows, kc - 1] - P[rows, kc + 1])
        delta = torch.where(denom.abs() < 1e-12, torch.zeros_like(num), num / denom)
        interior = (k >= 1) & (k <= P.shape[1] - 2)
        kf = torch.where(interior, k.float() + delta, k.float())
        frac = torch.where(total > 0, P[rows, k] / total.clamp_min(1e-12), torch.zeros_like(total))
        reliable = (total > 1e-8) & (frac >= self.peak_frac_thresh) & (kf > 0)
        period = torch.where(reliable, L / kf.clamp_min(1e-6), torch.full_like(kf, float("inf")))
        return period, reliable

    @torch.no_grad()
    def _refine_period(self, x, period, usable, rel_span=0.15, n_grid=121):
        """
        Refine the FFT period by minimizing the mean squared self-difference
        x[t] - x[t - P] over the history for P on a fine grid around the FFT
        estimate (fractional lags via linear interpolation). Returns [B].
        """
        B, L = x.shape
        P0 = torch.where(usable, period, torch.ones_like(period))
        grid = torch.linspace(1 - rel_span, 1 + rel_span, n_grid, device=x.device, dtype=x.dtype)
        cand = P0[:, None] * grid[None, :]                                  # [B, G]
        cand = cand.clamp(min=2.0, max=float(L - 1))
        t = torch.arange(L, device=x.device, dtype=x.dtype)                 # [L]
        src = t[None, None, :] - cand[:, :, None]                           # [B, G, L]
        valid = src >= 0
        srcc = src.clamp(0, L - 1)
        i0 = srcc.floor()
        i1 = (i0 + 1).clamp(max=L - 1)
        w = srcc - i0
        xe = x[:, None, :].expand(-1, cand.shape[1], -1)
        g0 = torch.gather(xe, 2, i0.long())
        g1 = torch.gather(xe, 2, i1.long())
        xs = (1 - w) * g0 + w * g1
        err = (((xe - xs) ** 2) * valid).sum(dim=2) / valid.sum(dim=2).clamp_min(1)
        best = cand[torch.arange(B, device=x.device), torch.argmin(err, dim=1)]
        return torch.where(usable, best, period)

    @torch.no_grad()
    def forward(self, x):
        # x: [B, L, C] -> [B, H, C]
        B, L, C = x.shape
        out = torch.empty(B, self.pred_len, C, dtype=x.dtype, device=x.device)
        t_future = torch.arange(1, self.pred_len + 1, device=x.device, dtype=x.dtype)
        for c in range(C):
            xc = x[:, :, c]
            period, reliable = self._period(xc)
            usable = reliable & (period <= L) & torch.isfinite(period)
            period = self._refine_period(xc, period, usable)
            # continuation: y[t] = x[L - P + ((t - 1) mod P)] with fractional P via linear interpolation
            P_ = torch.where(usable, period, torch.full_like(period, float(L)))
            phase = torch.remainder(t_future[None, :] - 1.0, P_[:, None])          # [B, H] in [0, P)
            pos = (L - P_[:, None]) + phase                                       # [B, H] float index
            i0 = pos.floor().clamp(0, L - 1)
            i1 = (i0 + 1).clamp(0, L - 1)
            w = (pos - i0).clamp(0, 1)
            g0 = torch.gather(xc, 1, i0.long())
            g1 = torch.gather(xc, 1, i1.long())
            rep = (1 - w) * g0 + w * g1
            last = xc[:, -1:].expand(-1, self.pred_len)
            out[:, :, c] = torch.where(usable[:, None], rep, last)
        return out
