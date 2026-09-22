#!/usr/bin/env python3
"""
Phase 4 analysis (P4.3, P4.4): redesigned Markov paradigm.

Probe (same feature as the paper, Statistical_Test/markov.py): windowed Welch dominant
frequency of the horizon (win 16, hop 8 at 10 Hz), a 2-state GaussianHMM fitted on the
TRUE futures pooled over all test windows of one dwell time D, decoded on true and on
predicted futures (per sample for CSDI), states canonicalized by feature mean.

Metrics per (D, model, seed):
  kl_rate        symmetrized transition-matrix KL rate between the chain fitted to decoded
                 true futures and the chain fitted to decoded predicted futures (P4.3)
  dwell_true/pred/abs_err   mean dwell time (s) from the fitted matrices
  frac_between   P4.4 regression-to-the-mean: fraction of forecast samples whose local dominant
                 frequency lies strictly between the two state bands (f0 upper, f1 lower bound)
  mae / phase / freq        unit-level means for reference
Outputs: analysis/p4_markov/markov_metrics.csv, markov_summary.csv, figures/fig8_alt_futures,
figures/kl_by_dwell. Run:  python analysis/p4_markov/run.py
"""
import glob
import json
import os
import sys

import numpy as np
import pandas as pd
from hmmlearn.hmm import GaussianHMM
from scipy.signal import welch

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, REPO)
from analysis.common import RESULTS_ROOT, bias as load_bias, load_paradigm   # noqa: E402
from analysis.plotting import BLUE, GRAY, NAVY, RED, TEAL, plt, save, title   # noqa: E402
from utils import fidelity as F                                               # noqa: E402
from utils.config import DEFAULT_DATA_ROOT                                    # noqa: E402
from utils.results_io import load_result                                      # noqa: E402

FS, WIN, HOP = 10.0, 16, 8
GEN = json.load(open(os.path.join(DEFAULT_DATA_ROOT, "PhaseMod_Markov_Dwell", "generation_config.json")))
F0_HI, F1_LO = GEN["f0_range"][1], GEN["f1_range"][0]


def domfreq_windows(Y):
    """Y [N, H] -> list of feature sequences [n_win, 1]."""
    out = []
    for y in Y:
        y = y - y.mean()
        z = []
        for a in range(0, y.size - WIN + 1, HOP):
            f, P = welch(y[a:a + WIN], fs=FS, nperseg=WIN)
            z.append(f[np.argmax(P)])
        out.append(np.asarray(z)[:, None])
    return out


def fit_hmm(Zs, seeds=(0, 1, 2)):
    X = np.concatenate(Zs)
    lengths = [len(z) for z in Zs]
    mu, sd = X.mean(0), X.std(0) + 1e-9
    best, best_ll = None, -np.inf
    for s in seeds:
        m = GaussianHMM(n_components=2, covariance_type="diag", n_iter=500, tol=1e-4, random_state=s)
        try:
            m.fit((X - mu) / sd, lengths)
            ll = m.score((X - mu) / sd, lengths)
        except Exception:
            continue
        if ll > best_ll:
            best, best_ll = m, ll
    return best, (mu, sd)


def decode(model, norm, Zs):
    mu, sd = norm
    X = np.concatenate(Zs)
    st = model.predict((X - mu) / sd, [len(z) for z in Zs])
    # canonical: state 0 = lower mean frequency
    means = [X[st == k, 0].mean() if np.any(st == k) else np.inf for k in (0, 1)]
    if means[0] > means[1]:
        st = 1 - st
    out, i = [], 0
    for z in Zs:
        out.append(st[i:i + len(z)]); i += len(z)
    return out


def chain_metrics(true_states, pred_states):
    P = F.transition_matrix(true_states)
    Q = F.transition_matrix(pred_states)
    fs_win = FS / HOP
    return dict(kl_rate=F.transition_kl_rate(P, Q),
                dwell_true=float(F.mean_dwell_from_matrix(P, fs_win).mean()),
                dwell_pred=float(F.mean_dwell_from_matrix(Q, fs_win).mean()))


