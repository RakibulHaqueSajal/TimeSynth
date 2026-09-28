# Phase 1: real-data validation, findings

Written for: Rakib, as input to the Results section and the response letter.

Complete: 420 runs (Track A 16 models x 5 datasets x 3 seeds, Track B 15 models x 4 datasets x 3
seeds). Units are test subjects: BIDMC 11, NSRDB 6, Sleep-EDF 7, AFDB 4, DaLiA 3. Outstanding:
the synthetic-to-real ranking transfer (P1.6 item 1), which needs `p2a_synthetic_train`.

## 1. The headline: a trivial baseline is worst by MAE and best by phase

`SeasonalNaive` repeats the last dominant period of the history. Its rank among 15 to 16 models:

| dataset / track | rank by MAE | rank by phase error |
|---|---|---|
| BIDMC A / B | 1 / 1 | 1 / 1 |
| MIT-BIH NSR A | 16 (last) | 1 |
| AFDB A | 16 (last) | 1 |
| PPG-DaLiA A / B | 16 / 15 | 2 / 1 |
| Sleep-EDF A | 16 | 16 |

On real ECG, one model is simultaneously the worst by MAE and the best by phase. The learned
models sit at 87 to 90 degrees of phase error, which is what an unbiased random phase gives, so
they carry essentially no timing information; periodic extrapolation carries it and pays for it
in pointwise error. On clean PPG (BIDMC) the naive floor wins outright, on both tracks and on
every metric: MAE 0.50 against 0.65 for the best learned model, phase 33 degrees against 56,
beat-detection F1 0.64 against 0.38, heart-rate error 4.3 bpm against 4.8.

This is a stronger form of the paper's claim than the synthetic analysis supports, and it is the
most direct answer available to R4.2 and R4.3: the metric decides the winner, and on real
periodic signals none of the fourteen trained architectures beats periodic extrapolation from a
five-second history.

Sleep-EDF is the exception that keeps the claim honest: EEG has no dominant period to repeat, the
naive floor is last on both metrics, and the linear family leads.

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
| BIDMC A / B | SeasonalNaive | 4.3 / 6.7 |
| NSRDB A / B | PatchTST / SeasonalNaive | 12.5 / 13.1 |
| AFDB A / B | SeasonalNaive | 18.6 / 20.8 |
| DaLiA A / B | MICN Mean / Transformer | 18.2 / 43.9 |

Only clean PPG supports a clinically useful heart rate from a forecast; 4.3 bpm is within the
tolerance of consumer monitoring, while 12 to 44 bpm is not. The naive floor is best on four of
the eight dataset and track combinations.

## 5. What this changes in the write-up

1. The seasonal-naive floor moves from a sanity check to a main-text result. It is the cleanest
   demonstration that the choice of metric determines the ranking.
2. The claim to defend is not "MAE and fidelity always disagree" but "MAE selects low-amplitude,
   temporally uninformative forecasts, and how much that matters depends on the metric and the
   modality". The tau table above gives the conditions.
3. Locality still holds among trained models on PPG and ECG (ModernTCN, MICN, PatchTST lead) but
   not on EEG, where the linear family leads. Report the exception.
4. The real-data results are consistent with the P0.4 reanalysis: the disagreement lives in the
   failure tail and in metrics other than phase, not in a matched-MAE dissociation.
