"""Unit tests for the new baselines (REVISION_PLAN.md P2.2, P2.4)."""
import os
import sys
import types

import numpy as np
import pytest
import torch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from Model import SeasonalNaive, TSMixer  # noqa: E402


def cfg(**kw):
    base = dict(seq_len=50, pred_len=100, enc_in=1, e_layers=2, d_ff=64, dropout=0.0,
                revin=1, affine=0, subtract_last=0, task_name="long_term_forecast")
    base.update(kw)
    return types.SimpleNamespace(**base)


def test_tsmixer_forward_shape():
    m = TSMixer.Model(cfg())
    y = m(torch.randn(8, 50, 1))
    assert y.shape == (8, 100, 1)
    m3 = TSMixer.Model(cfg(enc_in=3))
    assert m3(torch.randn(4, 50, 3)).shape == (4, 100, 3)


def test_tsmixer_overfits_single_sinusoid():
    torch.manual_seed(0)
    # a small batch of sliding windows from one sinusoid (BatchNorm needs batch > 1)
    t = torch.arange(300, dtype=torch.float32) / 10.0
    s = torch.sin(2 * np.pi * 1.0 * t)
    wins = torch.stack([s[i:i + 150] for i in range(0, 16 * 3, 3)])[:, :, None]
    hist, fut = wins[:, :50], wins[:, 50:]
    m = TSMixer.Model(cfg(dropout=0.0))
    m.train()
    opt = torch.optim.Adam(m.parameters(), lr=5e-3)
    for _ in range(200):
        opt.zero_grad()
        loss = torch.mean((m(hist) - fut) ** 2)
        loss.backward()
        opt.step()
    m.eval()
    assert torch.mean((m(hist) - fut) ** 2).item() < 1e-3


def test_seasonal_naive_continues_sinusoid():
    m = SeasonalNaive.Model(cfg())
    fs, f = 10.0, 1.3
    t = torch.arange(150, dtype=torch.float32) / fs
    x = torch.sin(2 * np.pi * f * t)[None, :, None]
    y = m(x[:, :50])
    assert y.shape == (1, 100, 1)
    err = torch.mean(torch.abs(y - x[:, 50:])).item()
    assert err < 0.1                          # period 7.69 samples resolved by interpolation
    # flat history -> last-value forecast
    z = m(torch.zeros(2, 50, 1) + 0.7)
    assert torch.allclose(z, torch.full((2, 100, 1), 0.7))
    assert not any(p.requires_grad for p in m.parameters())


def test_csdi_shapes_and_loss_decreases():
    from Model import CSDI
    torch.manual_seed(0)
    c = cfg(e_layers=1, d_model=16, n_heads=4, diff_steps=5, n_samples=2)
    m = CSDI.Model(c)
    x = torch.randn(4, 50, 1)
    y = torch.randn(4, 100, 1)
    l0 = m.training_loss(x, y)
    assert l0.ndim == 0 and torch.isfinite(l0)
    s = m.sample(x, n_samples=3)
    assert s.shape == (3, 4, 100, 1)
    assert m(x).shape == (4, 100, 1)
    opt = torch.optim.Adam(m.parameters(), lr=1e-3)
    t = torch.arange(150, dtype=torch.float32) / 10.0
    sig = torch.sin(2 * np.pi * t)[None, :, None].repeat(8, 1, 1)
    losses = []
    for _ in range(60):
        opt.zero_grad()
        loss = m.training_loss(sig[:, :50], sig[:, 50:])
        loss.backward()
        opt.step()
        losses.append(loss.item())
    assert np.mean(losses[-10:]) < np.mean(losses[:10])
