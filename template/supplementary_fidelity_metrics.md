# Supplementary: Fidelity Metric Computation Details — LaTeX

```latex
% ======================================================================
% SUPPLEMENTARY: FIDELITY METRIC COMPUTATION DETAILS
% ======================================================================

\section{Fidelity Metric Computation Details}\label{sec:supp_fidelity}

This section provides full algorithmic details for the three fidelity
metrics introduced in the main text.  All metrics are computed
per-sequence over the $H$-step forecast horizon (i.e., excluding the
history window), and the per-sequence values are aggregated via the
median when comparing models.


% ----------------------------------------------------------------------
\subsection{Amplitude Error (MAE)}\label{sec:supp_mae}

For each forecast sequence, amplitude error is computed as the mean
absolute error between the predicted and true values over the prediction
horizon:
\begin{equation}
    \text{MAE}_i = \frac{1}{H} \sum_{t=1}^{H}
        \bigl|\,\hat{y}_i(t) - y_i(t)\,\bigr|
\end{equation}
where $i$ indexes the sequence and $H = 100$ is the prediction length.
No normalisation or scaling is applied; all signals share the same
amplitude range by construction.


% ----------------------------------------------------------------------
\subsection{Frequency Error}\label{sec:supp_freq}

Frequency error quantifies the mismatch in dominant oscillation rate
between the predicted and true signals.  The estimation proceeds in
four steps.

\paragraph{Step 1: DC removal.}
The signal mean is subtracted to eliminate the zero-frequency component:
\begin{equation}
    x(t) \leftarrow x(t) - \bar{x}
\end{equation}

\paragraph{Step 2: Power spectrum.}
The one-sided power spectrum is computed via the real-valued FFT:
\begin{equation}
    X(k) = \text{FFT}_{\text{real}}(x),
    \qquad
    P(k) = |X(k)|^2,
    \qquad
    k = 0, 1, \ldots, \lfloor N/2 \rfloor
\end{equation}
where $N$ is the FFT length (equal to the signal length; no zero-padding
is applied for frequency estimation).

\paragraph{Step 3: Peak detection with parabolic refinement.}
The bin $k^*$ with maximum power (excluding the DC bin $k = 0$) is
identified.  For non-edge bins ($1 < k^* < \lfloor N/2 \rfloor$),
the frequency estimate is refined using three-point parabolic
interpolation:
\begin{equation}
    \delta = \frac{P(k^*\!-\!1) - P(k^*\!+\!1)}
             {2\bigl(P(k^*\!-\!1) - 2\,P(k^*) + P(k^*\!+\!1)\bigr)},
    \qquad
    \hat{f} = (k^* + \delta)\,\frac{f_s}{N}
\end{equation}
where $f_s$ is the sampling rate.  This provides sub-bin accuracy
without increasing the FFT length.

\paragraph{Step 4: Reliability filtering.}
An estimate is marked as unreliable (NaN) and excluded from downstream
analysis if either of the following conditions holds:
\begin{itemize}
    \item \textbf{Low total power:} $\sum_k P(k) < 10^{-8}$
          (effectively a flat or constant signal).
    \item \textbf{Diffuse spectrum:} $P(k^*) < 0.10 \cdot \sum_k P(k)$
          (no single frequency dominates; the signal lacks a clear
          periodicity).
\end{itemize}
Both thresholds are applied identically to the true and predicted
signals.

\paragraph{Per-sequence frequency error.}
If both estimates are reliable:
\begin{equation}
    \Delta f_i = |\hat{f}_{\text{pred},i} - \hat{f}_{\text{true},i}|
\end{equation}
If either estimate is unreliable, $\Delta f_i$ is set to NaN and
excluded.  For model-level comparisons, only sequences where \emph{all}
models under comparison have finite frequency error are retained
(intersection-valid masking), ensuring that pairwise tests are conducted
on identical sample sets.


% ----------------------------------------------------------------------
\subsection{Phase Error}\label{sec:supp_phase}

Phase error quantifies temporal misalignment between the predicted and
true signals.  The computation involves constructing the analytic signal,
extracting instantaneous phase, and averaging the phase difference over
reliable regions.

\paragraph{Step 1: Preprocessing.}
The signal mean is subtracted:
\begin{equation}
    x(t) \leftarrow x(t) - \bar{x}
\end{equation}

\paragraph{Step 2: Analytic signal via frequency-domain Hilbert transform.}
The analytic signal $z(t)$ is constructed by:
\begin{enumerate}
    \item Zero-pad the signal to length $N_{\text{fft}} = 2N$
          (pad factor $= 2$) to reduce circular convolution edge effects.
    \item Compute the FFT: $X(k) = \text{FFT}(x_{\text{padded}})$.
    \item Construct the one-sided spectral mask:
          \begin{equation}
              H(k) =
              \begin{cases}
                  1   & k = 0 \\
                  2   & 1 \leq k < N_{\text{fft}}/2 \\
                  1   & k = N_{\text{fft}}/2 \\
                  0   & k > N_{\text{fft}}/2
              \end{cases}
          \end{equation}
    \item Inverse transform and crop to the original length:
          $z(t) = \text{IFFT}(X \cdot H)\big|_{t=0}^{N-1}$.
\end{enumerate}
The real part of $z(t)$ approximates the original signal, and the
imaginary part is its Hilbert transform.  This implementation is
equivalent to \texttt{scipy.signal.hilbert} but provides explicit
control over the padding factor.

\paragraph{Step 3: Instantaneous phase extraction.}
The instantaneous phase is extracted and unwrapped for temporal
continuity:
\begin{equation}
    \varphi(t) = \text{unwrap}\!\bigl(\arg(z(t))\bigr)
\end{equation}
Unwrapping removes $2\pi$ discontinuities, producing a monotonically
evolving phase suitable for computing differences.

\paragraph{Step 4: Amplitude-based masking.}
Phase estimates are unreliable where the signal amplitude is low
(e.g., near zero crossings of a modulated signal).  A binary mask
selects only time points where the true signal has sufficient amplitude:
\begin{equation}
    \mathcal{M} = \bigl\{\,t : |z_{\text{true}}(t)|
        > \alpha \cdot \text{median}\!\bigl(|z_{\text{true}}|\bigr)
    \,\bigr\},
    \qquad \alpha = 0.2
\end{equation}
The threshold $\alpha = 0.2$ (20\% of the median instantaneous amplitude)
was chosen to exclude low-amplitude regions while retaining the majority
of the signal.  If the median amplitude is zero or non-finite, or if no
time points pass the mask, the sequence is marked NaN.

\paragraph{Step 5: Phase difference and wrapping.}
The phase difference is computed at each masked time point and wrapped
to $(-\pi, \pi]$:
\begin{equation}
    \Delta\varphi(t) = \text{wrap}_\pi\!\bigl(
        \varphi_{\text{pred}}(t) - \varphi_{\text{true}}(t)
    \bigr)
\end{equation}
where the wrapping function is:
\begin{equation}
    \text{wrap}_\pi(\theta) =
        \bigl((\theta + \pi) \bmod 2\pi\bigr) - \pi
\end{equation}

\paragraph{Step 6: Per-sequence phase error.}
The per-sequence metric is the mean absolute wrapped phase difference
over the mask, converted to degrees:
\begin{equation}
    \Delta\varphi_i = \frac{180}{\pi} \cdot
        \frac{1}{|\mathcal{M}|}
        \sum_{t \in \mathcal{M}} |\Delta\varphi(t)|
\end{equation}
As with frequency error, intersection-valid masking is applied for
model-level comparisons.


% ----------------------------------------------------------------------
\subsection{Aggregation and Statistical Comparison}\label{sec:supp_metric_aggregation}

For each metric, the per-sequence values
$\{m_i\}_{i=1}^{N_{\text{seq}}}$ are summarised by the median across
sequences.  The median is preferred over the mean because phase and
frequency error distributions are typically right-skewed with occasional
outliers from low-confidence spectral estimates.

Pairwise model comparisons use the paired per-sequence differences
(model vs.\ Linear baseline) as described in the Statistical Analysis
section.  For frequency and phase error, where NaN values arise from
reliability filtering, only sequences with finite values across
\emph{all} models under comparison are retained before computing paired
differences (intersection-valid masking).  This ensures that all models
are evaluated on exactly the same set of sequences.


% ----------------------------------------------------------------------
\subsection{Relationship Between Metrics}\label{sec:supp_metric_dissociation}

The three fidelity metrics are designed to be complementary rather than
redundant.  A model may achieve:
\begin{itemize}
    \item Low MAE but high phase error: the predicted waveform has
          correct amplitude but is temporally shifted relative to the
          true signal.
    \item Low MAE but high frequency error: the model predicts a
          smoothed or averaged waveform that minimises pointwise error
          while oscillating at the wrong rate.
    \item Low frequency error but high phase error: the model captures
          the correct oscillation rate but with a temporal offset in
          peak timing.
\end{itemize}
These dissociations are demonstrated empirically in
Fig.~\ref{fig:dissociation} (main text), where models with comparable
MAE differ by more than $60^{\circ}$ in phase error and by an order of
magnitude in frequency error.
```
