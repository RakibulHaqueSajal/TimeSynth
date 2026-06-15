#!/usr/bin/env python3
"""
Supervised-calibrated HMM probe for Markov switching.

What it does:
  1) Load test_true_state.npy, test_true_with_history.npy, test_pred_with_history.npy
  2) Slice FUTURE window [L:L+H]
  3) Build TRUE window labels Yw_true by majority vote over each window (W, hop)
  4) Extract windowed features from signals (default: Welch dominant frequency) -> F_true, F_pred
  5) Normalize features using TRUE stats
  6) Build a FIXED HMM from TRUE labels:
       - pi from first window labels
       - A from TRUE window-label transitions
       - emissions (mu,var) from TRUE features grouped by TRUE labels
  7) Viterbi-decode TRUE and PRED features using the fixed HMM
  8) Print p_win + transition matrices + accuracies

Notes:
  - If you want the HMM to be closer to actual, the biggest lever is FEATURES.
    The default feature (dominant frequency) may be weak for your states.
"""

import numpy as np
from pathlib import Path
from scipy.signal import welch


# -------------------------
# CONFIG (EDIT THESE)
# -------------------------
FOLDER = Path(
    "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
    "long_term_forecast_Linear_50_100_Linear_PhaseMod_Single_Freq_TwoState_p_0.30000_70_10_20_0.001_0.0001_16_State"
)

L = 50
H = 100

W = 16
HOP = 8

K = 2            # number of Markov states
FS = 1.0         # sampling freq for Welch


# -------------------------
# IO helpers
# -------------------------
def load_2d(x: np.ndarray) -> np.ndarray:
    if x.ndim == 3 and x.shape[-1] == 1:
        return x[..., 0]
    if x.ndim == 2:
        return x
    raise ValueError(f"Expected [N,T] or [N,T,1], got {x.shape}")


# -------------------------
# True window labels (majority vote)
# -------------------------
def true_window_labels_majority(true_state_fut: np.ndarray, W: int, hop: int, K: int) -> np.ndarray:
    """
    true_state_fut: [N,H] ints in 0..K-1
    returns Yw_true: [N,Tw] majority vote label per window
    """
    N, Hh = true_state_fut.shape
    starts = np.arange(0, Hh - W + 1, hop)
    Tw = len(starts)
    Yw = np.zeros((N, Tw), dtype=np.int64)

    for j, st in enumerate(starts):
        win = true_state_fut[:, st:st + W]  # [N,W]
        for i in range(N):
            Yw[i, j] = np.bincount(win[i], minlength=K).argmax()

    return Yw


