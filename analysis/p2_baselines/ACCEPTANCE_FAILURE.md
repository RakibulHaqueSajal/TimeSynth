# P2.6 acceptance check: the retrained models do not reproduce the paper's numbers

Written for: Rakib. This is a blocking finding for Phase 2 and it changes a claim in the paper.

The plan's acceptance criterion for P2.6 was: "the regenerated Fig. 3 reproduces the paper's
seed-2021 numbers for the original 11 models before new models are added, which confirms that the
refactor changed nothing." It does not. The comparison is in `acceptance_seed2021.csv`, computed
on exactly the same test windows (the legacy stride-1 arrays subsampled to `window_start % 150 == 0`,
399 windows, against the 400 non-overlapping windows of the rerun).

## What reproduces and what does not

| group | models | agreement |
|---|---|---|
| linear and decomposition | Linear, DLinear, FITS, MLinear, FreMLP | within 1 to 10 percent on Drift and DPM, up to 25 percent on SPM |
| transformer family | Transformer, Autoformer | within 1 to 26 percent |
| **local receptive field** | **MICN Mean, MICN Regre, ModernTCN, PatchTST, NBeats** | **the rerun is 2 to 5 times worse** |

Examples, MAE on Dual Phase Modulation, seed 2021:

| model | paper | rerun | ratio |
|---|---|---|---|
| MICN Regre | 0.0133 | 0.0712 | 5.4 |
| MICN Mean | 0.0150 | 0.0711 | 4.7 |
| ModernTCN | 0.0232 | 0.0865 | 3.7 |
| PatchTST | 0.0335 | 0.0687 | 2.1 |
| Linear | 0.0792 | 0.0790 | 1.0 |

The affected models are exactly the ones whose advantage is the paper's central result.

## Cause 1, confirmed: ground-truth leakage into the MICN decoder

`Dataset_Custom` forces `self.label_len = 0` for every split, so `batch_y` is purely the forecast
target with no overlap with the history. The trainer then builds the decoder input as

    dec_inp = torch.cat([batch_y[:, :args.label_len, :], dec_inp], dim=1)

and the paper's MICN launch scripts pass `--label_len 50`. Those 50 values are therefore the
first 50 samples of the ground-truth future, i.e. the first 5 seconds of the 10-second horizon,
handed to the decoder at training and at test time. Verified numerically: with `label_len = 50`
the first 50 entries of `dec_inp` are bit-identical to `batch_y`.

The revision configs set `label_len: 0` from the paradigm, which removes the leak. That is why
MICN's error rises by a factor of about five.

Consequence for the paper: the published MICN results are not a 10-second forecast. Either MICN
is re-run without the leak (already done, numbers above) and the text is corrected, or the
leakage is disclosed. The honest option is the former, and it weakens but does not eliminate the
locality claim, since ModernTCN and PatchTST do not use the decoder path at all.

Note this corrects an entry in `configs/DISCREPANCIES.md`, which recorded `label_len` as inert
because `Dataset_Custom` zeroes it. The dataset zeroes its own copy; `args.label_len` still
reaches the decoder construction.

## Cause 2, not yet explained: ModernTCN, PatchTST and NBeats

These three take the `model(batch_x)` path and never see `dec_inp`, so leakage cannot explain
them. Their training in the rerun is well behaved: ModernTCN early-stopped at epoch 34 with best
validation MSE 0.0141, PatchTST at 67 with 0.0095, NBeats at 54 with 0.0114, against Linear's
0.0113. In other words ModernTCN converges to a worse optimum than Linear in the rerun, while the
paper has it three times better.

Hypotheses, in the order I would test them:

1. The published checkpoints were trained with settings that are not in the launch scripts. Every
   training block in `slurm/*.sh` is commented out; the live blocks are `--is_training 2`
   (test-only). The hyperparameters in `configs/models/*.yaml` were reconstructed from those
   commented blocks plus the checkpoint folder names, and they may not be what actually produced
   the checkpoints.
2. The OneCycle schedule interacts badly with early stopping: with `epochs = 300` and
   `pct_start = 0.3` the learning rate is still rising at epoch 34, so a model that early-stops
   there never reaches the decay phase. This would hit the fast-converging local models hardest,
   which matches the pattern.
3. Torch or cuDNN version differences between the original runs and this environment.

Hypothesis 2 is the most likely and the cheapest to test: rerun ModernTCN and PatchTST on one
signal with `--train_epochs 60` so the schedule completes within the run, and compare.

## What this means for the revision

* Phase 2 cannot be reported as a clean regeneration of the paper's table until cause 2 is
  resolved. The numbers are internally consistent (all 15 models trained identically under the
  revision protocol) and can be reported as a new experiment, but they are not a reproduction.
* The MICN leak is a correction the paper must carry regardless of how cause 2 resolves.
* Phase 1, the real-data validation, is unaffected: it never used the legacy checkpoints and all
  its models were trained under the revision protocol.
