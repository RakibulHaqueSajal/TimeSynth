# Submission runbook (nothing has been submitted; policy C5: 5 jobs at a time)

All scripts live in `slurm/generated/` and were produced by `scripts/make_jobs.py` from
`configs/run_matrix/*.yaml`. Every array carries `%5`, so SLURM runs five elements at a
time and starts the next five as they finish. Re-running `make_jobs.py` on a matrix skips
jobs whose `pred.npy` already exists, so a failed array is resubmitted the same way.

Submit from the workstation with

    python scripts/make_jobs.py configs/run_matrix/<matrix>.yaml --submit --ssh compute [--after <jobid>]

or on the cluster with `sbatch slurm/generated/<phase>.sbatch`. Check with
`ssh compute squeue -u rakibul`. Logs: `logs/slurm/<phase>_<array>_<task>.out`.

## Order and dependencies

| step | matrix | jobs | needs | what it is |
|---|---|---|---|---|
| 1 | `p1a_real_pilot` | 4 | BIDMC processed (done) | P1.4 pilot: Linear, PatchTST, Transformer, CSDI on BIDMC Track A; fills the compute table |
| 2 | `p2a_synthetic_train` | 240 | synthetic corpora (done) | clean x3 signals, state transition, redesigned Markov; 16 models x 3 seeds |
| 3 | `p2b_synthetic_testonly_part0/1` | 1584 | step 2 finished (`--after`) | noise SNR 1-6 and shift buckets on the clean checkpoints; Markov per dwell time |
| 4 | `p1b_real_trackA` | 240 | all real datasets processed | PPG (BIDMC, DaLiA), ECG (NSRDB, AFDB), EEG (Sleep-EDF); 16 models x 3 seeds |
| 5 | `p1c_real_trackB` | 180 | same | PPG and ECG morphology at 50 Hz; 15 point models x 3 seeds |
| 6 | `p3a_tier2_train` | 135 | Tier 2 corpora (done) | Tier 2 ECG, PPG (50 Hz), EEG (100 Hz); 15 models x 3 seeds |
| 7 | `p3b_tier2_testonly` | 810 | step 6 | Tier 2 noise SNR 1-6 on the Tier 2 checkpoints |
| 8 | `p7a_adapt_aug_train` | 30 | - | augmentation retraining, SPM and DPM, 5 representative models |
| 9 | `p7b_adapt_testonly` | 360 | steps 2 and 8 | augmented checkpoints on shift; few-shot k = 5, 20 from clean checkpoints |

Steps 2, 4, 5, 6, 8 are independent and can be queued together; SLURM still runs at most
five elements per array, so queuing several arrays at once runs up to 5 x (number of arrays)
jobs concurrently. If that is not wanted, submit one array at a time.

## Compute estimate (workstation RTX-class GPU, 10 Hz clean paradigm; the pilot refines this)

| job type | per job | count | GPU hours |
|---|---|---|---|
| small models (Linear, DLinear, FITS, MLinear, NBeats, FreMLP, TSMixer, naive), 10 Hz | 5 to 25 min | ~370 | ~90 |
| CNN (ModernTCN, MICN x2), 10 Hz | ~45 min | ~140 | ~105 |
| Transformer family (PatchTST, Transformer, Autoformer, TimesNet), 10 Hz | 1.5 to 3 h | ~190 | ~430 |
| CSDI, 10 Hz (100 epochs, 52 s/epoch measured) | ~2 h | ~50 | ~100 |
| any model at 750 to 1500 samples (Track B, Tier 2) | 2 to 5x the above | ~315 | ~450 |
| test-only evaluations (incl. CSDI sampling) | 2 to 10 min | ~2750 | ~200 |
| **total** | | **~4050** | **~1400 GPU h** |

At five concurrent jobs that is roughly 12 days of wall-clock, which does not fit the
2026-10-05 deadline with margin. Recommendation: raise `max_concurrent` to 15 to 20 for the
test-only arrays (they are short) and to 10 for training arrays; edit the `slurm:` block in the
matrix YAML and regenerate. The `medvic` partition (2 x 4 H200) can take a second copy of the
training arrays with `partition: medvic`.

## After each array finishes

    python analysis/p2_baselines/run.py     # after steps 2 and 3 (acceptance check vs paper numbers)
    python analysis/p1_real/run.py          # after 4 and 5
    python analysis/p3_tier2/run.py         # after 6 and 7
    python analysis/p4_markov/run.py        # after 3
    python analysis/p5_stats/run.py && python analysis/p6_framing/run.py   # everything
