# P0.4 reanalysis of the paper's predictions (seed 2021)

Inputs: `Train_Test_Validation/` legacy folders, 12 models x 3 signals; clean (Shift_0), 
noise SNR 1-6, shift buckets 0-4. Window `file_id` reconstructed from the CSV lengths 
(`utils.results_io.legacy_file_ids`, verified against the saved array sizes). Bias groups from 
`configs/bias_groups.yaml` (D4 recommended placement).

## 1. Absolute-MAE dissociation at the sequence level (R1.4 / R2.4)

Windows from all models pooled and binned by `MAE / A_rms(true)`; inside each bin, Kruskal-Wallis 
across bias groups on phase error (deg) and frequency error (Hz). `eps2` is epsilon-squared. 
Window-level p-values treat overlapping windows as independent (they are not); the file-level 
test averages windows within each (model, test signal) first and is the one to quote.

| signal | bin (rel. MAE) | metric | n windows | eps2 (window) | units (model x file) | p (file) | eps2 (file) |
|---|---|---|---|---|---|---|---|
| Drift | [0.00, 0.05) | phase | 230714 | 0.425 | 134 | 4.05e-14 | 0.480 |
| Drift | [0.00, 0.05) | freq | 230714 | 0.061 | 134 | 1.86e-01 | 0.014 |
| Drift | [0.05, 0.10) | phase | 83733 | 0.084 | 140 | 5.05e-11 | 0.352 |
| Drift | [0.05, 0.10) | freq | 83733 | 0.016 | 140 | 8.02e-02 | 0.028 |
| Drift | [0.10, 0.20) | phase | 62522 | 0.131 | 163 | 9.17e-14 | 0.382 |
| Drift | [0.10, 0.20) | freq | 62522 | 0.035 | 163 | 2.87e-07 | 0.190 |
| Drift | [0.20, inf) | phase | 306551 | 0.287 | 240 | 2.14e-16 | 0.310 |
| Drift | [0.20, inf) | freq | 306549 | 0.256 | 240 | 1.41e-12 | 0.234 |
| SPM | [0.00, 0.05) | phase | 177 | 0.182 | 3 | nan | nan |
| SPM | [0.00, 0.05) | freq | 177 | 0.218 | 3 | nan | nan |
| SPM | [0.05, 0.10) | phase | 55072 | 0.005 | 63 | 4.97e-01 | -0.010 |
| SPM | [0.05, 0.10) | freq | 55072 | 0.047 | 63 | 7.66e-01 | -0.024 |
| SPM | [0.10, 0.20) | phase | 126726 | 0.009 | 106 | 2.34e-01 | 0.009 |
| SPM | [0.10, 0.20) | freq | 126726 | 0.025 | 106 | 8.21e-02 | 0.029 |
| SPM | [0.20, inf) | phase | 501545 | 0.326 | 216 | 4.88e-17 | 0.359 |
| SPM | [0.20, inf) | freq | 501103 | 0.268 | 216 | 4.87e-17 | 0.359 |
| DPM | [0.00, 0.05) | phase | 409 | nan | 21 | nan | nan |
| DPM | [0.00, 0.05) | freq | 409 | nan | 21 | nan | nan |
| DPM | [0.05, 0.10) | phase | 49448 | nan | 61 | nan | nan |
| DPM | [0.05, 0.10) | freq | 49448 | nan | 61 | nan | nan |
| DPM | [0.10, 0.20) | phase | 86709 | nan | 79 | nan | nan |
| DPM | [0.10, 0.20) | freq | 86709 | nan | 79 | nan | nan |
| DPM | [0.20, inf) | phase | 546954 | 0.399 | 225 | 6.07e-31 | 0.637 |
| DPM | [0.20, inf) | freq | 546641 | 0.171 | 225 | 1.07e-12 | 0.252 |
| ALL | [0.00, 0.05) | phase | 231300 | 0.425 | 135 | 5.09e-14 | 0.473 |
| ALL | [0.00, 0.05) | freq | 231300 | 0.061 | 135 | 1.55e-01 | 0.017 |
| ALL | [0.05, 0.10) | phase | 188253 | 0.024 | 141 | 1.41e-09 | 0.300 |
| ALL | [0.05, 0.10) | freq | 188253 | 0.011 | 141 | 1.42e-03 | 0.091 |
| ALL | [0.10, 0.20) | phase | 275957 | 0.039 | 163 | 3.48e-05 | 0.128 |
| ALL | [0.10, 0.20) | freq | 275957 | 0.010 | 163 | 9.57e-05 | 0.114 |
| ALL | [0.20, inf) | phase | 1355050 | 0.315 | 240 | 1.66e-32 | 0.627 |
| ALL | [0.20, inf) | freq | 1354293 | 0.201 | 240 | 6.19e-18 | 0.340 |

Group medians (window level) inside each bin:

**Drift**

