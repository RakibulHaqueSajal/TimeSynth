#!/bin/bash
#SBATCH --job-name=p1a_real_pilot
#SBATCH --partition=general-gpu
#SBATCH --account=medvic
#SBATCH --time=0-06:00:00
#SBATCH --mem=32G
#SBATCH --cpus-per-task=6
#SBATCH --gres=gpu:1
#SBATCH --ntasks=1
#SBATCH --array=0-3%5
#SBATCH --output=/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/logs/slurm/p1a_real_pilot_%A_%a.out

mkdir -p /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/logs/slurm
cd /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast
export PYTHONUNBUFFERED=1
export OMP_NUM_THREADS=4

CMDS=()
CMDS+=('/uufs/sci.utah.edu/projects/medvic-lab/Rakib/miniconda3/envs/timeenv/bin/python -u main.py --is_training 1 --model_config Linear --paradigm_config real_ppg_A --signal BIDMC --seeds 2021 --results_dir /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/results --checkpoint_dir /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/checkpoints --num_workers 4')
CMDS+=('/uufs/sci.utah.edu/projects/medvic-lab/Rakib/miniconda3/envs/timeenv/bin/python -u main.py --is_training 1 --model_config PatchTST --paradigm_config real_ppg_A --signal BIDMC --seeds 2021 --results_dir /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/results --checkpoint_dir /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/checkpoints --num_workers 4')
CMDS+=('/uufs/sci.utah.edu/projects/medvic-lab/Rakib/miniconda3/envs/timeenv/bin/python -u main.py --is_training 1 --model_config Transformer --paradigm_config real_ppg_A --signal BIDMC --seeds 2021 --results_dir /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/results --checkpoint_dir /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/checkpoints --num_workers 4')
CMDS+=('/uufs/sci.utah.edu/projects/medvic-lab/Rakib/miniconda3/envs/timeenv/bin/python -u main.py --is_training 1 --model_config CSDI --paradigm_config real_ppg_A --signal BIDMC --seeds 2021 --results_dir /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/results --checkpoint_dir /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/checkpoints --num_workers 4')

echo "[$(date)] task $SLURM_ARRAY_TASK_ID on $(hostname): ${CMDS[$SLURM_ARRAY_TASK_ID]}"
eval "${CMDS[$SLURM_ARRAY_TASK_ID]}"
echo "[$(date)] exit $?"
