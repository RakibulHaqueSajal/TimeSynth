"""Generator tests (REVISION_PLAN.md P3, P4)."""
import os
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "Bio_Synthesize", "Synthetic_Signals_bio"))

import markov_dwell_pooled as M  # noqa: E402


def test_dwell_parameterization_mean_dwell():
    rng = np.random.default_rng(0)
    fs = 10.0
    for D in (2.0, 5.0, 10.0):
        st = M.simulate_chain(200_000, M.p_from_dwell(D, fs), rng)
        n_sw = np.sum(np.diff(st) != 0)
        mean_dwell = (st.size / n_sw) / fs
        assert abs(mean_dwell - D) / D < 0.05


def test_continue_from_reproduces_truth_when_states_match():
    """A continuation driven by the TRUE future states must equal the true future exactly."""
    rng = np.random.default_rng(1)
    fs, T = 10.0, 3000
    params = dict(D=5.0, A=0.11, f0=0.8, f1=1.15, beta=0.1, dbeta=0.03, fmod=0.05, offset=0.4)
    st = M.simulate_chain(T, M.p_from_dwell(params["D"], fs), rng)
    t, x, _ = M.synthesize(st, fs, params["A"], params["f0"], params["f1"], params["beta"],
                           params["dbeta"], params["fmod"], params["offset"])
    df = pd.DataFrame({"Time": t, "Value": x, "State": st})
    start, L, H = 300, 50, 100
    b = start + L
    # monkeypatch the chain draw to return the true states
    true_future = st[b - 1:b + H]                     # includes the boundary state as start
    M_sim = M.simulate_chain
    M.simulate_chain = lambda n, p, rng, start_state=0: true_future[:n]
    try:
        alt = M.continue_from(df, start, L, H, 1, fs, params, rng)
    finally:
        M.simulate_chain = M_sim
    assert np.max(np.abs(alt[0] - x[b:b + H])) < 1e-9


def test_parse_params_roundtrip():
    name = M.file_name("test", 3, 5.0, 0.11, 0.8, 1.15, 0.1, 0.03, 0.05, 0.4)
    p = M.parse_params(name)
    assert p["D"] == 5.0 and abs(p["f1"] - 1.15) < 1e-9 and abs(p["dbeta"] - 0.03) < 1e-9
