# Open issues found during the revision runs

## 1. CSDI sample dispersion on small real datasets (observed 2026-09-22, BIDMC Track A)

`results/real_ppg_A/BIDMC/CSDI/seed2021`: the 50 drawn samples have std 3.65 against a true
std of 1.00, so the sample median is over-smoothed (std 0.18) and the point metrics are worse
than a linear baseline (frequency error 1.63 Hz, heart-rate error 98 bpm).

Checked and ruled out: the reverse-diffusion coefficients and the quadratic beta schedule match
the reference implementation (Tashiro et al. 2021); the conditional mask, side information and
the noise-prediction loss on target positions are as published. `pred.npy` differs from
`np.median(samples)` only because `torch.median` returns the lower of the two middle values for
an even sample count, which is a definitional difference, not an error.

Most likely cause: undertraining. BIDMC Track A has 1183 training windows and the run stopped
after 44 epochs. The synthetic clean paradigm has about 57000 windows per signal and will
settle the question.

Known weakness regardless of the cause: `Exp_Long_Term_Forecast.vali` evaluates CSDI's loss at a
random diffusion step per batch, so early stopping acts on a noisy statistic. Fix, if needed, is
a deterministic step grid for validation. Not applied yet, because changing it while an array is
running would give different jobs different protocols.

Decision point: after `p2a_synthetic_train`, compare CSDI there. If it is also poor, apply the
deterministic-validation fix and re-run the CSDI jobs only (they are a separate `--model_config`,
so a small run matrix suffices).

## 2. Heart-rate proxy on Track B is an approximation

`analysis/p1_real/run.py` converts the RR-interval error to bpm at a nominal 75 bpm rather than
per window. Replace with per-window `60/RR_pred - 60/RR_true` once Track B results exist.

## 3. Training-budget imbalance across real datasets (found and fixed 2026-09-25)

The first `p1b_real_trackA` run (job 201943) used a fixed training stride per modality, which
produced very different training-set sizes:

| dataset | training windows (stride 10, EEG 20) |
|---|---|
| BIDMC | 17223 |
| AFDB | 31541 |
| NSRDB | 34851 |
| DaLiA | 84483 |
| Sleep-EDF | 629902 |

Sleep-EDF therefore gave every model about 18x more gradient steps per epoch than the ECG
datasets, which is a protocol imbalance, not only a compute problem: it was also why TimesNet
(95 min per epoch, 8 epochs in 12 h) and ModernTCN hit the wall clock on Sleep-EDF while every
other model early-stopped normally (max 213 epochs of the 300 allowed).

Fix: `--max_train_windows` (uniform cap, evenly spaced over the split) set to 35000 in all five
real paradigm configs. It binds only for DaLiA and Sleep-EDF; BIDMC, NSRDB and AFDB are below it
and their results from job 201943 are unchanged and still used.

The 96 affected runs were re-submitted as `p1b2_real_trackA_capped` (job 204714, 24 h limit).
The superseded outputs are archived under
`TimeSynth_runs/revision/superseded_uncapped/` with a README, not deleted.

Methods wording: "Training windows were capped at 35000 per dataset by evenly spaced
subsampling, so that datasets of very different recording length contribute a comparable
training budget."

## 4. Too few test subjects for subject-level statistics (fixed 2026-09-26, Rakib's decision)

The 70/10/20 subject split gave: BIDMC 11 test subjects, AFDB 4, Sleep-EDF 4, DaLiA 3, NSRDB 3.
A two-sided Wilcoxon signed-rank test over n = 3 units cannot produce p below 0.25, so the
subject-level statistics that answer R4.6 were unreachable on two of the three primary datasets.

Decision (Rakib, 2026-09-26): re-split the primary ECG and EEG datasets only.
`RealData/preprocess.py::SPLIT_FRACS_BY_DATASET` now uses 50/15/35 for `nsrdb` and `sleepedfx`,
giving NSRDB 9/3/6 and Sleep-EDF 10/3/7 subjects. BIDMC keeps 70/10/20 (37/5/11).
DaLiA (3) and AFDB (4) stay as secondary datasets and are reported with effect sizes and
bootstrap CIs, without p-values.

Affected runs archived under `TimesNet_runs/revision/superseded_smallsplit/` and re-submitted in
`p1d_real_remaining` (job 205496): NSRDB Track A and B, Sleep-EDF Track A. Track B for BIDMC,
DaLiA and AFDB was unaffected and its completed runs were reused.

Methods wording: "Recordings were split by subject, 70/10/20 for datasets with many subjects and
50/15/35 for MIT-BIH NSR and Sleep-EDF, so that every primary dataset has at least six test
subjects for the subject-level tests."
