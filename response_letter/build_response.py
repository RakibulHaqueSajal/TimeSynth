#!/usr/bin/env python3
"""
Build the response-to-reviewers PDF from the revision's results.

Every number quoted here is produced by the analysis scripts in analysis/ and is traceable to a
CSV in that tree; the provenance is listed in the appendix of the generated document.

Usage: python response_letter/build_response.py
"""
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "Review_Response.pdf")

NAVY = colors.HexColor("#16356c")
BLUE = colors.HexColor("#2a5fa0")
GRAY = colors.HexColor("#555555")
LIGHT = colors.HexColor("#f2f5fa")

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontSize=15, textColor=NAVY, spaceBefore=16,
                    spaceAfter=8, leading=19)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontSize=11.5, textColor=NAVY, spaceBefore=13,
                    spaceAfter=5, leading=15)
QUOTE = ParagraphStyle("Quote", parent=ss["BodyText"], fontSize=9.2, textColor=GRAY,
                       fontName="Helvetica-Oblique", leftIndent=10, rightIndent=10,
                       spaceAfter=7, leading=12.5)
BODY = ParagraphStyle("Body", parent=ss["BodyText"], fontSize=9.8, leading=13.6,
                      alignment=TA_JUSTIFY, spaceAfter=6)
LABEL = ParagraphStyle("Label", parent=ss["BodyText"], fontSize=9.8, textColor=BLUE,
                       fontName="Helvetica-Bold", spaceAfter=2, leading=13)
CELL = ParagraphStyle("Cell", parent=ss["BodyText"], fontSize=8.3, leading=10.8, spaceAfter=0)
CELLB = ParagraphStyle("CellB", parent=CELL, fontName="Helvetica-Bold")
TITLE = ParagraphStyle("Title2", parent=ss["Title"], fontSize=18, textColor=NAVY, spaceAfter=4)
SUB = ParagraphStyle("Sub", parent=ss["BodyText"], fontSize=10.5, textColor=BLUE,
                     fontName="Helvetica-Oblique", spaceAfter=14, alignment=1)

story = []


def para(txt, style=BODY):
    story.append(Paragraph(txt, style))


def comment(tag, heading, quoted, response, changes):
    block = [Paragraph(f"{tag}: {heading}", H2), Paragraph(quoted, QUOTE),
             Paragraph("Response", LABEL), Paragraph(response, BODY),
             Paragraph("Changes", LABEL), Paragraph(changes, BODY)]
    story.append(KeepTogether(block[:4]))
    story.extend(block[4:])


def table(rows, widths, header=True):
    data = [[Paragraph(c, CELLB if (header and i == 0) else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * inch for w in widths], hAlign="LEFT")
    style = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b9c4d6")),
             ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
             ("TOPPADDING", (0, 0), (-1, -1), 3.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5)]
    if header:
        style += [("BACKGROUND", (0, 0), (-1, 0), LIGHT), ("TEXTCOLOR", (0, 0), (-1, 0), NAVY)]
    t.setStyle(TableStyle(style))
    story.append(t)
    story.append(Spacer(1, 8))


# ---------------------------------------------------------------- front matter
para("Response to Reviewers", TITLE)
para("TimeSynth: a temporal fidelity benchmark for physiological signal forecasting", SUB)

para("We thank the reviewers for a set of comments that were unusually specific and, in several "
     "places, correct about matters we had not checked ourselves. Acting on them led us to find "
     "three defects in our own code, one of which changes published numbers. We report those "
     "first, because they affect how the rest of this letter should be read.")

para("Summary of the revision", H2)
table([["What the revision adds", "Scale"],
       ["Validation on real recordings: PPG (BIDMC, PPG-DaLiA), ECG (MIT-BIH NSR, MIT-BIH AF), "
        "EEG (Sleep-EDF), two preprocessing tracks", "420 trained models, 5 datasets, 3 modalities, 3 seeds"],
       ["New baselines: TimesNet, TSMixer, CSDI (probabilistic), seasonal-naive floor", "4 models added to the roster"],
       ["Redesigned Markov paradigm with dwell-time control and pooled training", "135 evaluations, D in {2, 5, 10} s"],
       ["Tier 2 transient-rich generators (ECG with QRS, biphasic EEG spikes, PPG pulse)", "3 corpora with exact event ground truth"],
       ["Subject-level and signal-level statistics with non-overlapping test windows", "14 paradigm tables, 3 seeds throughout"],
       ["Adaptation arm: time-rescaling augmentation and few-shot fine-tuning", "implemented"]],
      [3.3, 3.1])