| bin | metric | Local receptive field | Global attention | Decomposition | Linear and MLP | Probabilistic | Floor |
|---|---|---|---|---|---|---|---|
| [0.00, 0.05) | freq | 8.8e-05 (n=87059, 3 models) | 0.000125 (n=14894, 1 models) | 6.48e-05 (n=47601, 1 models) | 2.43e-05 (n=81160, 2 models) | - | - |
| [0.00, 0.05) | phase | 1.05 (n=87059, 3 models) | 1.58 (n=14894, 1 models) | 0.391 (n=47601, 1 models) | 0.158 (n=81160, 2 models) | - | - |
| [0.05, 0.10) | freq | 0.000307 (n=48495, 3 models) | 0.000151 (n=16543, 1 models) | 0.00024 (n=1977, 1 models) | 0.000267 (n=16718, 2 models) | - | - |
| [0.05, 0.10) | phase | 1.9 (n=48495, 3 models) | 2.64 (n=16543, 1 models) | 1.36 (n=1977, 1 models) | 2.75 (n=16718, 2 models) | - | - |
| [0.10, 0.20) | freq | 0.000263 (n=44881, 4 models) | 0.000128 (n=10469, 1 models) | 0.000336 (n=1503, 2 models) | 0.000896 (n=5669, 3 models) | - | - |
| [0.10, 0.20) | phase | 1.96 (n=44881, 4 models) | 3.3 (n=10469, 1 models) | 2.09 (n=1503, 2 models) | 5.57 (n=5669, 3 models) | - | - |
| [0.20, inf) | freq | 0.000705 (n=47405, 4 models) | 0.00144 (n=15054, 1 models) | 0.0617 (n=176757, 4 models) | 0.0296 (n=67333, 3 models) | - | - |
| [0.20, inf) | phase | 3.12 (n=47405, 4 models) | 9.68 (n=15054, 1 models) | 71.2 (n=176759, 4 models) | 46.5 (n=67333, 3 models) | - | - |

**SPM**

| bin | metric | Local receptive field | Global attention | Decomposition | Linear and MLP | Probabilistic | Floor |
|---|---|---|---|---|---|---|---|
| [0.00, 0.05) | freq | 0.000399 (n=141, 2 models) | - | - | 0.000149 (n=36, 1 models) | - | - |
| [0.00, 0.05) | phase | 1.42 (n=141, 2 models) | - | - | 1.98 (n=36, 1 models) | - | - |
| [0.05, 0.10) | freq | 0.000324 (n=41039, 3 models) | - | 0.000247 (n=51, 1 models) | 0.000155 (n=13982, 1 models) | - | - |
| [0.05, 0.10) | phase | 3.33 (n=41039, 3 models) | - | 3.63 (n=51, 1 models) | 3.49 (n=13982, 1 models) | - | - |
| [0.10, 0.20) | freq | 0.000286 (n=85321, 4 models) | - | 0.000569 (n=12049, 1 models) | 0.000337 (n=29356, 1 models) | - | - |
| [0.10, 0.20) | phase | 6.41 (n=85321, 4 models) | - | 7.04 (n=12049, 1 models) | 6.63 (n=29356, 1 models) | - | - |
| [0.20, inf) | freq | 0.000424 (n=101339, 4 models) | 0.0314 (n=56960, 1 models) | 0.00992 (n=215298, 4 models) | 0.0113 (n=127506, 3 models) | - | - |
| [0.20, inf) | phase | 13.7 (n=101339, 4 models) | 60.9 (n=56960, 1 models) | 49.9 (n=215740, 4 models) | 47.1 (n=127506, 3 models) | - | - |

**DPM**

| bin | metric | Local receptive field | Global attention | Decomposition | Linear and MLP | Probabilistic | Floor |
|---|---|---|---|---|---|---|---|
| [0.00, 0.05) | freq | 6.62e-05 (n=409, 3 models) | - | - | - | - | - |
| [0.00, 0.05) | phase | 1.92 (n=409, 3 models) | - | - | - | - | - |
| [0.05, 0.10) | freq | 0.000225 (n=49448, 4 models) | - | - | - | - | - |
| [0.05, 0.10) | phase | 3.8 (n=49448, 4 models) | - | - | - | - | - |
| [0.10, 0.20) | freq | 0.000919 (n=86709, 4 models) | - | - | - | - | - |
| [0.10, 0.20) | phase | 6.77 (n=86709, 4 models) | - | - | - | - | - |
| [0.20, inf) | freq | 0.00287 (n=91274, 4 models) | 0.0912 (n=56884, 1 models) | 0.0802 (n=227603, 4 models) | 0.0437 (n=170880, 3 models) | - | - |
| [0.20, inf) | phase | 13 (n=91274, 4 models) | 75.9 (n=56960, 1 models) | 69.5 (n=227840, 4 models) | 58.9 (n=170880, 3 models) | - | - |

**ALL**

| bin | metric | Local receptive field | Global attention | Decomposition | Linear and MLP | Probabilistic | Floor |
|---|---|---|---|---|---|---|---|
| [0.00, 0.05) | freq | 8.82e-05 (n=87609, 3 models) | 0.000125 (n=14894, 1 models) | 6.48e-05 (n=47601, 1 models) | 2.43e-05 (n=81196, 2 models) | - | - |
| [0.00, 0.05) | phase | 1.05 (n=87609, 3 models) | 1.58 (n=14894, 1 models) | 0.391 (n=47601, 1 models) | 0.159 (n=81196, 2 models) | - | - |
| [0.05, 0.10) | freq | 0.000281 (n=138982, 4 models) | 0.000151 (n=16543, 1 models) | 0.00024 (n=2028, 1 models) | 0.000191 (n=30700, 2 models) | - | - |
| [0.05, 0.10) | phase | 3.18 (n=138982, 4 models) | 2.64 (n=16543, 1 models) | 1.38 (n=2028, 1 models) | 3.16 (n=30700, 2 models) | - | - |
| [0.10, 0.20) | freq | 0.000403 (n=216911, 4 models) | 0.000128 (n=10469, 1 models) | 0.00055 (n=13552, 2 models) | 0.000365 (n=35025, 3 models) | - | - |
| [0.10, 0.20) | phase | 5.84 (n=216911, 4 models) | 3.3 (n=10469, 1 models) | 6.83 (n=13552, 2 models) | 6.47 (n=35025, 3 models) | - | - |
| [0.20, inf) | freq | 0.000803 (n=240018, 4 models) | 0.0461 (n=128898, 1 models) | 0.0407 (n=619658, 4 models) | 0.0258 (n=365719, 3 models) | - | - |
| [0.20, inf) | phase | 12.4 (n=240018, 4 models) | 65.5 (n=128974, 1 models) | 63.7 (n=620339, 4 models) | 54.8 (n=365719, 3 models) | - | - |

