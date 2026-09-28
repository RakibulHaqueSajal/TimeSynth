"""
Regression tests for Layers/Transformers_Embed.py.

The original code applied the temporal embedding only when the encoder input had exactly 125
time steps (`if x_mark.shape[1] == 125`). Every published run used seq_len = 50, so the encoder
saw 25 steps and the branch was never taken; the temporal embedding was therefore never used.
Track B (seq_len 250, encoder half 125) was the first configuration to take it, and it crashed
on a `.view()` of a non-contiguous slice.

These tests pin the two properties that matter:
  1. for the shapes used by every completed run, the new code is numerically identical to the
     old behavior (value + position only), so no finished result is invalidated;
  2. the embedding works for any sequence length, including 125, and on non-contiguous input.
"""
import os
import sys

import torch

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from Layers.Transformers_Embed import DataEmbedding, DataEmbedding_wo_pos, DataEmbedding_wo_temp  # noqa: E402


def test_matches_paper_behavior_for_completed_runs():
    torch.manual_seed(0)
    emb = DataEmbedding(c_in=1, d_model=16, embed_type="timeF", freq="h", dropout=0.0).eval()
    for L in (25, 50, 250):                       # encoder halves and full windows actually used
        x = torch.randn(4, L, 1)
        x_mark = torch.randn(4, L, 1)
        with torch.no_grad():
            got = emb(x, x_mark)
            want = emb.dropout(emb.value_embedding(x) + emb.position_embedding(x))
        assert torch.allclose(got, want, atol=1e-6), L


def test_no_length_dependent_branch():
    """L = 125 must behave like every other length (it used to switch the branch)."""
    torch.manual_seed(0)
    emb = DataEmbedding(c_in=1, d_model=16, embed_type="timeF", freq="h", dropout=0.0).eval()
    with torch.no_grad():
        a = emb(torch.ones(2, 125, 1), torch.ones(2, 125, 1))
        b = emb(torch.ones(2, 124, 1), torch.ones(2, 124, 1))
    assert a.shape == (2, 125, 16) and b.shape == (2, 124, 16)


def test_non_contiguous_slice_is_accepted():
    """The encoder input is batch_x[:, :half, :], which is not contiguous."""
    torch.manual_seed(0)
    emb = DataEmbedding(c_in=1, d_model=16, embed_type="timeF", freq="h", dropout=0.0).eval()
    DataEmbedding.USE_TEMPORAL_EMBEDDING = True          # force the previously broken path
    try:
        full = torch.randn(3, 250, 1)
        half = full[:, :125, :]
        assert not half.is_contiguous()
        with torch.no_grad():
            out = emb(half, half)
        assert out.shape == (3, 125, 16) and torch.isfinite(out).all()
    finally:
        DataEmbedding.USE_TEMPORAL_EMBEDDING = False


def test_wo_temp_and_wo_pos_variants_run():
    torch.manual_seed(0)
    x, xm = torch.randn(2, 125, 1), torch.randn(2, 125, 1)
    with torch.no_grad():
        assert DataEmbedding_wo_temp(c_in=1, d_model=8, dropout=0.0).eval()(x, xm).shape == (2, 125, 8)
        e = DataEmbedding_wo_pos(c_in=1, d_model=8, embed_type="timeF", freq="h", dropout=0.0).eval()
        assert e(x, xm).shape == (2, 125, 8)
        assert e(x, None).shape == (2, 125, 8)
