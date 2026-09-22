#!/usr/bin/env python3
"""
Phase 2 analysis (P2.6): full-roster synthetic results with three seeds.

Writes to analysis/p2_baselines/
  clean_table.csv            per (signal, model): mean and SD over seeds of the unit-level mean
                             MAE / phase / freq (unit = test signal), plus bias group
  paired_vs_linear.csv       Phase 5 tests vs Linear on clean, per signal and metric (units, Holm)
  noise_curves.csv           per (signal, model, SNR level): unit-level mean and seed SD
  shift_curves.csv           per (signal, model, bucket)
  state_transition_tags.csv  per (model, tag class H_d / F_d bins): mean metrics
  acceptance_seed2021.csv    P2.6 acceptance: the rerun seed-2021 numbers for the 11 paper models on
                             clean against the legacy numbers recomputed on the same non-overlapping
                             windows (window_start % 150 == 0 of the legacy stride-1 arrays)
  figures/clean_bars         bar chart with seed error bars, colored by bias group
Run:  python analysis/p2_baselines/run.py
"""
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, REPO)
from analysis import legacy_registry as R                                   # noqa: E402
from analysis.common import bias as load_bias, load_paradigm               # noqa: E402
from analysis.plotting import GRAY, plt, save, title                        # noqa: E402
from utils import fidelity as F                                             # noqa: E402
from utils.results_io import legacy_file_ids, load_legacy                   # noqa: E402
from utils.stats import aggregate_units, paired_vs_baseline                 # noqa: E402

METRICS = ["mae", "phase", "freq"]


def seed_table(df, keys):
    """unit-level mean per (keys, model, seed) -> mean and SD over seeds."""
    u = df.groupby(keys + ["model", "seed", "unit"])[METRICS].mean().reset_index()
    per_seed = u.groupby(keys + ["model", "seed"])[METRICS].mean().reset_index()
    agg = per_seed.groupby(keys + ["model"])[METRICS].agg(["mean", "std", "count"])
    agg.columns = [f"{m}_{s}" for m, s in agg.columns]
    return agg.reset_index()


def acceptance(df_clean, B):
    """Compare rerun seed 2021 (non-overlapping windows) with the legacy arrays subsampled to the same windows."""
    rows = []
    d = df_clean[(df_clean.seed == 2021) & (df_clean.condition == "")]
    for sig in R.SIGNALS:
        for m in R.MODEL_ORDER:
            new = d[(d.signal == sig) & (d.model == m)]
            folder = R.clean_folder(m, sig)
            if new.empty or not os.path.exists(os.path.join(folder, "test_pred_with_history.npy")):
                continue
            hist, true, pred = load_legacy(folder, 50)
            meta = legacy_file_ids(true.shape[0], R.test_split_dir("clean", sig), 50, 100)
            sel = (meta.window_start % 150 == 0).values
            old = dict(mae=np.mean(F.mae(pred[sel], true[sel])), phase=np.nanmean(F.phase_error_deg(pred[sel], true[sel])),
                       freq=np.nanmean(F.freq_error(pred[sel], true[sel], fs=10.0)))
            rows.append(dict(signal=sig, model=m, n_new=len(new), n_legacy=int(sel.sum()),
                             **{f"{k}_new": new[k].mean() for k in METRICS}, **{f"{k}_legacy": old[k] for k in METRICS}))
    out = pd.DataFrame(rows)
    if len(out):
        for k in METRICS:
            out[f"{k}_rel_diff"] = (out[f"{k}_new"] - out[f"{k}_legacy"]) / out[f"{k}_legacy"].abs()
    return out


def main():
    B = load_bias()
    clean = load_paradigm("clean")
    if clean.empty:
        print("no clean results yet")
        return
    clean = clean[clean.condition == ""]
    clean["group"] = clean.model.map(B["model_to_group"])
    tab = seed_table(clean, ["signal"])
    tab["group"] = tab.model.map(B["model_to_group"])
    tab.to_csv(os.path.join(HERE, "clean_table.csv"), index=False)

    tests = []
    for sig, d in clean.groupby("signal"):
        units = aggregate_units(d, METRICS, unit_col="unit")
        if "Linear" not in set(units.model):
            continue
        for m in METRICS:
            t = paired_vs_baseline(units, m, baseline="Linear", unit_col="unit")
            t["signal"] = sig
            tests.append(t)
    if tests:
        pd.concat(tests).to_csv(os.path.join(HERE, "paired_vs_linear.csv"), index=False)

    noise = load_paradigm("noise")
    if not noise.empty:
        seed_table(noise, ["signal", "condition"]).to_csv(os.path.join(HERE, "noise_curves.csv"), index=False)
    shift = load_paradigm("shift")
    if not shift.empty:
        seed_table(shift, ["signal", "condition"]).to_csv(os.path.join(HERE, "shift_curves.csv"), index=False)
    st = load_paradigm("state_transition")
    if not st.empty and "tag" in st.columns:
        st["tag_class"] = st.tag.str.replace(r"_d\d+", "", regex=True)
        st["dist"] = st.tag.str.extract(r"_d(\d+)")[0].astype(float)
        st["dist_bin"] = pd.cut(st.dist, [0, 5, 10, 20, 40, 100], include_lowest=True).astype(str)
        st.groupby(["model", "tag_class", "dist_bin"])[METRICS].agg(["mean", "count"]).to_csv(os.path.join(HERE, "state_transition_tags.csv"))

    acc = acceptance(clean, B)
    acc.to_csv(os.path.join(HERE, "acceptance_seed2021.csv"), index=False)
    if len(acc):
        print("acceptance: max |rel diff| per metric:", {k: float(acc[f"{k}_rel_diff"].abs().max()) for k in METRICS})

    # figure: clean bars with seed error bars
    fig, axes = plt.subplots(3, 3, figsize=(13, 9))
    for i, sig in enumerate(R.SIGNALS):
        for j, m in enumerate(METRICS):
            ax = axes[i, j]
            t = tab[tab.signal == sig].sort_values(f"{m}_mean")
            ax.bar(range(len(t)), t[f"{m}_mean"], yerr=t[f"{m}_std"].fillna(0), capsize=2,
                   color=[B["model_to_color"].get(x, GRAY) for x in t.model], edgecolor="black", lw=0.4)
            ax.set_xticks(range(len(t)))
            ax.set_xticklabels([B["display"].get(x, x) for x in t.model], rotation=60, ha="right", fontsize=6.5)
            title(ax, f"{R.SIGNAL_SHORT[sig]}: {m}", "mean over 20 test signals; error bar = SD over 3 seeds")
    fig.tight_layout()
    save(fig, os.path.join(HERE, "figures", "clean_bars"))
    print("done")


if __name__ == "__main__":
    main()
