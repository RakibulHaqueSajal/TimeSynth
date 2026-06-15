
# #!/bin/bash

export CUDA_VISIBLE_DEVICES=0

# Create directories if they don't exist

if [ ! -d "./logs" ]; then
    mkdir ./logs
fi

if [ ! -d "./logs/LongForecasting" ]; then
    mkdir ./logs/LongForecasting
fi

if [ ! -d "./logs/LongForecasting/synthetic_MLP_Models" ]; then
    mkdir ./logs/LongForecasting/synthetic_MLP_Models
fi






# #Drift Harmonic Clean

# #Normal MLP

# seq_len=50
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 60 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# # #Nbeats
   


# seq_len=50
# model_name=NBeats
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Nbeats_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --n_blocks 6\
#     --n_layers 5\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 60 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --block_type generic\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done



# # #FreTS

# seq_len=50
# model_name=FreMLP
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FreMLP__Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
# for pred_len in 100 200
# do
#     python -u main.py \
#     --is_training 0\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 60 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 



# #Drift Harmonic (SNR-Level-1)
# # #Normal MLP

# seq_len=50
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Drift_Harmonic_SNR_Level_1
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 60 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# # #Nbeats
   


# seq_len=50
# model_name=NBeats
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Nbeats_Drift_Harmonic_SNR_Level_1
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0  \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --n_blocks 6\
#     --n_layers 5\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 60 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --block_type generic\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done



# # #FreTS

# seq_len=50
# model_name=FreMLP
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FreMLP_Drift_Harmonic_SNR_Level_1
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 60 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #Drift Harmonic SNR_Level_2


# #MLinear
# seq_len=50
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Drift_Harmonic_SNR_Level_2
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 60 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# # #Nbeats
   


# seq_len=50
# model_name=NBeats
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Nbeats_Drift_Harmonic_SNR_Level_2
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --n_blocks 6\
#     --n_layers 5\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 60 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --block_type generic\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done



# # #FreTS

# seq_len=50
# model_name=FreMLP
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FreMLP_Drift_Harmonic_SNR_Level_2
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 60 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# ##Drift Harmonic (SNR_Level_3)

# #MLinear
# seq_len=50
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Drift_Harmonic_SNR_Level_3
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 60 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# # #Nbeats
   


# seq_len=50
# model_name=NBeats
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Nbeats_Drift_Harmonic_SNR_Level_3
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --n_blocks 6\
#     --n_layers 5\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 60 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --block_type generic\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done



# # #FreTS

# seq_len=50
# model_name=FreMLP
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FreMLP_Drift_Harmonic_SNR_Level_3
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 60 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 





# # #Phasemod Single Phase Clean

# # # #Normal MLP

# seq_len=50
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/clean
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# # #Nbeats
   


# seq_len=50
# model_name=NBeats
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Nbeats_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/clean
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --n_blocks 6\
#     --n_layers 5\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --block_type generic\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done



# # #FreTS

# seq_len=50
# model_name=FreMLP
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FreMLP__Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/clean
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 



# #PhaseMod Single Phase (SNR-Level-1)
# # #Normal MLP

# seq_len=50
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Single_Phase_Modulation_SNR_Level_1
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# # #Nbeats
   


# seq_len=50
# model_name=NBeats
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Nbeats_Single_Phase_Modulation_SNR_Level_1
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --n_blocks 6\
#     --n_layers 5\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --block_type generic\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done



# # #FreTS

# seq_len=50
# model_name=FreMLP
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FreMLP_Single_Phase_Modulation_SNR_Level_1
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #PhaseMod SNR_Level_2


# #MLinear
# seq_len=50
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Single_Phase_Modulation_SNR_Level_2
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# # #Nbeats
   


# seq_len=50
# model_name=NBeats
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Nbeats_Single_Phase_Modulation_SNR_Level_2
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --n_blocks 6\
#     --n_layers 5\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --block_type generic\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done



# # #FreTS

# seq_len=50
# model_name=FreMLP
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FreMLP_Single_Phase_Modulation_SNR_Level_2
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# #PhaseMod Single Phase  (SNR_Level_3)

# #MLinear
# seq_len=50
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Single_Phase_Modulation_SNR_Level_3
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# # #Nbeats
   


# seq_len=50
# model_name=NBeats
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Nbeats_Single_Phase_Modulation_SNR_Level_3
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --n_blocks 6\
#     --n_layers 5\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --block_type generic\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done



# # #FreTS

# seq_len=50
# model_name=FreMLP
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FreMLP_Single_Phase_Modulation_SNR_Level_3
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 





