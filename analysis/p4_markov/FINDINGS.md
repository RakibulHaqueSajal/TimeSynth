# Phase 4: redesigned Markov paradigm, findings

Written for: Rakib, as input to Q4 of the Results and to the replies to R3.2 to R3.5 and R4.7.

Complete: 135 evaluations, 15 models x 3 dwell times x 3 seeds, on the regenerated paradigm
(`PhaseMod_Markov_Dwell`, pooled training over D, tested per D). TimesNet is absent because its
training job exceeded the wall clock.

## What changed from the paper

| | paper | revision |
|---|---|---|
| switching | `P(switch) = p` at every sample; at 10 Hz with p = 0.5 the mean dwell is 0.2 s, shorter than one carrier cycle | expected dwell `D` in seconds, `p = 1/(fs D)`, D in {2, 5, 10} s |
| training | one model per `p` | one model pooled over all D, tested per D (R3.3) |
| divergence metric | 1-D Gaussian KL on decoded switching rates | symmetrized transition-matrix KL rate between the chain fitted to the true futures and the chain fitted to the predicted futures, plus mean dwell error (R3.5) |
| multiple futures | not available | K = 20 independent continuations saved per test window (R3.2) |

## The main result: the models with the best MAE almost never switch state

At D = 10 s (the probe measures a true dwell of 11.2 s on the true futures):

| model | MAE | phase | KL rate | predicted dwell | time between bands |
|---|---|---|---|---|---|
| MICN Mean | **0.051** | 45.1 | 0.038 | 44.7 s | 0.288 |
| PatchTST | 0.053 | **43.6** | 0.108 | **292.8 s** | 0.289 |
| TSMixer | 0.052 | 45.2 | 0.067 | 93.6 s | 0.278 |
| NBeats | 0.052 | 46.1 | 0.066 | 89.9 s | 0.296 |
| Transformer | 0.053 | 49.2 | 0.021 | 28.7 s | 0.319 |
| Linear | 0.061 | 62.6 | **0.005** | **8.2 s** | 0.232 |
| **truth** | - | - | 0 | **11.2 s** | **0.358** |

PatchTST has the best phase error of any model and a predicted dwell time 26 times too long: its
forecasts essentially never switch state. The same holds at D = 2 s, where the true dwell is 3.1 s
and PatchTST predicts 29.6 s, a factor of 10. The ordering by MAE and the ordering by switching
fidelity are close to opposite: the five best models by MAE occupy five of the six worst KL rates
at D = 2 s, while the linear family and the linear family reproduce the switching
statistics best.

This is the answer to R4.7. A deterministic model minimizes expected pointwise error on a
stochastic switching task by refusing to commit to a state, which produces a smooth forecast with
almost no transitions. MAE rewards exactly that behavior, and only a metric defined on the
switching process exposes it.

## The probabilistic baseline does not fix it, in our implementation

CSDI's per-sample switching statistics are not better: its predicted dwell is 5.1 to 5.3 s
regardless of whether the true dwell is 3.1 or 11.2 s, so it switches at a roughly fixed rate
rather than inferring the rate from the history, and its samples spend more time between the two
frequency bands (0.51 to 0.55) than the true futures do (0.36 to 0.69). Individual samples are
therefore also failing to commit to a state.

This should be reported as a negative result with its caveat: CSDI's dispersion problem is
documented in `analysis/OPEN_ISSUES.md` item 1, and it was not retrained after that was found. The
honest claim is that a diffusion baseline trained under the same protocol does not recover the
switching statistics, not that probabilistic forecasting cannot.

## Two measurement caveats to state in the text

1. The HMM probe measures the true dwell as 3.1, 6.0 and 11.2 s for nominal D of 2, 5 and 10 s.
   The probe decodes windowed features with a hop of 0.8 s, so it cannot resolve dwells close to
   its own hop and reports them as longer. Comparisons between predicted and true dwell are
   therefore internally consistent, since both pass through the same probe, but the absolute
   values are biased upward for short dwells.
2. The regression-to-the-mean metric must not use the probe's 16-sample Welch windows. At 10 Hz
   that gives a frequency resolution of 0.625 Hz, and there is no spectral bin inside the gap
   between the two state bands (0.861 to 1.081 Hz), so the metric was identically zero for every
   model including the ground truth. It now uses 32-sample windows with the parabolic peak
   interpolation of `utils.fidelity.peak_freq_batch`, validated on synthetic tones: a pure f0 or
   f1 tone gives 0.0 and a mid-band tone gives 1.0.

## Figure 8

`figures/fig8_alt_futures` shows one history with two different realized futures drawn from the
same chain statistics, the point forecasts of Linear and PatchTST regressing to a blend, and the
CSDI samples. `figures/kl_by_dwell` shows the KL rate and the between-band fraction against D with
seed error bars. Both are built from the saved `alt_futures` arrays, so no extra runs are needed.
