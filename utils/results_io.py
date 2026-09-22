"""
Loading helpers for saved predictions.

Two layouts are supported:

1. Legacy (paper) layout, written by Experiment/exp_test_only.py into
   ``Train_Test_Validation/<setting>/``:
       test_pred_with_history.npy   [N, L+H, 1]
       test_true_with_history.npy   [N, L+H, 1]
       tag_<tag>__pred_with_history.npy / tag_<tag>__true_with_history.npy
   No per-window metadata was stored. Because ``Dataset_Custom`` emits windows
   file by file in sorted order with stride 1, and the test loader used
   ``drop_last=True``, the originating file of window ``i`` can be
   reconstructed from the CSV lengths: see ``legacy_file_ids``.

2. Revision layout (P0.2): ``results/{paradigm}/{signal}/{model}/seed{k}/``
       pred.npy [N, H], true.npy [N, H], hist.npy [N, L], meta.parquet
"""
from __future__ import annotations

import glob
import os
from typing import Dict, Optional, Tuple

import numpy as np
import pandas as pd


def _squeeze(a: np.ndarray) -> np.ndarray:
    return a[..., 0] if (a.ndim == 3 and a.shape[-1] == 1) else a


# ---------------------------------------------------------------------------
# Legacy layout
# ---------------------------------------------------------------------------
def load_legacy(model_path: str, history_len: int, tag: Optional[str] = None,
                split: str = "test") -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Returns (hist, true_h, pred_h) as float64 arrays of shapes
    [N, L], [N, H], [N, H] from a legacy result folder.
    """
    if tag is None:
        t_fp = os.path.join(model_path, f"{split}_true_with_history.npy")
        p_fp = os.path.join(model_path, f"{split}_pred_with_history.npy")
    else:
        from Statistical_Test.state_transition import _resolve_tag_file  # lazy
        t_fp = _resolve_tag_file(model_path, tag, "true_with_history")
        p_fp = _resolve_tag_file(model_path, tag, "pred_with_history")
    true = _squeeze(np.load(t_fp)).astype(float)
    pred = _squeeze(np.load(p_fp)).astype(float)
    return true[:, :history_len], true[:, history_len:], pred[:, history_len:]


def csv_lengths(split_dir: str) -> Dict[str, int]:
    """Number of rows (excluding header) of every CSV in a split folder, sorted by name."""
    out = {}
    for fp in sorted(glob.glob(os.path.join(split_dir, "*.csv"))):
        with open(fp, "rb") as f:
            n = sum(1 for _ in f) - 1
        out[os.path.basename(fp)] = n
    return out


def legacy_file_ids(n_windows: int, split_dir: str, seq_len: int, pred_len: int,
                    batch_size: int = 128, drop_last: bool = True) -> pd.DataFrame:
    """
    Reconstruct, for each of the ``n_windows`` saved test windows, the source
    CSV and window start index, replicating Dataset_Custom's enumeration
    (stride 1, file by file in sorted order) and the loader's ``drop_last``.

    Returns a DataFrame with columns ``file_id`` (int, sorted position),
    ``file_name`` and ``window_start``. Raises if the count does not match,
    which guards against applying the wrong split folder.
    """
    lengths = csv_lengths(split_dir)
    if not lengths:
        raise FileNotFoundError(f"no CSVs in {split_dir}")
    rows = []
    for fid, (name, L) in enumerate(lengths.items()):
        n_win = L - seq_len - pred_len + 1
        for s in range(max(0, n_win)):
            rows.append((fid, name, s))
    total = len(rows)
    kept = (total // batch_size) * batch_size if drop_last else total
    if kept != n_windows:
        raise ValueError(
            f"window count mismatch for {split_dir}: enumeration gives {kept} "
            f"(total {total}, batch {batch_size}, drop_last={drop_last}) but "
            f"saved arrays have {n_windows}")
    df = pd.DataFrame(rows[:kept], columns=["file_id", "file_name", "window_start"])
    return df


# ---------------------------------------------------------------------------
# Revision layout
# ---------------------------------------------------------------------------
def result_dir(results_root: str, paradigm: str, signal: str, model: str, seed: int) -> str:
    return os.path.join(results_root, paradigm, signal, model, f"seed{seed}")


def save_result(out_dir: str, pred: np.ndarray, true: np.ndarray, hist: np.ndarray,
                meta: pd.DataFrame, samples: Optional[np.ndarray] = None) -> None:
    os.makedirs(out_dir, exist_ok=True)
    np.save(os.path.join(out_dir, "pred.npy"), _squeeze(np.asarray(pred, np.float32)))
    np.save(os.path.join(out_dir, "true.npy"), _squeeze(np.asarray(true, np.float32)))
    np.save(os.path.join(out_dir, "hist.npy"), _squeeze(np.asarray(hist, np.float32)))
    if samples is not None:
        S = np.asarray(samples, np.float32)
        if S.ndim == 4 and S.shape[-1] == 1:
            S = S[..., 0]
        np.save(os.path.join(out_dir, "samples.npy"), S)                     # [S, N, H]
    meta.to_parquet(os.path.join(out_dir, "meta.parquet"), index=False)


def load_result(out_dir: str):
    """Returns (hist, true, pred, meta_df[, samples]) from a revision-layout folder."""
    hist = np.load(os.path.join(out_dir, "hist.npy")).astype(float)
    true = np.load(os.path.join(out_dir, "true.npy")).astype(float)
    pred = np.load(os.path.join(out_dir, "pred.npy")).astype(float)
    meta = pd.read_parquet(os.path.join(out_dir, "meta.parquet"))
    s_fp = os.path.join(out_dir, "samples.npy")
    if os.path.exists(s_fp):
        return hist, true, pred, meta, np.load(s_fp).astype(float)
    return hist, true, pred, meta


# ---------------------------------------------------------------------------
# Runner glue (P0.2)
# ---------------------------------------------------------------------------
def build_meta(args, n_windows: int, dataset=None, tags=None, seed=None) -> pd.DataFrame:
    """
    One row per saved test window. Uses ``dataset.meta`` (file_id, file_name,
    window_start) when the loader provides it, else per-window ``tags`` from the
    tag-aware loaders, else a bare index. Condition labels come from ``args``.
    """
    if dataset is not None and getattr(dataset, "meta", None):
        m = list(dataset.meta)[:n_windows]
        df = pd.DataFrame(m, columns=["file_id", "file_name", "window_start"])
    else:
        df = pd.DataFrame({"file_id": np.arange(n_windows), "file_name": "", "window_start": -1})
    if len(df) != n_windows:
        raise ValueError(f"meta has {len(df)} rows but {n_windows} windows were saved")
    df["tag"] = (list(tags)[:n_windows] if tags is not None else "")
    df["paradigm"] = getattr(args, "paradigm", "")
    df["signal"] = getattr(args, "signal", "")
    df["condition"] = getattr(args, "condition", None) or ""
    df["model"] = getattr(args, "model_label", getattr(args, "model", ""))
    df["seed"] = int(seed if seed is not None else getattr(args, "seed", -1))
    df["fs"] = float(getattr(args, "fs", np.nan))
    df["seq_len"] = int(args.seq_len)
    df["pred_len"] = int(args.pred_len)
    df["eval_stride"] = int(getattr(args, "eval_stride", 1))
    return df


def write_run_outputs(args, out_dir: str, hist, true, pred, meta: pd.DataFrame,
                      metrics=None, samples=None, save_legacy: bool = True) -> None:
    """Write the P0.2 layout and, optionally, the legacy *_with_history arrays."""
    save_result(out_dir, pred, true, hist, meta, samples=samples)
    if metrics is not None:
        np.save(os.path.join(out_dir, "metrics.npy"), np.asarray(metrics))
    if save_legacy:
        h, t, p = (np.asarray(a, np.float32) for a in (hist, true, pred))
        if h.ndim == 2: h = h[..., None]
        if t.ndim == 2: t = t[..., None]
        if p.ndim == 2: p = p[..., None]
        np.save(os.path.join(out_dir, "test_true_with_history.npy"), np.concatenate([h, t], axis=1))
        np.save(os.path.join(out_dir, "test_pred_with_history.npy"), np.concatenate([h, p], axis=1))
    with open(os.path.join(out_dir, "args.json"), "w") as f:
        import json
        json.dump({k: (v if isinstance(v, (int, float, str, bool, list, type(None))) else str(v))
                   for k, v in vars(args).items()}, f, indent=1, sort_keys=True)
