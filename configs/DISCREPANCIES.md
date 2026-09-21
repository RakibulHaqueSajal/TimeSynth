# Hyperparameter provenance and discrepancies (P0.2)

`configs/models/*.yaml` were built from the SLURM launch scripts in `slurm/`
(917 `main.py` invocations parsed, commented and live). Checkpoint folder names
encode `{weight_decay}_{learning_rate}_{patch_len}` and were used as an
independent check; every model's YAML matches its checkpoint names.

**Supplementary Tables A5 to A7 are not in this repository** (`template/supplementary.tex`
only contains the generator, SNR, fitting and dataset-size tables), so the
plan's "copy from A5 to A7 and flag disagreements" could only be done against
the scripts. Rakib: please diff the YAMLs against the manuscript tables.

## Conflicts found in the scripts (majority value used)

| Model | Argument | Values seen (count) | Used | Note |
|-------|----------|---------------------|------|------|
| Linear | `train_epochs` | 200 (12), 400 (2) in training blocks; 300 in test-only blocks | 200 | early stopping (patience 70) makes this rarely binding |
| Linear, MLinear, PatchTST | `backcast` | 0 (all but 1) | 0 | single `backcast 1` block belongs to an abandoned MLP_Backcast experiment |
| MLinear, NBeats, FreMLP | `patience` | 30 (16), 60 (8) | 30 | 60 appears only in the earliest run_mlp.sh blocks |
| MLinear | `train_epochs`, `patience` | 500/200 or 300 (3 blocks) | 300 / 30 | the 500-epoch blocks are the very first experiments |
| PatchTST | `d_model` | 256 (26), 128 (3) | 256 | 128 was a one-off sweep |
| PatchTST | `patch_len` | 15 (28), 30 (1) | 15 | checkpoint names confirm 15 |
| PatchTST, Transformer, Autoformer | `patience` | 30 (majority), 80 (early blocks) | 30 | |
| PatchTST, Transformer, Autoformer | `train_epochs` | 300; a few `2` | 300 | the `2` blocks are debugging runs |
| ModernTCN | `dropout` | passed twice in the same command (0.4 then 0.2) | 0.2 | argparse keeps the last occurrence |
| MICN | `label_len` | 50 in scripts | 50 (kept) | `Dataset_Custom` forces `label_len = 0` for every split, so the value is inert |
| DLinear | `train_epochs` | 300 (12 training), 200 (10 test-only) | 300 | |

## Things the scripts do that the paper text may not say

* Autoformer and Transformer receive only the first 25 samples of the 50-sample
  history in the encoder; the second 25 are the decoder warm-up
  (`Experiment/exp_forecast.py`, the `"former"` branch). PatchTST is not affected
  (`patchtst` does not contain "former"). TimesNet is routed through the generic
  `else` branch and sees the full history.
* `--is_training 0` in the scripts corresponds to a training branch of an older
  `main.py`; today only `1` (train + test) and `2` (test-only) do anything.
* All paper runs used `--itr 1` and `--seed 2021`.
* The test loader used `drop_last=True` with batch 128, so 60 of the 57 020
  stride-1 test windows were silently dropped from every clean run.

## Revision defaults that differ from the paper on purpose

| Setting | Paper | Revision | Reason |
|---------|-------|----------|--------|
| test window stride | 1 | `seq_len + pred_len` (150) | R4.6, non-overlapping test windows |
| test `drop_last` | True | False | keep every window |
| seeds | 2021 | 2021, 2022, 2023 | R4.6 |
| result layout | `Train_Test_Validation/<setting>/` | `results/{paradigm}/{signal}/{model}/seed{k}/` | P0.2 |