# #PhaseMod Dual Phase Clean

# #Normal MLP

# seq_len=50
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0 \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# # #Nbeats
   


# seq_len=50
# model_name=NBeats
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Nbeats_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0 \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --n_blocks 6\
#     --n_layers 5\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --block_type generic\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done



# # #FreTS

# seq_len=50
# model_name=FreMLP
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FreMLP__Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0 \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 



# #PhaseMod Dual Phase (SNR-Level-1)
# # #Normal MLP

# seq_len=50
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Dual_Phase_Modulation_SNR_Level_1
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0 \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# # #Nbeats
   


# seq_len=50
# model_name=NBeats
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Nbeats_Dual_Phase_Modulation_SNR_Level_1
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0 \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --n_blocks 6\
#     --n_layers 5\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --block_type generic\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done



# # #FreTS

# seq_len=50
# model_name=FreMLP
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FreMLP_Dual_Phase_Modulation_SNR_Level_1
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0 \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #PhaseMod SNR_Level_2


# #MLinear
# seq_len=50
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Dual_Phase_Modulation_SNR_Level_2
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0 \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# # #Nbeats
   


# seq_len=50
# model_name=NBeats
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Nbeats_Dual_Phase_Modulation_SNR_Level_2
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0 \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --n_blocks 6\
#     --n_layers 5\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --block_type generic\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done



# # #FreTS

# seq_len=50
# model_name=FreMLP
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FreMLP_Dual_Phase_Modulation_SNR_Level_2
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0 \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# #PhaseMod Dual Phase  (SNR_Level_3)

# #MLinear
# seq_len=50
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Dual_Phase_Modulation_SNR_Level_3
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0 \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# # #Nbeats
   


# seq_len=50
# model_name=NBeats
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Nbeats_Dual_Phase_Modulation_SNR_Level_3
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0 \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --n_blocks 6\
#     --n_layers 5\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --block_type generic\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done



# # #FreTS

# seq_len=50
# model_name=FreMLP
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FreMLP_Dual_Phase_Modulation_SNR_Level_3
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 0 \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 






# #Train on Clean Test on Noisy





# #Drift Harmonic (SNR-Level-0)

#  #Normal MLP

# seq_len=50
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --distribution_number _SNR_Level_0 \
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 60 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# # #Nbeats
   


# seq_len=50
# model_name=NBeats
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Nbeats_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --distribution_number _SNR_Level_0 \
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --n_blocks 6\
#     --n_layers 5\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 60 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --block_type generic\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done



# # #FreTS

# seq_len=50
# model_name=FreMLP
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FreMLP__Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
# for pred_len in 100
# do
#     python -u main.py \
#     --is_training 2\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_0 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 60 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 



# #Drift Harmonic (SNR-Level-1)
# # #Normal MLP

# seq_len=50
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_1 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 60 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# # #Nbeats
   


# seq_len=50
# model_name=NBeats
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Nbeats_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2  \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_1 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --n_blocks 6\
#     --n_layers 5\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 60 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --block_type generic\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done



# # #FreTS

# seq_len=50
# model_name=FreMLP
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FreMLP__Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --distribution_number _SNR_Level_1 \
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 60 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #Drift Harmonic SNR_Level_2


# #MLinear
# seq_len=50
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_2 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 60 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# # #Nbeats
   


# seq_len=50
# model_name=NBeats
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Nbeats_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_2 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --n_blocks 6\
#     --n_layers 5\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 60 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --block_type generic\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done



# # #FreTS

# seq_len=50
# model_name=FreMLP
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FreMLP__Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --distribution_number _SNR_Level_2 \
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 60 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# ##Drift Harmonic (SNR_Level_3)

# #MLinear
# seq_len=50
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --distribution_number _SNR_Level_3 \
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 60 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# # #Nbeats
   


# seq_len=50
# model_name=NBeats
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Nbeats_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_3 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --n_blocks 6\
#     --n_layers 5\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 60 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --block_type generic\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done



# # #FreTS

# seq_len=50
# model_name=FreMLP
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FreMLP__Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --distribution_number _SNR_Level_3 \
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 60 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 












# # # #Phasemod Single Phase Clean

# # # # #Normal MLP

# seq_len=50
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/clean
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --distribution_number _SNR_Level_0 \
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# # #Nbeats
   


# seq_len=50
# model_name=NBeats
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Nbeats_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/clean
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_0 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --n_blocks 6\
#     --n_layers 5\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --block_type generic\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done



# # #FreTS

