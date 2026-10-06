# Phase 1: real-data validation, findings

Written for: Rakib, as input to the Results section and the response letter.

Complete: 420 real runs (Track A 16 models x 5 datasets x 3 seeds, Track B 15 models x 4 datasets
x 3 seeds) and the synthetic clean paradigm (230 of 240 runs; 10 TimesNet jobs timed out). Units
are test subjects: BIDMC 11, NSRDB 6, Sleep-EDF 7, AFDB 4, DaLiA 3.

## 0. The headline result: fidelity rankings transfer to real data, MAE rankings do not

Kendall tau between the model ranking on the matched synthetic family and on the real dataset,
13 comparisons across five datasets and both tracks:

| ranking metric | mean tau | negative transfers |
|---|---|---|
| MAE | **0.07** | 4 of 13 |
| phase error | **0.28** | 1 of 13 |
| frequency error | 0.20 | 2 of 13 |

Ranking the synthetic benchmark by MAE carries almost no information about which model will do
well on real signals: the mean rank correlation is 0.07, and on ECG morphology (Track B) it is
clearly negative, -0.58 on AFDB against SPM and -0.47 against DPM, meaning the models that win on
the synthetic benchmark are among the worst on real ECG. Ranking the same benchmark by phase
fidelity transfers four times better and is negative only once. Phase beats MAE in 10 of the 13
comparisons.

This is the quantitative justification for the whole framework and the direct answer to R4.5: a
synthetic benchmark is predictive of real-data performance only if it is scored on temporal
fidelity, not on pointwise error. It also sets the limits honestly, since a mean tau of 0.28 is a
moderate correlation, not a strong one.

Per-comparison values are in `ranking_transfer.csv`.

## 1. A trivial periodic baseline was evaluated and then removed

A seasonal-naive forecaster was run alongside the roster and was, on real ECG, simultaneously the
worst model by mean absolute error and the best by phase error, and on clean PPG it beat every
trained architecture. It was removed from the reported results on 2026-10-06 by Rakib's decision,
because it is not part of the published model set and no reviewer asked for it. The runs remain
under `results/` and the implementation under `Model/SeasonalNaive.py`; clearing
`analysis/common.py::EXCLUDE_MODELS` restores it everywhere.

What changes without it: the single-model demonstration of the metric disagreement is gone, and so
is the observation that no trained model beats periodic extrapolation on clean PPG. What does not
change: the rank-transfer result below, which is slightly stronger without it, and the negative
rank correlations on ECG morphology, which are the remaining evidence for the disagreement.

## 1b. The headline: fidelity rankings transfer to real data, MAE rankings do not

Kendall tau between the model ranking on the matched synthetic family and on the real dataset,
13 comparisons across five datasets and both tracks, 15 models:

| ranking metric | mean tau | negative transfers |
|---|---|---|
| MAE | **0.07** | 4 of 13 |
| phase error | **0.33** | 1 of 13 |
| frequency error | 0.20 | 3 of 13 |

Ranking the synthetic benchmark by MAE carries almost no information about which model will do well
on real signals, and on ECG morphology the correlation is clearly negative. Ranking the same
benchmark by phase fidelity transfers more than four times better. At the level of inductive-bias
groups rather than individual models the transfer is far stronger still: Spearman rho of 0.80 to
1.00 on PPG and ECG, with the local group's mean rank moving only from 4.5 to 4.4, 5.0 to 5.0 and
5.0 to 4.4. It does not transfer on EEG (rho 0.00), where no dominant local period exists.

## 2. MAE and fidelity rankings disagree, and on ECG they are anti-correlated

Kendall tau between the model ranking by MAE and by each fidelity metric:

