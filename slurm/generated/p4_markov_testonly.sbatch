#!/bin/bash
#SBATCH --job-name=p4_markov_testonly
#SBATCH --partition=general-gpu
#SBATCH --time=0-06:00:00
#SBATCH --mem=24G
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:1
#SBATCH --ntasks=1
#SBATCH --array=0-8%5
#SBATCH --output=/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/logs/slurm/p4_markov_testonly_%A_%a.out

mkdir -p /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/logs/slurm
cd /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast
export PYTHONUNBUFFERED=1
export OMP_NUM_THREADS=4

CMDS=()
CMDS+=('/uufs/sci.utah.edu/projects/medvic-lab/Rakib/miniconda3/envs/timeenv/bin/python -u main.py --is_training 2 --model_config CSDI --paradigm_config markov_dwell --signal Single_Phase_Modulation --seeds 2021 --results_dir /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/results --checkpoint_dir /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/checkpoints --condition D2 --checkpoint_name long_term_forecast_CSDI_50_100_markov_dwell_Single_Phase_Modulation_1e-06_0.0005_16_seed2021 --num_workers 4')
CMDS+=('/uufs/sci.utah.edu/projects/medvic-lab/Rakib/miniconda3/envs/timeenv/bin/python -u main.py --is_training 2 --model_config CSDI --paradigm_config markov_dwell --signal Single_Phase_Modulation --seeds 2021 --results_dir /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/results --checkpoint_dir /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/checkpoints --condition D5 --checkpoint_name long_term_forecast_CSDI_50_100_markov_dwell_Single_Phase_Modulation_1e-06_0.0005_16_seed2021 --num_workers 4')
CMDS+=('/uufs/sci.utah.edu/projects/medvic-lab/Rakib/miniconda3/envs/timeenv/bin/python -u main.py --is_training 2 --model_config CSDI --paradigm_config markov_dwell --signal Single_Phase_Modulation --seeds 2021 --results_dir /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/results --checkpoint_dir /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/checkpoints --condition D10 --checkpoint_name long_term_forecast_CSDI_50_100_markov_dwell_Single_Phase_Modulation_1e-06_0.0005_16_seed2021 --num_workers 4')
CMDS+=('/uufs/sci.utah.edu/projects/medvic-lab/Rakib/miniconda3/envs/timeenv/bin/python -u main.py --is_training 2 --model_config CSDI --paradigm_config markov_dwell --signal Single_Phase_Modulation --seeds 2022 --results_dir /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/results --checkpoint_dir /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/checkpoints --condition D2 --checkpoint_name long_term_forecast_CSDI_50_100_markov_dwell_Single_Phase_Modulation_1e-06_0.0005_16_seed2022 --num_workers 4')
CMDS+=('/uufs/sci.utah.edu/projects/medvic-lab/Rakib/miniconda3/envs/timeenv/bin/python -u main.py --is_training 2 --model_config CSDI --paradigm_config markov_dwell --signal Single_Phase_Modulation --seeds 2022 --results_dir /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/results --checkpoint_dir /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/checkpoints --condition D5 --checkpoint_name long_term_forecast_CSDI_50_100_markov_dwell_Single_Phase_Modulation_1e-06_0.0005_16_seed2022 --num_workers 4')
CMDS+=('/uufs/sci.utah.edu/projects/medvic-lab/Rakib/miniconda3/envs/timeenv/bin/python -u main.py --is_training 2 --model_config CSDI --paradigm_config markov_dwell --signal Single_Phase_Modulation --seeds 2022 --results_dir /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/results --checkpoint_dir /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/checkpoints --condition D10 --checkpoint_name long_term_forecast_CSDI_50_100_markov_dwell_Single_Phase_Modulation_1e-06_0.0005_16_seed2022 --num_workers 4')
CMDS+=('/uufs/sci.utah.edu/projects/medvic-lab/Rakib/miniconda3/envs/timeenv/bin/python -u main.py --is_training 2 --model_config CSDI --paradigm_config markov_dwell --signal Single_Phase_Modulation --seeds 2023 --results_dir /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/results --checkpoint_dir /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/checkpoints --condition D2 --checkpoint_name long_term_forecast_CSDI_50_100_markov_dwell_Single_Phase_Modulation_1e-06_0.0005_16_seed2023 --num_workers 4')
CMDS+=('/uufs/sci.utah.edu/projects/medvic-lab/Rakib/miniconda3/envs/timeenv/bin/python -u main.py --is_training 2 --model_config CSDI --paradigm_config markov_dwell --signal Single_Phase_Modulation --seeds 2023 --results_dir /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/results --checkpoint_dir /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/checkpoints --condition D5 --checkpoint_name long_term_forecast_CSDI_50_100_markov_dwell_Single_Phase_Modulation_1e-06_0.0005_16_seed2023 --num_workers 4')
CMDS+=('/uufs/sci.utah.edu/projects/medvic-lab/Rakib/miniconda3/envs/timeenv/bin/python -u main.py --is_training 2 --model_config CSDI --paradigm_config markov_dwell --signal Single_Phase_Modulation --seeds 2023 --results_dir /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/results --checkpoint_dir /uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/TimeSynth_runs/revision/checkpoints --condition D10 --checkpoint_name long_term_forecast_CSDI_50_100_markov_dwell_Single_Phase_Modulation_1e-06_0.0005_16_seed2023 --num_workers 4')

echo "[$(date)] task $SLURM_ARRAY_TASK_ID on $(hostname): ${CMDS[$SLURM_ARRAY_TASK_ID]}"
eval "${CMDS[$SLURM_ARRAY_TASK_ID]}"
rc=$?
echo "[$(date)] exit $rc"
exit $rc
