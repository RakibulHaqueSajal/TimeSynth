# TimeSynth Revision: Experiment Plan for Claude Code

Target: Nature Communications revision of "TimeSynth: A Temporal Fidelity Framework for Health Signal Digital Twins".
Repository: https://github.com/RakibulHaqueSajal/TimeSynth
Plan written: 2026-09-21, against the `main` branch as of that date.

Priority order set by Rakib:

1. Real-data validation (R4.5)
2. New baselines: TimesNet, TSMixer, one probabilistic model (R1.1/R2.1, R4.7)
3. Tier 2 transient-rich synthetic signals (R1.3/R2.3, R4.4)
4. Everything else the reviews require (Markov redesign, statistics, absolute-MAE analysis, adaptation arm, text fixes)

Phase 0 is infrastructure that all four priorities depend on. It is short and should be done first.

---

## How Claude Code should use this file

- Work on a branch named `revision`. Commit after every numbered task with a message that starts with the task ID, for example `P1.3: subject-wise splits for PPG-DaLiA`.
- Read the relevant source files before editing any of them. Do not assume a script does what its name says; several scripts in `Statistical_Test/` and `Data_Creator/` contain commented-out alternatives.
- Never delete or overwrite existing result folders, checkpoints, or prediction `.npy` files. New outputs go under `results/` using the layout in P0.2.
- Everything heavier than a unit test runs through SLURM on Redtail. Do not train on the login node.
- Environment: Ubuntu, conda. Add any new package to `requirements.txt` with a pinned version.
- Any item marked **DECISION** needs Rakib's answer before implementation. Record the answer in the Decision Log at the bottom of this file.
- Writing conventions for any text, captions, or LaTeX this work produces: American English, no em-dashes, all symbols and inline numbers in math mode in LaTeX, tables with `\hline` grids plus `\renewcommand{\arraystretch}{1.2}` and `\resizebox{\textwidth}{!}{}`, no booktabs.
- Figures: build as SVG and export a high-resolution PNG alongside. Navy `#16356c` bold titles, blue `#2a5fa0` italic subtitles, teal for good states and red for warning states, error bars on every summary plot, no overlapping elements.

---

## 1. Code audit findings (verified 2026-09-21)

These were checked directly in the repository and change the scope of the revision.

| ID | Finding | Location | Consequence | Reviewer |
|----|---------|----------|-------------|----------|
| A1 | TimesNet is implemented and registered in `model_dict` | `Model/TimesNet.py`, `Experiment/Exp_Basic.py` | Only configs and runs are needed | R1.1/R2.1 |
| A2 | **TSMixer does not exist in the codebase** | no match for `mixer` anywhere | Must be implemented; the response letter should politely correct the reviewers' premise | R1.1/R2.1 |
| A3 | Markov chain switches with probability `p` **at every sample** | `simulate_two_state_chain` in `Bio_Synthesize/Synthetic_Signals_bio/single_phase_modulation_markov.py` | Reviewer 3 is right: at 10 Hz with `p = 0.5`, mean dwell is 0.2 s, shorter than one 1 Hz cycle. Paradigm must be regenerated | R3.4 |
| A4 | Markov data is written to `base_dir/p_<p>/{train,val,test}` and `Dataset_Custom` reads `root_path/{flag}/*.csv` | same file, `Data_Creator/data_creator.py` | Training was almost certainly per-`p`. Confirm from the Redtail launch scripts, then switch to pooled training | R3.3 |
| A5 | Generator `__main__` uses `transition_probs=(0, 0.1, 0.5, 0.9, 1)`, the function default is `(0, 0.1, 0.5, 0.9, 0.9999)`, the paper reports `{0.1, 0.3, 0.5, 0.7, 0.9}` | same file | Three different lists. Find which one produced the paper numbers before rewriting | R3.3 |
| A6 | Markov KL is a 1D Gaussian KL on decoded switching rates | `kl_gaussian_1d` in `Statistical_Test/markov.py` | Replace with transition-matrix KL rate between fitted chains | R3.5 |
| A7 | Eq. A7 in code gives `f0 in [0.7149, 0.8615]` and `f1 in [1.0814, 1.2279]` Hz | `make_well_separated_freq_ranges` | The code is correct and the Appendix text is wrong. Text-only fix | R1.6/R2.6 |
| A8 | Every dataset class windows with stride 1; `--itr` defaults to 1; seed fixed at 2021 | `Data_Creator/data_creator.py`, `main.py` | Test windows overlap heavily and each model has one training run. Paired tests on windows inflate significance | R4.6 |
| A9 | Test outputs go to a hard-coded `./Changing_F1_Mod/` folder and checkpoints to a hard-coded `/uufs/...` path | `Experiment/exp_forecast.py`, `main.py` | Must be parameterized before any large run | infra |
| A10 | Phase and frequency metrics are duplicated inside `Statistical_Test/shift.py` and `Statistical_Test/state_transition.py`; `utils/metrics.py` only has pointwise metrics | as listed | One shared metrics module is needed so real-data and Tier 2 use identical definitions | infra |
| A11 | TimesNet selects periods from the batch-averaged spectrum | `FFT_for_Period` in `Model/TimesNet.py` | Acceptable, but note it in the Supplement since it makes the period choice batch-dependent at test time | R1.1 |

