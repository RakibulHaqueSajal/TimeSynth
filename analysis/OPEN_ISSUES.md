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

## 5. Hard-coded sequence length in the transformer embedding (found and fixed 2026-09-27)

`Layers/Transformers_Embed.py` (original code, commit 95a9f3b) gated the temporal embedding on a
hard-coded window length, in three separate classes:

    if x_mark.shape[1] == 125:
        x = value + position + temporal_embedding(x_mark)
    else:
        x = value + position

Consequences:

* Every published run used `seq_len = 50`, so the encoder half was 25 steps and the branch was
  never taken. Transformer, Autoformer and TimesNet therefore never used time features in the
  paper, although the Supplement describes a `DataEmbedding` with them.
* Real-data Track B uses `seq_len = 250`, so the encoder half is exactly 125 and the branch fired
  for the first time. It then crashed in `TimeFeatureEmbedding.forward` on `x.view(-1, D)`,
  because the encoder input `batch_x[:, :half, :]` is not contiguous. 24 jobs (Transformer and
  Autoformer, 4 datasets x 3 seeds) produced no output while SLURM still reported success, since
  the traceback did not change the exit code.
* `DataEmbedding_wo_temp` has no `temporal_embedding` attribute at all, so the branch would have
  raised `AttributeError` had it ever been taken there.

Fix: `.view` to `.reshape`, and the temporal embedding is now controlled by
`DataEmbedding.USE_TEMPORAL_EMBEDDING`, default `False`, instead of switching itself on at one
window length. That default reproduces the behavior of every completed run exactly
(`tests/test_embedding.py::test_matches_paper_behavior_for_completed_runs`), so no finished
result is invalidated, and it is the defensible choice: synthetic timestamps are uniform, and on
real data wall-clock features encode recording identity rather than physiology.

Note for the Supplement: state that the transformer family uses value and positional embeddings
only.

Open risk of the same kind: a job whose python process dies with a traceback still exits 0 in the
array script, so SLURM reports COMPLETED. `scripts/validate_jobs.py` and the `pred.npy` existence
check in `make_jobs.py` are what actually catch this; always compare result counts against the
job matrix after an array finishes.
