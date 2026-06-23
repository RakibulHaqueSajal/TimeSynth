# TimeSynth: A Temporal Fidelity Framework for Health Signal Digital Twins

Benchmarking 11 forecasting architectures (Linear / DLinear / MLinear / NBeats /
FreMLP / FITS / PatchTST / MICN / ModernTCN / Transformer / Autoformer) on
synthetic physiological signals — clean, noise-corrupted, distribution-shifted,
and Markov state-transition regimes — under amplitude, frequency, and phase
fidelity metrics in addition to standard MAE.

## Repository layout

```
.
├── main.py                       # CLI entry point (argparse for every experiment)
├── Model/                        # Architectures (Autoformer, PatchTST, MICN, ...)
├── Layers/                       # Building blocks (attention, conv, embeds, RevIN, ...)
├── Experiment/                   # Train / evaluate / test orchestration
├── Bio_Synthesize/               # Synthetic biosignal generation (matches supplementary appendix)
├── Data_Creator/                 # Synthetic signal generation
├── Data_Loader/                  # Dataset / DataLoader wrappers
├── utils/                        # Metrics, losses, tools, augmentation
├── markov_state/                 # Markov-state analysis scripts
├── Statistical_Test/             # Paired tests (clean, noise, shift, state-transition) + plotting
├── fidelity_metric_illustration/ # Standalone figures for the fidelity metrics
├── template/                     # Paper LaTeX (result.tex) + supplementary.tex appendix
├── slurm/                        # SLURM launch scripts
├── run_*.sh                      # Parameter sweep launchers (linear, mlp, CNN, transformer, ...)
├── test_*.py                     # Ad-hoc test entry points
├── requirements.txt
└── LICENSE
```

Large derived artifacts (model checkpoints, train/test predictions, per-model
SLURM stdout, comparison CSVs, exploratory plots) are excluded via
`.gitignore` — they are regenerable from the scripts in this repo.

## Installation

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

CUDA-enabled PyTorch is recommended — install the build matching your driver
from <https://pytorch.org/get-started/locally/>.

## Quickstart

Train one architecture on a synthetic dataset:

```bash
python main.py \
  --task_name long_term_forecast \
  --is_training 1 \
  --model_id Linear_50_100_demo \
  --model Linear \
  --data custom \
  --root_path ./Synthetic_datasets/ \
  --features S --target Value \
  --seq_len 50 --pred_len 100 \
  --enc_in 1 --train_epochs 100 --patience 20 \
  --batch_size 128 --learning_rate 1e-3
```

The `run_*.sh` files at the repo root and under `slurm/` contain the full
parameter sweeps used in the paper (per-model × signal × evaluation paradigm).

## Evaluation paradigms

| Paradigm           | Driver               | Outputs                                    |
| ------------------ | -------------------- | ------------------------------------------ |
| Clean              | `Statistical_Test/clean.py`            | Per-architecture vs Linear deltas         |
| Noise (SNR sweep)  | `Statistical_Test/noise.py`            | Option A per-level CSVs → heatmap & line  |
| Distribution shift | `Statistical_Test/shift.py`            | Shift Option A CSVs → heatmap             |
| Markov / state     | `Statistical_Test/state_transition.py` | Tagwise paired tests → heatmap            |

Plot regeneration:

```bash
python Statistical_Test/plot_noise_optionA.py
python Statistical_Test/plot_shift_optionA.py
python Statistical_Test/plot_state_transition_tagwise.py
```

## Reproducing the figures

Each plotting script auto-discovers the CSVs produced by its companion
analysis script and writes `*_heatmap.{png,pdf}` and `*_line.{png,pdf}` under
the script's own `plots/` directory.

## License

[MIT](LICENSE) © 2026 Rakibul Haque Sajal
