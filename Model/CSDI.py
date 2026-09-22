"""
CSDI: Conditional Score-based Diffusion Models for Probabilistic Time Series
Imputation. Tashiro, Song, Song, Ermon. NeurIPS 2021. https://arxiv.org/abs/2107.03502

Re-implementation (MIT-licensed reference: https://github.com/ermongroup/CSDI) of the
CSDI denoiser for the forecasting setting used in this benchmark: the history is
the conditional (observed) part, the horizon is the imputation target. Kept as
close to the reference as the univariate setting allows:

* diffusion: T = 50 steps, quadratic beta schedule from 1e-4 to 0.5 (reference default)
* denoiser: ``layers`` residual blocks, each with a temporal Transformer layer and a
  feature Transformer layer (trivial for one channel but kept), gated residual and
  skip connections, dilation-free 1x1 convolutions, ``channels`` = 64
* side information: 128-dim sinusoidal time embedding + 16-dim learned feature
  embedding + the conditional mask; diffusion-step embedding of 128 dims
* training loss: MSE between the injected noise and the predicted noise on target
  positions only; sampling: ancestral reverse diffusion, ``n_samples`` draws

Interface used by the runner (Experiment/exp_forecast.py):
    model.training_loss(batch_x, batch_y) -> scalar
    model.sample(batch_x, n_samples)      -> [S, B, H, C]
    model(batch_x)                        -> median forecast [B, H, C]
"""
import math

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


def _conv1d(cin, cout, k=1):
    layer = nn.Conv1d(cin, cout, k)
    nn.init.kaiming_normal_(layer.weight)
    return layer


