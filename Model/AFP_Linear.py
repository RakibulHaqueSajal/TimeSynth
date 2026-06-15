import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


class Model(nn.Module):
    """
    Linear model that predicts amplitude, frequency, phase offset,
    trend, and residual noise to reconstruct:
    x(t) = T(t) + A(t) * sin(2π ∫f(t) + φ₀) + ε(t)
    """
    def __init__(self, configs):
        super(Model, self).__init__()
        self.seq_len = configs.seq_len
        self.pred_len = configs.pred_len

        # Heads for signal components
        self.amp_head = nn.Linear(self.seq_len, self.pred_len)
        self.freq_head = nn.Linear(self.seq_len, self.pred_len)
        self.offset_head = nn.Linear(self.seq_len, 1)
        self.trend_head = nn.Linear(self.seq_len, self.pred_len)
        self.noise_head = nn.Linear(self.seq_len, self.pred_len)

    def forward(self, x):
        # x: [B, L, 1]
        x = x.squeeze(-1)  # [B, L]

        amp_out = self.amp_head(x)      # [B, H]
        freq_out = self.freq_head(x)    # [B, H]
        offset_out = self.offset_head(x)  # [B, 1]
        trend_out = self.trend_head(x)  # [B, H]
        noise_out = self.noise_head(x)  # [B, H]

        phi = 2 * np.pi * torch.cumsum(freq_out, dim=1) + offset_out  # [B, H]
        waveform = amp_out * torch.sin(phi)  # [B, H]

        signal = trend_out + waveform + noise_out  # [B, H]
        return signal.unsqueeze(-1)  # [B, H, 1]