Reviewers' absolute window, MAE in [0, 0.03]:

| signal | metric | n windows | p (file) | eps2 (file) |
|---|---|---|---|---|
| Drift | phase | 454242 | 3.84e-12 | 0.225 |
| Drift | freq | 454240 | 7.09e-16 | 0.299 |
| SPM | phase | 305241 | 2.30e-05 | 0.157 |
| SPM | freq | 305241 | 1.52e-04 | 0.127 |
| DPM | phase | 200631 | 1.27e-15 | 0.626 |
| DPM | freq | 200396 | 2.86e-09 | 0.358 |
| ALL | phase | 960114 | 1.93e-19 | 0.370 |
| ALL | freq | 959877 | 1.72e-13 | 0.252 |

Sensitivity, the paper's model-level slab (p20-p80 of model-median MAE, Linear excluded):

| signal | variant | metric | models inside | Local receptive field | Global attention | Decomposition | Linear and MLP | Probabilistic | Floor | top - bottom |
|---|---|---|---|---|---|---|---|---|---|---|
| Drift | with_Autoformer | phase | 7 | 1.6 | 2.72 | 51 | 1.96 | - | - | 49.4 |
| Drift | with_Autoformer | freq | 7 | 0.000235 | 0.000222 | 0.0374 | 0.000269 | - | - | 0.0372 |
| Drift | without_Autoformer | phase | 6 | 1.6 | 2.72 | - | 1.96 | - | - | 1.12 |
| Drift | without_Autoformer | freq | 6 | 0.000235 | 0.000222 | - | 0.000269 | - | - | 4.71e-05 |
| SPM | with_Autoformer | phase | 7 | 6.77 | 60.9 | 39.8 | - | - | - | 54.1 |
| SPM | with_Autoformer | freq | 7 | 0.000333 | 0.0314 | 0.0131 | - | - | - | 0.0311 |
| SPM | without_Autoformer | phase | 6 | 6.77 | - | 39.8 | - | - | - | 33 |
| SPM | without_Autoformer | freq | 6 | 0.000333 | - | 0.0131 | - | - | - | 0.0127 |
| DPM | with_Autoformer | phase | 7 | 9.74 | - | 63.7 | 56.7 | - | - | 54 |
| DPM | with_Autoformer | freq | 7 | 0.00171 | - | 0.0462 | 0.0431 | - | - | 0.0445 |
| DPM | without_Autoformer | phase | 6 | 9.74 | - | 64.1 | 56.7 | - | - | 54.3 |
| DPM | without_Autoformer | freq | 6 | 0.00171 | - | 0.0412 | 0.0431 | - | - | 0.0413 |

Bin occupancy per model (windows). A bias-group comparison inside a bin is only as good as its 
coverage; models absent from a bin contribute nothing there.

```
bin                                  [0.0, 0.05)  [0.05, 0.1)  [0.1, 0.2)  [0.2, inf)
signal                  model                                                        
Drift_Harmonic          Autoformer             0            0           0       56960
                        DLinear                0            0           2       56958
                        FITS                   0            0           0       56960
                        FreMLP             47601         1977        1501        5881
                        Linear                 0            0          31       56929
                        MICN_Mean          36226        11484        1708        7542
                        MICN_Regre         49023         1932         795        5210
                        MLinear            28479        15208        4469        8804
                        ModernTCN           1810        35079       18136        1935
                        NBeats             52681         1510        1169        1600
                        PatchTST               0            0       24242       32718
                        Transformer        14894        16543       10469       15054
Dual_Phase_Modulation   Autoformer             0            0           0       56960
                        DLinear                0            0           0       56960
                        FITS                   0            0           0       56960
                        FreMLP                 0            0           0       56960
                        Linear                 0            0           0       56960
                        MICN_Mean             80        19487       27530        9863
                        MICN_Regre           320        26144       23318        7178
                        MLinear                0            0           0       56960
                        ModernTCN              9         3816       28960       24175
                        NBeats                 0            0           0       56960
                        PatchTST               0            1        6901       50058
                        Transformer            0            0           0       56960
Single_Phase_Modulation Autoformer             0            0           0       56960
                        DLinear                0            0           0       56960
                        FITS                   0            0           0       56960
                        FreMLP                 0           51       12049       44860
                        Linear                 0            0           0       56960
                        MICN_Mean             30        15757       24888       16285
                        MICN_Regre             0        12281       28980       15699
                        MLinear                0            0           0       56960
                        ModernTCN            111        13001       25002       18846
                        NBeats                36        13982       29356       13586
                        PatchTST               0            0        6451       50509
                        Transformer            0            0           0       56960
```

