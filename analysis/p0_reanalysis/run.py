#!/usr/bin/env python3
"""
P0.4: cheap reanalysis of the paper's saved predictions (seed 2021, stride-1 windows).

Stage "metrics" computes per-window MAE, MSE, A_rms, phase error and frequency
error for every legacy result folder (clean, noise SNR 1-6, shift buckets 0-4;
12 models x 3 signals) and caches them under cache/ with the reconstructed
file_id of every window.

Stage "analyze" produces:
  1. dissociation_*.csv     sequence-level MAE-conditioned comparison of phase and
                            frequency error across bias groups (R1.4/R2.4)
  2. rank_correlation.csv   Kendall tau between the model ranking by MAE and by
                            phase / frequency error, bootstrap CI over test signals (R4.2/R4.3)
  3. signal_level_tests.csv paired tests vs Linear at the window level (paper) and
                            at the signal level, n = 20 (R4.6)
  SUMMARY.md                what survives

Run:  python analysis/p0_reanalysis/run.py --stage all
"""
from __future__ import annotations

import argparse
import itertools
import os
import sys
import warnings

import numpy as np
import pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, REPO)

from analysis import legacy_registry as R                    # noqa: E402
from utils import fidelity as F                              # noqa: E402
from utils.config import load_bias_groups                    # noqa: E402
from utils.results_io import legacy_file_ids, load_legacy    # noqa: E402

CACHE = os.path.join(HERE, "cache")
OUT = HERE
FS = 10.0
L = 50
SEQ_METRICS = ["mae", "phase", "freq"]
warnings.filterwarnings("ignore", category=RuntimeWarning)


# ---------------------------------------------------------------------------
# Stage 1: per-window metrics
# ---------------------------------------------------------------------------
def folder_list():
    """(paradigm, level, signal, model, folder, test_split_dir)"""
    out = []
    for sig in R.SIGNALS:
        for m in R.MODEL_ORDER:
            out.append(("clean", 0, sig, m, R.clean_folder(m, sig), R.test_split_dir("clean", sig)))
            for k in range(1, 7):
                out.append(("noise", k, sig, m, R.noise_folder(m, sig, k), R.test_split_dir("noise", sig, k)))
            for k in range(0, 5):
                out.append(("shift", k, sig, m, R.shift_folder(m, sig, k), R.test_split_dir("shift", sig, k)))
    return out


def cache_path(paradigm, level, signal, model):
    return os.path.join(CACHE, f"{paradigm}_{level}_{signal}_{model}.parquet")


def _one_folder(job):
    par, lvl, sig, m, folder, split_dir = job
    cp = cache_path(par, lvl, sig, m)
    hist, true, pred = load_legacy(folder, history_len=L)
    n = true.shape[0]
    meta = legacy_file_ids(n, split_dir, L, 100, batch_size=128, drop_last=True)
    tc = true - true.mean(axis=1, keepdims=True)
    df = pd.DataFrame({
        "paradigm": par, "level": lvl, "signal": sig, "model": m,
        "file_id": meta.file_id.values, "window_start": meta.window_start.values,
        "mae": F.mae(pred, true), "mse": F.mse(pred, true),
        "a_rms": np.sqrt(np.mean(tc ** 2, axis=1)),
        "phase": F.phase_error_deg(pred, true, unit="deg"),
        "freq": F.freq_error(pred, true, fs=FS),
    })
    df.to_parquet(cp, index=False)
    return (f"{par} L{lvl} {sig} {m}: n={n} mae={df.mae.mean():.4f} "
            f"phase={np.nanmean(df.phase):.2f} freq={np.nanmean(df.freq):.4f}")


def compute_metrics(force=False, workers=8):
    from multiprocessing import Pool
    os.makedirs(CACHE, exist_ok=True)
    todo, missing = [], []
    for job in folder_list():
        par, lvl, sig, m, folder, _ = job
        if os.path.exists(cache_path(par, lvl, sig, m)) and not force:
            continue
        if not os.path.exists(os.path.join(folder, "test_pred_with_history.npy")):
            missing.append(os.path.basename(folder))
            continue
        todo.append(job)
    print(f"{len(todo)} folders to compute", flush=True)
    with Pool(workers) as pool:
        for i, msg in enumerate(pool.imap_unordered(_one_folder, todo)):
            print(f"[{i + 1}/{len(todo)}] {msg}", flush=True)
    if missing:
        with open(os.path.join(OUT, "missing_folders.txt"), "w") as f:
            f.write("\n".join(missing) + "\n")
        print("missing folders:", missing)


