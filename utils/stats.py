"""
Statistics for the revision (REVISION_PLAN.md Phase 5, R4.6).

Unit of analysis: the test signal (synthetic) or the subject (real data). All
windows of a unit are averaged first; seeds are averaged into the unit-level
value unless a seed effect is requested explicitly.

Functions
---------
aggregate_units     window table -> one row per (model, unit[, seed]) with metric means
paired_vs_baseline  Wilcoxon signed-rank of every model against a baseline over units,
                    Holm within the call, bootstrap 95% CI of the mean difference, dz
kendall_tau_ci      rank agreement between two model orderings with bootstrap over units
mixed_model_check   metric ~ model + (1|unit) + (1|seed) via statsmodels MixedLM (sensitivity)
holm                Holm step-down adjustment
sample_size_table   per paradigm: units, windows per unit, stride, overlap fraction, seeds, test
"""
from __future__ import annotations

from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
from scipy import stats


def holm(p: Sequence[float]) -> np.ndarray:
    p = np.asarray(p, float)
    n = p.size
    order = np.argsort(p)
    adj = np.empty(n)
    running = 0.0
    for rank, idx in enumerate(order):
        running = max(running, (n - rank) * p[idx])
        adj[idx] = min(1.0, running)
    return adj


def aggregate_units(df: pd.DataFrame, metrics: Iterable[str], unit_col: str = "unit",
                    keep_seed: bool = False) -> pd.DataFrame:
    """
    ``df`` has one row per window with columns model, seed, <unit_col> and the
    metrics (NaN allowed). Returns the mean per (model, unit) after averaging
    within seed, or per (model, unit, seed) if ``keep_seed``.
    """
    metrics = list(metrics)
    per_seed = df.groupby(["model", unit_col, "seed"])[metrics].mean().reset_index()
    if keep_seed:
        return per_seed
    return per_seed.groupby(["model", unit_col])[metrics].mean().reset_index()


def _boot_mean_ci(d: np.ndarray, n_boot: int, rng) -> Tuple[float, float]:
    idx = rng.integers(0, d.size, (n_boot, d.size))
    m = d[idx].mean(axis=1)
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def paired_vs_baseline(units: pd.DataFrame, metric: str, baseline: str = "Linear",
                       unit_col: str = "unit", n_boot: int = 2000, seed: int = 0,
                       models: Optional[List[str]] = None) -> pd.DataFrame:
    """
    For each model m != baseline: d_i = metric(m, unit i) - metric(baseline, unit i)
    over units where both are finite. Wilcoxon signed-rank (two-sided, exact for
    small n), Holm across models, bootstrap 95% CI over units, paired Cohen dz.
    """
    rng = np.random.default_rng(seed)
    wide = units.pivot(index=unit_col, columns="model", values=metric)
    if baseline not in wide.columns:
        raise KeyError(f"baseline {baseline} not in table")
    rows = []
    for m in (models or [c for c in wide.columns if c != baseline]):
        if m not in wide.columns:
            continue
        pair = wide[[m, baseline]].dropna()
        d = (pair[m] - pair[baseline]).values
        n = d.size
        if n < 5:
            rows.append(dict(model=m, metric=metric, n_units=n, mean_delta=np.nan, ci_lo=np.nan, ci_hi=np.nan,
                             dz=np.nan, p=np.nan))
            continue
        try:
            p = stats.wilcoxon(d, zero_method="wilcox", alternative="two-sided").pvalue if np.any(d != 0) else 1.0
        except ValueError:
            p = np.nan
        lo, hi = _boot_mean_ci(d, n_boot, rng)
        sd = d.std(ddof=1)
        rows.append(dict(model=m, metric=metric, n_units=int(n), mean_delta=float(d.mean()), ci_lo=lo, ci_hi=hi,
                         dz=float(d.mean() / sd) if sd > 0 else np.nan, p=float(p),
                         median_delta=float(np.median(d))))
    out = pd.DataFrame(rows)
    if len(out):
        pv = out.p.fillna(1.0).values
        out["p_holm"] = holm(pv)
        out["significant"] = out.p_holm < 0.05
        out["direction"] = np.where(out.mean_delta < 0, "better", "worse")
    return out