def frac_between(Y):
    Zs = domfreq_windows(Y)
    z = np.concatenate(Zs)[:, 0]
    return float(np.mean((z > F0_HI) & (z < F1_LO)))


def main():
    B = load_bias()
    rows = []
    for cond in ["D2", "D5", "D10"]:
        runs = sorted(glob.glob(os.path.join(RESULTS_ROOT, f"markov_dwell__{cond}", "*", "*", "seed*")))
        if not runs:
            print("no results for", cond); continue
        # HMM fitted on the true futures once per D (identical across models)
        hist, true, pred, meta = load_result(runs[0])[:4]
        Zt = domfreq_windows(true)
        hmm, norm = fit_hmm(Zt)
        if hmm is None:
            print("HMM fit failed for", cond); continue
        st_true = decode(hmm, norm, Zt)
        for run in runs:
            rel = os.path.relpath(run, RESULTS_ROOT).split(os.sep)
            model, seed = rel[2], int(rel[3][4:])
            res = load_result(run)
            hist, true, pred, meta = res[:4]
            samples = res[4] if len(res) > 4 else None
            if samples is not None:                      # CSDI: chain statistics per sample, then averaged
                per = [chain_metrics(st_true, decode(hmm, norm, domfreq_windows(samples[s]))) for s in range(min(10, samples.shape[0]))]
                cm = {k: float(np.mean([p[k] for p in per])) for k in per[0]}
                fb = float(np.mean([frac_between(samples[s]) for s in range(min(10, samples.shape[0]))]))
            else:
                cm = chain_metrics(st_true, decode(hmm, norm, domfreq_windows(pred)))
                fb = frac_between(pred)
            rows.append(dict(D=float(cond[1:]), model=model, seed=seed, group=B["model_to_group"].get(model),
                             n_windows=len(true), **cm, dwell_abs_err=abs(cm["dwell_pred"] - cm["dwell_true"]),
                             frac_between=fb, frac_between_true=frac_between(true),
                             mae=float(F.mae(pred, true).mean()), phase=float(np.nanmean(F.phase_error_deg(pred, true))),
                             freq=float(np.nanmean(F.freq_error(pred, true, fs=FS)))))
            print(cond, model, seed, {k: round(v, 3) for k, v in cm.items()}, "between", round(fb, 3), flush=True)
    if not rows:
        return
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(HERE, "markov_metrics.csv"), index=False)
    summ = df.groupby(["D", "model", "group"])[["kl_rate", "dwell_abs_err", "frac_between", "mae", "phase", "freq"]].agg(["mean", "std"])
    summ.columns = [f"{a}_{b}" for a, b in summ.columns]
    summ.reset_index().to_csv(os.path.join(HERE, "markov_summary.csv"), index=False)

    # figure: KL rate by dwell time, one line per model, seed error bars
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for model, g in df.groupby("model"):
        s = g.groupby("D")[["kl_rate", "frac_between"]].agg(["mean", "std"])
        c = B["model_to_color"].get(model, GRAY)
        axes[0].errorbar(s.index, s[("kl_rate", "mean")], yerr=s[("kl_rate", "std")].fillna(0), color=c, marker="o", ms=3, lw=1, capsize=2, label=B["display"].get(model, model))
        axes[1].errorbar(s.index, s[("frac_between", "mean")], yerr=s[("frac_between", "std")].fillna(0), color=c, marker="o", ms=3, lw=1, capsize=2)
    title(axes[0], "Transition-matrix KL rate vs dwell time", "chain fitted to predicted futures vs chain fitted to true futures; lower is better")
    axes[0].set_xlabel("expected dwell time D (s)"); axes[0].set_ylabel("KL rate (nats / step)")
    title(axes[1], "Regression to the mean", "fraction of forecast time with local frequency between the two state bands")
    axes[1].set_xlabel("expected dwell time D (s)"); axes[1].set_ylabel("fraction")
    axes[0].legend(fontsize=6.5, ncol=2)
    fig.tight_layout()
    save(fig, os.path.join(HERE, "figures", "kl_by_dwell"))
    fig8(B)
    print("done")