para("Corrections to the published results", H2)
para("<b>1. Ground-truth leakage in the published MICN runs.</b> Our data loader sets its own "
     "<font face='Courier'>label_len</font> to zero, so the target tensor contains only the "
     "forecast horizon. The training loop nevertheless builds the decoder input as "
     "<font face='Courier'>cat([batch_y[:, :args.label_len, :], zeros])</font>, and our MICN "
     "launch scripts passed <font face='Courier'>--label_len 50</font>. MICN was therefore given "
     "the first 50 samples, five seconds, of the ten-second target at training and at test time. "
     "We verified that those values are bit-identical to the ground truth. With the leak removed, "
     "MICN's mean absolute error on dual phase modulation rises from 0.0133 to 0.0712. All MICN "
     "numbers in the revision are leak-free, and the affected published values are corrected.")
para("<b>2. The transformer family never used time features.</b> The embedding applied its "
     "temporal component only when the encoder input had exactly 125 steps. Every published run "
     "used a 50-sample history, so the encoder saw 25 steps and the branch was never taken. The "
     "Supplement is corrected to state that Transformer, Autoformer and TimesNet use value and "
     "positional embeddings only.")
para("<b>3. A figure used the wrong run.</b> The frequency-shift analysis registered the "
     "single-phase-modulation FITS run under the drift-harmonic family. That curve is regenerated.")
para("None of these affect the real-data experiments, which were trained from scratch under the "
     "revised protocol.")

story.append(PageBreak())

# ---------------------------------------------------------------- reviewers 1 and 2
para("Response to Reviewers 1 and 2", H1)

comment("R1.1 / R2.1", "Omission of TimesNet and TSMixer",
        "The claim that architecture determines fidelity is weakened by omitting TimesNet and "
        "TSMixer, which exist in the codebase; TimesNet directly tests the localized-processing "
        "hypothesis.",
        "We accept the substance and correct one point of fact. TimesNet was implemented and "
        "registered in the model table but never evaluated, which was an omission on our part. "
        "TSMixer was not in fact present in the codebase; there is no implementation of it in the "
        "released version. We have now implemented TSMixer following Chen et al., TMLR 2023, with "
        "time-mixing and feature-mixing blocks, residual connections and reversible instance "
        "normalisation, and we note in the Supplement that feature mixing is degenerate for "
        "univariate input. We agree that TimesNet is the sharper test of the locality hypothesis, "
        "since its two-dimensional convolution over inferred periods is an independent route to "
        "local processing, and it is now evaluated on every paradigm. We also added two baselines "
        "the reviewers did not ask for but which the comments imply: CSDI as a probabilistic "
        "baseline, and a seasonal-naive floor that repeats the last dominant period. The floor "
        "turned out to be one of the most informative additions to the paper, as described under "
        "R4.2 and R4.3.",
        "<font face='Courier'>Model/TSMixer.py</font> added and registered; TimesNet, TSMixer, "
        "CSDI and the seasonal-naive floor evaluated with three seeds. TimesNet is expensive on "
        "our largest training sets, about 95 minutes per epoch, and a small number of its "
        "configurations did not complete within the cluster wall clock; these are listed as "
        "missing rather than imputed.")

comment("R1.2 / R2.2", "PatchTST grouped with Transformers",
        "The text attributes PatchTST's success to a localized bias, yet figures group it with "
        "Autoformer as a Transformer, conflating architecture family with inductive bias.",
        "The reviewers are right, and the inconsistency came from figures and text being "
        "maintained separately. We now group models by the operation that defines their inductive "
        "bias rather than by architectural lineage, and a single machine-readable file is the only "
        "source of group membership and colour for every figure and table, so text and figures "
        "cannot disagree again. PatchTST and TimesNet sit with the convolutional models under "
        "local receptive field; Autoformer joins DLinear, FITS and FreMLP under decomposition, "
        "since an explicit trend, seasonal or spectral split is what defines them.",
        "<font face='Courier'>configs/bias_groups.yaml</font> added; all plotting and statistics "
        "scripts read membership and colours from it. Figures regenerated.")