def load_cached(paradigm, level=None, signals=None):
    frames = []
    for par, lvl, sig, m, _, _ in folder_list():
        if par != paradigm or (level is not None and lvl != level):
            continue
        if signals and sig not in signals:
            continue
        cp = cache_path(par, lvl, sig, m)
        if os.path.exists(cp):
            frames.append(pd.read_parquet(cp))
    return pd.concat(frames, ignore_index=True)


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def holm(p):
    p = np.asarray(p, float)
    n = len(p)
    order = np.argsort(p)
    adj = np.empty(n)
    running = 0.0
    for rank, idx in enumerate(order):
        val = (n - rank) * p[idx]
        running = max(running, val)
        adj[idx] = min(1.0, running)
    return adj


def kruskal_eps2(groups):
    """Kruskal-Wallis H, p, epsilon-squared effect size for a list of arrays."""
    groups = [np.asarray(g, float) for g in groups]
    groups = [g[np.isfinite(g)] for g in groups]
    groups = [g for g in groups if g.size >= 2]
    k = len(groups)
    n = sum(g.size for g in groups)
    if k < 2 or n <= k:
        return np.nan, np.nan, np.nan, k, n
    H, p = stats.kruskal(*groups)
    eps2 = (H - k + 1) / (n - k)
    return H, p, eps2, k, n


def per_file_means(df, metrics=SEQ_METRICS):
    """Average windows within each (model, file_id); NaN-aware."""
    return df.groupby(["model", "file_id"])[metrics].mean().reset_index()


def kendall_ci(pf, metric_a, metric_b, n_boot=2000, seed=0):
    """
    Kendall tau between model rankings by metric_a and metric_b, where a model's
    score is its mean over test files. Bootstrap CI resamples files.
    """
    wide_a = pf.pivot(index="file_id", columns="model", values=metric_a)
    wide_b = pf.pivot(index="file_id", columns="model", values=metric_b)
    models = [m for m in wide_a.columns if m in wide_b.columns]
    wide_a, wide_b = wide_a[models], wide_b[models]
    files = wide_a.index.values
    ra, rb = wide_a.mean(axis=0).values, wide_b.mean(axis=0).values
    tau, p = stats.kendalltau(ra, rb)
    rng = np.random.default_rng(seed)
    boots = []
    for _ in range(n_boot):
        idx = rng.integers(0, len(files), len(files))
        a = np.nanmean(wide_a.values[idx], axis=0)
        b = np.nanmean(wide_b.values[idx], axis=0)
        boots.append(stats.kendalltau(a, b)[0])
    boots = np.array(boots)
    lo, hi = np.nanpercentile(boots, [2.5, 97.5])
    # permutation test for tau > 0: permute model labels of metric_b
    perm = []
    for _ in range(n_boot):
        perm.append(stats.kendalltau(ra, rng.permutation(rb))[0])
    p_perm = float(np.mean(np.array(perm) >= tau))
    return tau, p, lo, hi, p_perm, len(models)


# ---------------------------------------------------------------------------
# Analysis 1: absolute-MAE dissociation (sequence level)
# ---------------------------------------------------------------------------
REL_BINS = [(0.0, 0.05), (0.05, 0.10), (0.10, 0.20), (0.20, np.inf)]


