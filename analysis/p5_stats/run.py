#!/usr/bin/env python3
"""
Phase 5: statistics and sample-size reporting (R4.6).

Writes analysis/p5_stats/
  sample_size_table.csv   per paradigm/condition: units, windows per unit, stride, overlap, seeds, test
  paired_tests.csv        Wilcoxon signed-rank vs Linear over units (seed-averaged), Holm within
                          (paradigm, condition, signal, metric), bootstrap CI, dz
  mixed_model_check.csv   metric ~ model + (1|unit) + (1|seed) for the clean paradigm (sensitivity)
Run:  python analysis/p5_stats/run.py
"""
import os, sys
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); sys.path.insert(0, REPO)
from analysis.common import load_paradigm
from utils.stats import aggregate_units, mixed_model_check, paired_vs_baseline, sample_size_table

PARADIGMS = ["clean", "noise", "shift", "state_transition", "markov_dwell", "real_ppg_A", "real_ecg_A", "real_eeg_A",
             "real_ppg_B", "real_ecg_B", "tier2_ecg", "tier2_ppg", "tier2_eeg"]
CORE = ["mae", "phase", "freq"]


def main():
    metas, tests, mm = {}, [], []
    for par in PARADIGMS:
        df = load_paradigm(par)
        if df.empty:
            continue
        for (cond, sig), d in df.groupby(["condition", "signal"]):
            key = f"{par}{'__' + cond if cond else ''}/{sig}"
            metas[key] = d
            metrics = [m for m in CORE + ["peak_timing", "peak_f1", "rr_err", "crps"] if m in d.columns and d[m].notna().any()]
            units = aggregate_units(d, metrics, unit_col="unit")
            if "Linear" not in set(units.model):
                continue
            for m in metrics:
                t = paired_vs_baseline(units, m, baseline="Linear", unit_col="unit")
                t["paradigm"], t["condition"], t["signal"] = par, cond, sig
                tests.append(t)
            if par == "clean":
                ps = aggregate_units(d, CORE, unit_col="unit", keep_seed=True)
                for m in CORE:
                    tab = mixed_model_check(ps, m, baseline="Linear", unit_col="unit")
                    if tab is not None:
                        tab["signal"], tab["metric"] = sig, m
                        mm.append(tab)
    if metas:
        sample_size_table(metas).to_csv(os.path.join(HERE, "sample_size_table.csv"), index=False)
    if tests:
        pd.concat(tests).to_csv(os.path.join(HERE, "paired_tests.csv"), index=False)
    if mm:
        pd.concat(mm).to_csv(os.path.join(HERE, "mixed_model_check.csv"), index=False)
    print("done", len(metas), "paradigm/signal tables")


if __name__ == "__main__":
    main()