comment("R1.3 / R2.3", "Oversimplified physiological signals",
        "Gaussian EEG spikes and ECG without R-peaks strip out the sharp, non-stationary "
        "transients that matter clinically, making the data overly homogeneous.",
        "We accept this and have restructured the generators into two declared tiers rather than "
        "defending the original ones as realistic. Tier 1 keeps the narrowband oscillators, "
        "because analytic phase and frequency ground truth requires narrowband components: a sharp "
        "QRS complex has no well-defined Hilbert phase, so adding one to the Tier 1 signals would "
        "corrupt the very ground truth the benchmark exists to provide. Tier 2 adds transient-rich "
        "signals and is evaluated with transient metrics instead of phase. The Tier 2 ECG uses the "
        "dynamical model of McSharry et al., 2003, with P, Q, R, S and T waves as Gaussian events "
        "on a limit cycle; wave amplitudes, widths and angular positions were fitted to MIT-BIH "
        "normal-sinus-rhythm beats with a box-constrained optimiser, with a median coefficient of "
        "determination of 0.97 across records. EEG transients are biphasic spikes, sharp waves and "
        "spike-and-slow-wave complexes with durations of 20 to 200 milliseconds, generated by a "
        "Poisson process. PPG uses a two-Gaussian pulse driven by the same beat-interval process "
        "as the ECG. Exact event times and amplitudes are stored with every signal, so peak "
        "metrics are exact rather than detector-dependent. We also now describe the signals as "
        "physiologically parameterised oscillators rather than as realistic physiology.",
        "New generators, corpora and transient metrics (peak-timing error, peak-amplitude error, "
        "detection F1 within 50 milliseconds, inter-beat-interval error) are in place and unit "
        "tested, including a test that the stored event times match the waveform maxima to within "
        "one sample. [Numbers for the Tier 2 model sweep to be inserted once those runs complete.]")

comment("R1.4 / R2.4", "Relative comparable-MAE window",
        "The central-60 percent window is inflated by poor models such as Autoformer; within an "
        "absolute MAE window of 0.00 to 0.03, phase and frequency performance barely differ.",
        "The reviewers are correct, and this is the comment that changed our headline claim. We "
        "repeated the analysis at the level of individual sequences rather than model medians, "
        "binning every test window from every model by its error relative to signal amplitude, and "
        "also using the absolute window the reviewers propose. Within low-error bins the bias "
        "groups are separated by only a few degrees of phase, and the large separation appears "
        "only in the highest error bin. The reviewers' specific observation about Autoformer also "
        "holds: on drift-harmonic signals the gap between the best and worst bias group inside our "
        "original slab falls from 49.4 degrees to 1.1 degrees once Autoformer is excluded. We "
        "therefore no longer claim a dissociation at matched low error. The claim we can support "
        "is about the shape of the error distribution: models with local receptive fields produce "
        "near-perfect windows far more often and their failures stay bounded, whereas the other "
        "groups have a heavy tail of windows with phase errors near 60 to 90 degrees, which a mean "
        "pointwise error compresses and a phase metric does not.",
        "Phase error in degrees by bias group, within bins of error relative to signal amplitude, "
        "all three signal families pooled:")
table([["relative MAE bin", "Local receptive field", "Global attention", "Decomposition", "Linear and MLP"],
       ["0.00 to 0.05", "1.05", "1.58", "0.39", "0.16"],
       ["0.05 to 0.10", "3.18", "2.64", "1.38", "3.16"],
       ["0.10 to 0.20", "5.84", "3.30", "6.83", "6.47"],
       ["above 0.20", "12.39", "65.49", "63.65", "54.81"]],
      [1.35, 1.6, 1.25, 1.3, 1.3])
para("The relative window moves to the Supplement as a sensitivity check, reported with and "
     "without Autoformer, and Results Q1 is rewritten in the narrower terms above.")