# seq_len=50
# model_name=FreMLP
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FreMLP__Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/clean
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_0 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 



# #PhaseMod Single Phase (SNR-Level-1)
# # #Normal MLP

# seq_len=50
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_1 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# # #Nbeats
   


# seq_len=50
# model_name=NBeats
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Nbeats_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_1 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --n_blocks 6\
#     --n_layers 5\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --block_type generic\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done



# # #FreTS

# seq_len=50
# model_name=FreMLP
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FreMLP__Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --distribution_number _SNR_Level_1 \
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# # #PhaseMod SNR_Level_2


# #MLinear
# seq_len=50
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2 \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --distribution_number _SNR_Level_2 \
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# # # #Nbeats
   


# seq_len=50
# model_name=NBeats
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Nbeats_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_2\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --n_blocks 6\
#     --n_layers 5\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --block_type generic\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done



# # #FreTS

# seq_len=50
# model_name=FreMLP
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FreMLP__Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_2 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# #PhaseMod Single Phase  (SNR_Level_3)

# #MLinear
# seq_len=50
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --distribution_number _SNR_Level_3 \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# # #Nbeats
   


# seq_len=50
# model_name=NBeats
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Nbeats_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_3 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --n_blocks 6\
#     --n_layers 5\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --block_type generic\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done



# # #FreTS

# seq_len=50
# model_name=FreMLP
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FreMLP__Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2\
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_3 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# ##Dual_Phase_Clean

# #PhaseMod Dual Phase Clean

# # #Normal MLP

# seq_len=50
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2 \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_0 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# # #Nbeats
   
 
# seq_len=50
# model_name=NBeats
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Nbeats_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2 \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_0 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --n_blocks 6\
#     --n_layers 5\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --block_type generic\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done



# # #FreTS

# seq_len=50
# model_name=FreMLP
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FreMLP__Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2 \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_0 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 



# #PhaseMod Dual Phase (SNR-Level-1)
# # #Normal MLP

# seq_len=50
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2 \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_1 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# # # #Nbeats
   


# seq_len=50
# model_name=NBeats
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Nbeats_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2 \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_1 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --n_blocks 6\
#     --n_layers 5\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --block_type generic\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done



# # # #FreTS

# seq_len=50
# model_name=FreMLP
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FreMLP__Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2 \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --distribution_number _SNR_Level_1 \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# # #PhaseMod SNR_Level_2


# #MLinear

# seq_len=50
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2 \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_2 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# # # #Nbeats
   


# seq_len=50
# model_name=NBeats
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Nbeats_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2 \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_2 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --n_blocks 6\
#     --n_layers 5\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --block_type generic\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done



# # #FreTS

# seq_len=50
# model_name=FreMLP
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FreMLP__Dual_Phase_Modulation_Clean 
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2 \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_2 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# #PhaseMod Dual Phase  (SNR_Level_3)

# #MLinear
# seq_len=50
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2 \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_3 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# # #Nbeats
   


# seq_len=50
# model_name=NBeats
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Nbeats_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2 \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --distribution_number _SNR_Level_3 \
#     --enc_in 1 \
#     --n_blocks 6\
#     --n_layers 5\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --block_type generic\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done



# # #FreTS

# seq_len=50
# model_name=FreMLP
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FreMLP__Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#     --is_training 2 \
#     --train_sample_size $train_sample_size \
#     --val_sample_size $val_sample_size \
#     --test_sample_size $test_sample_size \
#     --root_path $root_path \
#     --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#     --model $model_name \
#     --data custom\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_3 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --enc_in 1 \
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30\
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




##Drift Harmonic (SNR_Level_4)

#MLinear
seq_len=50
model_name=MLinear
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=MLinear_Drift_Harmonic_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_4
for pred_len in 100 
do
    python -u main.py \
    --is_training 2\
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --distribution_number _SNR_Level_4 \
    --task_name  long_term_forecast\
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --enc_in 1 \
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 60 \
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 


# #Nbeats
   


seq_len=50
model_name=NBeats
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Nbeats_Drift_Harmonic_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_4
for pred_len in 100 
do
    python -u main.py \
    --is_training 2\
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --task_name  long_term_forecast\
    --distribution_number _SNR_Level_4 \
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --enc_in 1 \
    --n_blocks 6\
    --n_layers 5\
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 60 \
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --block_type generic\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done



# #FreTS

seq_len=50
model_name=FreMLP
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=FreMLP__Drift_Harmonic_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_4
for pred_len in 100 
do
    python -u main.py \
    --is_training 2\
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --distribution_number _SNR_Level_4 \
    --task_name  long_term_forecast\
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --enc_in 1 \
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 60 \
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 