---

## 2. Timeline at a glance

Week numbers are relative to the start of work. Fill the actual revision deadline into the Decision Log.

| Week | Phase 0 | P1 Real data | P2 Baselines | P3 Tier 2 | P4 to P7 |
|------|---------|--------------|--------------|-----------|----------|
| 1 | Metrics module, runner, SLURM, cheap reanalysis | Download, preprocess, splits | Implement TSMixer, TimesNet configs | Generator design | Markov code check |
| 2 | | Pilot runs, then full real-data runs | New models on synthetic paradigms | ECG and EEG generators, transient metrics | Markov regeneration |
| 3 | | Ranking-transfer analysis | Probabilistic baseline | Tier 2 runs | Markov runs, stats rework |
| 4 | | Clinical proxy, figures | Regroup taxonomy, regenerate figures | Tier 2 analysis | Adaptation arm if approved |
| 5 | | Final figures and tables for all phases | | | Supplement and response-letter numbers |

---

## Phase 0: Infrastructure (prerequisite, about 3 days)

### P0.1 Unified fidelity metrics module

Create `utils/fidelity.py` holding one implementation of every metric used in the paper and in the revision. Extract the existing phase and frequency code from `Statistical_Test/shift.py` and `Statistical_Test/state_transition.py` without changing behavior, then add the new metrics.

Functions, all operating per sequence on arrays of shape `[N, H]`:

- `mae`, `mse`
- `freq_error`: DC removal, FFT, parabolic peak refinement, 10% peak-power reliability filter, exactly as in Methods Eq. 5
- `phase_error_deg`: frequency-domain Hilbert with pad factor 2, mask where true amplitude exceeds 20% of its median, as in Eq. 6
- `band_power_error`: relative error of power in a named band, for real data
- `xcorr_lag`: lag of the cross-correlation peak between prediction and truth, in seconds
- `peak_timing_error`, `peak_amplitude_error`, `peak_detection_f1(tol_s)`, `rr_interval_error`: for Tier 2 and real ECG or PPG
- `crps_empirical`: for probabilistic models given `[S, N, H]` samples

Acceptance:

- `tests/test_fidelity.py` checks each metric on analytic signals with known answers: a sinusoid shifted by 30 degrees must return 30 within 0.5 degrees; a frequency offset of 0.05 Hz must be recovered within the FFT resolution after interpolation; a peak train shifted by 40 ms must return 40 ms.
- Regression test: recomputing phase and frequency error on at least one saved `pred.npy`/`true.npy` pair from the paper reproduces the old values to 1e-6.
- `Statistical_Test/*.py` import from `utils/fidelity.py` instead of defining their own copies.

### P0.2 Config-driven runner and result layout

- Add `--results_dir`, `--checkpoint_dir`, `--eval_stride`, and `--seeds` arguments to `main.py`. Remove the hard-coded `./Changing_F1_Mod/` and `/uufs/...` defaults.
- Result layout: `results/{paradigm}/{signal}/{model}/seed{k}/` containing `pred.npy`, `true.npy`, `hist.npy`, and `meta.parquet` with one row per window: `file_id`, `window_start`, `tag`, and any condition label such as SNR level, shift bucket, dwell time, or subject ID. The `file_id` column is what makes signal-level statistics possible in Phase 5.
- Configs live in `configs/models/{model}.yaml` and `configs/paradigms/{paradigm}.yaml`. Hyperparameters for the existing 11 models are copied from Supplementary Tables A5 to A7 and from the existing SLURM scripts. Where the two disagree, flag it in `configs/DISCREPANCIES.md` rather than picking one silently.

### P0.3 SLURM array launcher

`scripts/make_jobs.py` reads a run matrix YAML and writes one `sbatch` array script per phase. Each array element is a single (model, paradigm, signal, seed) job. It skips jobs whose `results/.../seed{k}/pred.npy` already exists, so partial failures can be resumed.

