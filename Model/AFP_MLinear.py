import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


class MLPHead(nn.Module):
    """
    A simple 2-layer MLP with non-linear activation.
    """
    def __init__(self, input_dim, output_dim, hidden_dim=128):
        super(MLPHead, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, x):
        return self.net(x)


class Model(nn.Module):
    """
    Non-linear model that predicts amplitude, frequency, phase offset,
    trend, and residual noise to reconstruct:
    x(t) = T(t) + A(t) * sin(2π ∫f(t) + φ₀) + ε(t)
    """
    def __init__(self, configs):
        super(Model, self).__init__()
        self.seq_len = configs.seq_len
        self.pred_len = configs.pred_len
        hidden_dim = 128  # you can change this based on complexity

        # Non-linear MLP heads
        self.amp_head = MLPHead(self.seq_len, self.pred_len, hidden_dim)
        self.freq_head = MLPHead(self.seq_len, self.pred_len, hidden_dim)
        self.offset_head = MLPHead(self.seq_len, 1, hidden_dim)
        self.trend_head = MLPHead(self.seq_len, self.pred_len, hidden_dim)
        self.noise_head = MLPHead(self.seq_len, self.pred_len, hidden_dim)

    def forward(self, x):
        x = x.squeeze(-1)  # [B, L]

        amp_out = self.amp_head(x)        # [B, H]
        freq_out = self.freq_head(x)      # [B, H]
        offset_out = self.offset_head(x)  # [B, 1]
        trend_out = self.trend_head(x)    # [B, H]
        noise_out = self.noise_head(x)    # [B, H]

        phi = 2 * np.pi * torch.cumsum(freq_out, dim=1) + offset_out  # [B, H]
        waveform = amp_out * torch.sin(phi)  # [B, H]

        signal = trend_out + waveform + noise_out  # [B, H]
        return signal.unsqueeze(-1)  # [B, H, 1]
