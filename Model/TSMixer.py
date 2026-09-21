"""
TSMixer: An All-MLP Architecture for Time Series Forecasting.
Chen, Li, Arik, Yoder, Pfister. TMLR 2023. https://arxiv.org/abs/2303.06053

Implementation of the univariate/multivariate "TSMixer" block stack (Fig. 1 of
the paper): each mixer layer applies a time-mixing MLP (shared across
channels, acting along the sequence axis) and a feature-mixing MLP (shared
across time steps, acting along the channel axis), each with pre-normalization,
dropout and a residual connection. A temporal linear projection maps the mixed
sequence from ``seq_len`` to ``pred_len``. Reversible instance normalization
(RevIN) is applied when ``configs.revin`` is set, as in the paper's
long-horizon experiments.

With univariate input (``enc_in = 1``) the feature-mixing MLP acts on a single
channel and is therefore a per-timestep scalar MLP; it is kept so that the
architecture matches the published one (noted in the Supplement).

Hyperparameters read from ``configs``:
    seq_len, pred_len, enc_in
    e_layers      number of mixer blocks       (paper: 2 to 8)
    d_ff          hidden size of the feature-mixing MLP (paper: 32 to 512)
    dropout       dropout rate                 (paper: 0.1 to 0.9)
    revin, affine, subtract_last  RevIN switches (as for PatchTST in this repo)
"""
import torch
import torch.nn as nn

from Layers.RevIN import RevIN


class _TimeMix(nn.Module):
    """MLP along the time axis, shared across channels. x: [B, L, C]"""

    def __init__(self, seq_len: int, dropout: float, channels: int):
        super().__init__()
        self.norm = nn.BatchNorm1d(channels) if channels > 1 else nn.BatchNorm1d(seq_len)
        self.channels = channels
        self.fc = nn.Linear(seq_len, seq_len)
        self.act = nn.ReLU()
        self.drop = nn.Dropout(dropout)

    def _bn(self, x):
        # 2D batch norm over the flattened [L, C] as in the reference implementation
        B, L, C = x.shape
        if self.channels > 1:
            return self.norm(x.transpose(1, 2)).transpose(1, 2)
        return self.norm(x[:, :, 0]).unsqueeze(-1)

    def forward(self, x):
        res = x
        x = self._bn(x)
        x = x.transpose(1, 2)            # [B, C, L]
        x = self.drop(self.act(self.fc(x)))
        x = x.transpose(1, 2)            # [B, L, C]
        return res + x


class _FeatureMix(nn.Module):
    """MLP along the channel axis, shared across time steps. x: [B, L, C]"""

    def __init__(self, seq_len: int, channels: int, d_ff: int, dropout: float):
        super().__init__()
        self.norm = nn.BatchNorm1d(channels) if channels > 1 else nn.BatchNorm1d(seq_len)
        self.channels = channels
        self.fc1 = nn.Linear(channels, d_ff)
        self.fc2 = nn.Linear(d_ff, channels)
        self.act = nn.ReLU()
        self.drop1 = nn.Dropout(dropout)
        self.drop2 = nn.Dropout(dropout)

    def _bn(self, x):
        if self.channels > 1:
            return self.norm(x.transpose(1, 2)).transpose(1, 2)
        return self.norm(x[:, :, 0]).unsqueeze(-1)

    def forward(self, x):
        res = x
        x = self._bn(x)
        x = self.drop1(self.act(self.fc1(x)))
        x = self.drop2(self.fc2(x))
        return res + x


class MixerBlock(nn.Module):
    def __init__(self, seq_len, channels, d_ff, dropout):
        super().__init__()
        self.time_mix = _TimeMix(seq_len, dropout, channels)
        self.feat_mix = _FeatureMix(seq_len, channels, d_ff, dropout)

    def forward(self, x):
        return self.feat_mix(self.time_mix(x))


class Model(nn.Module):
    def __init__(self, configs):
        super().__init__()
        self.seq_len = configs.seq_len
        self.pred_len = configs.pred_len
        self.channels = configs.enc_in
        n_blocks = getattr(configs, "e_layers", 2)
        d_ff = getattr(configs, "d_ff", 64)
        dropout = getattr(configs, "dropout", 0.1)

        self.revin = bool(getattr(configs, "revin", 1))
        if self.revin:
            self.revin_layer = RevIN(self.channels, affine=bool(getattr(configs, "affine", 0)),
                                     subtract_last=bool(getattr(configs, "subtract_last", 0)))
        self.blocks = nn.ModuleList(
            [MixerBlock(self.seq_len, self.channels, d_ff, dropout) for _ in range(n_blocks)])
        self.temporal_proj = nn.Linear(self.seq_len, self.pred_len)

    def forward(self, x):
        # x: [B, L, C] -> [B, H, C]
        if self.revin:
            x = self.revin_layer(x, "norm")
        for blk in self.blocks:
            x = blk(x)
        x = self.temporal_proj(x.transpose(1, 2)).transpose(1, 2)
        if self.revin:
            x = self.revin_layer(x, "denorm")
        return x