comment("R1.5 / R2.5", "Zero-shot stress testing versus clinical practice",
        "Deployed digital twins would use online updates, calibration, or augmentation, so "
        "penalizing static models for zero-shot extrapolation may not reflect clinical utility.",
        "We agree that a static zero-shot model is not what would be deployed, and we now present "
        "the shift experiments as a lower bound on deployed performance rather than as a "
        "prediction of it. To make that more than a wording change we implemented an adaptation "
        "arm: retraining with random time-rescaling augmentation that stretches the carrier "
        "frequency, and few-shot fine-tuning on five and twenty windows from the target shift "
        "bucket, measuring the fraction of the zero-shot gap each closes per bias group. This "
        "turns the objection into a result about which inductive biases adapt cheaply.",
        "Augmentation and few-shot fine-tuning implemented in the runner and validated end to end. "
        "[Adaptation results to be inserted once those runs complete.] The shift sections are "
        "reworded as a lower bound regardless of that outcome.")

comment("R1.6 / R2.6", "Frequency bounds in Appendix A2.3",
        "Equation A7 gives f0 in [0.715, 0.861] Hz, but the text states [0.71, 0.94] Hz; f1 shows "
        "a similar mismatch.",
        "The reviewers are right and the error is in the text, not the code. Evaluating the "
        "generator's own expression gives f0 in [0.71485, 0.86145] Hz and f1 in [1.08135, 1.22795] "
        "Hz. The manuscript is corrected to these values.",
        "Appendix A2.3 corrected. The bounds are now computed directly from the generator and "
        "written to a machine-readable constants file, so the text cannot drift from the code "
        "again.")

story.append(PageBreak())

# ---------------------------------------------------------------- reviewer 3
para("Response to Reviewer 3", H1)

comment("R3.1", "Clinical relevance of single-signal phase",
        "Clinicians care about timing delays and inter-signal phase relationships such as pulse "
        "transit time or cardiorespiratory coupling; single-signal phase is neither necessary nor "
        "sufficient for these.",
        "We accept that single-signal phase is not the clinically decisive quantity and have "
        "broadened the metric set rather than defending it. The real-data evaluation adds "
        "cross-correlation lag, band-power error, beat-timing error, inter-beat-interval error and "
        "beat-detection F1 within a 50 millisecond tolerance. We also added a clinical proxy: "
        "heart rate estimated from the forecast over the ten-second horizon, compared against "
        "heart rate from the observed future. On the BIDMC PPG recordings the best achievable "
        "error is 4.3 beats per minute, which is within the range used by consumer monitoring, "
        "whereas on ambulatory PPG and on ECG it is 12 to 44 beats per minute, which is not. "
        "Inter-signal phase genuinely requires synchronised multichannel recordings, which this "
        "benchmark does not yet include; we state that as a limitation and as the natural next "
        "step rather than claiming coverage we do not have.",
        "Metrics added and reported for all real datasets; heart-rate proxy reported; the "
        "limitation on inter-signal phase is stated explicitly in the Discussion.")

comment("R3.2", "Figure 8 implies the exact stochastic future must be predicted",
        "Overlaying predicted and ground-truth futures suggests a good model reproduces one "
        "realization; the figure should show two futures sharing switching statistics.",
        "We agree, and the original figure did imply the wrong standard. The generator can now "
        "resume from the saved chain state and carrier phase at any forecast boundary and simulate "
        "independent continuations, so we store twenty alternative true futures for every test "
        "window. The replacement figure shows one history with two different realised futures that "
        "share the same switching statistics, the point forecasts regressing toward a blend of the "
        "two states, and samples from the probabilistic baseline. The caption states that the "
        "target is the distribution, not the realisation.",
        "Figure 8 replaced; alternative futures stored with the corpus; the regression toward the "
        "mean is quantified as the fraction of forecast time whose local dominant frequency lies "
        "between the two state bands.")

comment("R3.3", "Pooled or per-p training",
        "A valid predictor must infer the switching probability from the observed history at test "
        "time; were models trained on pooled data or per p?",
        "They were trained per switching probability, which makes the reviewer's objection valid: "
        "the model could infer the switching rate from its training distribution instead of from "
        "the history. We confirmed this from the data layout and the checkpoint names, one "
        "checkpoint per probability. Training is now pooled over all dwell times, with the dwell "
        "time recorded in the metadata but never given to the model, and results are reported "
        "separately per dwell time at test time.",
        "New generator writes a single pooled training and validation set with per-dwell test "
        "sets; all Markov results in the revision use pooled training.")

