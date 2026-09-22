#!/usr/bin/env python3
"""
Phase 3 analysis (P3.5, P3.6): Tier 2 transient-rich signals.

Writes analysis/p3_tier2/
  tier2_table.csv          per (paradigm, condition, model): unit-level means of MAE, freq, peak timing (ms),
                           peak amplitude, detection F1, RR error; seed mean and SD
  locality_peak_timing.csv Wilcoxon vs Linear over units for peak timing and F1 (Phase 5 statistics)
  tier_agreement.csv       Kendall tau between Tier 2 and Tier 1 model rankings (ECG <-> SPM/DPM, PPG <-> Drift,
                           EEG <-> DPM) and between each tier and the real Track B ranking (from p1_real)
Run:  python analysis/p3_tier2/run.py
"""
import os, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); sys.path.insert(0, REPO)
from analysis.common import bias as load_bias, load_paradigm
from utils.stats import aggregate_units, paired_vs_baseline, rank_transfer

T2 = {"tier2_ecg": ["Single_Phase_Modulation", "Dual_Phase_Modulation"], "tier2_ppg": ["Drift_Harmonic"], "tier2_eeg": ["Dual_Phase_Modulation"]}
REALB = {"tier2_ecg": "real_ecg_B", "tier2_ppg": "real_ppg_B"}
METRICS = ["mae", "freq", "peak_timing", "peak_amp", "peak_f1", "rr_err"]


def main():
    B = load_bias()
    clean = load_paradigm("clean")
    rows, tests, agree = [], [], []
    for par, fams in T2.items():
        df = load_paradigm(par)
        if df.empty:
            print("no results for", par); continue
        metrics = [m for m in METRICS if m in df.columns]
        for cond, d in df.groupby("condition"):
            u = d.groupby(["model", "seed", "unit"])[metrics].mean().reset_index()
            ps = u.groupby(["model", "seed"])[metrics].mean().reset_index()
            agg = ps.groupby("model")[metrics].agg(["mean", "std"]); agg.columns = [f"{a}_{b}" for a, b in agg.columns]
            agg = agg.reset_index(); agg["paradigm"], agg["condition"] = par, cond
            agg["peak_timing_ms_mean"] = agg["peak_timing_mean"] * 1000
            rows.append(agg)
            units = aggregate_units(d, metrics, unit_col="unit")
            if cond == "" and "Linear" in set(units.model):
                for m in ["peak_timing", "peak_f1", "mae"]:
                    t = paired_vs_baseline(units, m, baseline="Linear", unit_col="unit"); t["paradigm"] = par; tests.append(t)
            if cond == "" and len(clean):
                for fam in fams:
                    su = aggregate_units(clean[(clean.signal == fam) & (clean.condition == "")], ["mae", "freq"], unit_col="unit")
                    for m in ["mae", "freq"]:
                        r = rank_transfer(su, units, m, unit_col="unit")
                        agree.append(dict(tier2=par, other=f"tier1:{fam}", metric=m, **{k: v for k, v in r.items() if k not in ("models", "rank_syn", "rank_real")}))
                if par in REALB:
                    real = load_paradigm(REALB[par])
                    if not real.empty:
                        for ds, rd in real.groupby("signal"):
                            ru = aggregate_units(rd, [m for m in metrics if m in rd.columns], unit_col="unit")
                            for m in [x for x in ["mae", "peak_timing", "peak_f1"] if x in ru.columns]:
                                r = rank_transfer(units, ru, m, unit_col="unit")
                                agree.append(dict(tier2=par, other=f"real:{ds}", metric=m, **{k: v for k, v in r.items() if k not in ("models", "rank_syn", "rank_real")}))
                            for fam in fams:
                                su = aggregate_units(clean[(clean.signal == fam) & (clean.condition == "")], ["mae"], unit_col="unit")
                                r = rank_transfer(su, ru, "mae", unit_col="unit")
                                agree.append(dict(tier2=f"tier1:{fam}", other=f"real:{ds}", metric="mae", **{k: v for k, v in r.items() if k not in ("models", "rank_syn", "rank_real")}))
    if rows: pd.concat(rows).to_csv(os.path.join(HERE, "tier2_table.csv"), index=False)
    if tests: pd.concat(tests).to_csv(os.path.join(HERE, "locality_peak_timing.csv"), index=False)
    if agree: pd.DataFrame(agree).to_csv(os.path.join(HERE, "tier_agreement.csv"), index=False)
    print("done")


if __name__ == "__main__":
    main()
