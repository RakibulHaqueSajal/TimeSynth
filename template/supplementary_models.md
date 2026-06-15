# Supplementary: Forecasting Model Architectures and Hyperparameters — LaTeX

```latex
% ======================================================================
% SUPPLEMENTARY: FORECASTING MODEL ARCHITECTURES AND HYPERPARAMETERS
% ======================================================================

\section{Forecasting Model Architectures and Hyperparameters}\label{sec:supp_models}

We benchmarked 11 forecasting models spanning four architectural families.
All models were configured for univariate forecasting with an input
sequence length of 50 time steps and a prediction horizon of 100 time
steps.  Each model was trained independently on each signal type and
evaluation paradigm using the AdamW optimiser with OneCycleLR scheduling,
MSE loss, and early stopping on validation loss.  Below we describe each
family and report architecture-specific hyperparameters.


% ----------------------------------------------------------------------
\subsection{Linear Models}\label{sec:supp_linear}

To evaluate linear approaches, we consider three representative models.
The first is a basic \textbf{Linear} model, which applies a single linear
layer mapping from the input sequence to the prediction horizon, serving
as the simplest baseline.  The second is \textbf{DLinear}~\cite{zeng2023transformers},
which decomposes the input into trend and seasonal components using a
moving average kernel before applying separate linear transformations to
each component.  The third is \textbf{FITS}~\cite{xu2023fits}, which
operates in the complex frequency domain, interpolating low-frequency
components to generate forecasts.  All three models use Reversible Instance
Normalisation (RevIN) to handle distribution shift.  The hyperparameters
for the linear family are reported in Table~\ref{tab:hp_linear}.

\begin{table}[ht]
\centering
\caption{Training hyperparameters for linear-family models.}
\label{tab:hp_linear}
\begin{tabular}{lccc}
\toprule
\textbf{Hyperparameter} & \textbf{Linear} & \textbf{DLinear} & \textbf{FITS} \\
\midrule
Training epochs          & 300    & 300    & 300    \\
Learning rate            & 0.0001 & 0.0001 & 0.0001 \\
Weight decay             & 0.001  & 0.001  & 0.001  \\
Batch size               & 128    & 128    & 128    \\
Patience                 & 70     & 70     & 70     \\
LR schedule              & OneCycleLR & OneCycleLR & OneCycleLR \\
RevIN                    & Yes    & Yes    & Yes    \\
Decomposition kernel     & --     & 25     & --     \\
Cutoff frequency         & --     & --     & 15\,Hz \\
\bottomrule
\end{tabular}
\end{table}


% ----------------------------------------------------------------------
\subsection{MLP-Based Models}\label{sec:supp_mlp}

For MLP-based models, we begin with \textbf{MLinear}, a two-layer
multilayer perceptron with hidden dimensions [256, 512] and dropout
regularisation, serving as a nonlinear baseline.  We then consider
\textbf{N-BEATS}~\cite{oreshkin2019n} (Neural Basis Expansion Analysis
for Time Series), which introduces a deep architecture with backward and
forward residual links organised into stacks of fully connected blocks.
Each block produces both a backcast (reconstruction of the input) and a
forecast, enabling interpretable decomposition.  N-BEATS is the only model
in our benchmark that produces an explicit backcast output.  Finally, we
evaluate \textbf{FreMLP} (FreTS)~\cite{yi2023frequency}, a frequency-domain
MLP that operates in two stages: domain conversion, which maps time-domain
signals into complex-valued frequency components via FFT, and frequency
learning, where redesigned MLPs jointly learn the real and imaginary parts
of these components.  The hyperparameters for MLP-based models are
reported in Table~\ref{tab:hp_mlp}.

\begin{table}[ht]
\centering
\caption{Architectural and training hyperparameters for MLP-based models.}
\label{tab:hp_mlp}
\begin{tabular}{lccc}
\toprule
\textbf{Hyperparameter} & \textbf{MLinear} & \textbf{N-BEATS} & \textbf{FreMLP} \\
\midrule
Number of layers        & 2         & 5 per block & 2       \\
Number of blocks        & --        & 6           & --      \\
Hidden dimensions       & 256, 512  & 256, 512    & 256     \\
Embed size              & --        & --          & 128     \\
Activation              & GELU      & ReLU        & ReLU    \\
Block type              & --        & Generic     & --      \\
Backcast                & No        & Yes         & No      \\
MLP dropout             & 0.3       & 0.3         & 0.3     \\
Weight decay            & 0.0001    & 0.0001      & 0.0001  \\
Learning rate           & 0.0001    & 0.0001      & 0.0001  \\
Training epochs         & 300       & 300         & 300     \\
Patience                & 30        & 30          & 30      \\
Batch size              & 128       & 128         & 128     \\
LR schedule             & OneCycleLR & OneCycleLR & OneCycleLR \\
\bottomrule
\end{tabular}
\end{table}


% ----------------------------------------------------------------------
\subsection{CNN-Based Models}\label{sec:supp_cnn}

For CNN-based models, we evaluate \textbf{ModernTCN}~\cite{luo2024moderntcn}
and \textbf{MICN}~\cite{wang2023micn}.  ModernTCN is a temporal convolutional
architecture featuring depthwise separable convolutions, residual connections,
and structural reparameterisation that fuses large and small kernels during
inference to efficiently capture both short- and long-range temporal
dependencies.  MICN (Multi-scale Isometric Convolution Network) employs a
multi-branch structure to capture diverse temporal patterns: local features
are extracted through downsampling convolutions, while global dependencies
are modelled using isometric convolutions with linear complexity in sequence
length.  We consider both \textbf{MICN-Mean} and \textbf{MICN-Regre}, which
implement different strategies for handling trend-cyclical components:
MICN-Mean uses the mean of the decomposed trend for prediction, while
MICN-Regre applies a regression-based approach.  The hyperparameters for
CNN-based models are reported in Table~\ref{tab:hp_cnn}.

\begin{table}[ht]
\centering
\caption{Architectural and training hyperparameters for CNN-based models.}
\label{tab:hp_cnn}
\begin{tabular}{lcc}
\toprule
\textbf{Hyperparameter} & \textbf{ModernTCN} & \textbf{MICN} \\
\midrule
Number of blocks        & [2, 2, 2, 2]        & --             \\
Large kernel sizes      & [21, 19, 17, 13]    & --             \\
Small kernel sizes      & [3, 3, 3, 3]        & --             \\
Embedding dims          & [64, 128, 256, 512]  & --             \\
FFN ratio               & 4                   & --             \\
Patch size / stride     & 20 / 10             & --             \\
Conv kernels            & --                  & [7, 17]        \\
Decomposition kernels   & --                  & [25, 49]       \\
Isometric kernels       & --                  & [17, 49]       \\
Hidden dimensions       & --                  & 256, 512       \\
Label length            & --                  & 50             \\
Trend prediction mode   & --                  & Regre / Mean   \\
Dropout                 & 0.2                 & --             \\
Head dropout            & 0.1                 & --             \\
MLP dropout             & --                  & 0.3            \\
Learning rate           & 0.001               & 0.0001         \\
Weight decay            & 0.001               & 0.0001         \\
Training epochs         & 300                 & 300            \\
Patience                & 30                  & 30             \\
Batch size              & 128                 & 128            \\
LR schedule             & OneCycleLR          & OneCycleLR     \\
\bottomrule
\end{tabular}
\end{table}


% ----------------------------------------------------------------------
\subsection{Transformer-Based Models}\label{sec:supp_transformer}

For transformer-based models, we evaluate three variants.  As a baseline,
we include a standard \textbf{Transformer} adapted for time series
forecasting with an encoder-decoder architecture.  We then consider
\textbf{Autoformer}~\cite{wu2021autoformer}, which replaces the
self-attention mechanism with an auto-correlation module to better capture
long-range periodic dependencies and incorporates series decomposition
within the architecture.  Finally, we evaluate
\textbf{PatchTST}~\cite{nie2022time}, which processes time series by
dividing them into patches and applying transformer encoders over these
patch-level representations, enabling localised attention patterns.
For the Transformer and Autoformer, half of the history window (25 time
steps) was used as the label length to warm up the decoder.  PatchTST
uses 3 encoder layers (compared to 2 for the other transformer variants)
and does not require a decoder.  The hyperparameters for transformer-based
models are reported in Table~\ref{tab:hp_transformer}.

\begin{table}[ht]
\centering
\caption{Architectural and training hyperparameters for transformer-based models.}
\label{tab:hp_transformer}
\begin{tabular}{lccc}
\toprule
\textbf{Hyperparameter} & \textbf{PatchTST} & \textbf{Autoformer} & \textbf{Transformer} \\
\midrule
Encoder layers      & 3      & 2      & 2      \\
Attention heads     & 8      & 8      & 8      \\
Embed dimension     & 256    & 256    & 256    \\
Feed-forward dim    & 256    & 256    & 256    \\
Dropout             & 0.2    & 0.2    & 0.2    \\
FC dropout          & 0.2    & 0.2    & 0.2    \\
Head dropout        & 0.2    & 0.2    & 0.2    \\
Patch length        & 15     & --     & --     \\
Stride              & 10     & --     & --     \\
Label length        & --     & 25     & 25     \\
Factor              & --     & --     & 3      \\
RevIN               & Yes    & Yes    & Yes    \\
Decomposition       & No     & No     & No     \\
Training epochs     & 300    & 300    & 300    \\
Patience            & 30     & 30     & 30     \\
Learning rate       & 0.0001 & 0.0001 & 0.0001 \\
Weight decay        & 0.0001 & 0.0001 & 0.0001 \\
Batch size          & 128    & 128    & 128    \\
LR schedule         & OneCycleLR & OneCycleLR & OneCycleLR \\
\bottomrule
\end{tabular}
\end{table}

The hyperparameters across different signal families were largely
consistent, with only minor adjustments applied to the learning rate
and weight decay.  Each model was trained independently on each signal
type and evaluation paradigm to ensure fair comparison.
```
