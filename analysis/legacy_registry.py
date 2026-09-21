"""
Registry of the paper-era result folders under Train_Test_Validation/ (seed 2021).

One place that knows the folder-naming quirks of the 11 original models so the
reanalysis scripts do not repeat the per-model path tables of Statistical_Test/*.py
(where one of them, the Drift_Harmonic FITS entry of shift.py, was wrong).
"""
from __future__ import annotations

import os
from typing import Dict, List, Optional

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEGACY_ROOT = os.path.join(REPO, "Train_Test_Validation")
DATA_ROOT = "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_data/Generation_Synthesized_Bio_Signals"

SIGNALS = ["Drift_Harmonic", "Single_Phase_Modulation", "Dual_Phase_Modulation"]
SIGNAL_SHORT = {"Drift_Harmonic": "Drift", "Single_Phase_Modulation": "SPM", "Dual_Phase_Modulation": "DPM"}

# model label -> (folder model token, descriptor prefix, weight_decay, lr, patch_len)
MODELS: Dict[str, tuple] = {
    "Linear":      ("Linear",      "Linear",      "0.001",  "0.0001", 16),
    "DLinear":     ("DLinear",     "DLinear",     "0.001",  "0.0001", 16),
    "FITS":        ("FITS",        "FITS",        "0.001",  "0.0001", 16),
    "MLinear":     ("MLinear",     "MLinear",     "0.0001", "0.0001", 16),
    "NBeats":      ("NBeats",      "Nbeats",      "0.0001", "0.0001", 16),
    "FreMLP":      ("FreMLP",      "FreMLP_",     "0.0001", "0.0001", 16),   # double underscore in folder
    "MICN_Mean":   ("MICN",        "MICN_Mean",   "0.0001", "0.0001", 16),
    "MICN_Regre":  ("MICN",        "MICN_Regre",  "0.0001", "0.0001", 16),
    "ModernTCN":   ("ModernTCN",   "ModernTCN",   "0.0",    "0.001",  16),
    "PatchTST":    ("PatchTST",    "PatchTST",    "0.0001", "0.0001", 15),
    "Transformer": ("Transformer", "Transformer", "0.0001", "0.0001", 16),
    "Autoformer":  ("Autoformer",  "Autoformer",  "0.0001", "0.0001", 16),
}
MODEL_ORDER = list(MODELS)

# test-split folders of the synthetic corpus, for file_id reconstruction
CLEAN_TEST_DIR = {
    "Drift_Harmonic": "Noise/Drift_Harmonic_Test/Clean/test",
    "Single_Phase_Modulation": "Noise/PhaseMod_SingleFreq/clean/test",
    "Dual_Phase_Modulation": "Noise/PhaseMod_TwoFreq/clean/test",
}
NOISE_TEST_DIR = {
    "Drift_Harmonic": "Noise/Drift_Harmonic_Test/SNR_{k}/test",
    "Single_Phase_Modulation": "Noise/PhaseMod_SingleFreq/SNR_{k}/test",
    "Dual_Phase_Modulation": "Noise/PhaseMod_TwoFreq/SNR_{k}/test",
}
# Frequency buckets in ascending order. The legacy Shift_k suffix does NOT follow this order:
# Shift_0 is the in-distribution bucket (index 2), Shift_1/Shift_2 the two lower buckets,
# Shift_3/Shift_4 the two higher buckets (verified from the slurm launch scripts).
SHIFT_LEVEL_TO_BUCKET_INDEX = {0: 2, 1: 0, 2: 1, 3: 3, 4: 4}
SHIFT_LEVEL_LABEL = {0: "in-dist", 1: "-2", 2: "-1", 3: "+1", 4: "+2"}
SHIFT_BUCKETS = {
    "Drift_Harmonic": ["f_0.35_0.60", "f_0.60_0.85", "f_0.85_1.10", "f_1.10_1.35", "f_1.35_1.60"],
    "Single_Phase_Modulation": ["f_0.000_0.340", "f_0.340_0.680", "f_0.680_1.410", "f_1.410_2.140", "f_2.140_2.880"],
    "Dual_Phase_Modulation": ["f0_0.00_0.34__f1_0.00_0.34", "f0_0.34_0.68__f1_0.34_0.68",
                              "f0_0.68_1.41__f1_0.68_1.41", "f0_1.41_2.14__f1_1.41_2.14",
                              "f0_2.14_2.88__f1_2.14_2.88"],
}
SHIFT_DIR = {"Drift_Harmonic": "Distribution_Shift/Drift_Harmonic",
             "Single_Phase_Modulation": "Distribution_Shift/Phasemod_SingleFreq",
             "Dual_Phase_Modulation": "Distribution_Shift/Phasemod_TwoFreq"}


def legacy_folder(model: str, signal: str, suffix: str) -> str:
    tok, desc, wd, lr, pl = MODELS[model]
    return os.path.join(
        LEGACY_ROOT,
        f"long_term_forecast_{tok}_50_100_{desc}_{signal}_Clean_70_10_20_{wd}_{lr}_{pl}_{suffix}")


def clean_folder(model: str, signal: str) -> str:
    return legacy_folder(model, signal, "Shift_0")


def noise_folder(model: str, signal: str, snr_level: int) -> str:
    return legacy_folder(model, signal, f"SNR_Level_{snr_level}")


def shift_folder(model: str, signal: str, level: int) -> str:
    return legacy_folder(model, signal, f"Shift_{level}")


def test_split_dir(paradigm: str, signal: str, level: Optional[int] = None) -> str:
    if paradigm == "clean":
        return os.path.join(DATA_ROOT, CLEAN_TEST_DIR[signal])
    if paradigm == "noise":
        if level == 0:
            return os.path.join(DATA_ROOT, CLEAN_TEST_DIR[signal])
        return os.path.join(DATA_ROOT, NOISE_TEST_DIR[signal].format(k=level))
    if paradigm == "shift":
        return os.path.join(DATA_ROOT, SHIFT_DIR[signal],
                            SHIFT_BUCKETS[signal][SHIFT_LEVEL_TO_BUCKET_INDEX[level]], "test")
    raise KeyError(paradigm)


def available(models: List[str], signal: str, folder_fn, *a) -> Dict[str, str]:
    out = {}
    for m in models:
        p = folder_fn(m, signal, *a)
        if os.path.isdir(p) and os.path.exists(os.path.join(p, "test_pred_with_history.npy")):
            out[m] = p
    return out
