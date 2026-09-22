#!/usr/bin/env python3
"""
SLURM array launcher (REVISION_PLAN.md P0.3).

Reads a run-matrix YAML and writes one sbatch array script per phase under
``slurm/generated/``. Each array element is a single (model, paradigm, signal,
seed[, condition]) job. Jobs whose ``results/.../seed{k}/pred.npy`` already
exists are skipped, so a partially failed array can simply be regenerated and
resubmitted.

Run-matrix schema (see configs/run_matrix/*.yaml)::

    phase: p2_synthetic_clean          # name of the generated script
    results_dir: /shared/path/results  # absolute, visible from the cluster
    checkpoint_dir: /shared/path/checkpoints
    slurm: {partition: general-gpu, account: medvic, time: "0-08:00:00", mem: 32G,
            cpus: 8, gres: "gpu:1", max_concurrent: 16}
    env: {conda_python: /path/to/python, TIMESYNTH_DATA_ROOT: /path}
    blocks:
      - paradigm: clean
        signals: [Drift_Harmonic, Single_Phase_Modulation, Dual_Phase_Modulation]
        models: [Linear, DLinear, ...]          # names of configs/models/*.yaml
        seeds: [2021, 2022, 2023]
        is_training: 1
      - paradigm: noise                         # test-only conditions on clean checkpoints
        conditions: [SNR_1, ..., SNR_6]
        checkpoint_from: {paradigm: clean}      # reuse the clean checkpoint of the same model/signal/seed
        is_training: 2
        ...
    extra_args: "--num_workers 4"               # appended to every main.py call

Usage::

    python scripts/make_jobs.py configs/run_matrix/p2_clean.yaml [--submit] [--dry]
"""
from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
from typing import Dict, List

import yaml

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)
from utils.config import load_yaml, model_config_path, paradigm_config_path  # noqa: E402

GEN_DIR = os.path.join(REPO, "slurm", "generated")


def setting_name(model_cfg: Dict, paradigm: str, signal: str, seq_len: int, pred_len: int, label_suffix: str = "") -> str:
    """Mirror main.py: setting = task_model-id_wd_lr_patch_len, model_id = label_seq_pred_paradigm_signal."""
    a = model_cfg.get("args", {})
    label = model_cfg.get("label", model_cfg["model"]) + label_suffix
    wd = a.get("weight_decay", 0.0)
    lr = a.get("learning_rate", 0.0001)
    pl = a.get("patch_len", 16)
    model_id = f"{label}_{seq_len}_{pred_len}_{paradigm}_{signal}"
    return f"long_term_forecast_{model_id}_{wd}_{lr}_{pl}"


def expand(matrix: Dict) -> List[Dict]:
    jobs = []
    results_dir = matrix["results_dir"]
    for blk in matrix["blocks"]:
        paradigm = blk["paradigm"]
        pcfg = load_yaml(paradigm_config_path(paradigm))
        pargs = pcfg.get("args", {})
        seq_len, pred_len = pargs.get("seq_len", 50), pargs.get("pred_len", 100)
        signals = blk.get("signals") or list(pcfg.get("signals", {}).keys())
        conditions = blk.get("conditions") or [None]
        is_training = int(blk.get("is_training", 1))
        suffix = blk.get("label_suffix", "")                 # results label = YAML label + suffix
        ck_suffix = blk.get("checkpoint_label_suffix", suffix if is_training == 1 else "")
        for model in blk["models"]:
            mcfg = load_yaml(model_config_path(model))
            label = mcfg.get("label", mcfg["model"]) + suffix
            for signal in signals:
                for seed in blk["seeds"]:
                    for cond in conditions:
                        pname = paradigm if cond is None else f"{paradigm}__{cond}"
                        out = os.path.join(results_dir, pname, signal, label, f"seed{seed}", "pred.npy")
                        ckpt = None
                        if is_training in (2, 3):
                            src = blk.get("checkpoint_from", {"paradigm": paradigm})
                            ckpt = blk.get("checkpoint_name") or (
                                setting_name(mcfg, src["paradigm"], signal, seq_len, pred_len, ck_suffix) + f"_seed{seed}")
                        jobs.append(dict(model=model, paradigm=paradigm, signal=signal, seed=seed,
                                         condition=cond, is_training=is_training, out=out,
                                         checkpoint_name=ckpt, done=os.path.exists(out),
                                         extra=blk.get("extra_args", ""), label=label if suffix else None))
    return jobs


def job_command(matrix: Dict, j: Dict) -> str:
    py = matrix.get("env", {}).get("conda_python", "python")
    parts = [py, "-u", "main.py",
             "--is_training", str(j["is_training"]),
             "--model_config", j["model"], "--paradigm_config", j["paradigm"],
             "--signal", j["signal"], "--seeds", str(j["seed"]),
             "--results_dir", matrix["results_dir"], "--checkpoint_dir", matrix["checkpoint_dir"]]
    if j["condition"]:
        parts += ["--condition", j["condition"]]
    if j["checkpoint_name"]:
        parts += ["--checkpoint_name", j["checkpoint_name"]]
    if j.get("label"):
        parts += ["--model_label", j["label"]]
    cmd = " ".join(shlex.quote(p) for p in parts)
    for extra in (matrix.get("extra_args", ""), j.get("extra", "")):
        if extra:
            cmd += " " + extra
    return cmd


