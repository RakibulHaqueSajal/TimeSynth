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

Priority order (Rakib, 2026-09-22): real-data validation first, then the synthetic roster.
Partition: `general-gpu` only for now; the `medvic` partition is not to be used until Rakib says so.
Concurrency: at most five jobs running in total, so exactly one array is submitted at a time.

| step | matrix | jobs | needs | what it is |
|---|---|---|---|---|
| 1 | `p1a_real_pilot` | 4 | BIDMC processed | P1.4 pilot: Linear, PatchTST, Transformer, CSDI on BIDMC Track A (submitted, job 201928) |
| 2 | `p1b_real_trackA` | 240 | all real datasets processed | PPG (BIDMC, DaLiA), ECG (NSRDB, AFDB), EEG (Sleep-EDF); 16 models x 3 seeds |
| 3 | `p1c_real_trackB` | 180 | same | PPG and ECG morphology at 50 Hz; 15 point models x 3 seeds |
| 4 | `p2a_synthetic_train` | 240 | synthetic corpora | clean x3 signals, state transition, redesigned Markov; 16 models x 3 seeds. Also required before the ranking-transfer analysis of Phase 1 can be completed |
| 5 | `p2b_synthetic_testonly_part0/1` | 1584 | step 4 (`--after`) | noise SNR 1-6 and shift buckets on the clean checkpoints; Markov per dwell time |
| 6 | `p3a_tier2_train` | 135 | Tier 2 corpora | Tier 2 ECG, PPG (50 Hz), EEG (100 Hz); 15 models x 3 seeds |
| 7 | `p3b_tier2_testonly` | 810 | step 6 | Tier 2 noise SNR 1-6 on the Tier 2 checkpoints |
| 8 | `p7a_adapt_aug_train` | 30 | - | augmentation retraining, SPM and DPM, 5 representative models |
| 9 | `p7b_adapt_testonly` | 360 | steps 4 and 8 | augmented checkpoints on shift; few-shot k = 5, 20 from clean checkpoints |

Queuing several arrays at once would run 5 x (number of arrays) jobs concurrently, which the
current policy does not allow: submit the next array only when the previous one has drained.

## Compute estimate

Measured in the pilot (`p1a_real_pilot`, BIDMC Track A, one seed, general-gpu):
Linear 3 min, CSDI 8 min, Transformer 9 min, PatchTST 16 min. BIDMC Track A has only
1183 training windows; DaLiA (5645) and Sleep-EDF (84000) are larger, and the 10 Hz synthetic
clean paradigm has ~57000 stride-1 windows per signal, so those jobs take proportionally longer.

| job type | per job | count | GPU hours |
|---|---|---|---|
| real Track A, small datasets (BIDMC, NSRDB, AFDB) | 3 to 16 min | ~140 | ~20 |
| real Track A, large datasets (DaLiA, Sleep-EDF) | 0.5 to 3 h | ~100 | ~120 |
| real Track B (50 Hz, 750-sample windows) | 0.5 to 2 h | ~180 | ~150 |
| synthetic 10 Hz training (stride 1, ~57k windows) | 0.5 to 3 h | ~240 | ~300 |
| Tier 2 training (50 to 100 Hz, long windows) | 1 to 4 h | ~135 | ~250 |
| test-only evaluations (incl. CSDI sampling) | 2 to 15 min | ~2750 | ~250 |
| adaptation arm | 0.5 to 3 h | ~390 | ~100 |
| **total** | | **~3935** | **~1200 GPU h** |

At five concurrent jobs that is roughly 10 days of wall-clock, which is tight against the
2026-10-05 deadline. Options, in the order I would take them: raise `max_concurrent` for the
short test-only arrays (they dominate the job count but not the hours), then raise it for the
training arrays, and only then consider the `medvic` partition.

## After each array finishes

    python analysis/p2_baselines/run.py     # after steps 2 and 3 (acceptance check vs paper numbers)
    python analysis/p1_real/run.py          # after 4 and 5
    python analysis/p3_tier2/run.py         # after 6 and 7
    python analysis/p4_markov/run.py        # after 3
    python analysis/p5_stats/run.py && python analysis/p6_framing/run.py   # everything
