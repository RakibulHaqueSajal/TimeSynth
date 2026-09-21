# P0.4: what survives, and what has to be reframed

Companion to the auto-generated `SUMMARY.md` (numbers) in this folder. Seed 2021 only,
12 original models, three signal families. Everything below is computed from the paper's
own saved predictions; nothing was retrained.

## Claim 1: "Architectures with similar MAE differ in temporal fidelity" (R1.4 / R2.4)

**Does not survive at the sequence level.** For narrowband signals, phase and frequency error
are almost deterministic functions of the per-window MAE. When windows from all models are
pooled and binned by relative MAE (`MAE / A_rms`), the bias groups sit within a few degrees
of each other inside every low and mid bin:

| rel. MAE bin (all signals) | Local | Global | Decomposition | Linear/MLP |
|---|---|---|---|---|
| [0.00, 0.05) | 1.05 deg | 1.58 | 0.39 | 0.16 |
| [0.05, 0.10) | 3.18 | 2.64 | 1.38 | 3.16 |
| [0.10, 0.20) | 5.84 | 3.30 | 6.83 | 6.47 |
| [0.20, inf) | 12.4 | 65.5 | 63.7 | 54.8 |

In the lowest bin the local group actually has *higher* phase error than the Linear/MLP
group. The only bin with a large group effect is `[0.20, inf)` (file-level epsilon-squared
0.63), and that bin is where the non-local models' catastrophic windows live. The Kruskal-Wallis
tests are significant in most bins because n is enormous, but the effect sizes in the low bins
are small (eps2 0.01 to 0.13 at the file level, except Drift phase in the lowest bin, 0.48,
where the *non-local* group is better).

The reviewers' absolute window (MAE in [0, 0.03]) gives eps2 0.13 to 0.63, but the bins are
not matched: on DPM **only the four local models ever produce a window with rel. MAE below
0.2**, and on SPM the Global group never does (see the occupancy table in `SUMMARY.md`). A
"comparable-MAE" comparison on those families compares local models with themselves.

The paper's model-level slab confirms the reviewers' suspicion on Drift: the 49 deg gap between
family means inside the slab collapses to 1.1 deg when Autoformer is removed. On SPM (33 deg)
and DPM (54 deg) the gap survives Autoformer's removal, because DLinear and FITS sit inside the
slab with large phase error. So the model-level finding is real for SPM/DPM, but it is not a
dissociation at matched error; it is a statement about *error distributions*.

**Reframing that the data support:** local models achieve near-perfect windows far more often,
and their failures are bounded, whereas linear, decomposition and attention models have a heavy
tail of windows with phase errors near 60 to 90 deg. Mean MAE, which saturates at about
2 A_rms, compresses that tail; phase error, which is bounded at 180 deg, does not. Fidelity
metrics therefore expose *which windows fail and how*, not a hidden property of good windows.
The absolute-MAE window analysis should be reported with this interpretation, and the word
"dissociation" should be dropped or redefined.

## Claim 2: "MAE is insufficient to rank models" (R4.2 / R4.3)

**Survives under distribution shift, partly under noise, not on clean data.** Kendall tau between
the ranking by mean MAE and the ranking by mean phase / frequency error (20 test signals,
bootstrap CI over signals):

| paradigm | mean tau | range |
|---|---|---|
| clean | 0.80 | 0.70 to 0.94 |
| noise (SNR 1 to 6) | 0.71 | 0.18 to 1.00 |
| shift (out-of-distribution buckets) | 0.08 | -0.55 to 0.39 |

On clean data MAE orders the 12 models almost exactly as phase error does (tau 0.76 to 0.94, all
CIs above 0.5). The exceptions are DPM frequency error under mild noise (tau 0.18 to 0.27, CI
includes 0) and every out-of-distribution shift bucket, where the correlation is zero or negative
and no permutation test rejects tau = 0. This is the quantitative headline: **under frequency
shift, the model that minimizes MAE is unrelated to the model that preserves phase or
frequency.** The Results text should lead with the shift numbers and state plainly that on
clean data MAE and fidelity agree.

## Claim 3: "Local receptive fields give the best fidelity" (R4.6, sample size)

**Survives.** Re-testing every model against Linear with the test signal as the unit
(n = 20, Wilcoxon signed-rank, Holm within signal and metric): all 36 local-model cells
(4 models x 3 signals x 3 metrics) remain significant with paired effect sizes dz between 1.4
and 9.8. Of the 99 window-level significant comparisons, 80 survive; the 19 that do not are
small-effect comparisons (DLinear, FITS, MLinear, FreMLP, Transformer on frequency error)
where the window-level test was reporting overlap-inflated significance. Those 19 cells
should be described as "no reliable difference from Linear" in the revision.

Conditions where a non-local model leads (for Phase 6's list): on Drift-harmonic signals
NBeats is the best model on all three metrics, and FreMLP matches the local group; on SPM
NBeats ties the local group. Locality is therefore sufficient but not necessary on the two
simpler families; it is necessary only on DPM, where every non-local model has a heavy failure
tail.

## Bug found in the paper pipeline

`Statistical_Test/shift.py` registered the *SPM* FITS run as the Drift-harmonic FITS run, so
the FITS curve in the Drift-harmonic panel of the shift figure was computed on the wrong
predictions. Fixed on the `revision` branch; the figure must be regenerated.

## Consequences for Phases 1 to 3

1. The real-data validation (Phase 1) should test rank transfer *and* the shape-of-error claim:
   fraction of near-perfect windows and size of the failure tail per bias group.
2. The headline table for Phase 6 is the Kendall-tau table by paradigm, with the shift row as
   the lead.
3. The absolute-MAE binning code (`analysis/p0_reanalysis/run.py::dissociation`) is ready to
   be rerun on the full roster and three seeds; expect the same picture.
4. Decision D9/D10 inputs: the clean-data story is weaker than the paper implies, so the
   adaptation arm (Phase 7) becomes more valuable, since shift is where fidelity metrics
   matter.