## 2. Rank-correlation headline (R4.2 / R4.3)

Kendall tau between the 12-model ranking by mean MAE and by mean phase / frequency error; 
means over 20 test signals; bootstrap 95% CI over test signals; permutation p for tau > 0. 
tau near 1 means MAE already orders models the way fidelity does; low or negative tau is the 
quantitative form of the 'MAE is insufficient' claim.

Shift levels are frequency buckets relative to training (-2, -1, in-dist, +1, +2); shift/in-dist is the same run as clean.

| paradigm | level | signal | fidelity | tau | 95% CI | perm p (tau>0) |
|---|---|---|---|---|---|---|
| clean | - | Drift | phase | 0.76 | [0.73, 0.79] | 0.000 |
| clean | - | Drift | freq | 0.70 | [0.64, 0.70] | 0.000 |
| clean | - | SPM | phase | 0.85 | [0.76, 0.88] | 0.000 |
| clean | - | SPM | freq | 0.70 | [0.55, 0.85] | 0.001 |
| clean | - | DPM | phase | 0.94 | [0.88, 1.00] | 0.000 |
| clean | - | DPM | freq | 0.88 | [0.61, 0.94] | 0.000 |
| noise | SNR_1 | Drift | phase | 0.85 | [0.82, 0.88] | 0.000 |
| noise | SNR_1 | Drift | freq | 0.79 | [0.73, 0.79] | 0.000 |
| noise | SNR_1 | SPM | phase | 0.82 | [0.76, 0.91] | 0.000 |
| noise | SNR_1 | SPM | freq | 0.79 | [0.67, 0.88] | 0.000 |
| noise | SNR_1 | DPM | phase | 1.00 | [0.82, 1.00] | 0.000 |
| noise | SNR_1 | DPM | freq | 0.18 | [0.06, 0.48] | 0.224 |
| noise | SNR_2 | Drift | phase | 0.85 | [0.85, 0.91] | 0.000 |
| noise | SNR_2 | Drift | freq | 0.79 | [0.70, 0.85] | 0.001 |
| noise | SNR_2 | SPM | phase | 0.85 | [0.73, 0.88] | 0.000 |
| noise | SNR_2 | SPM | freq | 0.88 | [0.70, 0.91] | 0.000 |
| noise | SNR_2 | DPM | phase | 1.00 | [0.82, 1.00] | 0.000 |
| noise | SNR_2 | DPM | freq | 0.18 | [0.06, 0.48] | 0.224 |
| noise | SNR_3 | Drift | phase | 0.85 | [0.82, 0.85] | 0.000 |
| noise | SNR_3 | Drift | freq | 0.76 | [0.67, 0.79] | 0.000 |
| noise | SNR_3 | SPM | phase | 0.85 | [0.73, 0.91] | 0.000 |
| noise | SNR_3 | SPM | freq | 0.82 | [0.70, 0.91] | 0.001 |
| noise | SNR_3 | DPM | phase | 0.97 | [0.76, 1.00] | 0.000 |
| noise | SNR_3 | DPM | freq | 0.27 | [0.12, 0.67] | 0.130 |
| noise | SNR_4 | Drift | phase | 0.78 | [0.75, 0.78] | 0.001 |
| noise | SNR_4 | Drift | freq | 0.75 | [0.71, 0.78] | 0.001 |
| noise | SNR_4 | SPM | phase | 0.85 | [0.70, 0.94] | 0.000 |
| noise | SNR_4 | SPM | freq | 0.85 | [0.76, 0.91] | 0.000 |
| noise | SNR_4 | DPM | phase | 0.64 | [0.48, 0.85] | 0.001 |
| noise | SNR_4 | DPM | freq | 0.64 | [0.30, 0.82] | 0.003 |
| noise | SNR_5 | Drift | phase | 0.85 | [0.82, 0.85] | 0.000 |
| noise | SNR_5 | Drift | freq | 0.73 | [0.64, 0.79] | 0.001 |
| noise | SNR_5 | SPM | phase | 0.70 | [0.48, 0.76] | 0.001 |
| noise | SNR_5 | SPM | freq | 0.70 | [0.58, 0.82] | 0.001 |
| noise | SNR_5 | DPM | phase | 0.55 | [0.30, 0.76] | 0.005 |
| noise | SNR_5 | DPM | freq | 0.52 | [0.33, 0.73] | 0.010 |
| noise | SNR_6 | Drift | phase | 0.70 | [0.64, 0.73] | 0.001 |
| noise | SNR_6 | Drift | freq | 0.61 | [0.52, 0.64] | 0.002 |
| noise | SNR_6 | SPM | phase | 0.58 | [0.36, 0.67] | 0.002 |
| noise | SNR_6 | SPM | freq | 0.64 | [0.52, 0.73] | 0.000 |
| noise | SNR_6 | DPM | phase | 0.61 | [0.27, 0.73] | 0.003 |
| noise | SNR_6 | DPM | freq | 0.48 | [0.27, 0.67] | 0.014 |
| shift | in-dist | Drift | phase | 0.76 | [0.73, 0.79] | 0.000 |
| shift | in-dist | Drift | freq | 0.70 | [0.64, 0.70] | 0.000 |
| shift | in-dist | SPM | phase | 0.85 | [0.76, 0.88] | 0.000 |
| shift | in-dist | SPM | freq | 0.70 | [0.55, 0.85] | 0.001 |
| shift | in-dist | DPM | phase | 0.94 | [0.88, 1.00] | 0.000 |
| shift | in-dist | DPM | freq | 0.88 | [0.61, 0.94] | 0.000 |
| shift | -2 | Drift | phase | -0.09 | [-0.33, 0.18] | 0.688 |
| shift | -2 | Drift | freq | -0.39 | [-0.45, -0.24] | 0.972 |
| shift | -2 | SPM | phase | 0.00 | [-0.18, 0.27] | 0.511 |
| shift | -2 | SPM | freq | -0.06 | [-0.15, 0.18] | 0.640 |
| shift | -2 | DPM | phase | -0.03 | [-0.18, 0.12] | 0.581 |
| shift | -2 | DPM | freq | 0.39 | [0.36, 0.52] | 0.038 |
| shift | -1 | Drift | phase | -0.55 | [-0.70, -0.15] | 0.996 |
| shift | -1 | Drift | freq | 0.00 | [-0.06, 0.21] | 0.544 |
| shift | -1 | SPM | phase | 0.00 | [-0.18, 0.21] | 0.554 |
| shift | -1 | SPM | freq | -0.09 | [-0.30, 0.09] | 0.674 |
| shift | -1 | DPM | phase | -0.33 | [-0.58, -0.09] | 0.942 |
| shift | -1 | DPM | freq | 0.15 | [-0.06, 0.27] | 0.273 |
| shift | +1 | Drift | phase | -0.42 | [-0.67, 0.06] | 0.976 |
| shift | +1 | Drift | freq | -0.42 | [-0.45, -0.15] | 0.979 |
| shift | +1 | SPM | phase | -0.06 | [-0.30, 0.48] | 0.621 |
| shift | +1 | SPM | freq | 0.12 | [-0.06, 0.21] | 0.322 |
| shift | +1 | DPM | phase | -0.06 | [-0.58, 0.30] | 0.626 |
| shift | +1 | DPM | freq | -0.12 | [-0.21, 0.12] | 0.723 |
| shift | +2 | Drift | phase | 0.00 | [-0.12, 0.09] | 0.521 |
| shift | +2 | Drift | freq | -0.15 | [-0.27, -0.06] | 0.773 |
| shift | +2 | SPM | phase | 0.00 | [-0.30, 0.27] | 0.535 |
| shift | +2 | SPM | freq | 0.21 | [0.06, 0.21] | 0.186 |
| shift | +2 | DPM | phase | -0.48 | [-0.64, -0.09] | 0.993 |
| shift | +2 | DPM | freq | 0.12 | [0.00, 0.24] | 0.333 |

