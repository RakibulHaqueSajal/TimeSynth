#!/usr/bin/env python3
"""
Supplementary table for the MAE-vs-fidelity dissociation figure.

For each signal family and each fidelity metric (phase / frequency),
reports the comparable-MAE window (central 60 % of MAE values, p20-p80)
and the mean fidelity error of each architecture family *inside* that
window. The Δ column is the gap between the highest and lowest family
mean — the dissociation the red arrow marks in the figure.

Outputs:
  <OUT_DIR>/dissociation_comparable_mae.tex
  <OUT_DIR>/dissociation_comparable_mae.csv
"""

import os
import csv
from typing import Dict, List, Tuple

import numpy as np

import dissociation as d


SIGNAL_LABELS: List[Tuple[str, str]] = [
    ("Drift_Harmonic",          "Drift Harmonic"),
    ("Single_Phase_Modulation", "Single-Phase Modulation"),
    ("Dual_Phase_Modulation",   "Dual-Phase Modulation"),
]

FAMILY_ORDER = ["CNN", "MLP", "Linear-family", "Transformer"]


def _slab_family_stats(model_data: Dict[str, Tuple[float, float]]):
    """Return (x_lo, x_hi, {family: (n, mean, members)}) for one panel."""
    by_fam: Dict[str, List[Tuple[str, float, float]]] = {}
    for m, (x, y) in model_data.items():
        fam = d.MODEL_FAMILIES.get(m, "Baseline")
        if fam == "Baseline":
            continue
        by_fam.setdefault(fam, []).append((m, x, y))

    xs = [x for pts in by_fam.values() for _, x, _ in pts]
    x_lo = float(np.percentile(xs, 20))
    x_hi = float(np.percentile(xs, 80))

    fam_stats: Dict[str, Tuple[int, float, List[str]]] = {}
    for fam, pts in by_fam.items():
        inside = [(m, y) for m, x, y in pts if x_lo <= x <= x_hi]
        if inside:
            ys = [y for _, y in inside]
            fam_stats[fam] = (len(inside), float(np.mean(ys)),
                              [m for m, _ in inside])
    return x_lo, x_hi, fam_stats


def _fmt(val: float, unit: str) -> str:
    if unit == "deg":
        return f"{val:.2f}"
    # Hz: 4 decimals for small values, 3 otherwise
    return f"{val:.4f}" if val < 0.1 else f"{val:.3f}"


def _row_delta(fam_stats, unit):
    means = [m for _, m, _ in fam_stats.values()]
    if not means:
        return None
    return max(means) - min(means)


def build_csv(csv_path: str):
    with open(csv_path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow([
            "metric", "signal", "slab_lo", "slab_hi",
            "CNN_n", "CNN_mean",
            "MLP_n", "MLP_mean",
            "Linear-family_n", "Linear-family_mean",
            "Transformer_n", "Transformer_mean",
            "Delta",
        ])
        for metric_name, loader, unit in [
            ("phase_deg", d.load_raw_medians, "deg"),
            ("freq_Hz",   d.load_raw_medians_mae_freq, "Hz"),
        ]:
            raw = loader()
            for sig_key, sig_lbl in SIGNAL_LABELS:
                x_lo, x_hi, fs = _slab_family_stats(raw[sig_key])
                delta = _row_delta(fs, unit)
                row = [metric_name, sig_lbl,
                       f"{x_lo:.4f}", f"{x_hi:.4f}"]
                for fam in FAMILY_ORDER:
                    if fam in fs:
                        n, mean, _ = fs[fam]
                        row += [n, _fmt(mean, unit)]
                    else:
                        row += ["", ""]
                row += [_fmt(delta, unit) if delta is not None else ""]
                w.writerow(row)


def build_latex(tex_path: str):
    lines: List[str] = []
    lines.append(r"\begin{table}[t]")
    lines.append(r"\centering")
    lines.append(r"\caption{\textbf{Family-level fidelity at comparable MAE.} "
                 r"For each signal family and each fidelity metric, the "
                 r"\emph{comparable-MAE window} is the central 60\,\% of "
                 r"MAE values across the full model set (20th--80th "
                 r"percentile). Entries are the mean fidelity error of "
                 r"each architecture family over the models whose MAE "
                 r"falls inside that window, with the per-family count "
                 r"in parentheses. $\Delta$ is the gap between the "
                 r"highest and lowest family mean in that row and "
                 r"corresponds to the red arrow in "
                 r"Fig.~\ref{fig:dissociation}. Linear-family models "
                 r"account for the upper extreme of both metrics in all "
                 r"three signal families.}")
    lines.append(r"\label{tab:comparable_mae_dissociation}")
    lines.append(r"\small")
    lines.append(r"\begin{tabular}{llcccccc}")
    lines.append(r"\toprule")
    lines.append(r"Metric & Signal family & MAE window "
                 r"& CNN & MLP & Linear-family & Transformer & $\Delta$ \\")
    lines.append(r"\midrule")

    for metric_name, loader, unit, unit_latex in [
        ("Phase error ($^\\circ$)", d.load_raw_medians, "deg", r"$^{\circ}$"),
        ("Frequency error (Hz)",    d.load_raw_medians_mae_freq, "Hz", r"~Hz"),
    ]:
        raw = loader()
        for i, (sig_key, sig_lbl) in enumerate(SIGNAL_LABELS):
            x_lo, x_hi, fs = _slab_family_stats(raw[sig_key])
            delta = _row_delta(fs, unit)

            if i == 0:
                metric_cell = metric_name
            else:
                metric_cell = ""

            cells: List[str] = []
            for fam in FAMILY_ORDER:
                if fam in fs:
                    n, mean, _ = fs[fam]
                    cells.append(f"{_fmt(mean, unit)} ({n})")
                else:
                    cells.append(r"---")

            delta_cell = _fmt(delta, unit) if delta is not None else "---"
            window_cell = f"[{x_lo:.3f},\\,{x_hi:.3f}]"

            lines.append(
                f"{metric_cell} & {sig_lbl} & {window_cell} & "
                + " & ".join(cells)
                + f" & {delta_cell} \\\\"
            )
        lines.append(r"\midrule")

    # Replace the last \midrule with \bottomrule.
    lines[-1] = r"\bottomrule"
    lines.append(r"\end{tabular}")
    lines.append(r"\end{table}")

    with open(tex_path, "w") as fh:
        fh.write("\n".join(lines) + "\n")


def main():
    out_dir = d.OUT_DIR
    os.makedirs(out_dir, exist_ok=True)
    tex_path = os.path.join(out_dir, "dissociation_comparable_mae.tex")
    csv_path = os.path.join(out_dir, "dissociation_comparable_mae.csv")

    build_csv(csv_path)
    build_latex(tex_path)

    print(f"Saved: {tex_path}")
    print(f"Saved: {csv_path}")


if __name__ == "__main__":
    main()
