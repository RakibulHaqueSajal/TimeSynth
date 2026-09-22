#!/usr/bin/env python3
"""
P3.2: fit the McSharry sum-of-Gaussians beat model to real MIT-BIH NSR beats.

McSharry et al. (IEEE TBME 2003) model the ECG on a limit cycle with angular
phase theta and five Gaussian events (P, Q, R, S, T). In phase coordinates the
steady-state waveform is

    z(theta) = sum_i  a_i * exp( -(theta - theta_i)^2 / (2 b_i^2) )  + z0

Here a_i is the event amplitude (mV), theta_i its angular position (rad, R at 0)
and b_i its angular width. Per record we build a mean beat template from the
annotated R peaks (RealData/download.py stores them), map beat time to phase
using the neighbouring RR intervals, and fit (a, theta, b) for the five events by
gradient descent in PyTorch with box constraints enforced through a sigmoid
reparameterization (the same approach as the repo's other parametric fits).

Output: ``tier2_ecg_fit.json`` with per-record parameters and the min/max
sampling ranges used by ``Synthetic_Signals_bio/tier2_ecg_dynamical.py``, plus a
PNG showing a real template next to its fit (figure for the Supplement, P3.6).

Usage: python Bio_Synthesize/Parametric_Fitting/tier2_ecg_fit.py
"""
from __future__ import annotations

import json
import os

import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(os.environ.get("TIMESYNTH_REAL",
                   "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_real"), "raw", "nsrdb")
OUT_JSON = os.path.join(HERE, "tier2_ecg_fit.json")
OUT_PNG = os.path.join(HERE, "tier2_ecg_fit.png")

WAVES = ["P", "Q", "R", "S", "T"]
# McSharry defaults as initialization and box centers: theta (rad), a (relative), b (rad)
INIT_THETA = np.array([-np.pi / 3, -np.pi / 12, 0.0, np.pi / 12, np.pi / 2])
INIT_A = np.array([0.075, -0.05, 0.30, -0.075, 0.12])      # a_i b_i^2 of the ODE form, scaled later
INIT_B = np.array([0.25, 0.10, 0.10, 0.10, 0.40])
# Boxes (lo, hi) per wave
BOX_THETA = np.array([[-1.5, -0.6], [-0.6, -0.08], [-0.08, 0.08], [0.08, 0.6], [0.9, 2.4]])
BOX_A = np.array([[0.0, 0.5], [-0.6, 0.0], [0.2, 3.0], [-1.5, 0.0], [0.0, 0.9]])
BOX_B = np.array([[0.08, 0.5], [0.03, 0.25], [0.03, 0.2], [0.03, 0.25], [0.15, 0.8]])


def beat_template(x, fs, beats, pre_s=0.35, post_s=0.55, max_beats=600):
    """Mean beat in PHASE coordinates: theta = 2*pi*(t - t_R)/RR_prev for t<t_R, /RR_next after."""
    beats = np.asarray(beats, int)
    beats = beats[(beats > int(pre_s * fs) + 1) & (beats < x.size - int(post_s * fs) - 1)]
    if beats.size < 10:
        return None
    sel = np.linspace(1, beats.size - 2, min(max_beats, beats.size - 2)).astype(int)
    theta_grid = np.linspace(-np.pi, np.pi, 400)
    acc = np.zeros_like(theta_grid)
    n = 0
    for k in sel:
        r, rp, rn = beats[k], beats[k - 1], beats[k + 1]
        rr_prev, rr_next = (r - rp) / fs, (rn - r) / fs
        if not (0.4 < rr_prev < 1.6 and 0.4 < rr_next < 1.6):
            continue
        a, b = r - int(0.5 * rr_prev * fs), r + int(0.5 * rr_next * fs)
        seg = x[a:b].astype(float)
        t = (np.arange(a, b) - r) / fs
        theta = np.where(t < 0, 2 * np.pi * t / rr_prev, 2 * np.pi * t / rr_next)
        seg = seg - np.median(seg)
        acc += np.interp(theta_grid, theta, seg)
        n += 1
    if n < 10:
        return None
    tpl = acc / n
    return theta_grid, tpl


def _box(u, lo, hi):
    return lo + (hi - lo) * torch.sigmoid(u)


def _inv_box(v, lo, hi):
    p = np.clip((v - lo) / (hi - lo), 1e-3, 1 - 1e-3)
    return np.log(p / (1 - p))