Per paradigm: mean / min / max tau

paradigm fidelity     mean       min      max
   clean     freq 0.757576  0.696970 0.878788
   clean    phase 0.848485  0.757576 0.939394
   noise     freq 0.630640  0.181818 0.878788
   noise    phase 0.792593  0.545455 1.000000
   shift     freq 0.135354 -0.424242 0.878788
   shift    phase 0.034343 -0.545455 0.939394

## 3. Window-level versus signal-level statistics (R4.6)

Paired comparison of every model against Linear on the clean paradigm. `window`: the paper's 
paired test on ~57k overlapping windows (normal approximation). `file`: Wilcoxon signed-rank on 
n = 20 per-signal means. Holm correction within (signal, metric). `survives` = significant in both.

**Drift**

| metric | model | group | mean delta vs Linear [95% CI] | dz | p window (Holm) | p file (Holm) | survives |
|---|---|---|---|---|---|---|---|
| freq | NBeats | Linear and MLP | -0.04454 [-0.0566, -0.0323] | -1.55 | 0.0e+00 | 0.000 | yes |
| freq | ModernTCN | Local receptive field | -0.04316 [-0.0561, -0.0304] | -1.48 | 0.0e+00 | 0.000 | yes |
| freq | PatchTST | Local receptive field | -0.04244 [-0.0545, -0.0301] | -1.45 | 0.0e+00 | 0.000 | yes |
| freq | FreMLP | Decomposition | -0.04178 [-0.054, -0.0299] | -1.46 | 0.0e+00 | 0.000 | yes |
| freq | MICN_Regre | Local receptive field | -0.04138 [-0.0539, -0.0293] | -1.41 | 0.0e+00 | 0.000 | yes |
| freq | MLinear | Linear and MLP | -0.04081 [-0.0525, -0.0282] | -1.42 | 0.0e+00 | 0.000 | yes |
| freq | MICN_Mean | Local receptive field | -0.03966 [-0.0517, -0.0273] | -1.37 | 0.0e+00 | 0.000 | yes |
| freq | Transformer | Global attention | -0.02972 [-0.0428, -0.0177] | -1.00 | 0.0e+00 | 0.003 | yes |
| freq | DLinear | Decomposition | -0.0001486 [-0.00137, +0.000687] | -0.06 | 3.5e-11 | 0.261 | no |
| freq | FITS | Decomposition | +0.01366 [+0.00606, +0.022] | 0.72 | 0.0e+00 | 0.010 | yes |
| freq | Autoformer | Decomposition | +0.1699 [+0.153, +0.188] | 4.29 | 0.0e+00 | 0.000 | yes |
| mae | NBeats | Linear and MLP | -0.1082 [-0.114, -0.102] | -7.89 | 0.0e+00 | 0.000 | yes |
| mae | FreMLP | Decomposition | -0.1062 [-0.112, -0.1] | -7.82 | 0.0e+00 | 0.000 | yes |
| mae | MICN_Regre | Local receptive field | -0.1048 [-0.111, -0.0991] | -7.58 | 0.0e+00 | 0.000 | yes |
| mae | MICN_Mean | Local receptive field | -0.1007 [-0.106, -0.0952] | -7.74 | 0.0e+00 | 0.000 | yes |
| mae | MLinear | Linear and MLP | -0.09986 [-0.105, -0.0941] | -7.63 | 0.0e+00 | 0.000 | yes |
| mae | ModernTCN | Local receptive field | -0.09503 [-0.102, -0.0885] | -6.22 | 0.0e+00 | 0.000 | yes |
| mae | Transformer | Global attention | -0.09437 [-0.1, -0.0885] | -6.67 | 0.0e+00 | 0.000 | yes |
| mae | PatchTST | Local receptive field | -0.07469 [-0.0803, -0.0689] | -5.65 | 0.0e+00 | 0.000 | yes |
| mae | DLinear | Decomposition | -0.001292 [-0.00162, -0.000979] | -1.71 | 0.0e+00 | 0.000 | yes |
| mae | FITS | Decomposition | +0.0203 [+0.0135, +0.0272] | 1.28 | 0.0e+00 | 0.000 | yes |
| mae | Autoformer | Decomposition | +0.03505 [+0.0263, +0.044] | 1.74 | 0.0e+00 | 0.000 | yes |
| phase | NBeats | Linear and MLP | -53.52 [-62.6, -44.7] | -2.51 | 0.0e+00 | 0.000 | yes |
| phase | ModernTCN | Local receptive field | -51.26 [-60.5, -41.7] | -2.30 | 0.0e+00 | 0.000 | yes |
| phase | FreMLP | Decomposition | -50.11 [-59.3, -40.9] | -2.36 | 0.0e+00 | 0.000 | yes |
| phase | MICN_Regre | Local receptive field | -49.4 [-58.3, -40] | -2.32 | 0.0e+00 | 0.000 | yes |
| phase | PatchTST | Local receptive field | -48.79 [-57.7, -39.4] | -2.28 | 0.0e+00 | 0.000 | yes |
| phase | MICN_Mean | Local receptive field | -47.9 [-56.6, -39.4] | -2.27 | 0.0e+00 | 0.000 | yes |
| phase | MLinear | Linear and MLP | -46.96 [-56.1, -38.2] | -2.22 | 0.0e+00 | 0.000 | yes |
| phase | Transformer | Global attention | -45.4 [-54.7, -36.2] | -2.05 | 0.0e+00 | 0.000 | yes |
| phase | DLinear | Decomposition | +0.1709 [-0.315, +0.629] | 0.15 | 0.0e+00 | 0.430 | no |
| phase | FITS | Decomposition | +11.71 [+7.25, +16.3] | 1.08 | 0.0e+00 | 0.001 | yes |
| phase | Autoformer | Decomposition | +26.13 [+16.8, +35] | 1.21 | 0.0e+00 | 0.000 | yes |

