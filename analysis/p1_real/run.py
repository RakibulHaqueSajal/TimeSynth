#!/usr/bin/env python3
"""
Phase 1 analysis (P1.5 to P1.8): real-data validation.

Reads results/real_*_{A,B}/ and results/clean/ (matched synthetic families), and writes
  analysis/p1_real/per_subject_metrics.parquet   one row per (dataset, track, model, subject)
  analysis/p1_real/ranking_transfer.csv          Kendall tau / Spearman rho synthetic -> real, per metric
  analysis/p1_real/disagreement.csv              tau between MAE ranking and each fidelity ranking on real data
  analysis/p1_real/bias_group_ranks.csv          mean rank per bias group, synthetic vs real
  analysis/p1_real/natural_events.csv            metrics on windows whose horizon contains a natural event
  analysis/p1_real/hr_proxy.csv                  P1.7 heart-rate error from forecasts (Track A: dominant
                                                 frequency; Track B: detected beats)
  analysis/p1_real/supp_table_real.csv           per-model metrics per dataset, mean and 95% CI over subjects
  figures/                                       rank-transfer scatter per modality and metric
Matched families: PPG <- Drift_Harmonic, ECG <- Single_Phase_Modulation and Dual_Phase_Modulation,
EEG <- Dual_Phase_Modulation.
Run:  python analysis/p1_real/run.py
"""
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, REPO)
from analysis.common import bias as load_bias, load_paradigm         # noqa: E402
from analysis.plotting import BLUE, GRAY, NAVY, RED, TEAL, plt, save, title  # noqa: E402
from utils import fidelity as F                                      # noqa: E402
from utils.stats import aggregate_units, kendall_tau_ci, paired_vs_baseline, rank_transfer  # noqa: E402

MATCH = {"ppg": ["Drift_Harmonic"], "ecg": ["Single_Phase_Modulation", "Dual_Phase_Modulation"],
         "eeg": ["Dual_Phase_Modulation"]}
REAL = ["real_ppg_A", "real_ecg_A", "real_eeg_A", "real_ppg_B", "real_ecg_B"]
METRICS_A = ["mae", "phase", "freq", "band_power", "xcorr_lag"]
METRICS_B = ["mae", "phase", "freq", "band_power", "xcorr_lag", "peak_timing", "peak_amp", "peak_f1", "rr_err"]


def ci95(x):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if x.size < 2:
        return np.nan, np.nan
    se = x.std(ddof=1) / np.sqrt(x.size)
    return x.mean() - 1.96 * se, x.mean() + 1.96 * se