def fit_template(theta, z, iters=3000, lr=0.03, seed=0):
    torch.manual_seed(seed)
    th = torch.tensor(theta, dtype=torch.float64)
    zt = torch.tensor(z, dtype=torch.float64)
    scale = float(np.max(np.abs(z)))
    u_th = torch.tensor(_inv_box(INIT_THETA, BOX_THETA[:, 0], BOX_THETA[:, 1]), requires_grad=True)
    u_a = torch.tensor(_inv_box(INIT_A / 0.3 * scale, BOX_A[:, 0] * scale, BOX_A[:, 1] * scale), requires_grad=True)
    u_b = torch.tensor(_inv_box(INIT_B, BOX_B[:, 0], BOX_B[:, 1]), requires_grad=True)
    z0 = torch.zeros(1, dtype=torch.float64, requires_grad=True)
    lo_a, hi_a = torch.tensor(BOX_A[:, 0] * scale), torch.tensor(BOX_A[:, 1] * scale)
    lo_t, hi_t = torch.tensor(BOX_THETA[:, 0]), torch.tensor(BOX_THETA[:, 1])
    lo_b, hi_b = torch.tensor(BOX_B[:, 0]), torch.tensor(BOX_B[:, 1])
    opt = torch.optim.Adam([u_th, u_a, u_b, z0], lr=lr)

    def model():
        a, t0, b = _box(u_a, lo_a, hi_a), _box(u_th, lo_t, hi_t), _box(u_b, lo_b, hi_b)
        return (a[None, :] * torch.exp(-(th[:, None] - t0[None, :]) ** 2 / (2 * b[None, :] ** 2))).sum(1) + z0

    for _ in range(iters):
        opt.zero_grad()
        loss = torch.mean((model() - zt) ** 2)
        loss.backward()
        opt.step()
    with torch.no_grad():
        a, t0, b = _box(u_a, lo_a, hi_a), _box(u_th, lo_t, hi_t), _box(u_b, lo_b, hi_b)
        fit = model().numpy()
        r2 = 1 - np.sum((fit - z) ** 2) / np.sum((z - z.mean()) ** 2)
    return dict(a=a.numpy().tolist(), theta=t0.numpy().tolist(), b=b.numpy().tolist(),
                z0=float(z0.item()), r2=float(r2), scale=scale), fit


def main():
    recs = sorted(f for f in os.listdir(RAW) if f.endswith(".npz"))
    per_rec, examples = {}, []
    for f in recs:
        z = np.load(os.path.join(RAW, f))
        if "beats" not in z.files:
            continue
        tpl = beat_template(z["x"], float(z["fs"]), z["beats"])
        if tpl is None:
            continue
        theta, zt = tpl
        params, fit = fit_template(theta, zt)
        # normalize amplitudes by R amplitude so the ranges are shape parameters
        aR = params["a"][2]
        params["a_rel"] = [ai / aR for ai in params["a"]]
        params["R_amp"] = aR
        per_rec[f[:-4]] = params
        examples.append((f[:-4], theta, zt, fit))
        print(f"{f[:-4]}: R2={params['r2']:.3f} theta={np.round(params['theta'], 2)} a_rel={np.round(params['a_rel'], 2)}")
    keys = ["a_rel", "theta", "b"]
    ranges = {k: {"min": np.min([p[k] for p in per_rec.values()], axis=0).tolist(),
                  "max": np.max([p[k] for p in per_rec.values()], axis=0).tolist()} for k in keys}
    ranges["R_amp"] = {"min": float(np.min([p["R_amp"] for p in per_rec.values()])),
                       "max": float(np.max([p["R_amp"] for p in per_rec.values()]))}
    # RR statistics from annotations: mean HR and RR SD per record
    rr_stats = {}
    for f in recs:
        z = np.load(os.path.join(RAW, f))
        rr = np.diff(z["beats"]) / float(z["fs"])
        rr = rr[(rr > 0.4) & (rr < 1.6)]
        rr_stats[f[:-4]] = {"rr_mean_s": float(rr.mean()), "rr_sd_s": float(rr.std())}
    out = {"model": "z(theta) = sum_i a_i exp(-(theta-theta_i)^2/(2 b_i^2)) + z0; a in mV, theta rad, b rad",
           "waves": WAVES, "source": "MIT-BIH NSR (nsrdb), mean beat templates, PyTorch sigmoid-box fit",
           "per_record": per_rec, "ranges": ranges,
           "rr": {"mean_s": [min(v["rr_mean_s"] for v in rr_stats.values()), max(v["rr_mean_s"] for v in rr_stats.values())],
                  "sd_s": [min(v["rr_sd_s"] for v in rr_stats.values()), max(v["rr_sd_s"] for v in rr_stats.values())],
                  "per_record": rr_stats},
           "median_r2": float(np.median([p["r2"] for p in per_rec.values()]))}
    json.dump(out, open(OUT_JSON, "w"), indent=1)
    print("median R2", out["median_r2"], "->", OUT_JSON)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.2))
    for ax, (name, th, zt, fit) in zip(axes, examples[:3]):
        ax.plot(th, zt, color="#16356c", lw=1.4, label="MIT-BIH NSR mean beat")
        ax.plot(th, fit, color="#2a5fa0", lw=1.2, ls="--", label="5-Gaussian fit")
        ax.set_title(f"Record {name}", color="#16356c", fontweight="bold")
        ax.set_xlabel(r"$\theta$ (rad)")
        ax.set_ylabel("mV")
    axes[0].legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=200)
    fig.savefig(OUT_PNG.replace(".png", ".svg"))
    print("wrote", OUT_PNG)


if __name__ == "__main__":
    main()