def fig8(B, D="D5"):
    """New Figure 8a: two true futures from the same history, point forecasts, CSDI samples."""
    alt_dir = os.path.join(DEFAULT_DATA_ROOT, "PhaseMod_Markov_Dwell", "alt_futures")
    metas = sorted(glob.glob(os.path.join(alt_dir, f"test_*_D_{D[1:]}_*.json")))
    if not metas:
        return
    info = json.load(open(metas[0]))
    alt = np.load(metas[0][:-5] + ".npy")                        # [n_windows, K, H]
    csv = os.path.join(DEFAULT_DATA_ROOT, "PhaseMod_Markov_Dwell", "by_dwell", D, "test", info["file"])
    x = pd.read_csv(csv).Value.values
    w = len(info["window_starts"]) // 2
    s0 = info["window_starts"][w]
    L, H = info["seq_len"], info["pred_len"]
    t_h = np.arange(L) / FS - L / FS
    t_f = np.arange(H) / FS
    fig, axes = plt.subplots(1, 3, figsize=(14, 3.6), sharey=True)
    for ax in axes:
        ax.plot(t_h, x[s0:s0 + L], color=NAVY, lw=1.2)
        ax.axvline(0, color=GRAY, lw=0.8, ls=":")
    axes[0].plot(t_f, x[s0 + L:s0 + L + H], color=TEAL, lw=1.2, label="true future (realized)")
    axes[0].plot(t_f, alt[w, 0], color=RED, lw=1.0, alpha=0.9, label="alternative true future")
    axes[0].legend(fontsize=7)
    title(axes[0], "Two valid futures of one history", f"same chain statistics (D = {D[1:]} s), independent switching")
    # point forecasts from results
    run_glob = os.path.join(RESULTS_ROOT, f"markov_dwell__{D}", "*", "{m}", "seed2021")
    for m, c in [("Linear", B["model_to_color"].get("Linear", GRAY)), ("PatchTST", B["model_to_color"].get("PatchTST", GRAY))]:
        runs = glob.glob(run_glob.format(m=m))
        if runs:
            hist, true, pred, meta = load_result(runs[0])[:4]
            idx = meta.index[(meta.file_name == info["file"]) & (meta.window_start == s0)]
            if len(idx):
                axes[1].plot(t_f, pred[idx[0]], color=c, lw=1.1, label=m)
    axes[1].plot(t_f, x[s0 + L:s0 + L + H], color=TEAL, lw=0.9, alpha=0.6)
    axes[1].legend(fontsize=7)
    title(axes[1], "Point forecasts", "deterministic models regress toward a blend of the two states")
    runs = glob.glob(run_glob.format(m="CSDI"))
    if runs:
        res = load_result(runs[0])
        meta, samples = res[3], res[4] if len(res) > 4 else None
        idx = meta.index[(meta.file_name == info["file"]) & (meta.window_start == s0)]
        if samples is not None and len(idx):
            for s in range(min(8, samples.shape[0])):
                axes[2].plot(t_f, samples[s, idx[0]], color=BLUE, lw=0.7, alpha=0.5)
    axes[2].plot(t_f, x[s0 + L:s0 + L + H], color=TEAL, lw=0.9, alpha=0.6)
    title(axes[2], "CSDI samples", "a probabilistic model can commit to one state per sample")
    for ax in axes:
        ax.set_xlabel("time from forecast boundary (s)")
    fig.tight_layout()
    save(fig, os.path.join(HERE, "figures", "fig8_alt_futures"))


if __name__ == "__main__":
    main()
