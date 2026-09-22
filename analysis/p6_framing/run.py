#!/usr/bin/env python3
"""
Phase 6: framing analyses on the full roster and three seeds (R4.2, R4.3, R1.4).

Writes analysis/p6_framing/
  headline_tau.csv          Kendall tau between the MAE ranking and each fidelity ranking, per
                            paradigm / condition / signal (synthetic and real), bootstrap CI over units
  dissociation_full.csv     sequence-level absolute-MAE binning by bias group (as P0.4) on all seeds
  nonlocal_leads.csv        every (paradigm, condition, signal, metric) where the best model is not in
                            the Local group, or where the local-group advantage over Linear is not
                            significant (from p5 paired tests)
Run:  python analysis/p6_framing/run.py   (after analysis/p5_stats/run.py)
"""
import os, sys
import numpy as np, pandas as pd
from scipy import stats
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); sys.path.insert(0, REPO)
from analysis.common import bias as load_bias, load_paradigm
from utils.stats import aggregate_units, kendall_tau_ci

PARADIGMS = ["clean", "noise", "shift", "state_transition", "markov_dwell", "real_ppg_A", "real_ecg_A", "real_eeg_A",
             "real_ppg_B", "real_ecg_B", "tier2_ecg", "tier2_ppg", "tier2_eeg"]
BINS = [(0.0, 0.05), (0.05, 0.10), (0.10, 0.20), (0.20, np.inf)]


def main():
    B = load_bias()
    taus, diss, leads = [], [], []
    p5 = os.path.join(REPO, "analysis", "p5_stats", "paired_tests.csv")
    p5 = pd.read_csv(p5) if os.path.exists(p5) else None
    for par in PARADIGMS:
        df = load_paradigm(par)
        if df.empty:
            continue
        df["group"] = df.model.map(B["model_to_group"])
        fids = [m for m in ["phase", "freq", "peak_timing", "peak_f1", "rr_err"] if m in df.columns and df[m].notna().any()]
        for (cond, sig), d in df.groupby(["condition", "signal"]):
            units = aggregate_units(d, ["mae"] + fids, unit_col="unit")
            for fid in fids:
                taus.append(dict(paradigm=par, condition=cond, signal=sig, fidelity=fid, **kendall_tau_ci(units, "mae", fid, unit_col="unit")))
            means = units.groupby("model")[["mae"] + fids].mean()
            for m in ["mae"] + fids:
                best = means[m].idxmin() if m != "peak_f1" else means[m].idxmax()
                if B["model_to_group"].get(best) != "Local receptive field":
                    leads.append(dict(paradigm=par, condition=cond, signal=sig, metric=m, best_model=best,
                                      best_group=B["model_to_group"].get(best), reason="best model is non-local"))
            if p5 is not None:
                t = p5[(p5.paradigm == par) & (p5.condition.fillna("") == cond) & (p5.signal == sig)]
                for m, g in t.groupby("metric"):
                    loc = g[g.model.map(B["model_to_group"]) == "Local receptive field"]
                    weak = loc[~(loc.significant & (loc.direction == "better"))]
                    for _, r in weak.iterrows():
                        leads.append(dict(paradigm=par, condition=cond, signal=sig, metric=m, best_model=r.model,
                                          best_group="Local receptive field", reason="local model not significantly better than Linear"))
            # sequence-level dissociation on all seeds
            d = d.assign(rel_mae=d.mae / d.a_rms)
            for lo, hi in BINS:
                sub = d[(d.rel_mae >= lo) & (d.rel_mae < hi)]
                for fid in [f for f in ["phase", "freq"] if f in sub.columns]:
                    pf = sub.groupby(["group", "model", "unit"])[fid].mean().reset_index()
                    groups = [pf.loc[pf.group == g, fid].dropna().values for g in B["groups"] if (pf.group == g).sum() >= 2]
                    if len(groups) >= 2:
                        H, p = stats.kruskal(*groups); k, n = len(groups), sum(len(g) for g in groups)
                        eps2 = (H - k + 1) / (n - k)
                    else:
                        p, eps2, k, n = np.nan, np.nan, len(groups), sum(len(g) for g in groups)
                    med = sub.groupby("group")[fid].median().to_dict()
                    diss.append(dict(paradigm=par, condition=cond, signal=sig, metric=fid, bin_lo=lo, bin_hi=hi,
                                     n_windows=len(sub), n_groups=k, n_units=n, p_file=p, eps2_file=eps2,
                                     **{f"median_{g}": med.get(g, np.nan) for g in B["groups"]}))
    for name, rows in [("headline_tau.csv", taus), ("dissociation_full.csv", diss), ("nonlocal_leads.csv", leads)]:
        if rows:
            pd.DataFrame(rows).to_csv(os.path.join(HERE, name), index=False)
    print("done")


if __name__ == "__main__":
    main()