def kendall_tau_ci(units: pd.DataFrame, metric_a: str, metric_b: str, unit_col: str = "unit",
                   n_boot: int = 2000, seed: int = 0) -> Dict[str, float]:
    """
    Kendall tau between the model ordering by mean metric_a and by mean metric_b
    (means over units), bootstrap CI resampling units, permutation p for tau > 0.
    """
    rng = np.random.default_rng(seed)
    wa = units.pivot(index=unit_col, columns="model", values=metric_a)
    wb = units.pivot(index=unit_col, columns="model", values=metric_b)
    models = [m for m in wa.columns if m in wb.columns]
    wa, wb = wa[models].values, wb[models].values
    ra, rb = np.nanmean(wa, axis=0), np.nanmean(wb, axis=0)
    tau, p = stats.kendalltau(ra, rb)
    n = wa.shape[0]
    boots = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        boots.append(stats.kendalltau(np.nanmean(wa[idx], axis=0), np.nanmean(wb[idx], axis=0))[0])
    perm = [stats.kendalltau(ra, rng.permutation(rb))[0] for _ in range(n_boot)]
    return dict(tau=float(tau), p_value=float(p), ci_lo=float(np.nanpercentile(boots, 2.5)),
                ci_hi=float(np.nanpercentile(boots, 97.5)), p_perm_gt0=float(np.mean(np.array(perm) >= tau)),
                n_models=len(models), n_units=int(n))


def rank_transfer(units_syn: pd.DataFrame, units_real: pd.DataFrame, metric: str, unit_col: str = "unit",
                  n_boot: int = 2000, seed: int = 0) -> Dict[str, float]:
    """
    P1.6: Kendall tau and Spearman rho between the model ranking on a synthetic
    family and on a real dataset, for one metric; bootstrap resamples synthetic
    units and real units independently; permutation p for tau > 0.
    """
    rng = np.random.default_rng(seed)
    ws = units_syn.pivot(index=unit_col, columns="model", values=metric)
    wr = units_real.pivot(index=unit_col, columns="model", values=metric)
    models = [m for m in ws.columns if m in wr.columns]
    ws, wr = ws[models].values, wr[models].values
    rs, rr = np.nanmean(ws, axis=0), np.nanmean(wr, axis=0)
    tau, p_t = stats.kendalltau(rs, rr)
    rho, p_r = stats.spearmanr(rs, rr)
    boots = []
    for _ in range(n_boot):
        i = rng.integers(0, ws.shape[0], ws.shape[0])
        j = rng.integers(0, wr.shape[0], wr.shape[0])
        boots.append(stats.kendalltau(np.nanmean(ws[i], axis=0), np.nanmean(wr[j], axis=0))[0])
    perm = [stats.kendalltau(rs, rng.permutation(rr))[0] for _ in range(n_boot)]
    return dict(tau=float(tau), tau_ci_lo=float(np.nanpercentile(boots, 2.5)), tau_ci_hi=float(np.nanpercentile(boots, 97.5)),
                p_perm_gt0=float(np.mean(np.array(perm) >= tau)), rho=float(rho), rho_p=float(p_r),
                n_models=len(models), models=models, rank_syn=rs.tolist(), rank_real=rr.tolist())


def mixed_model_check(per_seed_units: pd.DataFrame, metric: str, baseline: str = "Linear",
                      unit_col: str = "unit") -> Optional[pd.DataFrame]:
    """
    Sensitivity check: metric ~ C(model) with random intercepts for unit and for
    seed (variance component). Returns the fixed-effect table (model vs baseline)
    or None if the fit fails.
    """
    try:
        import statsmodels.formula.api as smf
    except ImportError:
        return None
    d = per_seed_units.dropna(subset=[metric]).copy()
    d["model"] = pd.Categorical(d["model"], categories=[baseline] + sorted(set(d.model) - {baseline}))
    d["seed"] = d["seed"].astype(str)
    try:
        md = smf.mixedlm(f"{metric} ~ C(model)", d, groups=d[unit_col], re_formula="1",
                         vc_formula={"seed": "0 + C(seed)"})
        fit = md.fit(reml=True, method="lbfgs", maxiter=500)
    except Exception:
        return None
    tab = fit.summary().tables[1]
    tab = tab.reset_index().rename(columns={"index": "term"})
    return tab[tab.term.str.startswith("C(model)")]


def sample_size_table(meta_frames: Dict[str, pd.DataFrame], test_name: str = "Wilcoxon signed-rank over units, Holm") -> pd.DataFrame:
    """
    One row per paradigm from the meta.parquet tables: number of units, windows
    per unit, stride, overlap fraction, seeds, and the test used.
    """
    rows = []
    for name, m in meta_frames.items():
        unit = m["unit"] if "unit" in m.columns else m["file_id"]
        L = int(m.seq_len.iloc[0] + m.pred_len.iloc[0])
        stride = int(m.eval_stride.iloc[0])
        rows.append(dict(paradigm=name, n_units=int(unit.nunique()),
                         windows_per_unit=float(m.groupby(unit).size().mean()),
                         window_stride=stride, overlap_fraction=max(0.0, 1.0 - stride / L),
                         n_seeds=int(m.seed.nunique()), test=test_name))
    return pd.DataFrame(rows)
