# Supplementary: Statistical Analysis Details — LaTeX

```latex
% ======================================================================
% SUPPLEMENTARY: STATISTICAL ANALYSIS DETAILS
% ======================================================================

\section{Statistical Analysis Details}\label{sec:supp_stats}


% ----------------------------------------------------------------------
\subsection{Pairwise Comparisons}\label{sec:supp_pairwise}

Per-sequence metric arrays (MAE, frequency error, phase error) were
compared across models using paired differences against the Linear
baseline.  For each model $m$ and metric, the paired difference for
sequence $i$ is:
\begin{equation}
    d_i = \text{metric}_{m,i} - \text{metric}_{\text{Linear},i}
\end{equation}

\paragraph{Paired $t$-test.}
For the clean, noise, and shift paradigms, significance was assessed
using the paired $t$-test with normal approximation:
\begin{equation}
    t = \frac{\bar{d}}{s_d / \sqrt{n}},
    \qquad
    p = 2\bigl(1 - \Phi(|t|)\bigr)
\end{equation}
where $\bar{d}$ is the mean paired difference, $s_d$ the standard
deviation, $n$ the number of paired sequences, and $\Phi$ the standard
normal CDF.  95\% confidence intervals were computed as
$\bar{d} \pm 1.96 \cdot s_d / \sqrt{n}$.

\paragraph{Wilcoxon signed-rank test.}
For state-transition analyses, where error distributions are
non-Gaussian due to the mixture of in-context and no-context conditions,
we used the Wilcoxon signed-rank test with tie correction:
\begin{enumerate}
    \item Remove zero differences.
    \item Rank the absolute values of the remaining differences,
          assigning average ranks to ties.
    \item Compute the sum of ranks for positive differences: $W^+$.
    \item Compute the $z$-statistic with tie-corrected variance:
          \begin{equation}
              z = \frac{W^+ - \mu}{\sqrt{\sigma^2}},
              \qquad
              \mu = \frac{n(n+1)}{4},
              \qquad
              \sigma^2 = \frac{n(n+1)(2n+1)}{24}
                  - \sum_g \frac{t_g^3 - t_g}{48}
          \end{equation}
          where $t_g$ is the number of ties in group $g$.
    \item Two-sided $p$-value: $p = 2(1 - \Phi(|z|))$.
\end{enumerate}


% ----------------------------------------------------------------------
\subsection{Multiple Comparison Correction}\label{sec:supp_holm}

All $p$-values within each metric and paradigm were adjusted using the
Holm step-down procedure:
\begin{enumerate}
    \item Sort the $m$ raw $p$-values in ascending order:
          $p_{(1)} \leq p_{(2)} \leq \cdots \leq p_{(m)}$.
    \item Multiply each by its rank-dependent factor:
          $\tilde{p}_{(k)} = (m - k + 1) \cdot p_{(k)}$.
    \item Enforce monotonicity:
          $p^{\text{Holm}}_{(k)} = \max\bigl(\tilde{p}_{(k)},\,
          p^{\text{Holm}}_{(k-1)}\bigr)$,
          capped at 1.0.
\end{enumerate}
The Holm procedure controls the family-wise error rate at $\alpha = 0.05$
while providing uniformly greater power than the classical Bonferroni
correction.


% ----------------------------------------------------------------------
\subsection{Intersection-Valid Masking}\label{sec:supp_masking}

For frequency and phase error, spectral reliability filtering
(Supplementary~\ref{sec:supp_freq}, \ref{sec:supp_phase}) can produce
NaN values for individual sequences.  To ensure that all models are
compared on exactly the same set of sequences, we apply
intersection-valid masking: a sequence is included in the comparison
only if \emph{all} models under evaluation have a finite (non-NaN)
value for that metric on that sequence.  This prevents differences in
sample composition from confounding pairwise comparisons.


% ----------------------------------------------------------------------
\subsection{State-Transition Adaptation Analysis}\label{sec:supp_adaptation}

\paragraph{Tag-wise paired tests.}
For the state-transition paradigm, sequences are grouped by distance
tags indicating how far the transition lies from the forecast boundary.
Tags take the form \texttt{hist\_dXX} (transition is $XX$ timesteps
before the boundary, i.e., within the observable history) and
\texttt{fut\_dXX} (transition is $XX$ timesteps after the boundary,
i.e., in the unobserved future).  The distance bins are
$XX \in \{2, 4, 6, 10, 12, 15, 20, 30, 40\}$.  Two additional tags,
\texttt{win\_no\_transition\_A} and \texttt{win\_no\_transition\_B},
denote sequences with no transition in the evaluation window, serving
as steady-state baselines.

Within each tag, a Wilcoxon signed-rank test is performed comparing
each model to the Linear baseline, with Holm correction applied
separately per tag.

\paragraph{Recovery analysis.}
Adaptation speed is characterised by the first history tag at which a
model's median phase error drops below a clinically meaningful threshold
(e.g., $20^{\circ}$).  This provides an intuitive measure of how many
timesteps of post-transition context a model requires to recover phase
fidelity.


% ----------------------------------------------------------------------
\subsection{Markov Fidelity Assessment}\label{sec:supp_hmm_method}

The HMM-based evaluation assesses whether forecasting models preserve
the temporal structure of stochastic state switching.  The full
procedure is as follows:

\begin{enumerate}
    \item \textbf{Feature extraction.}  Extract the dominant frequency
          from each window using a Welch periodogram (window $= 16$
          samples, hop $= 8$ samples, $f_s = 10$\,Hz).
    \item \textbf{Normalisation.}  Z-score normalise features across
          all sequences.
    \item \textbf{HMM fitting.}  Fit a two-state Gaussian HMM on the
          true-history features, selecting the best model across eight
          random seeds (0, 1, 2, 3, 4, 5, 10, 20) by log-likelihood.
    \item \textbf{State canonicalisation.}  Relabel states so that
          state\,0 always has the lower emission mean.
    \item \textbf{Decoding.}  Decode state sequences for both
          true-future and predicted-future using the fitted HMM.
    \item \textbf{Switching probability.}  Compute the windowed
          switching probability (flip rate) for each decoded sequence.
    \item \textbf{Distributional fit.}  Fit Gaussian distributions to
          the switching-probability distributions of true-history and
          predicted-future.
    \item \textbf{Comparison.}  Compare distributions via symmetric KL
          divergence:
          \begin{equation}
              \mathrm{KL_{sym}} = \mathrm{KL}(P\|Q) + \mathrm{KL}(Q\|P)
          \end{equation}
          where, for univariate Gaussians:
          \begin{equation}
              \mathrm{KL}(P\|Q) = \ln\!\frac{\sigma_Q}{\sigma_P}
              + \frac{\sigma_P^{2} + (\mu_P - \mu_Q)^{2}}
                     {2\,\sigma_Q^{2}} - \frac{1}{2}
          \end{equation}
\end{enumerate}

A model is classified as \emph{capturing} the switching dynamics at a
given transition probability if $\mathrm{KL_{sym}} < 0.05$.


% ----------------------------------------------------------------------
\subsection{Pareto Frontier Construction}\label{sec:supp_pareto}

Models were scored across five evaluation paradigms: clean accuracy,
noise robustness, shift robustness, state-transition adaptation, and
Markov fidelity.  Within each paradigm, scores were computed as the
aggregate improvement over the Linear baseline (averaged across signal
families and fidelity metrics), then min--max normalised to $[0, 1]$
across models so that a score of 1.0 corresponds to the best-performing
model on that paradigm and 0.0 to the worst.

A model $A$ is said to \emph{dominate} model $B$ if $A$ scores greater
than or equal to $B$ on all five paradigms and strictly greater on at
least one.  The \emph{Pareto frontier} consists of all non-dominated
models---those for which no other model achieves uniformly equal or
better performance.  Models not on the frontier are classified as
\emph{dominated}, meaning at least one frontier model matches or exceeds
them on every paradigm.
```
