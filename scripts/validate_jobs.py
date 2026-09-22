#!/usr/bin/env python3
"""Check that every job in slurm/generated/*.sbatch resolves its configs and that its data folder exists."""
import argparse, collections, glob, os, shlex, sys
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)
from utils.config import resolve_run, load_yaml, model_config_path  # noqa: E402

combos = set()
for f in sorted(glob.glob(os.path.join(REPO, "slurm/generated/p*.sbatch"))):
    for line in open(f):
        if line.startswith("CMDS+="):
            toks = shlex.split(shlex.split(line[len("CMDS+=("):-2])[0])
            d = {t: toks[i + 1] for i, t in enumerate(toks) if t.startswith("--") and i + 1 < len(toks)}
            combos.add((d["--model_config"], d["--paradigm_config"], d["--signal"], d.get("--condition")))
print(len(combos), "unique (model, paradigm, signal, condition) combos")
bad, missing = collections.Counter(), set()
for m, p, sig, c in sorted(combos, key=lambda t: tuple(str(x) for x in t)):
    ns = argparse.Namespace(model_config=m, paradigm_config=p, signal=sig, condition=c, model_label=None, model=None,
                            data="custom", seq_len=96, pred_len=96, label_len=0, train_stride=1, eval_stride=1,
                            test_drop_last=True, task_name="x", features="S", target="Value", enc_in=1, results_dir="r",
                            max_windows_per_file=None, train_sample_size=None, val_sample_size=None,
                            test_sample_size=None, batch_size=128)
    for k in load_yaml(model_config_path(m)).get("args", {}):
        setattr(ns, k, None)
    try:
        resolve_run(ns, argv=[])
    except Exception as e:
        bad[f"{m}/{p}: {str(e)[:70]}"] += 1
        continue
    if not os.path.isdir(os.path.join(ns.root_path, "test")):
        missing.add(ns.root_path)
print("config errors:", dict(bad) or "none")
print("missing data roots:", len(missing))
for x in sorted(missing):
    print("  ", x.split("Time_Series/")[-1])