**SPM**

| metric | model | group | mean delta vs Linear [95% CI] | dz | p window (Holm) | p file (Holm) | survives |
|---|---|---|---|---|---|---|---|
| freq | NBeats | Linear and MLP | -0.03762 [-0.0539, -0.0222] | -0.99 | 0.0e+00 | 0.000 | yes |
| freq | PatchTST | Local receptive field | -0.03762 [-0.0537, -0.0215] | -0.98 | 0.0e+00 | 0.000 | yes |
| freq | MICN_Regre | Local receptive field | -0.03761 [-0.054, -0.0218] | -0.99 | 0.0e+00 | 0.000 | yes |
| freq | MICN_Mean | Local receptive field | -0.03758 [-0.0549, -0.0222] | -0.99 | 0.0e+00 | 0.000 | yes |
| freq | ModernTCN | Local receptive field | -0.03747 [-0.0535, -0.0216] | -0.98 | 0.0e+00 | 0.000 | yes |
| freq | FreMLP | Decomposition | -0.03663 [-0.0537, -0.0219] | -0.96 | 0.0e+00 | 0.000 | yes |
| freq | MLinear | Linear and MLP | -0.00365 [-0.0168, +0.00887] | -0.12 | 0.0e+00 | 1.000 | no |
| freq | DLinear | Decomposition | +0.0003021 [-0.00163, +0.00239] | 0.06 | 0.0e+00 | 1.000 | no |
| freq | FITS | Decomposition | +0.002674 [-0.00627, +0.0114] | 0.13 | 0.0e+00 | 1.000 | no |
| freq | Transformer | Global attention | +0.02251 [+0.000863, +0.0486] | 0.42 | 0.0e+00 | 0.422 | no |
| freq | Autoformer | Decomposition | +0.05178 [+0.0187, +0.0866] | 0.65 | 0.0e+00 | 0.047 | yes |
| mae | NBeats | Linear and MLP | -0.04362 [-0.0474, -0.0392] | -4.55 | 0.0e+00 | 0.000 | yes |
| mae | MICN_Mean | Local receptive field | -0.04191 [-0.0467, -0.0368] | -3.54 | 0.0e+00 | 0.000 | yes |
| mae | MICN_Regre | Local receptive field | -0.04175 [-0.0466, -0.0369] | -3.59 | 0.0e+00 | 0.000 | yes |
| mae | ModernTCN | Local receptive field | -0.04119 [-0.046, -0.0359] | -3.47 | 0.0e+00 | 0.000 | yes |
| mae | PatchTST | Local receptive field | -0.03523 [-0.0395, -0.0307] | -3.42 | 0.0e+00 | 0.000 | yes |
| mae | FreMLP | Decomposition | -0.03259 [-0.0365, -0.0283] | -3.41 | 0.0e+00 | 0.000 | yes |
| mae | DLinear | Decomposition | -0.001816 [-0.00249, -0.0012] | -1.19 | 0.0e+00 | 0.000 | yes |
| mae | FITS | Decomposition | +0.0006065 [-0.00111, +0.00227] | 0.15 | 0.0e+00 | 0.571 | no |
| mae | Transformer | Global attention | +0.007816 [+0.00511, +0.0109] | 1.21 | 0.0e+00 | 0.000 | yes |
| mae | Autoformer | Decomposition | +0.008956 [+0.00613, +0.0122] | 1.27 | 0.0e+00 | 0.000 | yes |
| mae | MLinear | Linear and MLP | +0.009923 [+0.00774, +0.0124] | 1.75 | 0.0e+00 | 0.000 | yes |
| phase | NBeats | Linear and MLP | -43.69 [-53.6, -34.7] | -1.97 | 0.0e+00 | 0.000 | yes |
| phase | PatchTST | Local receptive field | -43.21 [-53.1, -34.3] | -1.92 | 0.0e+00 | 0.000 | yes |
| phase | MICN_Mean | Local receptive field | -41.98 [-51.6, -32.6] | -1.88 | 0.0e+00 | 0.000 | yes |
| phase | MICN_Regre | Local receptive field | -41.91 [-51.6, -33.2] | -1.88 | 0.0e+00 | 0.000 | yes |
| phase | ModernTCN | Local receptive field | -41.45 [-51, -32.2] | -1.82 | 0.0e+00 | 0.000 | yes |
| phase | FreMLP | Decomposition | -36.65 [-46, -28.4] | -1.78 | 0.0e+00 | 0.000 | yes |
| phase | DLinear | Decomposition | -2.238 [-3.72, -0.889] | -0.67 | 0.0e+00 | 0.028 | yes |
| phase | FITS | Decomposition | +1.902 [-1.95, +5.48] | 0.23 | 0.0e+00 | 0.349 | no |
| phase | MLinear | Linear and MLP | +7.066 [+3.27, +10.9] | 0.79 | 0.0e+00 | 0.004 | yes |
| phase | Transformer | Global attention | +9.006 [+3.51, +14.6] | 0.68 | 0.0e+00 | 0.028 | yes |
| phase | Autoformer | Decomposition | +15.72 [+8.78, +22.9] | 0.98 | 0.0e+00 | 0.002 | yes |