# -------------------------
# Feature extraction
# -------------------------
def dominant_freq_welch(x_1d: np.ndarray, fs: float = 1.0) -> float:
    """
    Returns Welch dominant frequency (Hz) for a 1D window.
    With W=16, Welch is noisy; consider adding more features if needed.
    """
    nperseg = min(len(x_1d), 16)
    if nperseg <= 1:
        return 0.0
    noverlap = min(max(nperseg // 2, 0), nperseg - 1)
    f, Pxx = welch(x_1d, fs=fs, nperseg=nperseg, noverlap=noverlap)
    return float(f[np.argmax(Pxx)]) if len(f) else 0.0


def extract_window_features(X_fut: np.ndarray, W: int, hop: int, fs: float = 1.0) -> np.ndarray:
    """
    X_fut: [N,H]
    Returns F: [N,Tw,D]
    Default D=1 feature: Welch dominant frequency per window.
    """
    N, Hh = X_fut.shape
    starts = np.arange(0, Hh - W + 1, hop)
    Tw = len(starts)

    # D=1 (dominant freq)
    F = np.zeros((N, Tw, 1), dtype=np.float64)

    for j, st in enumerate(starts):
        seg = X_fut[:, st:st + W]  # [N,W]
        F[:, j, 0] = np.array([dominant_freq_welch(seg[i], fs=fs) for i in range(N)], dtype=np.float64)

    return F


# -------------------------
# Metrics
# -------------------------
def switching_prob(S: np.ndarray) -> float:
    # S: [N,T]
    return float((S[:, 1:] != S[:, :-1]).mean())


def transition_matrix(S: np.ndarray, K: int) -> np.ndarray:
    Tmat = np.zeros((K, K), dtype=np.float64)
    for i in range(S.shape[0]):
        a = S[i, :-1]
        b = S[i, 1:]
        np.add.at(Tmat, (a, b), 1)
    row = Tmat.sum(axis=1, keepdims=True)
    return np.divide(Tmat, row, out=np.zeros_like(Tmat), where=row > 0)


# -------------------------
# Fixed HMM (Gaussian diag emissions) + Viterbi
# -------------------------
def gaussian_logpdf_diag(x: np.ndarray, mu: np.ndarray, var: np.ndarray) -> np.ndarray:
    """
    x: [T,D], mu: [D], var: [D]
    returns log p(x_t | state) for each t: [T]
    """
    var = np.maximum(var, 1e-12)
    return -0.5 * (
        np.sum(np.log(2.0 * np.pi * var)) +
        np.sum(((x - mu) ** 2) / var, axis=1)
    )


def viterbi_decode(logB: np.ndarray, logA: np.ndarray, logpi: np.ndarray) -> np.ndarray:
    """
    logB: [T,K], logA: [K,K], logpi: [K]
    returns z: [T]
    """
    T, K = logB.shape
    dp = np.full((T, K), -np.inf, dtype=np.float64)
    ptr = np.zeros((T, K), dtype=np.int64)

    dp[0] = logpi + logB[0]
    for t in range(1, T):
        for k in range(K):
            scores = dp[t - 1] + logA[:, k]
            j = int(np.argmax(scores))
            ptr[t, k] = j
            dp[t, k] = scores[j] + logB[t, k]

    z = np.zeros(T, dtype=np.int64)
    z[-1] = int(np.argmax(dp[-1]))
    for t in range(T - 2, -1, -1):
        z[t] = ptr[t + 1, z[t + 1]]
    return z


def decode_sequences_fixed_hmm(F_seq: np.ndarray, mu: np.ndarray, var: np.ndarray, logA: np.ndarray, logpi: np.ndarray) -> np.ndarray:
    """
    F_seq: [N,Tw,D]
    returns Z: [N,Tw]
    """
    N, Tw, D = F_seq.shape
    K = mu.shape[0]
    Z = np.zeros((N, Tw), dtype=np.int64)

    for i in range(N):
        Xi = F_seq[i]  # [Tw,D]
        logB = np.zeros((Tw, K), dtype=np.float64)
        for k in range(K):
            logB[:, k] = gaussian_logpdf_diag(Xi, mu[k], var[k])
        Z[i] = viterbi_decode(logB, logA, logpi)

    return Z


# -------------------------
# Main
# -------------------------
def main():
    # Load
    true_state = load_2d(np.load(FOLDER / "test_true_state.npy")).astype(np.int64)
    true_wh = load_2d(np.load(FOLDER / "test_true_with_history.npy")).astype(np.float64)
    pred_wh = load_2d(np.load(FOLDER / "test_pred_with_history.npy")).astype(np.float64)

    # Slice FUTURE signals
    if true_wh.shape[1] < L + H or pred_wh.shape[1] < L + H:
        raise ValueError(f"Need signals with length >= L+H={L+H}. Got true={true_wh.shape}, pred={pred_wh.shape}")

    true_fut = true_wh[:, L:L + H]
    pred_fut = pred_wh[:, L:L + H]

    # Slice FUTURE states
    if true_state.shape[1] >= L + H:
        true_state_fut = true_state[:, L:L + H]
    elif true_state.shape[1] == H:
        true_state_fut = true_state
    else:
        raise ValueError(f"Can't infer FUTURE states from shape {true_state.shape} with L={L}, H={H}")

    # Per-step actual
    p_step_true = switching_prob(true_state_fut)
    T_step_true = transition_matrix(true_state_fut, K)

    print("\n=== TRUE discrete (actual) ===")
    print(f"Per-step switching prob: {p_step_true:.6f}")
    print("Per-step transition matrix:")
    print(T_step_true)

    # Window labels (actual)
    Yw_true = true_window_labels_majority(true_state_fut, W=W, hop=HOP, K=K)
    p_win_true_actual = switching_prob(Yw_true)
    T_win_true_actual = transition_matrix(Yw_true, K)

    print("\n=== TRUE window labels (actual, majority vote) ===")
    print(f"p_win TRUE (actual): {p_win_true_actual:.6f}")
    print("T_win TRUE (actual):")
    print(T_win_true_actual)

    # Windowed features
    F_true = extract_window_features(true_fut, W=W, hop=HOP, fs=FS)  # [N,Tw,D]
    F_pred = extract_window_features(pred_fut, W=W, hop=HOP, fs=FS)

    # Normalize using TRUE stats
    muF = F_true.mean(axis=(0, 1), keepdims=True)
    sdF = F_true.std(axis=(0, 1), keepdims=True) + 1e-12
    F_true_n = (F_true - muF) / sdF
    F_pred_n = (F_pred - muF) / sdF

    # -------------------------
    # Supervised-calibrated HMM params from TRUE window labels
    # -------------------------
    N, Tw, D = F_true_n.shape

    # Start probs from first window labels
    pi = np.bincount(Yw_true[:, 0], minlength=K).astype(np.float64)
    pi = (pi + 1e-6) / (pi.sum() + 1e-6 * K)

    # Transition matrix from TRUE window labels
    A = T_win_true_actual.copy()
    A = (A + 1e-8) / (A.sum(axis=1, keepdims=True) + 1e-8 * K)

    # Emission params from TRUE features grouped by TRUE labels
    mu = np.zeros((K, D), dtype=np.float64)
    var = np.zeros((K, D), dtype=np.float64)

    F_flat = F_true_n.reshape(-1, D)
    Y_flat = Yw_true.reshape(-1)

    for k in range(K):
        Xk = F_flat[Y_flat == k]
        if len(Xk) == 0:
            mu[k] = 0.0
            var[k] = 1.0
        else:
            mu[k] = Xk.mean(axis=0)
            var[k] = Xk.var(axis=0) + 1e-6

    logpi = np.log(pi)
    logA = np.log(A)

    print("\n=== Supervised-calibrated HMM params (from TRUE window labels) ===")
    print("pi:", pi)
    print("A (TRUE window):\n", A)
    print("mu:\n", mu)
    print("var:\n", var)

    # Decode TRUE and PRED with fixed HMM
    Z_true_sup = decode_sequences_fixed_hmm(F_true_n, mu, var, logA, logpi)
    Z_pred_sup = decode_sequences_fixed_hmm(F_pred_n, mu, var, logA, logpi)

    # Metrics
    p_win_true_sup = switching_prob(Z_true_sup)
    p_win_pred_sup = switching_prob(Z_pred_sup)

    T_win_true_sup = transition_matrix(Z_true_sup, K)
    T_win_pred_sup = transition_matrix(Z_pred_sup, K)

    acc_true_sup = float((Z_true_sup == Yw_true).mean())
    acc_pred_sup = float((Z_pred_sup == Yw_true).mean())

    print("\n=== Supervised-calibrated decode ===")
    print(f"p_win TRUE (sup-decode): {p_win_true_sup:.6f}")
    print(f"p_win PRED (sup-decode): {p_win_pred_sup:.6f}")

    print("\nT_win TRUE (sup-decode):")
    print(T_win_true_sup)
    print("T_win PRED (sup-decode):")
    print(T_win_pred_sup)

    print("\nAgreement with TRUE window labels (actual):")
    print(f"Accuracy(TRUE sup-decode vs Yw_true): {acc_true_sup:.4f}")
    print(f"Accuracy(PRED sup-decode vs Yw_true): {acc_pred_sup:.4f}")

    cnt_pred = np.bincount(Z_pred_sup.reshape(-1), minlength=K)
    print("\nPRED sup-decoded state counts:", cnt_pred)
    print("Fraction:", cnt_pred / cnt_pred.sum())


if __name__ == "__main__":
    main()