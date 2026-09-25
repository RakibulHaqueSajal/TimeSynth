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