MAX_ARRAY = 1000   # cluster MaxArraySize is 1001


def write_scripts(matrix: Dict, jobs: List[Dict]) -> List[str]:
    """Split into arrays of at most MAX_ARRAY elements: <phase>.sbatch or <phase>_partK.sbatch."""
    if len(jobs) <= MAX_ARRAY:
        return [write_script(matrix, jobs)]
    paths = []
    for k in range(0, len(jobs), MAX_ARRAY):
        sub = dict(matrix, phase=f"{matrix['phase']}_part{k // MAX_ARRAY}")
        paths.append(write_script(sub, jobs[k:k + MAX_ARRAY]))
    return paths


def write_script(matrix: Dict, jobs: List[Dict]) -> str:
    os.makedirs(GEN_DIR, exist_ok=True)
    phase = matrix["phase"]
    s = matrix.get("slurm", {})
    env = matrix.get("env", {})
    n = len(jobs)
    lines = ["#!/bin/bash",
             f"#SBATCH --job-name={phase}",
             f"#SBATCH --partition={s.get('partition', 'general-gpu')}"]
    if s.get("account"):
        lines.append(f"#SBATCH --account={s['account']}")
    if s.get("qos"):
        lines.append(f"#SBATCH --qos={s['qos']}")
    lines += [f"#SBATCH --time={s.get('time', '0-08:00:00')}",
              f"#SBATCH --mem={s.get('mem', '32G')}",
              f"#SBATCH --cpus-per-task={s.get('cpus', 8)}",
              f"#SBATCH --gres={s.get('gres', 'gpu:1')}",
              "#SBATCH --ntasks=1",
              f"#SBATCH --array=0-{n - 1}%{s.get('max_concurrent', 16)}",
              f"#SBATCH --output={os.path.join(REPO, 'logs', 'slurm', phase + '_%A_%a.out')}",
              "",
              f"mkdir -p {os.path.join(REPO, 'logs', 'slurm')}",
              f"cd {REPO}",
              "export PYTHONUNBUFFERED=1",
              "export OMP_NUM_THREADS=4"]
    for k, v in env.items():
        if k != "conda_python":
            lines.append(f"export {k}={shlex.quote(str(v))}")
    lines += ["", "CMDS=()"]
    for j in jobs:
        lines.append(f"CMDS+=({shlex.quote(job_command(matrix, j))})")
    lines += ["",
              'echo "[$(date)] task $SLURM_ARRAY_TASK_ID on $(hostname): ${CMDS[$SLURM_ARRAY_TASK_ID]}"',
              'eval "${CMDS[$SLURM_ARRAY_TASK_ID]}"',
              'echo "[$(date)] exit $?"']
    path = os.path.join(GEN_DIR, f"{phase}.sbatch")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    os.chmod(path, 0o755)
    # human-readable manifest
    with open(os.path.join(GEN_DIR, f"{phase}.jobs.tsv"), "w") as f:
        f.write("idx\tmodel\tparadigm\tcondition\tsignal\tseed\tout\n")
        for i, j in enumerate(jobs):
            f.write(f"{i}\t{j['model']}\t{j['paradigm']}\t{j['condition'] or ''}\t{j['signal']}\t{j['seed']}\t{j['out']}\n")
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("matrix")
    ap.add_argument("--submit", action="store_true", help="sbatch the script (via --ssh host if given)")
    ap.add_argument("--ssh", default=None, help="submit through 'ssh <host> sbatch ...'")
    ap.add_argument("--dry", action="store_true", help="only list the jobs")
    ap.add_argument("--include-done", action="store_true", help="do not skip jobs whose pred.npy exists")
    ap.add_argument("--after", default=None, help="SLURM job id: submit with --dependency=afterany:<id>")
    a = ap.parse_args()

    matrix = load_yaml(a.matrix)
    jobs = expand(matrix)
    todo = [j for j in jobs if a.include_done or not j["done"]]
    print(f"{len(jobs)} jobs in matrix, {len(jobs) - len(todo)} already done, {len(todo)} to run")
    if a.dry:
        for j in todo:
            print(job_command(matrix, j))
        return
    if not todo:
        print("nothing to do")
        return
    paths = write_scripts(matrix, todo)
    for path in paths:
        print("wrote", path)
    if a.submit:
        for path in paths:
            cmd = ["sbatch"] + ([f"--dependency=afterany:{a.after}"] if a.after else []) + [path]
            if a.ssh:
                cmd = ["ssh", a.ssh, " ".join(shlex.quote(c) for c in cmd)]
            print("+", " ".join(cmd))
            subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
