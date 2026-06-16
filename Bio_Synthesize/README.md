# Bio_Synthesize

Synthetic biosignal generation pipeline backing the supplementary appendix
([`template/supplementary.tex`](../template/supplementary.tex)).

Three signal families — **SPM** (single-phase modulation, PPG-like), **DPM**
(dual-phase modulation, ECG S–Q-like) and **DH** (drift-harmonic, EEG arousal-
state-like) — are generated under five controlled evaluation paradigms (clean,
noise, frequency distribution shift, single state transition, two-changepoint,
Markov switching).

## Layout

```
Bio_Synthesize/
├── Synthetic_Signals_bio/   # Generation scripts (one per family x paradigm)
├── Parametric_Fitting/      # Differentiable parametric models fit to real biosignals
└── Visualization_Scripts/   # Reproduces the supplementary figures
```

## Appendix → file mapping

### §S1 Signal family equations / §S3 Generation procedure (clean baseline)

| Family | Equation        | Script |
| ------ | --------------- | ------ |
| SPM    | Eq. (S1)        | [`Synthetic_Signals_bio/phase_modulated_s_q_single_sine.py`](Synthetic_Signals_bio/phase_modulated_s_q_single_sine.py) |
| DPM    | Eq. (S2)        | [`Synthetic_Signals_bio/phase_modulated_s_q_dual_sine.py`](Synthetic_Signals_bio/phase_modulated_s_q_dual_sine.py)     |
| DH     | Eq. (S3)–(S4)   | [`Synthetic_Signals_bio/drift_harmonic_signal_generation.py`](Synthetic_Signals_bio/drift_harmonic_signal_generation.py) |

### §S2 Parametric fitting to real biosignals

| Dataset    | Signal      | Fitting model (Eq.)          | Script |
| ---------- | ----------- | ---------------------------- | ------ |
| PPG-DaLiA  | PPG / BVP   | Drift-harmonic, Eq. (S3)     | [`Parametric_Fitting/Drift_harmonic.py`](Parametric_Fitting/Drift_harmonic.py) |
| MIT-BIH    | ECG (S–Q)   | Phase-mod multisine, Eq. (S2)| [`Parametric_Fitting/phase_modulated_multiple_sinewave.py`](Parametric_Fitting/phase_modulated_multiple_sinewave.py) |
| CHB-MIT    | EEG (FP1–F7)| Multi-band + spike, Eq. (S7) | [`Parametric_Fitting/Spike_Burst_with_modulation.py`](Parametric_Fitting/Spike_Burst_with_modulation.py) |

Auxiliary parametric modules not directly cited in the appendix but used
during model exploration: `fractal_enevelope_modulation.py`, `Fractal_noise.py`,
`oscillator_ou_noise.py`, `Regime_Swithching.py`.

### §S4 Controlled evaluation paradigms

| §     | Paradigm                       | Scripts |
| ----- | ------------------------------ | ------- |
| §S4.1 | Noise robustness (6 SNR levels)| `*_noise.py` (SPM / DPM / DH) |
| §S4.2 | Frequency distribution shift   | `*_distribution_test.py` (SPM / DPM / DH) |
| §S4.3 | Single state transition        | [`Synthetic_Signals_bio/single_phase_modulation_single_markov.py`](Synthetic_Signals_bio/single_phase_modulation_single_markov.py) |
| §S4.4 | Two-changepoint                | [`Synthetic_Signals_bio/Single_Phase_Modulation_Two_Transition.py`](Synthetic_Signals_bio/Single_Phase_Modulation_Two_Transition.py) |
| §S4.5 | Markov switching               | [`Synthetic_Signals_bio/single_phase_modulation_markov.py`](Synthetic_Signals_bio/single_phase_modulation_markov.py), [`Synthetic_Signals_bio/Single_Phase_Modulation_Markov_Modulation_Change.py`](Synthetic_Signals_bio/Single_Phase_Modulation_Markov_Modulation_Change.py) |

## Reproducibility

Every generation script uses a fixed seed (`seed = 42`) and dedupes candidate
parameter tuples via MD5 hash at six-decimal precision (§S3 Eq. S8). All
sampling parameters are embedded in the output filename for traceability,
e.g. `train_000_A_0.1050_f_0.8234_beta_0.1234_fmod_0.0512_offset_0.4567.csv`.

Default sampling rate: `fs = 10 Hz`, duration `300 s` (`T = 3000`).

## Visualization

The four scripts under `Visualization_Scripts/` regenerate the supplementary
figures for each paradigm (markov, two-transition, single-markov, phase-mod
multisine).

## Generated outputs

Generated CSVs are written to a `Generated_Datasets/` directory next to each
script and are excluded from version control by `.gitignore` — they are
deterministic given the seed and parameter bounds in
[`template/supplementary.tex`](../template/supplementary.tex).