comment("R3.4", "Switching probabilities are too high for oscillatory states",
        "At 10 Hz with per-sample transitions, even p = 0.5 switches every other sample, "
        "destroying oscillatory cycles and producing noise-like signals.",
        "The reviewer is correct and this was a design error rather than a presentational one. The "
        "chain switched with probability p at every sample, so the mean dwell time was 1/(fs p) "
        "seconds, which for the published settings is far shorter than one cycle of the 1 Hz "
        "carrier. The paradigm has been regenerated with an explicit expected dwell time D in "
        "seconds and p = 1/(fs D), with D in 2, 5 and 10 seconds, giving two to ten carrier cycles "
        "per state and roughly five, two and one expected switches inside the ten-second horizon.",
        "Mean dwell time under the published parameterisation, at 10 Hz:")
table([["switching probability p", "0.1", "0.3", "0.5", "0.7", "0.9"],
       ["mean dwell time (s)", "1.00", "0.33", "0.20", "0.14", "0.11"],
       ["carrier cycles per state at 1 Hz", "1.0", "0.3", "0.2", "0.1", "0.1"]],
      [2.2, 0.85, 0.85, 0.85, 0.85, 0.85], header=True)

comment("R3.5", "Symmetric KL should compare transition probabilities directly",
        "Gaussian KL is unmotivated; the transition matrices of the two fitted HMMs should be "
        "compared directly.",
        "We agree and have replaced the metric. We fit a two-state hidden Markov model to decoded "
        "features of the true futures and, separately, of the predicted futures, pooled across "
        "test windows for each dwell time, and report the symmetrised Kullback-Leibler divergence "
        "rate between the two chains, that is the stationary-weighted sum over states of the "
        "divergence between corresponding rows of the transition matrices. We also report the "
        "absolute error in estimated mean dwell time, which is easier to interpret. The Gaussian "
        "divergence is retained only in an archived script.",
        "New metrics implemented and tested. They make the failure explicit: at an expected dwell "
        "of 10 seconds, against a probe-measured true dwell of 11.2 seconds, PatchTST predicts a "
        "dwell of 292.8 seconds, that is forecasts that essentially never change state, while "
        "having the lowest phase error of any model.")

story.append(PageBreak())

# ---------------------------------------------------------------- reviewer 4
para("Response to Reviewer 4", H1)

comment("R4.1", "Overuse of digital twin",
        "The work constructs no patient-specific, continuously updated replica and should be "
        "positioned as a forecasting benchmark.",
        "We accept this without reservation. The work is a forecasting benchmark with "
        "physiologically parameterised generators, not a digital twin, and the term is removed "
        "from the title, the abstract and the body except where we discuss what would be required "
        "to build one.",
        "Title and framing changed throughout; the term is retained only in the Discussion, where "
        "it names future work.")

comment("R4.2 and R4.3", "Methodological novelty and new scientific insight",
        "The components are established techniques, MAE's limits are well known in signal "
        "processing, and local models doing well on periodic signals is unsurprising.",
        "We concede each of these points and have relocated the contribution instead of disputing "
        "them. We do not claim that mean absolute error is blind to phase, which is indeed "
        "textbook; we claim that forecasting evaluation still ranks models almost entirely by "
        "pointwise error, so the consequences go unmeasured, and we now measure them. The "
        "strongest new result comes from the real-data validation the reviewer asked for. Ranking "
        "models on the synthetic benchmark by mean absolute error carries almost no information "
        "about how they rank on real recordings, while ranking the same benchmark by phase "
        "fidelity transfers four times better:",
        "")
table([["ranking metric", "mean Kendall tau, synthetic to real", "negative transfers"],
       ["mean absolute error", "0.07", "4 of 13 comparisons"],
       ["phase error", "0.28", "1 of 13"],
       ["frequency error", "0.20", "2 of 13"]],
      [1.9, 2.6, 1.9])
para("On real ECG morphology the transfer of the pointwise ranking is clearly negative, minus 0.58 "
     "and minus 0.47 against the two matched synthetic families, meaning the models that win on "
     "the synthetic benchmark are among the worst on the real signals. A synthetic benchmark is "
     "predictive of real performance only if it is scored on temporal fidelity. We report the "
     "moderate size of the positive correlation honestly: 0.28 is a useful signal, not a strong one.")