### P0.4 Cheap reanalysis on existing predictions (runs on CPU, in parallel with everything else)

This decides the framing of the paper, so it should be done in the first week using the predictions already on disk.

1. **Absolute-MAE dissociation (R1.4/R2.4).** Condition at the sequence level, not the model level: bin every test sequence from every model by its MAE, expressed relative to signal amplitude as `MAE / A_rms`. Use fixed bins, for example `[0, 0.05)`, `[0.05, 0.1)`, `[0.1, 0.2)`, `[0.2, inf)`. Inside each bin, compare phase and frequency error across bias groups with a Kruskal-Wallis test and report effect sizes. Repeat with the reviewers' absolute window of MAE in `[0, 0.03]`. Keep the old central-60% window as a sensitivity check, once with and once without Autoformer.
2. **Rank-correlation headline (R4.2/R4.3).** For each paradigm and signal family, compute Kendall `tau` between the model ranking by MAE and the ranking by phase error and by frequency error, with a bootstrap 95% CI over test signals. This becomes the quantitative "MAE is insufficient" claim.
3. **Signal-level statistics check (R4.6).** Rerun the existing paired tests after averaging windows within each test signal, so `n = 20` per family instead of thousands of overlapping windows. Report which paper claims keep significance.

Outputs: `analysis/p0_reanalysis/` with CSVs and a short `SUMMARY.md` listing, for each claim in Results, whether it survives. **Stop and report to Rakib after this task**, because the result changes how Phases 1 to 3 are written up.

---

## Phase 1: Real-data validation (Priority 1)

Goal: show whether synthetic rankings predict real rankings, and whether the MAE-versus-fidelity disagreement persists on real signals.

### P1.1 Datasets

**DECISION D1: which datasets.** Recommendation below. The core rule is that at least one dataset per modality must be independent of the three datasets used to fit the generator, so the validation is not circular.

| Modality | Primary, independent of fitting | Secondary | Natural event it offers |
|----------|--------------------------------|-----------|-------------------------|
| PPG | BIDMC PPG and Respiration (PhysioNet, 53 recordings, 8 min, 125 Hz) | PPG-DaLiA remaining segments (used for fitting, so label it as in-distribution) | DaLiA activity labels give real exercise-driven frequency shifts |
| ECG | MIT-BIH Normal Sinus Rhythm Database (PhysioNet, long recordings, 128 Hz) | MIT-BIH Atrial Fibrillation Database | AF onset annotations give real state transitions |
| EEG, optional | Sleep-EDF Expanded, Fpz-Cz channel (PhysioNet, 100 Hz) | CHB-MIT channels other than FP1-F7 | Hypnograms give real stochastic state switching |

Minimum viable scope: one PPG and one ECG dataset. EEG is added if time allows, and is the most valuable addition for the Markov paradigm because sleep staging is a genuine stochastic switching process.

Write `RealData/download.py` that pulls each dataset with `wfdb` or direct download into `$SCRATCH/TimeSynth_real/raw/`, and records dataset version and checksum in `RealData/MANIFEST.md`.

### P1.2 Preprocessing: the matched-cycles principle

The synthetic benchmark uses a 50-sample history and a 100-sample horizon at 10 Hz, which gives about 5 cycles of history for a 1 Hz rhythm. Real data must match that cycles-per-window ratio so architectural effects are comparable, otherwise the real task is a different task.

Two tracks:

- **Track A, rhythm band.** Bandpass around the dominant rhythm, then resample so the history holds about 5 dominant cycles with `seq_len = 50`, `pred_len = 100`.
  - PPG: bandpass 0.5 to 4 Hz, resample to 10 Hz.
  - ECG: bandpass 0.5 to 3 Hz, resample to 10 Hz. This is the real-data analog of the smooth S-Q baseline used for fitting, and it keeps Hilbert phase well defined.
  - EEG: bandpass 1 to 30 Hz, resample to 100 Hz, so a 50-sample history spans 5 alpha cycles.
- **Track B, full morphology.** Used for ECG and PPG only, and shares code with Tier 2 in Phase 3. ECG lowpass at 20 Hz and resample to 50 Hz; PPG resample to 50 Hz. Window lengths follow **DECISION D5** in Phase 3 so Track B and Tier 2 use identical settings.

Both tracks: remove segments flagged as artifact or with signal quality below a threshold, z-score per recording using training-portion statistics only, and store `[recording_id, t_start]` for every window.

Implement in `RealData/preprocess.py` with one function per dataset and a shared `make_windows(signal, fs, seq_len, pred_len, stride)`.

