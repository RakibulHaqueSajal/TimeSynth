# Supplementary: Individual Model Performance Profiles (Radar) — LaTeX

## File paths

| Figure | Full Path |
|--------|-----------|
| Radar (all models) | `/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Model_Comparison/Statistical/Radar_Plots/radar_all_models.pdf` |
| Radar (per model + Pareto) | `/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Model_Comparison/Statistical/Pareto_Frontier/pareto_per_model/pareto_per_model.pdf` |
| Pareto summary CSV | `/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Model_Comparison/Statistical/Pareto_Frontier/pareto_summary.csv` |

---

## Main text reference line

Replace:

> Individual model profiles are shown in Supplementary Fig.~16.

With:

> Individual model radar profiles across all five paradigms and the full normalised score table are provided in Supplementary Fig.~\ref{fig:supp_radar_per_model} and Supplementary Table~\ref{tab:pareto_scores}.

---

## LaTeX

```latex
% ======================================================================
% SUPPLEMENTARY: INDIVIDUAL MODEL PERFORMANCE PROFILES (RADAR)
% ======================================================================

\subsection{Individual Model Performance Profiles}\label{sec:supp_radar}

The main text summarises multi-paradigm performance via the Pareto frontier
(Fig.~\ref{fig:pareto}).  To provide a more detailed view of each
architecture's strengths and weaknesses, Figure~\ref{fig:supp_radar_all}
overlays all 11~models on a single radar chart, and
Figure~\ref{fig:supp_radar_per_model} shows individual profiles with
Pareto status annotations.

Each axis represents one of the five evaluation paradigms (clean accuracy,
noise robustness, shift robustness, state-transition adaptation, and
Markov fidelity).  Scores are min--max normalised across models (0--1
scale), where higher values indicate better performance relative to the
other architectures.  The normalised scores and Pareto classifications
are reported in Supplementary Table~\ref{tab:pareto_scores}.

\begin{figure}[ht]
\centering
\includegraphics[width=0.85\textwidth]{Figures/Statistical/radar_all_models.pdf}
\caption{\textbf{Comparative model performance across all five evaluation
paradigms.}  Radar chart overlaying all 11~models.  PatchTST (blue)
achieves the largest and most balanced polygon, dominating on four of
five axes.  NBeats (orange) shows consistently high performance but is
narrowly dominated by PatchTST.  MICN variants (green) achieve the
highest clean accuracy and noise robustness but collapse on
state-transition adaptation.  Linear-family models (cyan/light blue)
and Autoformer (grey) occupy the interior, indicating weak performance
across most paradigms.}
\label{fig:supp_radar_all}
\end{figure}

\begin{figure}[ht]
\centering
\includegraphics[width=\textwidth]{Figures/Statistical/pareto_per_model/pareto_per_model.pdf}
\caption{\textbf{Individual model performance profiles with Pareto
classification.}  Each subplot shows one model's radar profile across
five paradigms.  Solid coloured polygons denote Pareto-optimal models
(frontier); dashed grey polygons denote dominated models.  Four models
occupy the Pareto frontier: PatchTST (balanced across all five
dimensions), MICN\_Regre and MICN\_Mean (strong clean/noise performance,
weak state transition), and ModernTCN (strong state transition, weaker
noise/shift).  The remaining seven models are dominated---no paradigm
exists where they outperform all frontier members simultaneously.}
\label{fig:supp_radar_per_model}
\end{figure}

\begin{table}[ht]
\centering
\caption{\textbf{Normalised paradigm scores and Pareto classification.}
Scores are min--max normalised (0--1) across models per paradigm.
Frontier models cannot be improved on any dimension without sacrificing
another.}
\label{tab:pareto_scores}
\begin{tabular}{lccccccl}
\toprule
\textbf{Model} & \textbf{Clean} & \textbf{Noise} & \textbf{Shift}
    & \textbf{State Tr.} & \textbf{Markov} & \textbf{Mean} & \textbf{Status} \\
\midrule
PatchTST    & 0.97 & 0.98 & 1.00 & 1.00 & 1.00 & 0.99 & Frontier \\
MICN\_Regre & 1.00 & 1.00 & 0.96 & 0.54 & 0.83 & 0.86 & Frontier \\
NBeats      & 0.82 & 0.84 & 0.78 & 0.89 & 0.94 & 0.85 & Dominated \\
MICN\_Mean  & 0.99 & 0.99 & 0.96 & 0.00 & 0.82 & 0.75 & Frontier \\
FreMLP      & 0.69 & 0.75 & 0.71 & 0.91 & 0.74 & 0.76 & Dominated \\
ModernTCN   & 0.98 & 0.31 & 0.23 & 0.97 & 0.72 & 0.64 & Frontier \\
Transformer & 0.42 & 0.45 & 0.29 & 0.80 & 0.53 & 0.50 & Dominated \\
MLinear     & 0.49 & 0.53 & 0.35 & 0.51 & 0.20 & 0.42 & Dominated \\
DLinear     & 0.31 & 0.31 & 0.30 & 0.55 & 0.50 & 0.39 & Dominated \\
FITS        & 0.22 & 0.19 & 0.17 & 0.45 & 0.61 & 0.33 & Dominated \\
Autoformer  & 0.00 & 0.00 & 0.00 & 0.23 & 0.00 & 0.05 & Dominated \\
\bottomrule
\end{tabular}
\end{table}
```