class DiffusionEmbedding(nn.Module):
    def __init__(self, num_steps, dim=128, proj_dim=None):
        super().__init__()
        proj_dim = proj_dim or dim
        self.register_buffer("embedding", self._build(num_steps, dim // 2), persistent=False)
        self.p1 = nn.Linear(dim, proj_dim)
        self.p2 = nn.Linear(proj_dim, proj_dim)

    @staticmethod
    def _build(num_steps, half):
        steps = torch.arange(num_steps).unsqueeze(1)
        freqs = 10.0 ** (torch.arange(half) / (half - 1) * 4.0).unsqueeze(0)
        table = steps * freqs
        return torch.cat([torch.sin(table), torch.cos(table)], dim=1)

    def forward(self, t):
        x = self.embedding[t]
        x = F.silu(self.p1(x))
        return F.silu(self.p2(x))


def _transformer_layer(channels, heads=8):
    return nn.TransformerEncoderLayer(d_model=channels, nhead=heads, dim_feedforward=64,
                                      activation="gelu", batch_first=False)


class ResidualBlock(nn.Module):
    def __init__(self, side_dim, channels, diff_dim, heads=8):
        super().__init__()
        self.diff_proj = nn.Linear(diff_dim, channels)
        self.cond_proj = _conv1d(side_dim, 2 * channels)
        self.mid_proj = _conv1d(channels, 2 * channels)
        self.out_proj = _conv1d(channels, 2 * channels)
        self.time_layer = _transformer_layer(channels, heads)
        self.feat_layer = _transformer_layer(channels, heads)

    @staticmethod
    def _run_axis(layer, y, B, C, K, L, axis):
        # y: [B, C, K*L]; run the transformer along time (axis 'L') or features ('K')
        if axis == "L":
            y = y.reshape(B, C, K, L).permute(0, 2, 1, 3).reshape(B * K, C, L)
            y = layer(y.permute(2, 0, 1)).permute(1, 2, 0)          # [B*K, C, L]
            return y.reshape(B, K, C, L).permute(0, 2, 1, 3).reshape(B, C, K * L)
        if K == 1:
            return y
        y = y.reshape(B, C, K, L).permute(0, 3, 1, 2).reshape(B * L, C, K)
        y = layer(y.permute(2, 0, 1)).permute(1, 2, 0)
        return y.reshape(B, L, C, K).permute(0, 2, 3, 1).reshape(B, C, K * L)

    def forward(self, x, side, diff_emb):
        B, C, K, L = x.shape
        y = x.reshape(B, C, K * L) + self.diff_proj(diff_emb).unsqueeze(-1)
        y = self._run_axis(self.time_layer, y, B, C, K, L, "L")
        y = self._run_axis(self.feat_layer, y, B, C, K, L, "K")
        y = self.mid_proj(y)
        y = y + self.cond_proj(side.reshape(B, -1, K * L))
        gate, filt = torch.chunk(y, 2, dim=1)
        y = torch.sigmoid(gate) * torch.tanh(filt)
        y = self.out_proj(y)
        res, skip = torch.chunk(y, 2, dim=1)
        x = x.reshape(B, C, K * L)
        return ((x + res) / math.sqrt(2.0)).reshape(B, C, K, L), skip.reshape(B, C, K, L)


class Denoiser(nn.Module):
    def __init__(self, side_dim, channels, layers, num_steps, diff_dim=128, heads=8):
        super().__init__()
        self.channels = channels
        self.diff_emb = DiffusionEmbedding(num_steps, diff_dim)
        self.in_proj = _conv1d(2, channels)             # noisy target + conditional observation
        self.out1 = _conv1d(channels, channels)
        self.out2 = _conv1d(channels, 1)
        nn.init.zeros_(self.out2.weight)
        self.blocks = nn.ModuleList([ResidualBlock(side_dim, channels, diff_dim, heads) for _ in range(layers)])

    def forward(self, x, side, t):
        # x: [B, 2, K, L], side: [B, side_dim, K, L]
        B, _, K, L = x.shape
        y = F.relu(self.in_proj(x.reshape(B, 2, K * L))).reshape(B, self.channels, K, L)
        emb = self.diff_emb(t)
        skips = 0
        for blk in self.blocks:
            y, skip = blk(y, side, emb)
            skips = skips + skip
        y = skips / math.sqrt(len(self.blocks))
        y = F.relu(self.out1(y.reshape(B, self.channels, K * L)))
        return self.out2(y).reshape(B, K, L)


class Model(nn.Module):
    def __init__(self, configs):
        super().__init__()
        self.seq_len = configs.seq_len
        self.pred_len = configs.pred_len
        self.K = configs.enc_in
        self.num_steps = getattr(configs, "diff_steps", 50)
        self.n_samples = getattr(configs, "n_samples", 50)
        channels = getattr(configs, "d_model", 64)
        layers = getattr(configs, "e_layers", 4)
        heads = getattr(configs, "n_heads", 8)
        self.time_dim, self.feat_dim = 128, 16
        self.feat_emb = nn.Embedding(self.K, self.feat_dim)
        side_dim = self.time_dim + self.feat_dim + 1
        self.net = Denoiser(side_dim, channels, layers, self.num_steps, heads=heads)

        beta = np.linspace(getattr(configs, "beta_start", 1e-4) ** 0.5,
                           getattr(configs, "beta_end", 0.5) ** 0.5, self.num_steps) ** 2
        alpha = np.cumprod(1.0 - beta)
        self.register_buffer("beta", torch.tensor(beta, dtype=torch.float32), persistent=False)
        self.register_buffer("alpha", torch.tensor(alpha, dtype=torch.float32), persistent=False)

    # ---------------------------------------------------------------- helpers
    def _time_embedding(self, B, L, device):
        pos = torch.arange(L, device=device).float().unsqueeze(0).expand(B, L)
        d = self.time_dim
        div = 1.0 / torch.pow(10000.0, torch.arange(0, d, 2, device=device).float() / d)
        pe = torch.zeros(B, L, d, device=device)
        pe[:, :, 0::2] = torch.sin(pos.unsqueeze(-1) * div)
        pe[:, :, 1::2] = torch.cos(pos.unsqueeze(-1) * div)
        return pe

    def _side_info(self, cond_mask):
        # cond_mask: [B, K, L] -> side [B, side_dim, K, L]
        B, K, L = cond_mask.shape
        te = self._time_embedding(B, L, cond_mask.device).unsqueeze(2).expand(-1, -1, K, -1)   # [B, L, K, D]
        fe = self.feat_emb(torch.arange(K, device=cond_mask.device)).unsqueeze(0).unsqueeze(0).expand(B, L, -1, -1)
        side = torch.cat([te, fe], dim=-1).permute(0, 3, 2, 1)                                # [B, D+F, K, L]
        return torch.cat([side, cond_mask.unsqueeze(1)], dim=1)

    def _assemble(self, batch_x, batch_y=None):
        # -> data [B, K, L+H], cond_mask [B, K, L+H]
        B = batch_x.shape[0]
        hist = batch_x.permute(0, 2, 1)
        fut = batch_y.permute(0, 2, 1) if batch_y is not None else torch.zeros(B, self.K, self.pred_len, device=batch_x.device)
        data = torch.cat([hist, fut], dim=-1)
        mask = torch.zeros_like(data)
        mask[:, :, :self.seq_len] = 1.0
        return data, mask

    # ---------------------------------------------------------------- training
    def training_loss(self, batch_x, batch_y):
        data, cond_mask = self._assemble(batch_x, batch_y[:, -self.pred_len:, :])
        B = data.shape[0]
        t = torch.randint(0, self.num_steps, (B,), device=data.device)
        a = self.alpha[t].view(B, 1, 1)
        noise = torch.randn_like(data)
        noisy = (a ** 0.5) * data + ((1 - a) ** 0.5) * noise
        target_mask = 1.0 - cond_mask
        inp = torch.stack([cond_mask * data, target_mask * noisy], dim=1)      # [B, 2, K, L]
        pred = self.net(inp, self._side_info(cond_mask), t)
        resid = (noise - pred) * target_mask
        return (resid ** 2).sum() / target_mask.sum().clamp_min(1.0)

    # ---------------------------------------------------------------- sampling
    @torch.no_grad()
    def sample(self, batch_x, n_samples=None):
        n_samples = n_samples or self.n_samples
        data, cond_mask = self._assemble(batch_x)
        B, K, T = data.shape
        side = self._side_info(cond_mask)
        target_mask = 1.0 - cond_mask
        out = torch.zeros(n_samples, B, K, T, device=data.device)
        for s in range(n_samples):
            cur = torch.randn_like(data)
            for t in reversed(range(self.num_steps)):
                inp = torch.stack([cond_mask * data, target_mask * cur], dim=1)
                pred = self.net(inp, side, torch.full((B,), t, device=data.device, dtype=torch.long))
                c1 = 1.0 / (1.0 - self.beta[t]) ** 0.5
                c2 = (1.0 - (1.0 - self.beta[t])) / (1.0 - self.alpha[t]) ** 0.5
                cur = c1 * (cur - c2 * pred)
                if t > 0:
                    sigma = ((1.0 - self.alpha[t - 1]) / (1.0 - self.alpha[t]) * self.beta[t]) ** 0.5
                    cur = cur + sigma * torch.randn_like(cur)
            out[s] = cur
        # [S, B, K, T] -> [S, B, H, K] (horizon only)
        return out[:, :, :, self.seq_len:].permute(0, 1, 3, 2)

    def forward(self, batch_x):
        # point forecast = sample median (P2.3); the runner calls sample() directly for the full set
        return self.sample(batch_x, n_samples=min(self.n_samples, 10)).median(dim=0).values