### P1.3 Splits and leakage control

- Split by subject or recording, never by window: 70% train, 10% validation, 20% test, with a fixed seed stored in `RealData/splits/{dataset}.json`.
- Training windows: stride 10 samples to limit near-duplicates.
- Test windows: stride `seq_len + pred_len`, so no two test windows share any sample. This directly answers R4.6.
- Cap windows per test subject so no single long recording dominates the statistics.

### P1.4 Training

- All models from the final roster after Phase 2, three seeds each, using the same unified protocol and hyperparameters as the synthetic runs. No per-dataset tuning, since the question is whether benchmark rankings transfer as they are.
- Run a pilot with Linear, PatchTST, and Transformer on one dataset first to measure wall-clock time and to fill the compute table at the end of this file.

### P1.5 Metrics on real data

Real signals have no analytic ground truth, so use metrics that remain well defined on observed futures:

- MAE, MSE
- Frequency error on the dominant spectral peak, using the same `freq_error`
- Phase error after narrowband filtering both prediction and truth around the true dominant peak, using the same `phase_error_deg`. Justify in Methods that narrowband filtering is what makes Hilbert phase meaningful, which is also why Tier 1 synthetic signals are narrowband.
- Band-power error and cross-correlation lag
- For ECG and PPG: beat-timing error, inter-beat interval error, and beat detection F1 within a 50 ms tolerance, using standard beat detectors applied identically to prediction and truth

### P1.6 Central analyses

1. **Ranking transfer.** For each metric, compute Kendall `tau` and Spearman `rho` between model rankings on the matched synthetic family and on real data: PPG against drift-harmonic, ECG against SPM and DPM, EEG against DPM. Bootstrap the CI by resampling test subjects on the real side and test signals on the synthetic side. Add a permutation test for `tau > 0`.
2. **Disagreement persists.** Repeat P0.4 item 2 on real data: Kendall `tau` between MAE rank and each fidelity rank.
3. **Bias-group level.** Compare mean rank per bias group across synthetic and real, which is more robust than individual model ranks with 14 models.
4. **Natural-event paradigms, if D1 includes them.** DaLiA activity transitions as a real frequency shift, AFDB onset as a real state transition with the same H and F tags as Fig. 7, sleep hypnogram switching as a real Markov test.

Honest reporting rule: if rankings transfer only partly, the Results must say which synthetic findings held on real data and which did not. Do not drop a dataset because its result is inconvenient.

### P1.7 Clinical proxy

**DECISION D2: include a proxy now or leave it to future work.** Recommended cheap version: heart-rate estimation error from forecasted PPG and ECG over the 10 s horizon, compared against heart rate from the true future. It needs no labels and speaks directly to clinical utility. AF detection from forecasts is a stronger but more expensive option.

### P1.8 Outputs

- `analysis/p1_real/ranking_transfer.csv`, `disagreement.csv`, `per_subject_metrics.parquet`
- New main-text figure: synthetic rank versus real rank scatter per metric, one panel per modality, bias groups colored, `tau` with CI printed in each panel
- Supplementary table: per-model metrics on each dataset, mean and 95% CI over subjects

Acceptance: every model has three seeds on every chosen dataset; test windows are verified non-overlapping by an assertion in the loader; the analysis script regenerates all outputs from `results/` with one command.

---

## Phase 2: New baselines and bias taxonomy (Priority 2)

### P2.1 TimesNet

Already in the codebase. Tasks:

- Write `configs/models/TimesNet.yaml` using the published defaults scaled to this benchmark: `d_model = 64`, `d_ff = 64`, `top_k = 3`, `num_kernels = 6`, `e_layers = 2`. With `seq_len = 50`, confirm that the selected periods are sensible and log them per batch on a pilot run.
- Confirm that `DataEmbedding` time features do not leak information across windows, since synthetic timestamps are uniform.
- Citation: Wu et al., ICLR 2023.

### P2.2 TSMixer

Not in the codebase, contrary to the reviewers' statement.

- Implement `Model/TSMixer.py` following Chen et al., "TSMixer: An All-MLP Architecture for Time Series Forecasting", TMLR 2023: time-mixing MLP and feature-mixing MLP blocks with residuals, RevIN, and a temporal projection head. With univariate input, feature mixing is trivial; keep it so the architecture matches the paper, and note this in the Supplement.
- Register it in `Experiment/Exp_Basic.py` and add `configs/models/TSMixer.yaml`.
- Unit test: forward pass shape `[B, 50, 1]` to `[B, 100, 1]`, and a 200-step overfit test on a single sinusoid reaching MSE below 1e-3.