**DPM**

| metric | model | group | mean delta vs Linear [95% CI] | dz | p window (Holm) | p file (Holm) | survives |
|---|---|---|---|---|---|---|---|
| freq | MICN_Mean | Local receptive field | -0.1088 [-0.165, -0.0649] | -0.87 | 0.0e+00 | 0.000 | yes |
| freq | MICN_Regre | Local receptive field | -0.1088 [-0.17, -0.0629] | -0.88 | 0.0e+00 | 0.000 | yes |
| freq | PatchTST | Local receptive field | -0.0937 [-0.156, -0.0493] | -0.75 | 0.0e+00 | 0.000 | yes |
| freq | ModernTCN | Local receptive field | -0.084 [-0.15, -0.0279] | -0.57 | 0.0e+00 | 0.026 | yes |
| freq | NBeats | Linear and MLP | -0.01969 [-0.0507, +0.0103] | -0.27 | 0.0e+00 | 0.757 | no |
| freq | DLinear | Decomposition | -0.01196 [-0.0243, -0.00198] | -0.45 | 0.0e+00 | 0.684 | no |
| freq | MLinear | Linear and MLP | -0.0118 [-0.0462, +0.0236] | -0.14 | 0.0e+00 | 0.757 | no |
| freq | FreMLP | Decomposition | -0.009845 [-0.0286, +0.00836] | -0.22 | 0.0e+00 | 0.757 | no |
| freq | FITS | Decomposition | -0.003051 [-0.0294, +0.0196] | -0.05 | 5.3e-07 | 0.757 | no |
| freq | Transformer | Global attention | +0.03237 [-0.0211, +0.0841] | 0.27 | 0.0e+00 | 0.684 | no |
| freq | Autoformer | Decomposition | +0.2285 [+0.183, +0.274] | 2.20 | 0.0e+00 | 0.000 | yes |
| mae | MICN_Regre | Local receptive field | -0.06555 [-0.0683, -0.0627] | -9.76 | 0.0e+00 | 0.000 | yes |
| mae | MICN_Mean | Local receptive field | -0.064 [-0.0671, -0.0609] | -8.73 | 0.0e+00 | 0.000 | yes |
| mae | ModernTCN | Local receptive field | -0.05608 [-0.0599, -0.0522] | -5.98 | 0.0e+00 | 0.000 | yes |
| mae | PatchTST | Local receptive field | -0.04606 [-0.0496, -0.0425] | -5.56 | 0.0e+00 | 0.000 | yes |
| mae | NBeats | Linear and MLP | -0.01255 [-0.0157, -0.00962] | -1.69 | 0.0e+00 | 0.000 | yes |
| mae | DLinear | Decomposition | -0.001575 [-0.00191, -0.00123] | -2.03 | 0.0e+00 | 0.000 | yes |
| mae | MLinear | Linear and MLP | -0.0007397 [-0.00332, +0.00179] | -0.12 | 0.0e+00 | 0.546 | no |
| mae | FreMLP | Decomposition | +0.0004869 [-0.00144, +0.00203] | 0.12 | 0.0e+00 | 0.405 | no |
| mae | FITS | Decomposition | +0.003468 [+0.00171, +0.00522] | 0.82 | 0.0e+00 | 0.008 | yes |
| mae | Transformer | Global attention | +0.006677 [+0.00415, +0.00935] | 1.12 | 0.0e+00 | 0.000 | yes |
| mae | Autoformer | Decomposition | +0.01119 [+0.00951, +0.0129] | 2.78 | 0.0e+00 | 0.000 | yes |
| phase | MICN_Regre | Local receptive field | -58.59 [-66, -50.7] | -3.30 | 0.0e+00 | 0.000 | yes |
| phase | MICN_Mean | Local receptive field | -57.76 [-65.6, -50.2] | -3.24 | 0.0e+00 | 0.000 | yes |
| phase | ModernTCN | Local receptive field | -52.71 [-60.7, -44.3] | -2.64 | 0.0e+00 | 0.000 | yes |
| phase | PatchTST | Local receptive field | -51.53 [-60, -44.2] | -2.73 | 0.0e+00 | 0.000 | yes |
| phase | NBeats | Linear and MLP | -14.22 [-19.3, -9.06] | -1.19 | 0.0e+00 | 0.000 | yes |
| phase | MLinear | Linear and MLP | -2.647 [-9.73, +5.02] | -0.15 | 0.0e+00 | 1.000 | no |
| phase | DLinear | Decomposition | -1.857 [-2.6, -1.1] | -1.03 | 0.0e+00 | 0.002 | yes |
| phase | FITS | Decomposition | +1.455 [-1.8, +5.09] | 0.18 | 0.0e+00 | 1.000 | no |
| phase | FreMLP | Decomposition | +1.607 [-2.55, +5.63] | 0.17 | 0.0e+00 | 1.000 | no |
| phase | Transformer | Global attention | +9.572 [+3.68, +16.1] | 0.64 | 0.0e+00 | 0.043 | yes |
| phase | Autoformer | Decomposition | +19.64 [+15.2, +24.1] | 1.97 | 0.0e+00 | 0.000 | yes |