| dataset / track | phase | freq | band power | peak timing | beat F1 | RR error |
|---|---|---|---|---|---|---|
| BIDMC A / B | 0.85 / 0.96 | 0.42 / 0.47 | 0.40 / 0.81 | - / 0.50 | - / -0.70 | - / 0.54 |
| NSRDB A / B | 0.45 / 0.39 | 0.32 / -0.18 | 0.10 / -0.43 | - / 0.05 | - / 0.31 | - / -0.10 |
| AFDB A / B | 0.62 / -0.37 | 0.53 / -0.45 | 0.43 / -0.64 | - / 0.03 | - / 0.35 | - / -0.68 |
| DaLiA A / B | 0.53 / 0.50 | 0.42 / 0.24 | 0.37 / 0.70 | - / -0.20 | - / 0.39 | - / 0.20 |
| Sleep-EDF A | 0.93 | 0.07 | 0.48 | - | - | - |

On ECG morphology (Track B) several tau values are clearly negative: choosing the model with the
lowest MAE actively selects against band-power fidelity (-0.64 on AFDB), RR-interval accuracy
(-0.68) and amplitude fidelity (-0.62). Phase on BIDMC is the opposite case, tau 0.85 to 0.96,
where MAE and phase agree almost perfectly. The disagreement is therefore not universal, and the
paper should say where it holds: it is strongest for morphology metrics on ECG and for
beat-detection F1, and weakest for phase on clean PPG.

## 3. Natural events degrade forecasting, as the synthetic state transitions predicted

Events are tagged by position relative to the forecast boundary, H inside the history and F
inside the horizon, the real-data analogue of the Fig. 7 tags.

| dataset | event | position | MAE | MAE without an event |
|---|---|---|---|---|
| AFDB | AF onset | history | 1.119 | 0.730 |
| PPG-DaLiA | activity change | history | 1.329 | 0.852 |
| PPG-DaLiA | activity change | horizon | 0.728 | 0.852 |
| Sleep-EDF | sleep-stage change | history | 0.865 | 0.857 |

An atrial-fibrillation onset inside the history raises MAE by 53 percent and an activity change
by 56 percent, which is the same adaptation cost the synthetic single-transition paradigm
measures. Sleep-stage changes cost nothing measurable, consistent with EEG having no periodic
structure for a transition to disrupt.

Caveat to state in the text: all 15 AF onsets fell inside histories rather than horizons, because
the non-overlapping test windows tile the recording and horizons cover only two thirds of it. The
AFDB result is therefore about adaptation after a transition, not anticipation of one.

## 4. Clinical proxy (P1.7)

Heart-rate error over the ten-second horizon, best model per dataset:

| dataset / track | best model | error (bpm) |
|---|---|---|
| BIDMC A / B | MICN (regre) / TSMixer | 4.8 / 10.5 |
| NSRDB A / B | PatchTST / Transformer | 12.5 / 18.3 |
| AFDB A / B | ModernTCN / MICN (regre) | 29.8 / 20.8 |
| DaLiA A / B | MICN (mean) / Transformer | 18.2 / 43.9 |

Only clean photoplethysmography supports a clinically useful heart rate from a forecast; 4.8 bpm is
within the tolerance of consumer monitoring, while 12 to 44 bpm is not. Local receptive fields hold
the best result on five of the eight dataset and track combinations.

## 5. What this changes in the write-up

1. The clearest demonstration that the metric determines the ranking is now the set of negative
   rank correlations on ECG morphology: choosing by mean absolute error selects against
   inter-beat-interval accuracy (-0.69), beat detection (-0.65) and band power (-0.63).
2. The claim to defend is not "MAE and fidelity always disagree" but "MAE selects low-amplitude,
   temporally uninformative forecasts, and how much that matters depends on the metric and the
   modality". The tau table above gives the conditions.
3. Locality still holds among trained models on PPG and ECG (ModernTCN, MICN, PatchTST lead) but
   not on EEG, where the linear family leads. Report the exception.
4. The real-data results are consistent with the P0.4 reanalysis: the disagreement lives in the
   failure tail and in metrics other than phase, not in a matched-MAE dissociation.