#Drift_Harmonic SNR_Level_5

##Drift Harmonic (SNR_Level_5)

#MLinear
seq_len=50
model_name=MLinear
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=MLinear_Drift_Harmonic_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_5
for pred_len in 100 
do
    python -u main.py \
    --is_training 2\
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --distribution_number _SNR_Level_5 \
    --task_name  long_term_forecast\
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --enc_in 1 \
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 60 \
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 


# #Nbeats
   


seq_len=50
model_name=NBeats
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Nbeats_Drift_Harmonic_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_5
for pred_len in 100 
do
    python -u main.py \
    --is_training 2\
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --task_name  long_term_forecast\
    --distribution_number _SNR_Level_5 \
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --enc_in 1 \
    --n_blocks 6\
    --n_layers 5\
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 60 \
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --block_type generic\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done



# #FreTS

seq_len=50
model_name=FreMLP
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=FreMLP__Drift_Harmonic_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_5
for pred_len in 100 
do
    python -u main.py \
    --is_training 2\
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --distribution_number _SNR_Level_5 \
    --task_name  long_term_forecast\
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --enc_in 1 \
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 60 \
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 


#Drift_Harmonic SNR_Level_6

##Drift Harmonic (SNR_Level_6)

#MLinear
seq_len=50
model_name=MLinear
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=MLinear_Drift_Harmonic_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_6
for pred_len in 100 
do
    python -u main.py \
    --is_training 2\
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --distribution_number _SNR_Level_6 \
    --task_name  long_term_forecast\
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --enc_in 1 \
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 60 \
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 


# #Nbeats
   


seq_len=50
model_name=NBeats
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Nbeats_Drift_Harmonic_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_6
for pred_len in 100 
do
    python -u main.py \
    --is_training 2\
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --task_name  long_term_forecast\
    --distribution_number _SNR_Level_6 \
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --enc_in 1 \
    --n_blocks 6\
    --n_layers 5\
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 60 \
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --block_type generic\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done



# #FreTS

seq_len=50
model_name=FreMLP
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=FreMLP__Drift_Harmonic_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_6
for pred_len in 100 
do
    python -u main.py \
    --is_training 2\
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --distribution_number _SNR_Level_6 \
    --task_name  long_term_forecast\
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --enc_in 1 \
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 60 \
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 

#SPM_Harmonic_Signal 
#SNR_Level_4
#MLinear
seq_len=50
model_name=MLinear
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=MLinear_Single_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_4
for pred_len in 100 
do
    python -u main.py \
    --is_training 2\
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --task_name  long_term_forecast\
    --features S \
    --seq_len $seq_len \
    --distribution_number _SNR_Level_4 \
    --pred_len $pred_len \
    --enc_in 1 \
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30\
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 


# #Nbeats
   


seq_len=50
model_name=NBeats
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Nbeats_Single_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_4
for pred_len in 100 
do
    python -u main.py \
    --is_training 2\
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --task_name  long_term_forecast\
    --distribution_number _SNR_Level_4 \
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --enc_in 1 \
    --n_blocks 6\
    --n_layers 5\
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30\
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --block_type generic\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done



# #FreTS

seq_len=50
model_name=FreMLP
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=FreMLP__Single_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_4
for pred_len in 100 
do
    python -u main.py \
    --is_training 2\
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --task_name  long_term_forecast\
    --distribution_number _SNR_Level_4 \
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --enc_in 1 \
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30\
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 

#SNR_Level_5
#SPM_Harmonic_Signal 
#SNR_Level_5
#MLinear


seq_len=50
model_name=MLinear
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=MLinear_Single_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_5
for pred_len in 100 
do
    python -u main.py \
    --is_training 2\
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --task_name  long_term_forecast\
    --features S \
    --seq_len $seq_len \
    --distribution_number _SNR_Level_5 \
    --pred_len $pred_len \
    --enc_in 1 \
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30\
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 


# #Nbeats
   


seq_len=50
model_name=NBeats
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Nbeats_Single_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_5
for pred_len in 100 
do
    python -u main.py \
    --is_training 2\
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --task_name  long_term_forecast\
    --distribution_number _SNR_Level_5 \
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --enc_in 1 \
    --n_blocks 6\
    --n_layers 5\
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30\
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --block_type generic\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done



# #FreTS