### P2.3 Probabilistic baseline

**DECISION D3: which model.** Recommendation: CSDI (Tashiro et al., NeurIPS 2021) as the primary probabilistic baseline, since it handles univariate conditional forecasting cleanly and is well known. TimeGrad (Rasul et al., ICML 2021) is the alternative; it is autoregressive over the horizon and slower for `pred_len = 100`.

- Implement or vendor the model under `Model/CSDI.py` with a thin wrapper so `main.py` can train it. Keep the upstream license header if vendoring.
- At test time draw `S = 50` samples per window. Save `samples.npy` of shape `[S, N, H]`.
- Point metrics use the sample median. Add CRPS. For the Markov paradigm, switching statistics are computed per sample, which is the actual test of Reviewer 4's objection.
- Given its cost, CSDI runs on: clean for all three families, the redesigned Markov paradigm, and real data. It does not need the full noise and shift sweep unless time allows.

### P2.4 Naive floor

Add a seasonal-naive forecaster that repeats the last dominant period estimated from the history. No training. It gives every figure a sanity floor and costs nothing.

### P2.5 Regroup by inductive bias

Create `configs/bias_groups.yaml`. Proposed membership, to be verified against the code by reading each model's forward pass:

| Bias group | Defining mechanism | Models |
|------------|-------------------|--------|
| Local receptive field | Operations on short windows or patches | ModernTCN, MICN Mean, MICN Regre, PatchTST, TimesNet |
| Global attention | Pointwise tokens attending over the full context | Transformer |
| Decomposition | Explicit trend, seasonal, or spectral split | Autoformer, DLinear, FITS, FreMLP |
| Linear and MLP | Linear or MLP maps along time | Linear, MLinear, NBeats, TSMixer |
| Probabilistic | Sampled futures | CSDI |
| Floor | No learning | Seasonal naive |

**DECISION D4: where DLinear, FITS, and FreMLP sit.** They are linear or MLP maps that also perform an explicit decomposition or spectral transform. Pick one rule and apply it everywhere. The recommended rule: group by the operation that defines the model's inductive bias, which places them under Decomposition.

Every plotting script reads group membership and colors from this YAML so text, figures, and tables cannot disagree again (R1.2/R2.2).

### P2.6 Runs

- TimesNet and TSMixer on every existing synthetic paradigm: clean, noise, shift, state transition, and the redesigned Markov paradigm from Phase 4. Noise and shift are test-only on clean checkpoints, as before.
- Two extra seeds for the existing 11 models on clean, state transition, and Markov, so every model has three seeds (R4.6).
- Regenerate Figs. 3 to 9 and the Pareto analysis with the full roster.

Acceptance: the regenerated Fig. 3 reproduces the paper's seed-2021 numbers for the original 11 models before new models are added, which confirms that the refactor changed nothing.

---

## Phase 3: Tier 2 transient-rich synthetic signals (Priority 3)

Tier 1, the current narrowband generators, stays unchanged because analytic phase and frequency ground truth require narrowband components. Tier 2 adds sharp transients and evaluates them with transient metrics. Hilbert phase is not reported on Tier 2 raw waveforms; that trade-off is stated in Methods as a design choice.

### P3.1 Sampling rate and windows

**DECISION D5.** Transients cannot exist at 10 Hz because a QRS complex lasts roughly 80 to 100 ms. Recommendation: `fs = 50 Hz` with `seq_len = 250` and `pred_len = 500`, which keeps the same 5 s history and 10 s horizon in seconds. Real-data Track B uses the same settings. Check memory for Transformer and Autoformer at `seq_len + pred_len = 750` in a pilot, and reduce `d_model` for those two only if needed, documenting it.

### P3.2 ECG generator

**DECISION D6: sum-of-Gaussians dynamical ECG model or narrow transients on the current baseline.** Recommendation: the dynamical model of McSharry et al., IEEE Transactions on Biomedical Engineering, 2003, which produces P, Q, R, S, and T waves as Gaussian events on a limit cycle and has RR variability built in.

- File: `Bio_Synthesize/Synthetic_Signals_bio/tier2_ecg_dynamical.py`
- Fit wave amplitudes, widths, and angular positions to MIT-BIH beats with the existing PyTorch box-constrained fitting approach in `Bio_Synthesize/Parametric_Fitting/`, then sample from the fitted ranges.
- Save ground-truth R-peak times and amplitudes with each signal in a sidecar `.json`, so peak metrics are exact rather than detector-dependent.
- Hash-based uniqueness and 70/10/20 split, same as Tier 1.