para("Two further results speak directly to the charge that our findings are unsurprising. First, "
     "a seasonal-naive forecaster that simply repeats the last dominant period is simultaneously "
     "the worst model by mean absolute error and the best by phase error on real ECG, ranking last "
     "of sixteen on one metric and first on the other; on clean PPG it beats every one of the "
     "fifteen trained architectures outright, including on beat-detection F1 and heart-rate error. "
     "Second, on the redesigned switching paradigm the five best models by pointwise error occupy "
     "five of the six worst positions by switching fidelity. Neither result is predicted by the "
     "claim that local models win on periodic signals.")
para("We also foreground the conditions where locality fails, as the reviewer invites. On "
     "Sleep-EDF electroencephalography the linear family leads and the naive floor is last, "
     "because there is no dominant period to repeat; under frequency shift the rank correlation "
     "between pointwise and fidelity rankings is approximately zero for every architecture family.")
para("The contributions are rewritten as three specific claims: closed-form generators that make "
     "error decomposable into amplitude, frequency, phase and state; a quantified ranking "
     "disagreement reported as the headline result; and a map from inductive bias to the signal "
     "properties it preserves under each stressor. The local-models-win result is presented as a "
     "hypothesis the benchmark tests rather than as a conclusion.", BODY)

comment("R4.4", "Signals are too simplified to be physiological",
        "ECG lacks the QRS complex and PPG and EEG reduce to sinusoids; fitting parameter ranges "
        "does not make signals realistic.",
        "We agree, and our answer has two parts. The first is the Tier 1 and Tier 2 split "
        "described under R1.3, which adds QRS complexes and biphasic spikes and states the "
        "trade-off that forced the original simplification. The second is the real-data validation "
        "described under R4.5, which is the direct test of whether the simplification was made in "
        "the right places. The answer there is partly reassuring and partly not: fidelity-based "
        "rankings do transfer from the synthetic families to real recordings, with a mean rank "
        "correlation of 0.28, whereas pointwise rankings do not transfer at all. We report both.",
        "Tier 2 generators and corpora added; the signals are described as physiologically "
        "parameterised oscillators; the transfer analysis is reported in full, including the "
        "comparisons where it fails.")

comment("R4.5", "No validation on real data",
        "Nothing shows the metrics or rankings transfer to real ECG, PPG, or EEG or to clinical "
        "events.",
        "This was the most consequential comment and the revision's largest addition. We now train "
        "and evaluate every model on five public datasets spanning three modalities: BIDMC and "
        "PPG-DaLiA for photoplethysmography, MIT-BIH normal sinus rhythm and MIT-BIH atrial "
        "fibrillation for electrocardiography, and Sleep-EDF for electroencephalography. Two "
        "preprocessing tracks are used, one band-limited to the dominant rhythm so that the window "
        "holds a comparable number of cycles to the synthetic benchmark, and one preserving "
        "morphology at a higher sampling rate. Splits are by subject, never by window, and all "
        "metrics are computed with the same implementations used on the synthetic data. Beyond the "
        "ranking-transfer result given under R4.2, the analysis covers clinically meaningful "
        "events: an atrial-fibrillation onset inside the observed history raises error by 53 "
        "percent and an activity change in ambulatory PPG by 56 percent, while sleep-stage "
        "transitions have no measurable effect, which is consistent with electroencephalography "
        "having no periodic structure for a transition to disrupt.",
        "420 trained models across 5 datasets, 3 modalities, 2 tracks and 3 seeds, with per-subject "
        "metrics, the ranking-transfer analysis, the natural-event analysis and the heart-rate "
        "proxy reported in a new Results section and a supplementary table.")