def dissociation(bias):
    df = load_cached("clean")
    df["group"] = df.model.map(bias["model_to_group"])
    df["rel_mae"] = df.mae / df.a_rms
    rows, rows_group = [], []

    def run_bin(sub, sig, scheme, lo, hi):
        for metric in ["phase", "freq"]:
            # window level (descriptive) and file level (inferential; units = model x file)
            g_win = [sub.loc[sub.group == g, metric].values for g in bias["groups"] if (sub.group == g).any()]
            H_w, p_w, e_w, k_w, n_w = kruskal_eps2(g_win)
            pf = sub.groupby(["group", "model", "file_id"])[metric].mean().reset_index()
            g_file = [pf.loc[pf.group == g, metric].values for g in bias["groups"] if (pf.group == g).any()]
            H_f, p_f, e_f, k_f, n_f = kruskal_eps2(g_file)
            rows.append(dict(signal=sig, scheme=scheme, bin_lo=lo, bin_hi=hi, metric=metric,
                             n_windows=n_w, n_groups=k_w, H_window=H_w, p_window=p_w, eps2_window=e_w,
                             n_model_file_units=n_f, H_file=H_f, p_file=p_f, eps2_file=e_f))
            for g in bias["groups"]:
                gs = sub.loc[sub.group == g, metric].dropna()
                gf = pf.loc[pf.group == g, metric].dropna()
                if gs.size == 0:
                    continue
                rows_group.append(dict(signal=sig, scheme=scheme, bin_lo=lo, bin_hi=hi, metric=metric,
                                       group=g, n_windows=int(gs.size), n_models=int(sub.loc[sub.group == g, "model"].nunique()),
                                       median=float(gs.median()), q25=float(gs.quantile(.25)), q75=float(gs.quantile(.75)),
                                       file_mean=float(gf.mean()), file_sd=float(gf.std(ddof=1)) if gf.size > 1 else np.nan))

    for sig in R.SIGNALS:
        d = df[df.signal == sig]
        for lo, hi in REL_BINS:
            run_bin(d[(d.rel_mae >= lo) & (d.rel_mae < hi)], sig, "rel_mae", lo, hi)
        run_bin(d[(d.mae >= 0) & (d.mae <= 0.03)], sig, "abs_mae_0_0.03", 0.0, 0.03)
    # pooled across signals
    for lo, hi in REL_BINS:
        run_bin(df[(df.rel_mae >= lo) & (df.rel_mae < hi)], "ALL", "rel_mae", lo, hi)
    run_bin(df[(df.mae >= 0) & (df.mae <= 0.03)], "ALL", "abs_mae_0_0.03", 0.0, 0.03)

    pd.DataFrame(rows).to_csv(os.path.join(OUT, "dissociation_tests.csv"), index=False)
    pd.DataFrame(rows_group).to_csv(os.path.join(OUT, "dissociation_groups.csv"), index=False)

    # bin occupancy per model: is the comparison actually matched?
    occ = (df.assign(bin=pd.cut(df.rel_mae, [b[0] for b in REL_BINS] + [np.inf], right=False))
             .groupby(["signal", "model", "bin"]).size().rename("n").reset_index())
    occ.to_csv(os.path.join(OUT, "dissociation_bin_occupancy.csv"), index=False)

    # Sensitivity: the paper's model-level slab (p20-p80 of model medians, Linear excluded),
    # with and without Autoformer.
    sens = []
    for sig in R.SIGNALS:
        d = df[df.signal == sig]
        med = d.groupby("model")[["mae", "phase", "freq"]].median()
        for variant, drop in [("with_Autoformer", ["Linear"]), ("without_Autoformer", ["Linear", "Autoformer"])]:
            mm = med.drop(index=[x for x in drop if x in med.index])
            lo, hi = np.percentile(mm.mae, [20, 80])
            inside = mm[(mm.mae >= lo) & (mm.mae <= hi)].copy()
            inside["group"] = inside.index.map(bias["model_to_group"])
            fam = inside.groupby("group")[["phase", "freq"]].mean()
            for metric in ["phase", "freq"]:
                sens.append(dict(signal=sig, variant=variant, metric=metric, slab_lo=lo, slab_hi=hi,
                                 n_models_inside=len(inside), models_inside=";".join(inside.index),
                                 **{f"{g}": fam.loc[g, metric] if g in fam.index else np.nan for g in bias["groups"]},
                                 top_minus_bottom=(fam[metric].max() - fam[metric].min()) if len(fam) else np.nan))
    pd.DataFrame(sens).to_csv(os.path.join(OUT, "dissociation_model_level_sensitivity.csv"), index=False)
    return pd.DataFrame(rows), pd.DataFrame(rows_group), pd.DataFrame(sens), occ


# ---------------------------------------------------------------------------
# Analysis 2: rank correlation between MAE and fidelity rankings
# ---------------------------------------------------------------------------
def rank_correlation():
    rows = []
    for par, levels in [("clean", [0]), ("noise", range(1, 7)), ("shift", range(0, 5))]:
        for lvl in levels:
            df = load_cached(par, lvl)
            for sig in R.SIGNALS:
                pf = per_file_means(df[df.signal == sig])
                for fid in ["phase", "freq"]:
                    tau, p, lo, hi, p_perm, k = kendall_ci(pf, "mae", fid)
                    rows.append(dict(paradigm=par, level=lvl, signal=sig, fidelity=fid, n_models=k,
                                     tau=tau, p_value=p, ci_lo=lo, ci_hi=hi, p_perm_gt0=p_perm))
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(OUT, "rank_correlation.csv"), index=False)
    return out