Of 99 model-vs-Linear comparisons, 99 were significant at the window level and 80 remain significant at the signal level (n = 20).

Comparisons that lose significance at the signal level:

- Drift / phase: DLinear (worse, delta +0.171, p_file 0.430)
- Drift / freq: DLinear (better, delta -0.000149, p_file 0.261)
- SPM / mae: FITS (worse, delta +0.000607, p_file 0.571)
- SPM / phase: FITS (worse, delta +1.9, p_file 0.349)
- SPM / freq: DLinear (worse, delta +0.000302, p_file 1.000)
- SPM / freq: FITS (worse, delta +0.00267, p_file 1.000)
- SPM / freq: MLinear (better, delta -0.00365, p_file 1.000)
- SPM / freq: Transformer (worse, delta +0.0225, p_file 0.422)
- DPM / mae: MLinear (better, delta -0.00074, p_file 0.546)
- DPM / mae: FreMLP (worse, delta +0.000487, p_file 0.405)
- DPM / phase: FITS (worse, delta +1.46, p_file 1.000)
- DPM / phase: MLinear (better, delta -2.65, p_file 1.000)
- DPM / phase: FreMLP (worse, delta +1.61, p_file 1.000)
- DPM / freq: DLinear (better, delta -0.012, p_file 0.684)
- DPM / freq: FITS (better, delta -0.00305, p_file 0.757)
- DPM / freq: MLinear (better, delta -0.0118, p_file 0.757)
- DPM / freq: NBeats (better, delta -0.0197, p_file 0.757)
- DPM / freq: FreMLP (better, delta -0.00984, p_file 0.757)
- DPM / freq: Transformer (worse, delta +0.0324, p_file 0.684)

### Locality advantage at the signal level

- mae: local-group models better than Linear and significant at file level in 12/12 (signal, model) cells; non-local: 10/21.
- phase: local-group models better than Linear and significant at file level in 12/12 (signal, model) cells; non-local: 9/21.
- freq: local-group models better than Linear and significant at file level in 12/12 (signal, model) cells; non-local: 6/21.

## Notes

- `Statistical_Test/shift.py` registered the SPM FITS run under Drift_Harmonic; fixed in the 
  revision branch. The paper's Fig. 5 FITS curve for Drift_Harmonic should be regenerated.
- One legacy folder is missing: ModernTCN / Drift_Harmonic / SNR_Level_4 (the paper had the same gap).
- All numbers here are seed 2021 only; Phase 2 adds seeds 2022 and 2023.