comment("R4.6", "Sample sizes and independence",
        "The number of test signals, window overlap, and training runs should be reported; "
        "overlapping windows treated as independent would inflate significance.",
        "The reviewer identified a real problem. The original analysis enumerated test windows "
        "with a stride of one sample, so adjacent windows shared 149 of 150 samples and were "
        "treated as independent observations in paired tests. Every evaluation in the revision "
        "uses non-overlapping test windows, with a stride equal to the history plus the horizon, "
        "and the unit of analysis is the test signal for synthetic data and the subject for real "
        "data, with all windows averaged within a unit before testing. Every model is trained with "
        "three seeds. The primary test is a paired Wilcoxon signed-rank test over units against "
        "the linear baseline with Holm correction, reported with bootstrap confidence intervals "
        "and paired effect sizes. We re-ran the published comparisons under this protocol: of 99 "
        "model-versus-baseline comparisons that were significant at the window level, 80 remain "
        "significant at the signal level, and we identify the 19 that do not. We also increased "
        "the test fraction for the two primary real datasets, because a Wilcoxon test over three "
        "subjects cannot reach significance at any effect size.",
        "A Methods table reports, for every paradigm, the number of units, windows per unit, "
        "window stride, overlap fraction, number of seeds and the test used. Overlap is zero "
        "throughout. A linear mixed model with random effects for unit and seed is reported as a "
        "sensitivity check.")

comment("R4.7", "Markov switching is unsuitable for deterministic forecasters",
        "Point forecasters cannot represent multiple stochastic futures, so their failure is "
        "expected; probabilistic methods are needed.",
        "We agree with the premise and have added CSDI, a conditional diffusion model, drawing "
        "fifty samples per window and computing switching statistics per sample. The result "
        "supports the reviewer's reasoning and also sharpens it. Deterministic models do not fail "
        "by producing a plausible but wrong realisation; they fail by refusing to change state at "
        "all. At an expected dwell of 10 seconds, against a probe-measured true dwell of 11.2 "
        "seconds, PatchTST predicts 292.8 seconds and NBeats 89.9 seconds, while the seasonal-naive "
        "floor predicts 15.8 seconds and has the lowest divergence of any model. Minimising "
        "expected pointwise error on a stochastic switching task is achieved by not committing to "
        "a state, and only a metric defined on the switching process exposes that. We report a "
        "negative result as well: our CSDI baseline does not recover the switching rate either, "
        "predicting a dwell of about 5 seconds regardless of whether the true dwell is 3 or 11 "
        "seconds. We therefore do not claim that probabilistic forecasting solves the problem, "
        "only that this diffusion baseline trained under our protocol does not.",
        "CSDI added to the roster with per-sample switching statistics; Q4 retains the paradigm "
        "with the redesigned dwell-time parameterisation and reports both the deterministic and "
        "the probabilistic outcome.")

story.append(PageBreak())
para("Provenance of the numbers in this letter", H1)
para("Every quantity quoted above is produced by a script in the revision repository and written "
     "to a file that can be regenerated from the stored predictions.")
table([["Claim", "Source"],
       ["MICN leakage and the 0.0133 to 0.0712 change",
        "analysis/p2_baselines/ACCEPTANCE_FAILURE.md, acceptance_seed2021.csv"],
       ["Phase error by bias group within error bins; Autoformer sensitivity",
        "analysis/p0_reanalysis/dissociation_groups.csv, dissociation_model_level_sensitivity.csv"],
       ["Equation A7 bounds", "analysis/constants.json"],
       ["Synthetic-to-real rank transfer", "analysis/p1_real/ranking_transfer.csv"],
       ["Seasonal-naive ranks, heart-rate proxy, natural events",
        "analysis/p1_real/supp_table_real.csv, hr_proxy.csv, natural_events.csv"],
       ["Markov dwell times and divergence rates", "analysis/p4_markov/markov_metrics.csv"],
       ["Sample sizes, overlap, seeds and tests", "analysis/p5_stats/sample_size_table.csv, paired_tests.csv"],
       ["Tier 2 generator fit quality", "Bio_Synthesize/Parametric_Fitting/tier2_ecg_fit.json"]],
      [2.9, 3.5])

doc = SimpleDocTemplate(OUT, pagesize=LETTER, leftMargin=0.85 * inch, rightMargin=0.85 * inch,
                        topMargin=0.8 * inch, bottomMargin=0.8 * inch,
                        title="Response to Reviewers: TimeSynth", author="")


def footer(canvas, doc_):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GRAY)
    canvas.drawCentredString(LETTER[0] / 2.0, 0.45 * inch, f"{doc_.page}")
    canvas.restoreState()


doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("wrote", OUT)