seq_len=50
model_name=FreMLP
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=FreMLP__Single_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_5
for pred_len in 100 
do
    python -u main.py \
    --is_training 2\
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --task_name  long_term_forecast\
    --distribution_number _SNR_Level_5 \
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --enc_in 1 \
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30\
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 

#SNR_Level_6
#SPM_Harmonic_Signal 
#SNR_Level_6
#MLinear


seq_len=50
model_name=MLinear
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=MLinear_Single_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_6
for pred_len in 100 
do
    python -u main.py \
    --is_training 2\
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --task_name  long_term_forecast\
    --features S \
    --seq_len $seq_len \
    --distribution_number _SNR_Level_6 \
    --pred_len $pred_len \
    --enc_in 1 \
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30\
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 


# #Nbeats
   


seq_len=50
model_name=NBeats
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Nbeats_Single_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_6
for pred_len in 100 
do
    python -u main.py \
    --is_training 2\
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --task_name  long_term_forecast\
    --distribution_number _SNR_Level_6\
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --enc_in 1 \
    --n_blocks 6\
    --n_layers 5\
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30\
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --block_type generic\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done



# #FreTS

seq_len=50
model_name=FreMLP
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=FreMLP__Single_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_6
for pred_len in 100 
do
    python -u main.py \
    --is_training 2\
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --task_name  long_term_forecast\
    --distribution_number _SNR_Level_6 \
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --enc_in 1 \
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30\
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 





##SNR_Level_4

##DPM_Harmonic_Signal


#MLinear
seq_len=50
model_name=MLinear
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=MLinear_Dual_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_4
for pred_len in 100 
do
    python -u main.py \
    --is_training 2 \
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --task_name  long_term_forecast\
    --distribution_number _SNR_Level_4\
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --enc_in 1 \
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30\
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 


# #Nbeats
   


seq_len=50
model_name=NBeats
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Nbeats_Dual_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_4
for pred_len in 100 
do
    python -u main.py \
    --is_training 2 \
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --task_name  long_term_forecast\
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --distribution_number _SNR_Level_4 \
    --enc_in 1 \
    --n_blocks 6\
    --n_layers 5\
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30\
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --block_type generic\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done



# #FreTS

seq_len=50
model_name=FreMLP
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=FreMLP__Dual_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_4
for pred_len in 100 
do
    python -u main.py \
    --is_training 2 \
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --task_name  long_term_forecast\
    --distribution_number _SNR_Level_4 \
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --enc_in 1 \
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30\
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 




##SNR_Level_5

##DPM_Harmonic_Signal


#MLinear
seq_len=50
model_name=MLinear
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=MLinear_Dual_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_5
for pred_len in 100 
do
    python -u main.py \
    --is_training 2 \
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --task_name  long_term_forecast\
    --distribution_number _SNR_Level_5\
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --enc_in 1 \
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30\
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 


# #Nbeats
   


seq_len=50
model_name=NBeats
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Nbeats_Dual_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_5
for pred_len in 100 
do
    python -u main.py \
    --is_training 2 \
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --task_name  long_term_forecast\
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --distribution_number _SNR_Level_5 \
    --enc_in 1 \
    --n_blocks 6\
    --n_layers 5\
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30\
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --block_type generic\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done



# #FreTS

seq_len=50
model_name=FreMLP
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=FreMLP__Dual_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_5
for pred_len in 100 
do
    python -u main.py \
    --is_training 2 \
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --task_name  long_term_forecast\
    --distribution_number _SNR_Level_5 \
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --enc_in 1 \
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30\
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 



##SNR_Level_6

##DPM_Harmonic_Signal


#MLinear
seq_len=50
model_name=MLinear
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=MLinear_Dual_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_6
for pred_len in 100 
do
    python -u main.py \
    --is_training 2 \
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --task_name  long_term_forecast\
    --distribution_number _SNR_Level_6\
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --enc_in 1 \
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30\
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 


# #Nbeats
   


seq_len=50
model_name=NBeats
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Nbeats_Dual_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_6
for pred_len in 100 
do
    python -u main.py \
    --is_training 2 \
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --task_name  long_term_forecast\
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --distribution_number _SNR_Level_6 \
    --enc_in 1 \
    --n_blocks 6\
    --n_layers 5\
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30\
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --block_type generic\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done



# #FreTS

seq_len=50
model_name=FreMLP
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=FreMLP__Dual_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_6
for pred_len in 100 
do
    python -u main.py \
    --is_training 2 \
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --task_name  long_term_forecast\
    --distribution_number _SNR_Level_6 \
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --enc_in 1 \
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30\
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_MLP_Models/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 