### P3.3 EEG generator

- File: `Bio_Synthesize/Synthetic_Signals_bio/tier2_eeg_spikes.py`
- Background: the existing narrowband oscillation.
- Transients: biphasic spikes built as a difference of two Gaussians or a single Mexican-hat cycle, plus optional spike-and-slow-wave complexes, with durations of 20 to 70 ms for spikes and 70 to 200 ms for sharp waves. Event times follow a Poisson process whose rate is a sampled parameter.
- Sampling rate for EEG Tier 2 follows from D5; if spikes need finer resolution, use 100 Hz for EEG only and state it.
- Save event times, polarity, and amplitude as ground truth.

### P3.4 PPG

**DECISION D7: PPG in or out of Tier 2.** Recommended in, cheaply: a two-Gaussian pulse per beat for the systolic peak and dicrotic wave, driven by the same RR process as the ECG generator.

### P3.5 Metrics and paradigms

- Metrics: peak timing error in ms, peak amplitude error, detection F1 within a 50 ms tolerance, RR interval error, plus MAE. Frequency error still applies to the beat rate.
- Paradigms: clean and noise are the minimum. Add a heart-rate step change as a Tier 2 state transition if time allows, since it pairs with AF onset on real data.

### P3.6 Analyses

- Does the locality advantage hold on transient timing? Bias-group comparison on peak timing error with the Phase 5 statistics.
- Does Tier 2 ranking agree with Tier 1 ranking, and which one better predicts real Track B ranking from Phase 1? This is the strongest reply to R4.4: if Tier 1 already predicts real rankings, the simplification was in the right places; if only Tier 2 does, that is reported.

Acceptance: a figure showing a real MIT-BIH beat next to a generated Tier 2 beat, generator unit tests confirming saved peak times match `argmax` of the generated waveform within one sample, and complete runs for every model with three seeds.

---

## Phase 4: Markov paradigm redesign (R3.2 to R3.5, R4.7)

First confirm A4 and A5 from the Redtail launch scripts actually used for the paper, and write the answer into the Decision Log. If training was per-`p` or switching was per-sample, which A3 already confirms, the paradigm is regenerated as follows.

### P4.1 Dwell-time parameterization

- Replace per-sample `p` with an expected dwell time `D` in seconds, and set `p = 1 / (fs * D)`.
- **DECISION D8: dwell times.** Recommendation: `D in {2, 5, 10}` s. At 10 Hz and 1 Hz carriers, this gives 2 to 10 oscillation cycles per state, and with a 10 s horizon it gives roughly 5, 2, and 1 expected switches.
- Keep the well-separated frequency bands from Eq. A7, which the code already implements correctly.

### P4.2 Pooled training

- Generate all dwell times into one training pool, with `D` stored in `meta.parquet` but never given to the model. Test separately per `D`.
- This makes the task valid in Reviewer 3's sense: the model must infer switching statistics from the history.

### P4.3 Transition-matrix divergence

- Fit the two-state HMM probe to decoded features of the true futures and, separately, to the predicted futures, pooled across test windows per `D` because single-window estimates are too noisy.
- Report the KL divergence rate between the two Markov chains: the stationary-weighted sum over states of the KL divergence between corresponding transition-matrix rows, computed in both directions and symmetrized. Also report the absolute error in estimated mean dwell time, which is easier to interpret.
- Remove `kl_gaussian_1d` from the reported pipeline and keep it only in an archived script.

### P4.4 Multiple futures and Figure 8

- Extend the generator so that, from a saved chain state and phase at the forecast boundary, it can simulate `K` independent continuations. Save them as `alt_futures.npy`.
- New Figure 8a: two panels showing two different true futures from the same history with the same switching statistics, plus a panel of point forecasts regressing toward a blend of the two states, plus CSDI samples.
- Quantify the regression-to-the-mean effect: the fraction of forecast time spent between the two state frequencies.

### P4.5 Framing

**DECISION D9: keep Q4 in the main text or move to the Supplement.** If the redesigned paradigm gives clean results with the probabilistic baseline, keep it in the main text. Otherwise move it to the Supplement as exploratory and keep the deterministic state-transition experiment in the main text.

---

## Phase 5: Statistics and sample-size reporting (R4.6)