# ---------------------------------------------------------------------------
# Analysis 3: window-level vs signal-level paired tests vs Linear
# ---------------------------------------------------------------------------
def signal_level_tests(bias, baseline="Linear"):
    from Statistical_Test.clean import paired_ttest_normal_approx  # the paper's window-level test
    df = load_cached("clean")
    rows = []
    rng = np.random.default_rng(0)
    for sig in R.SIGNALS:
        d = df[df.signal == sig]
        wide = {m: d[d.model == m].set_index(["file_id", "window_start"]) for m in R.MODEL_ORDER}
        for metric in SEQ_METRICS:
            # intersection-valid windows across all models (as in clean.py)
            valid = None
            for m, w in wide.items():
                v = w[metric].notna()
                valid = v if valid is None else (valid & v.reindex(valid.index).fillna(False))
            idx = valid[valid].index
            base = wide[baseline].loc[idx, metric].values
            base_file = wide[baseline].loc[idx, metric].groupby(level=0).mean()
            pw, pf = [], []
            recs = []
            for m in R.MODEL_ORDER:
                if m == baseline:
                    continue
                x = wide[m].loc[idx, metric].values
                dwin = x - base
                _, p_win = paired_ttest_normal_approx(dwin)
                xf = wide[m].loc[idx, metric].groupby(level=0).mean()
                dfile = (xf - base_file).values
                n_f = dfile.size
                try:
                    p_file = stats.wilcoxon(dfile, zero_method="wilcox", alternative="two-sided").pvalue
                except ValueError:
                    p_file = np.nan
                boots = [np.mean(dfile[rng.integers(0, n_f, n_f)]) for _ in range(2000)]
                lo, hi = np.percentile(boots, [2.5, 97.5])
                # Cohen's d on paired file-level differences
                dz = dfile.mean() / dfile.std(ddof=1) if n_f > 1 and dfile.std(ddof=1) > 0 else np.nan
                recs.append(dict(signal=sig, metric=metric, model=m, group=bias["model_to_group"].get(m),
                                 n_windows=int(dwin.size), n_files=int(n_f),
                                 mean_delta=float(dfile.mean()), ci_lo=lo, ci_hi=hi, cohen_dz=dz,
                                 p_window=p_win, p_file=p_file))
                pw.append(p_win)
                pf.append(p_file)
            pw_h, pf_h = holm(pw), holm(np.nan_to_num(pf, nan=1.0))
            for r, a, b in zip(recs, pw_h, pf_h):
                r["p_window_holm"] = a
                r["p_file_holm"] = b
                r["sig_window"] = a < 0.05
                r["sig_file"] = b < 0.05
                r["direction"] = "better" if r["mean_delta"] < 0 else "worse"
                r["survives"] = bool(r["sig_window"] and r["sig_file"])
                rows.append(r)
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(OUT, "signal_level_tests.csv"), index=False)
    return out


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
def write_summary(bias, diss_tests, diss_groups, sens, occ, rc, slt):
    lines = ["# P0.4 reanalysis of the paper's predictions (seed 2021)", ""]
    lines += ["Inputs: `Train_Test_Validation/` legacy folders, 12 models x 3 signals; clean (Shift_0), ",
              "noise SNR 1-6, shift buckets 0-4. Window `file_id` reconstructed from the CSV lengths ",
              "(`utils.results_io.legacy_file_ids`, verified against the saved array sizes). Bias groups from ",
              "`configs/bias_groups.yaml` (D4 recommended placement).", ""]

    # ---- 1
    lines += ["## 1. Absolute-MAE dissociation at the sequence level (R1.4 / R2.4)", ""]
    lines += ["Windows from all models pooled and binned by `MAE / A_rms(true)`; inside each bin, Kruskal-Wallis ",
              "across bias groups on phase error (deg) and frequency error (Hz). `eps2` is epsilon-squared. ",
              "Window-level p-values treat overlapping windows as independent (they are not); the file-level ",
              "test averages windows within each (model, test signal) first and is the one to quote.", ""]
    t = diss_tests[diss_tests.scheme == "rel_mae"]
    lines += ["| signal | bin (rel. MAE) | metric | n windows | eps2 (window) | units (model x file) | p (file) | eps2 (file) |",
              "|---|---|---|---|---|---|---|---|"]
    for _, r in t.iterrows():
        hi = "inf" if not np.isfinite(r.bin_hi) else f"{r.bin_hi:.2f}"
        lines.append(f"| {R.SIGNAL_SHORT.get(r.signal, r.signal)} | [{r.bin_lo:.2f}, {hi}) | {r.metric} | {int(r.n_windows)} | "
                     f"{r.eps2_window:.3f} | {int(r.n_model_file_units)} | {r.p_file:.2e} | {r.eps2_file:.3f} |")
    lines += ["", "Group medians (window level) inside each bin:", ""]
    g = diss_groups[(diss_groups.scheme == "rel_mae")]
    for sig in list(R.SIGNALS) + ["ALL"]:
        gs = g[g.signal == sig]
        if gs.empty:
            continue
        lines += [f"**{R.SIGNAL_SHORT.get(sig, sig)}**", "",
                  "| bin | metric | " + " | ".join(bias["groups"]) + " |", "|---|---|" + "---|" * len(bias["groups"])]
        for (lo, hi_, metric), sub in gs.groupby(["bin_lo", "bin_hi", "metric"]):
            hi = "inf" if not np.isfinite(hi_) else f"{hi_:.2f}"
            cells = []
            for grp in bias["groups"]:
                s = sub[sub.group == grp]
                cells.append(f"{s['median'].values[0]:.3g} (n={int(s.n_windows.values[0])}, {int(s.n_models.values[0])} models)" if len(s) else "-")
            lines.append(f"| [{lo:.2f}, {hi}) | {metric} | " + " | ".join(cells) + " |")
        lines.append("")
    t2 = diss_tests[diss_tests.scheme == "abs_mae_0_0.03"]
    lines += ["Reviewers' absolute window, MAE in [0, 0.03]:", "",
              "| signal | metric | n windows | p (file) | eps2 (file) |", "|---|---|---|---|---|"]
    for _, r in t2.iterrows():
        lines.append(f"| {R.SIGNAL_SHORT.get(r.signal, r.signal)} | {r.metric} | {int(r.n_windows)} | {r.p_file:.2e} | {r.eps2_file:.3f} |")
    lines += ["", "Sensitivity, the paper's model-level slab (p20-p80 of model-median MAE, Linear excluded):", "",
              "| signal | variant | metric | models inside | " + " | ".join(bias["groups"]) + " | top - bottom |",
              "|---|---|---|---|" + "---|" * len(bias["groups"]) + "---|"]
    for _, r in sens.iterrows():
        cells = " | ".join("-" if pd.isna(r[grp]) else f"{r[grp]:.3g}" for grp in bias["groups"])
        lines.append(f"| {R.SIGNAL_SHORT[r.signal]} | {r.variant} | {r.metric} | {r.n_models_inside} | {cells} | {r.top_minus_bottom:.3g} |")
    lines.append("")
    # occupancy warning
    occ_w = occ.pivot_table(index=["signal", "model"], columns="bin", values="n", fill_value=0)
    lines += ["Bin occupancy per model (windows). A bias-group comparison inside a bin is only as good as its ",
              "coverage; models absent from a bin contribute nothing there.", "", "```",
              occ_w.to_string(), "```", ""]

    # ---- 2
    lines += ["## 2. Rank-correlation headline (R4.2 / R4.3)", "",
              "Kendall tau between the 12-model ranking by mean MAE and by mean phase / frequency error; ",
              "means over 20 test signals; bootstrap 95% CI over test signals; permutation p for tau > 0. ",
              "tau near 1 means MAE already orders models the way fidelity does; low or negative tau is the ",
              "quantitative form of the 'MAE is insufficient' claim.", "",
              "Shift levels are frequency buckets relative to training (-2, -1, in-dist, +1, +2); "
              "shift/in-dist is the same run as clean.", "",
              "| paradigm | level | signal | fidelity | tau | 95% CI | perm p (tau>0) |", "|---|---|---|---|---|---|---|"]
    for _, r in rc.iterrows():
        lvl = R.SHIFT_LEVEL_LABEL[int(r.level)] if r.paradigm == "shift" else (f"SNR_{int(r.level)}" if r.paradigm == "noise" else "-")
        lines.append(f"| {r.paradigm} | {lvl} | {R.SIGNAL_SHORT[r.signal]} | {r.fidelity} | {r.tau:.2f} | "
                     f"[{r.ci_lo:.2f}, {r.ci_hi:.2f}] | {r.p_perm_gt0:.3f} |")
    lines.append("")
    summ = rc.groupby(["paradigm", "fidelity"]).tau.agg(["mean", "min", "max"]).reset_index()
    lines += ["Per paradigm: mean / min / max tau", "", summ.to_string(index=False), ""]

    # ---- 3
    lines += ["## 3. Window-level versus signal-level statistics (R4.6)", "",
              "Paired comparison of every model against Linear on the clean paradigm. `window`: the paper's ",
              "paired test on ~57k overlapping windows (normal approximation). `file`: Wilcoxon signed-rank on ",
              "n = 20 per-signal means. Holm correction within (signal, metric). `survives` = significant in both.", ""]
    for sig in R.SIGNALS:
        s = slt[slt.signal == sig]
        lines += [f"**{R.SIGNAL_SHORT[sig]}**", "",
                  "| metric | model | group | mean delta vs Linear [95% CI] | dz | p window (Holm) | p file (Holm) | survives |",
                  "|---|---|---|---|---|---|---|---|"]
        for _, r in s.sort_values(["metric", "mean_delta"]).iterrows():
            lines.append(f"| {r.metric} | {r.model} | {r.group} | {r.mean_delta:+.4g} [{r.ci_lo:+.3g}, {r.ci_hi:+.3g}] | "
                         f"{r.cohen_dz:.2f} | {r.p_window_holm:.1e} | {r.p_file_holm:.3f} | "
                         f"{'yes' if r.survives else ('no' if r.sig_window else 'n.s. at window level')} |")
        lines.append("")
    n_win = int(slt.sig_window.sum())
    n_both = int(slt.survives.sum())
    lost = slt[slt.sig_window & ~slt.sig_file]
    lines += [f"Of {len(slt)} model-vs-Linear comparisons, {n_win} were significant at the window level and "
              f"{n_both} remain significant at the signal level (n = 20).", ""]
    if len(lost):
        lines += ["Comparisons that lose significance at the signal level:", ""]
        for _, r in lost.iterrows():
            lines.append(f"- {R.SIGNAL_SHORT[r.signal]} / {r.metric}: {r.model} ({r.direction}, delta {r.mean_delta:+.3g}, p_file {r.p_file_holm:.3f})")
        lines.append("")
    # locality claim: local group vs others at the file level
    lines += ["### Locality advantage at the signal level", ""]
    for metric in SEQ_METRICS:
        s = slt[slt.metric == metric]
        loc = s[s.group == "Local receptive field"]
        lines.append(f"- {metric}: local-group models better than Linear and significant at file level in "
                     f"{int((loc.survives & (loc.direction == 'better')).sum())}/{len(loc)} (signal, model) cells; "
                     f"non-local: {int((s[s.group != 'Local receptive field'].survives & (s[s.group != 'Local receptive field'].direction == 'better')).sum())}"
                     f"/{len(s[s.group != 'Local receptive field'])}.")
    lines.append("")

    lines += ["## Notes", "",
              "- `Statistical_Test/shift.py` registered the SPM FITS run under Drift_Harmonic; fixed in the ",
              "  revision branch. The paper's Fig. 5 FITS curve for Drift_Harmonic should be regenerated.",
              "- One legacy folder is missing: ModernTCN / Drift_Harmonic / SNR_Level_4 (the paper had the same gap).",
              "- All numbers here are seed 2021 only; Phase 2 adds seeds 2022 and 2023.", ""]
    with open(os.path.join(OUT, "SUMMARY.md"), "w") as f:
        f.write("\n".join(lines))
    print("wrote", os.path.join(OUT, "SUMMARY.md"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["metrics", "analyze", "all"], default="all")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    if a.stage in ("metrics", "all"):
        compute_metrics(force=a.force, workers=a.workers)
    if a.stage in ("analyze", "all"):
        bias = load_bias_groups()
        diss_tests, diss_groups, sens, occ = dissociation(bias)
        rc = rank_correlation()
        slt = signal_level_tests(bias)
        write_summary(bias, diss_tests, diss_groups, sens, occ, rc, slt)


if __name__ == "__main__":
    main()