def main():
    B = load_bias()
    syn = load_paradigm("clean")
    syn = syn[syn.condition == ""] if len(syn) else syn
    out_rows_rt, out_rows_dis, out_rows_bg, per_subject, supp, events, hr = [], [], [], [], [], [], []
    for par in REAL:
        df = load_paradigm(par)
        if df.empty:
            print("no results yet for", par)
            continue
        mod = par.split("_")[1]
        metrics = METRICS_B if par.endswith("_B") else METRICS_A
        metrics = [m for m in metrics if m in df.columns]
        for ds, d in df.groupby("signal"):
            units = aggregate_units(d, metrics, unit_col="unit")
            units["dataset"], units["track"] = ds, par[-1]
            per_subject.append(units)
            # supplementary table: mean and CI over subjects per model
            for model, g in units.groupby("model"):
                row = dict(dataset=ds, track=par[-1], model=model, n_subjects=len(g))
                for m in metrics:
                    lo, hi = ci95(g[m])
                    row[f"{m}_mean"], row[f"{m}_ci_lo"], row[f"{m}_ci_hi"] = g[m].mean(), lo, hi
                supp.append(row)
            # disagreement on real data
            for fid in [m for m in metrics if m != "mae"]:
                r = kendall_tau_ci(units, "mae", fid, unit_col="unit")
                out_rows_dis.append(dict(dataset=ds, track=par[-1], fidelity=fid, **r))
            # ranking transfer against matched synthetic families (Track A metrics shared: mae/phase/freq)
            if len(syn):
                for fam in MATCH[mod]:
                    s_units = aggregate_units(syn[syn.signal == fam], ["mae", "phase", "freq"], unit_col="unit")
                    for m in ["mae", "phase", "freq"]:
                        r = rank_transfer(s_units, units, m, unit_col="unit")
                        out_rows_rt.append(dict(dataset=ds, track=par[-1], synthetic_family=fam, metric=m,
                                                **{k: v for k, v in r.items() if k not in ("models", "rank_syn", "rank_real")}))
                        # bias-group mean ranks
                        rs = pd.Series(r["rank_syn"], index=r["models"]).rank()
                        rr = pd.Series(r["rank_real"], index=r["models"]).rank()
                        for grp in B["groups"]:
                            ms = [x for x in r["models"] if B["model_to_group"].get(x) == grp]
                            if ms:
                                out_rows_bg.append(dict(dataset=ds, track=par[-1], synthetic_family=fam, metric=m,
                                                        group=grp, mean_rank_syn=rs[ms].mean(), mean_rank_real=rr[ms].mean(), n_models=len(ms)))
            # natural events: windows with an event inside the horizon vs none, per model
            if "event_in_horizon" in d.columns and (d.event_in_horizon != "").any():
                for (model, has), g in d.groupby(["model", d.event_in_horizon != ""]):
                    ev = dict(dataset=ds, track=par[-1], model=model, event_in_horizon=bool(has), n_windows=len(g))
                    for m in metrics:
                        ev[m] = g[m].mean()
                    events.append(ev)
            # P1.7 heart-rate proxy (PPG / ECG only)
            if mod in ("ppg", "ecg"):
                fs = float(d.fs.iloc[0])
                for (model, seed), g in d.groupby(["model", "seed"]):
                    # per window HR error is recomputed from saved arrays via freq (Track A) or rr_err (Track B)
                    if par.endswith("_A"):
                        hr_err = 60.0 * g["freq"]                      # bpm, dominant-frequency HR
                    else:
                        # RR error (s) -> HR error at the true mean RR: |60/RR_pred - 60/RR_true| ~ 60 * dRR / RR^2
                        hr_err = 60.0 * g["rr_err"] / (60.0 / 75.0) ** 2   # nominal 75 bpm
                    hr.append(dict(dataset=ds, track=par[-1], model=model, seed=seed,
                                   hr_abs_error_bpm=float(np.nanmean(hr_err)), n_windows=int(np.isfinite(hr_err).sum())))
    if per_subject:
        pd.concat(per_subject).to_parquet(os.path.join(HERE, "per_subject_metrics.parquet"), index=False)
        pd.DataFrame(supp).to_csv(os.path.join(HERE, "supp_table_real.csv"), index=False)
    if out_rows_rt:
        pd.DataFrame(out_rows_rt).to_csv(os.path.join(HERE, "ranking_transfer.csv"), index=False)
        pd.DataFrame(out_rows_bg).to_csv(os.path.join(HERE, "bias_group_ranks.csv"), index=False)
    if out_rows_dis:
        pd.DataFrame(out_rows_dis).to_csv(os.path.join(HERE, "disagreement.csv"), index=False)
    if events:
        pd.DataFrame(events).to_csv(os.path.join(HERE, "natural_events.csv"), index=False)
    if hr:
        pd.DataFrame(hr).to_csv(os.path.join(HERE, "hr_proxy.csv"), index=False)
    if out_rows_rt:
        make_figure(pd.DataFrame(out_rows_rt), B)
    print("done")


def make_figure(rt, B):
    """Synthetic rank vs real rank scatter, one panel per (modality, metric), bias groups colored."""
    syn = load_paradigm("clean")
    from utils.stats import aggregate_units
    panels = [(ds, fam, m) for (ds, fam, m) in rt[["dataset", "synthetic_family", "metric"]].drop_duplicates().itertuples(index=False)]
    n = len(panels)
    if n == 0:
        return
    cols = min(3, n)
    rows = int(np.ceil(n / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(4.2 * cols, 3.8 * rows), squeeze=False)
    for ax, (ds, fam, m) in zip(axes.ravel(), panels):
        real = pd.read_parquet(os.path.join(HERE, "per_subject_metrics.parquet"))
        real = real[real.dataset == ds]
        s_units = aggregate_units(syn[syn.signal == fam], [m], unit_col="unit")
        rs = s_units.groupby("model")[m].mean().rank()
        rr = real.groupby("model")[m].mean().rank()
        models = [x for x in rs.index if x in rr.index]
        for x in models:
            ax.scatter(rs[x], rr[x], color=B["model_to_color"].get(x, GRAY), s=36, zorder=3)
            ax.annotate(B["display"].get(x, x), (rs[x], rr[x]), fontsize=6.5, xytext=(3, 3), textcoords="offset points")
        k = len(models)
        ax.plot([1, k], [1, k], color=GRAY, lw=0.8, ls=":")
        r = rt[(rt.dataset == ds) & (rt.synthetic_family == fam) & (rt.metric == m)].iloc[0]
        ax.text(0.02, 0.95, rf"$\tau$ = {r.tau:.2f} [{r.tau_ci_lo:.2f}, {r.tau_ci_hi:.2f}]", transform=ax.transAxes,
                fontsize=8, color=TEAL if r.tau_ci_lo > 0 else RED, va="top")
        title(ax, f"{ds}: {m}", f"synthetic family {fam}")
        ax.set_xlabel("rank on synthetic (1 = best)")
        ax.set_ylabel("rank on real (1 = best)")
    for ax in axes.ravel()[n:]:
        ax.axis("off")
    fig.tight_layout()
    save(fig, os.path.join(HERE, "figures", "rank_transfer"))


if __name__ == "__main__":
    main()