- Unit of analysis is the test signal for synthetic data and the subject for real data. Average all windows within a unit before testing.
- Primary test: paired Wilcoxon signed-rank over units against the Linear baseline, Holm correction within each metric and paradigm. Report effect sizes with bootstrap 95% CIs over units.
- Seeds: report mean and standard deviation across three seeds; compute the unit-level statistic on the seed-averaged prediction error.
- Sensitivity check: a linear mixed model `metric ~ model + (1 | unit) + (1 | seed)` for the headline comparisons.
- Methods gets a table listing, for every paradigm: number of units, windows per unit, window stride, overlap fraction, number of seeds, and the test used.
- Update `Statistical_Test/*.py` to read `meta.parquet` and aggregate by `file_id` or `subject_id` before testing.

---

## Phase 6: Framing analyses (R4.2, R4.3, R1.4)

These reuse Phase 0 code on the final full-roster results.

- Final absolute-MAE dissociation with all models and seeds.
- Headline table: Kendall `tau` between MAE ranking and each fidelity ranking, per paradigm, synthetic and real.
- A list, generated from the data, of every condition where a non-local model leads or the local advantage disappears. Candidate sources already visible in the paper: NBeats and Transformer on drift-harmonic signals, MICN under deterministic transitions, and every model at extreme shift. Add any from real data and Tier 2. These are the most direct answer to "unsurprising".

---

## Phase 7: Adaptation arm (optional, R1.5/R2.5)

**DECISION D10: reframing only, or reframing plus this experiment.**

If approved, run on SPM and DPM only, with one representative model per bias group plus PatchTST to limit cost:

- Augmentation: retrain with random time-rescaling augmentation that stretches carrier frequency by a factor drawn from `[0.5, 2.0]`, then test on the existing shift buckets.
- Few-shot: fine-tune the clean checkpoint on `k in {5, 20}` windows from the target shift bucket for a fixed small number of steps.
- Report the fraction of the zero-shot gap closed per bias group. This turns the objection into a result: which biases adapt cheaply.

---

## Phase 8: Text-only items tracked here so nothing is missed

No experiments needed. Claude Code should not edit the manuscript; these are listed so the analysis outputs include what the text will need.

| Item | Reviewer | Required output from analysis |
|------|----------|-------------------------------|
| Fix Eq. A7 ranges to `[0.715, 0.861]` and `[1.081, 1.228]` Hz | R1.6/R2.6 | Print exact values from `make_well_separated_freq_ranges` into `analysis/constants.json` |
| Reposition from digital twin to forecasting benchmark | R4.1 | None |
| PatchTST grouped under local bias in every figure | R1.2/R2.2 | Figures regenerated from `bias_groups.yaml` |
| Zero-shot results framed as a lower bound on deployed performance | R1.5/R2.5 | Phase 7 numbers if run |
| Single-signal phase versus inter-signal phase | R3.1 | None, unless a multichannel real dataset is added later |
| Response letter note that TSMixer was not previously in the codebase and has now been added | R1.1/R2.1 | Commit hash of `Model/TSMixer.py` |

---

## Run matrix and compute budget

Final roster: 11 existing models, TimesNet, TSMixer, CSDI, and seasonal naive, which needs no training. Three seeds each.

| Block | Trained configurations per model-seed | Models | Seeds | Approx. training jobs |
|-------|---------------------------------------|--------|-------|----------------------|
| Synthetic Tier 1: clean for 3 families, state transition, new Markov | 5 | 14 | 3 | 210, minus about 44 already done |
| Real data Track A: PPG, ECG, optional EEG | 2 to 3 | 14 | 3 | 84 to 126 |
| Real data Track B: PPG, ECG | 2 | 13, excluding CSDI unless time allows | 3 | 78 |
| Tier 2: ECG, EEG, optional PPG | 2 to 3 | 13 | 3 | 78 to 117 |
| Adaptation arm, optional | about 6 | 6 | 3 | about 108 |

Noise and shift remain test-only on clean checkpoints, so they add inference but no training. Fill in wall-clock hours per job type after the Phase 1 pilot, then multiply out here before submitting the large arrays.

| Job type | Measured GPU hours per job | Jobs | Total |
|----------|---------------------------|------|-------|
| Small models, 10 Hz | TBD | | |
| Transformer family, 10 Hz | TBD | | |
| CSDI, 10 Hz | TBD | | |
| Any model, 50 Hz Tier 2 or Track B | TBD | | |

---

## Proposed directory additions

