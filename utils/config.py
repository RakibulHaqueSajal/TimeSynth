"""
YAML config loading for the revision runner (REVISION_PLAN.md P0.2).

A run is described by two files that are merged onto the argparse namespace:

    configs/models/<model>.yaml      hyperparameters of one model
    configs/paradigms/<paradigm>.yaml data location, window sizes, signals, conditions

Explicit command-line flags win over YAML values. Keys under ``args:`` must be
existing argparse destinations; unknown keys raise so that typos cannot be
silently ignored.
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import Any, Dict, List, Optional

import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_DIR = os.path.join(REPO_ROOT, "configs")

# Root of the shared synthetic corpus. Overridable with the TIMESYNTH_DATA_ROOT
# environment variable so the same configs work on the workstation and on the cluster.
DEFAULT_DATA_ROOT = "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_data/Generation_Synthesized_Bio_Signals"


def data_root() -> str:
    return os.environ.get("TIMESYNTH_DATA_ROOT", DEFAULT_DATA_ROOT)


def load_yaml(path: str) -> Dict[str, Any]:
    with open(path) as f:
        return yaml.safe_load(f) or {}


def model_config_path(name: str) -> str:
    return name if os.path.isfile(name) else os.path.join(CONFIG_DIR, "models", f"{name}.yaml")


def paradigm_config_path(name: str) -> str:
    return name if os.path.isfile(name) else os.path.join(CONFIG_DIR, "paradigms", f"{name}.yaml")


def _explicit_flags(argv: List[str]) -> set:
    """Destinations the user set explicitly on the command line (so YAML does not override them)."""
    out = set()
    for tok in argv:
        if tok.startswith("--"):
            out.add(tok[2:].split("=")[0])
    return out


def apply_yaml_args(args: argparse.Namespace, cfg: Dict[str, Any], explicit: set, source: str) -> None:
    for k, v in (cfg.get("args") or {}).items():
        if not hasattr(args, k):
            raise KeyError(f"{source}: unknown argument '{k}' (not an argparse destination)")
        if k in explicit:
            continue
        setattr(args, k, v)


def resolve_run(args: argparse.Namespace, argv: Optional[List[str]] = None) -> None:
    """
    Merge --model_config and --paradigm_config (if given) onto ``args`` in place,
    and derive root_path / results labels.

    Paradigm YAML schema::

        name: clean                       # results/<name>/...
        data_root_rel: Noise              # relative to TIMESYNTH_DATA_ROOT
        signals:                          # signal label -> sub-path under data_root_rel
          Drift_Harmonic: Drift_Harmonic_Test/Clean
        args: {seq_len: 50, pred_len: 100, ...}
        conditions:                       # optional, test-only evaluations of a clean checkpoint
          SNR_1: Drift_Harmonic_Test/SNR_1
        fs: 10.0
    """
    explicit = _explicit_flags(argv if argv is not None else sys.argv[1:])

    if getattr(args, "model_config", None):
        cfg = load_yaml(model_config_path(args.model_config))
        apply_yaml_args(args, cfg, explicit, args.model_config)
        if "model" in cfg and "model" not in explicit:
            args.model = cfg["model"]
        args.model_label = cfg.get("label", getattr(args, "model_label", None) or args.model)

    if getattr(args, "paradigm_config", None):
        cfg = load_yaml(paradigm_config_path(args.paradigm_config))
        apply_yaml_args(args, cfg, explicit, args.paradigm_config)
        args.paradigm = cfg.get("name", os.path.splitext(os.path.basename(args.paradigm_config))[0])
        args.fs = float(cfg.get("fs", getattr(args, "fs", 10.0)))
        signals = cfg.get("signals") or {}
        if args.signal is None:
            if len(signals) != 1:
                raise ValueError(f"--signal is required; paradigm defines {list(signals)}")
            args.signal = next(iter(signals))
        if args.signal not in signals:
            raise KeyError(f"signal '{args.signal}' not in paradigm {args.paradigm}: {list(signals)}")
        base = os.path.join(data_root(), cfg.get("data_root_rel", ""))
        if getattr(args, "condition", None):
            conds = cfg.get("conditions") or {}
            spec = conds.get(args.condition)
            if spec is None:
                raise KeyError(f"condition '{args.condition}' not in paradigm {args.paradigm}: {list(conds)}")
            # a condition may be a plain sub-path (same for every signal) or a per-signal map
            sub = spec[args.signal] if isinstance(spec, dict) else spec.format(signal=signals[args.signal])
            args.root_path = os.path.join(base, sub)
        else:
            args.root_path = os.path.join(base, signals[args.signal])

    if not getattr(args, "model_label", None):
        args.model_label = args.model
    if not getattr(args, "paradigm", None):
        args.paradigm = "adhoc"
    if getattr(args, "signal", None) is None:
        args.signal = "unspecified"


def result_dir_for(args: argparse.Namespace, seed: int) -> str:
    paradigm = args.paradigm if not getattr(args, "condition", None) else f"{args.paradigm}__{args.condition}"
    return os.path.join(args.results_dir, paradigm, args.signal, args.model_label, f"seed{seed}")


# ---------------------------------------------------------------------------
# Bias groups (P2.5)
# ---------------------------------------------------------------------------
def load_bias_groups(path: Optional[str] = None) -> Dict[str, Any]:
    """
    Returns {'groups': {name: {...}}, 'model_to_group': {model: group_name},
             'model_to_color': {model: hex}, 'model_order': [...], 'display': {...}}.
    """
    cfg = load_yaml(path or os.path.join(CONFIG_DIR, "bias_groups.yaml"))
    m2g, m2c = {}, {}
    for gname, g in cfg["groups"].items():
        for m in g["models"]:
            if m in m2g:
                raise ValueError(f"model {m} listed in two bias groups")
            m2g[m] = gname
            m2c[m] = g["color"]
    return {"groups": cfg["groups"], "model_to_group": m2g, "model_to_color": m2c,
            "model_order": cfg.get("model_order", list(m2g)), "display": cfg.get("display", {})}
