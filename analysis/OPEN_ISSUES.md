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