```
configs/
  models/*.yaml
  paradigms/*.yaml
  bias_groups.yaml
  DISCREPANCIES.md
RealData/
  download.py
  preprocess.py
  splits/*.json
  MANIFEST.md
Model/
  TSMixer.py
  CSDI.py
  SeasonalNaive.py
Bio_Synthesize/Synthetic_Signals_bio/
  tier2_ecg_dynamical.py
  tier2_eeg_spikes.py
  tier2_ppg_pulse.py
  markov_dwell_pooled.py
utils/
  fidelity.py
scripts/
  make_jobs.py
analysis/
  p0_reanalysis/
  p1_real/
  p2_baselines/
  p3_tier2/
  p4_markov/
  p5_stats/
  constants.json
tests/
  test_fidelity.py
  test_generators.py
  test_models.py
  test_loaders.py
results/            # gitignored
```

---

## Reviewer traceability

| Comment | Addressed by |
|---------|--------------|
| R1.1/R2.1 TimesNet and TSMixer | P2.1, P2.2, P2.6 |
| R1.2/R2.2 PatchTST grouping | P2.5 |
| R1.3/R2.3 Oversimplified signals | Phase 3, P1.6 item 1 |
| R1.4/R2.4 Relative MAE window | P0.4 item 1, Phase 6 |
| R1.5/R2.5 Zero-shot versus deployment | Phase 7, Phase 8 |
| R1.6/R2.6 Eq. A7 bounds | A7, Phase 8 |
| R3.1 Single-signal phase | Phase 8 |
| R3.2 Figure 8 | P4.4 |
| R3.3 Pooled or per-p training | A4, A5, P4.2 |
| R3.4 Switching too fast | A3, P4.1 |
| R3.5 Transition-matrix KL | A6, P4.3 |
| R4.1 Digital twin overuse | Phase 8 |
| R4.2/R4.3 Novelty and insight | P0.4 item 2, Phase 6 |
| R4.4 Signals too simple | Phase 3, Phase 1 |
| R4.5 No real data | Phase 1 |
| R4.6 Sample sizes and independence | A8, P1.3, Phase 5, P2.6 seeds |
| R4.7 Deterministic models on Markov | P2.3, P4.4 |

---

## Decision log

Fill these in before the dependent task starts.

| ID | Question | Recommendation | Rakib's decision | Date |
|----|----------|----------------|------------------|------|
| D0 | Revision deadline | | 2026-10-05 | 2026-09-21 |
| D1 | Real datasets | BIDMC PPG, MIT-BIH NSR; DaLiA and AFDB secondary; Sleep-EDF if time | All three modalities: PPG (BIDMC primary, DaLiA secondary), ECG (MIT-BIH NSR primary, AFDB secondary), EEG (Sleep-EDF Fpz-Cz primary) | 2026-09-21 |
| D2 | Clinical proxy | Heart-rate error from forecasts | As recommended | 2026-09-21 |
| D3 | Probabilistic baseline | CSDI | CSDI | 2026-09-21 |
| D4 | Group for DLinear, FITS, FreMLP | Decomposition | Decomposition | 2026-09-21 |
| D5 | Tier 2 sampling and windows | 50 Hz, 250 in, 500 out | As recommended | 2026-09-21 |
| D6 | Tier 2 ECG generator | McSharry dynamical model | McSharry | 2026-09-21 |
| D7 | PPG in Tier 2 | In, two-Gaussian pulse | In | 2026-09-21 |
| D8 | Markov dwell times | 2, 5, 10 s | 2, 5, 10 s | 2026-09-21 |
| D9 | Q4 in main text or Supplement | Decide after P4 results | | |
| D10 | Adaptation arm | Decide after P0.4 and P1 | | |
| C1 | Was the paper's Markov training per-p? | Check Redtail launch scripts | Yes: data live in `p_<p>/{train,val,test}` and every checkpoint is `..._TwoState_p_<p>_...` (one per p). Resolved from disk, no decision needed | 2026-09-21 |
| C2 | Which `transition_probs` list produced the paper numbers? | Check Redtail outputs | Base run `(0, 0.1, 0.5, 0.9, 1)` into `PhaseMod_Single_Freq_TwoState` plus `_Extended` run `(0.3, 0.7)`; the paper's `{0.1, 0.3, 0.5, 0.7, 0.9}` is the union minus the degenerate 0 and 1. `analysis/constants.json` | 2026-09-21 |
| C3 | TSMixer commit hash for the response letter | | `6f356a6` (Model/TSMixer.py) | 2026-09-21 |
| C5 | Cluster submission policy | | Prepare every sbatch script first, submit nothing until approved; run at most 5 jobs at a time (`max_concurrent: 5`) | 2026-09-21 |
| C4 | `Statistical_Test/shift.py` Drift_Harmonic FITS entry pointed at the SPM run | | Fixed on `revision`; Fig. 5 Drift FITS curve must be regenerated | 2026-09-21 |
