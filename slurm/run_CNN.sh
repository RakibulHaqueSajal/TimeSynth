#!/bin/bash

export CUDA_VISIBLE_DEVICES=0

# Create directories if they don't exist

if [ ! -d "./logs" ]; then
    mkdir ./logs
fi

if [ ! -d "./logs/LongForecasting" ]; then
    mkdir ./logs/LongForecasting
fi

if [ ! -d "./logs/LongForecasting/synthetic_CNN" ]; then
    mkdir ./logs/LongForecasting/synthetic_CNN
fi




# #Drift Harmonic Clean Version


#ModernTCN

# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Drift_Harmonic_Clean
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
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# #MICN with Regre

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Drift_Harmonic_Clean
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #MICN with mean
# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Drift_Harmonic_Clean
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #Drift Harmonic (SNR_Level_1)
# #ModernTCN

# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Drift_Harmonic_SNR_level_1
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
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# #MICN with Regre

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Drift_Harmonic_SNR_level_1
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #MICN with mean
# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Drift_Harmonic_SNR_level_1
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done


# #Drift Harmonic (SNR_Level_2)
# #ModernTCN

# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Drift_Harmonic_SNR_level_2
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
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# #MICN with Regre

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Drift_Harmonic_SNR_level_2
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #MICN with mean
# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Drift_Harmonic_SNR_level_2
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done

# #Drift Harmonic(Level-3)
# #ModernTCN

# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Drift_Harmonic_SNR_level_3
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
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# #MICN with Regre

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Drift_Harmonic_SNR_level_3
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #MICN with mean
# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean__Drift_Harmonic_SNR_level_3
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done


#phase modulation clean version

#Single_Phase_Modulation Clean Version


#ModernTCN

# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Single_Phase_Modulation_Clean
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
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# #MICN with Regre

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Single_Phase_Modulation_Clean
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #MICN with mean
# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Single_Phase_Modulation_Clean
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #Single_Phase_Modulation (SNR_Level_1)
# #ModernTCN

# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Single_Phase_Modulation_SNR_level_1
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
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# #MICN with Regre

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Single_Phase_Modulation_SNR_level_1
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #MICN with mean
# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Single_Phase_Modulation_SNR_level_1
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done


# #Single_Phase_Modulation (SNR_Level_2)
# #ModernTCN

# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Single_Phase_Modulation_SNR_level_2
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
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# #MICN with Regre

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Single_Phase_Modulation_SNR_level_2
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #MICN with mean
# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Single_Phase_Modulation_SNR_level_2
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done

# #Single_Phase_Modulation(Level-3)
# #ModernTCN

# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Single_Phase_Modulation_SNR_level_3
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
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# #MICN with Regre

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Single_Phase_Modulation_SNR_level_3
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #MICN with mean
# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean__Single_Phase_Modulation_SNR_level_3
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done

#phase modulation clean version

#Dual_Phase_Modulation Clean Version


#ModernTCN

# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
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
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# #MICN with Regre

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #MICN with mean
# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #Dual_Phase_Modulation (SNR_Level_1)
# #ModernTCN

# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Dual_Phase_Modulation_SNR_level_1
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
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
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# #MICN with Regre

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Dual_Phase_Modulation_SNR_level_1
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #MICN with mean
# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Dual_Phase_Modulation_SNR_level_1
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done


# #Dual_Phase_Modulation (SNR_Level_2)
# #ModernTCN

# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Dual_Phase_Modulation_SNR_level_2
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
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
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# #MICN with Regre

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Dual_Phase_Modulation_SNR_level_2
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #MICN with mean
# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Dual_Phase_Modulation_SNR_level_2
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done

# #Dual_Phase_Modulation(Level-3)
# #ModernTCN

# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Dual_Phase_Modulation_SNR_level_3
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
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
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# #MICN with Regre

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Dual_Phase_Modulation_SNR_level_3
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# ##MICN with mean
# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean__Dual_Phase_Modulation_SNR_level_3
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done



##Distribution_Test

# ##Drift_Harmonic 

#ModernTCN

# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.85_1.10
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
#     --pred_len $pred_len \
#     --distribution_number _Shift_0\
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 



# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.35_0.60
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
#     --pred_len $pred_len \
#     --distribution_number _Shift_1\
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 







# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.60_0.85
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
#     --pred_len $pred_len \
#     --distribution_number _Shift_2\
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_1.10_1.35
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
#     --pred_len $pred_len \
#     --distribution_number _Shift_3\
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 






# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_1.35_1.60
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
#     --pred_len $pred_len \
#     --distribution_number _Shift_4\
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 



# #MICN



# #MICN with Regre

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.85_1.10
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --distribution_number _Shift_0\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 



# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.35_0.60
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --distribution_number _Shift_1\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 



# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.60_0.85
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --distribution_number _Shift_2\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_1.10_1.35
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --distribution_number _Shift_3\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 



# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_1.35_1.60
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --distribution_number _Shift_4\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# #MICN Mean

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.85_1.10
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --distribution_number _Shift_0\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 



# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.35_0.60
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --distribution_number _Shift_1\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 



# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.60_0.85
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --distribution_number _Shift_2\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_1.10_1.35
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --distribution_number _Shift_3\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 



# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_1.35_1.60
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --distribution_number _Shift_4\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 



##Single_Sine_Phase_Modulation_OOD_Distribution_Check


#ModernTCN

# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.680_1.410
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
#     --pred_len $pred_len \
#     --distribution_number _Shift_0\
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 



# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.000_0.340
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
#     --pred_len $pred_len \
#     --distribution_number _Shift_1\
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 







# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.340_0.680
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
#     --pred_len $pred_len \
#     --distribution_number _Shift_2\
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_1.410_2.140
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
#     --pred_len $pred_len \
#     --distribution_number _Shift_3\
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 






# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_2.140_2.880
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
#     --pred_len $pred_len \
#     --distribution_number _Shift_4\
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 



# #MICN



# #MICN with Regre

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.680_1.410
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --distribution_number _Shift_0\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 



# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.000_0.340
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --distribution_number _Shift_1\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 



# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.340_0.680
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --distribution_number _Shift_2\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_1.410_2.140
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --distribution_number _Shift_3\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 



# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_2.140_2.880
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --distribution_number _Shift_4\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# #MICN Mean

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.680_1.410
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --distribution_number _Shift_0\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 



# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.000_0.340
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --distribution_number _Shift_1\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 



# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.340_0.680
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --distribution_number _Shift_2\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_1.410_2.140
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --distribution_number _Shift_3\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 



# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_2.140_2.880
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --distribution_number _Shift_4\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 







#Dual Phase Modulation

#ModernTCN

# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.68_1.41__f1_0.68_1.41
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
#     --pred_len $pred_len \
#     --distribution_number _Shift_0 \
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# #MICN with Regre

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.68_1.41__f1_0.68_1.41
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --distribution_number _Shift_0 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #MICN with mean
# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.68_1.41__f1_0.68_1.41
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --distribution_number _Shift_0 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# ##SHIFT_1

# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.00_0.34__f1_0.00_0.34
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
#     --pred_len $pred_len \
#     --distribution_number _Shift_1 \
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# #MICN with Regre

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.00_0.34__f1_0.00_0.34
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --distribution_number _Shift_1 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #MICN with mean
# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.00_0.34__f1_0.00_0.34
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --distribution_number _Shift_1 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# ##SHIFT_2

# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.34_0.68__f1_0.34_0.68
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
#     --pred_len $pred_len \
#     --distribution_number _Shift_2 \
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# #MICN with Regre

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.34_0.68__f1_0.34_0.68
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --distribution_number _Shift_2 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #MICN with mean
# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.34_0.68__f1_0.34_0.68
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --distribution_number _Shift_2 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 



# #Shift_3

# ##SHIFT_2

# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_1.41_2.14__f1_1.41_2.14
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
#     --pred_len $pred_len \
#     --distribution_number _Shift_3 \
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# #MICN with Regre

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_1.41_2.14__f1_1.41_2.14
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --distribution_number _Shift_3 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #MICN with mean
# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_1.41_2.14__f1_1.41_2.14
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --distribution_number _Shift_3 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# ##Shift_4
# #Training on Clean Testing on Noise



# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_2.14_2.88__f1_2.14_2.88
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
#     --pred_len $pred_len \
#     --distribution_number _Shift_4 \
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# #MICN with Regre

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_2.14_2.88__f1_2.14_2.88
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --distribution_number _Shift_4 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #MICN with mean
# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_2.14_2.88__f1_2.14_2.88
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --distribution_number _Shift_4 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 



##Training on Clean and Testing on Noise


# #Drift Harmonic Clean Version


#ModernTCN

seq_len=50
model_name=ModernTCN
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=ModernTCN_Drift_Harmonic_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
for pred_len in 100
do
    python -u main.py \
    --is_training 2\
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --distribution_number _SNR_Level_0 \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --data custom\
    --task_name  long_term_forecast\
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --ffn_ratio 4 \
    --patch_size 20 \
    --patch_stride 10 \
    --num_blocks 2 2 2 2\
    --large_size 21 19 17 13 \
    --small_size 3 3 3 3\
    --dims 64 128 256 512\
    --head_dropout 0.1 \
    --dropout 0.4\
    --enc_in 1 \
    --dropout 0.2 \
    --patience 10 \
    --use_multi_scale True \
    --small_kernel_merged True \
    --train_epochs 300\
    --patience 30 \
    --lradj 'TST' \
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 




# # #MICN with Regre

seq_len=50
model_name=MICN
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=MICN_Regre_Drift_Harmonic_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
for pred_len in 100
do
    python -u main.py \
    --is_training 2\
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --distribution_number _SNR_Level_0 \
    --root_path $root_path \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --mode regre\
    --data custom\
    --conv_kernel 7 17\
    --decomp_kernel 25 49\
    --isometric_kernel 17 49\
    --task_name  long_term_forecast\
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --label_len 50\
    --enc_in 1 \
    --dec_in 1\
    --c_out 1\
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30 \
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 

# #MICN with mean
seq_len=50
model_name=MICN
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=MICN_Mean_Drift_Harmonic_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
for pred_len in 100
do
    python -u main.py \
    --is_training 2\
    --train_sample_size $train_sample_size \
    --val_sample_size $val_sample_size \
    --test_sample_size $test_sample_size \
    --root_path $root_path \
    --distribution_number _SNR_Level_0 \
    --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
    --model $model_name \
    --mode mean\
    --data custom\
    --conv_kernel 7 17\
    --decomp_kernel 25 49\
    --isometric_kernel 17 49\
    --task_name  long_term_forecast\
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --label_len 50\
    --enc_in 1 \
    --dec_in 1\
    --c_out 1\
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30 \
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 

# #Drift Harmonic (SNR_Level_1)
# #ModernTCN

seq_len=50
model_name=ModernTCN
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=ModernTCN_Drift_Harmonic_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_1
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
    --distribution_number _SNR_Level_1 \
    --task_name  long_term_forecast\
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --ffn_ratio 4 \
    --patch_size 20 \
    --patch_stride 10 \
    --num_blocks 2 2 2 2\
    --large_size 21 19 17 13 \
    --small_size 3 3 3 3\
    --dims 64 128 256 512\
    --head_dropout 0.1 \
    --dropout 0.4\
    --enc_in 1 \
    --dropout 0.2 \
    --patience 10 \
    --use_multi_scale True \
    --small_kernel_merged True \
    --train_epochs 300\
    --patience 30 \
    --lradj 'TST' \
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 




#MICN with Regre

seq_len=50
model_name=MICN
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=MICN_Regre_Drift_Harmonic_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_1
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
    --mode regre\
    --data custom\
    --conv_kernel 7 17\
    --decomp_kernel 25 49\
    --isometric_kernel 17 49\
    --distribution_number _SNR_Level_1 \
    --task_name  long_term_forecast\
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --label_len 50\
    --enc_in 1 \
    --dec_in 1\
    --c_out 1\
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30 \
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 

#MICN with mean
# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Drift_Harmonic_Clean
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --distribution_number _SNR_Level_1 \
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done


# # #Drift Harmonic (SNR_Level_2)
# # #ModernTCN

# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Drift_Harmonic_Clean
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
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# # #MICN with Regre

seq_len=50
model_name=MICN
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=MICN_Regre_Drift_Harmonic_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_2
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
    --mode regre\
    --data custom\
    --conv_kernel 7 17\
    --decomp_kernel 25 49\
    --isometric_kernel 17 49\
    --task_name  long_term_forecast\
    --distribution_number _SNR_Level_2 \
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --label_len 50\
    --enc_in 1 \
    --dec_in 1\
    --c_out 1\
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30 \
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 

# #MICN with mean
# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Drift_Harmonic_Clean
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
#     --mode mean\
#     --data custom\
#     --distribution_number _SNR_Level_2 \
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done

# # #Drift Harmonic(Level-3)
# # #ModernTCN

# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Drift_Harmonic_Clean
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
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# # #MICN with Regre

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Drift_Harmonic_Clean
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_3 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

#MICN with mean
seq_len=50
model_name=MICN
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=MICN_Mean_Drift_Harmonic_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_3
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
    --mode mean\
    --data custom\
    --conv_kernel 7 17\
    --distribution_number _SNR_Level_3 \
    --decomp_kernel 25 49\
    --isometric_kernel 17 49\
    --task_name  long_term_forecast\
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --label_len 50\
    --enc_in 1 \
    --dec_in 1\
    --c_out 1\
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30 \
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done



#Single_Phase_Modulation Clean Version


#ModernTCN

# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Single_Phase_Modulation_Clean
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
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# #MICN with Regre

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Single_Phase_Modulation_Clean
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --distribution_number _SNR_Level_0 \
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #MICN with mean
# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Single_Phase_Modulation_Clean
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_0 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #Single_Phase_Modulation (SNR_Level_1)
# #ModernTCN

# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Single_Phase_Modulation_Clean
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
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# #MICN with Regre

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Single_Phase_Modulation_Clean
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_1 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #MICN with mean
# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Single_Phase_Modulation_Clean
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --distribution_number _SNR_Level_1 \
#     --task_name  long_term_forecast\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done


# #Single_Phase_Modulation (SNR_Level_2)
# #ModernTCN

seq_len=50
model_name=ModernTCN
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=ModernTCN_Single_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
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
    --distribution_number _SNR_Level_2 \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --ffn_ratio 4 \
    --patch_size 20 \
    --patch_stride 10 \
    --num_blocks 2 2 2 2\
    --large_size 21 19 17 13 \
    --small_size 3 3 3 3\
    --dims 64 128 256 512\
    --head_dropout 0.1 \
    --dropout 0.4\
    --enc_in 1 \
    --dropout 0.2 \
    --patience 10 \
    --use_multi_scale True \
    --small_kernel_merged True \
    --train_epochs 300\
    --patience 30 \
    --lradj 'TST' \
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 




#MICN with Regre

seq_len=50
model_name=MICN
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=MICN_Regre_Single_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
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
    --mode regre\
    --data custom\
    --conv_kernel 7 17\
    --decomp_kernel 25 49\
    --isometric_kernel 17 49\
    --task_name  long_term_forecast\
    --distribution_number _SNR_Level_2 \
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --label_len 50\
    --enc_in 1 \
    --dec_in 1\
    --c_out 1\
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30 \
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 

#MICN with mean
seq_len=50
model_name=MICN
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=MICN_Mean_Single_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
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
    --mode mean\
    --data custom\
    --conv_kernel 7 17\
    --decomp_kernel 25 49\
    --isometric_kernel 17 49\
    --task_name  long_term_forecast\
    --distribution_number _SNR_Level_2 \
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --label_len 50\
    --enc_in 1 \
    --dec_in 1\
    --c_out 1\
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30 \
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done

#Single_Phase_Modulation(Level-3)
#ModernTCN

seq_len=50
model_name=ModernTCN
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=ModernTCN_Single_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
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
    --distribution_number _SNR_Level_3 \
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --ffn_ratio 4 \
    --patch_size 20 \
    --patch_stride 10 \
    --num_blocks 2 2 2 2\
    --large_size 21 19 17 13 \
    --small_size 3 3 3 3\
    --dims 64 128 256 512\
    --head_dropout 0.1 \
    --dropout 0.4\
    --enc_in 1 \
    --dropout 0.2 \
    --patience 10 \
    --use_multi_scale True \
    --small_kernel_merged True \
    --train_epochs 300\
    --patience 30 \
    --lradj 'TST' \
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 




#MICN with Regre

seq_len=50
model_name=MICN
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=MICN_Regre_Single_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
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
    --distribution_number _SNR_Level_3 \
    --mode regre\
    --data custom\
    --conv_kernel 7 17\
    --decomp_kernel 25 49\
    --isometric_kernel 17 49\
    --task_name  long_term_forecast\
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --label_len 50\
    --enc_in 1 \
    --dec_in 1\
    --c_out 1\
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30 \
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done 

#MICN with mean
seq_len=50
model_name=MICN
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=MICN_Mean_Single_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
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
    --mode mean\
    --data custom\
    --conv_kernel 7 17\
    --decomp_kernel 25 49\
    --isometric_kernel 17 49\
    --task_name  long_term_forecast\
    --distribution_number _SNR_Level_3 \
    --features S \
    --seq_len $seq_len \
    --pred_len $pred_len \
    --label_len 50\
    --enc_in 1 \
    --dec_in 1\
    --c_out 1\
    --hidden_dims  256  512\
    --train_epochs 300\
    --patience 30 \
    --lradj 'TST' \
    --weight_decay 0.0001\
    --mlp_dropout 0.3 \
    --backcast 0\
    --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
done



#Dual Phase Modulation 




# #ModernTCN

# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
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
#     --pred_len $pred_len \
#     --distribution_number _SNR_Level_0 \
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# #MICN with Regre

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_0 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #MICN with mean
# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_0 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #Dual_Phase_Modulation (SNR_Level_1)
# #ModernTCN

# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
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
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# #MICN with Regre

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_1\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #MICN with mean
# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_1 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done


# #Dual_Phase_Modulation (SNR_Level_2)
# #ModernTCN

# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
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
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# #MICN with Regre

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Dual_Phase_Modulation_Clean 
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_2 \
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# #MICN with mean
# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_2\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done

# #Dual_Phase_Modulation(Level-3)
# #ModernTCN

# seq_len=50
# model_name=ModernTCN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=ModernTCN_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
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
#     --distribution_number _SNR_Level_3\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --ffn_ratio 4 \
#     --patch_size 20 \
#     --patch_stride 10 \
#     --num_blocks 2 2 2 2\
#     --large_size 21 19 17 13 \
#     --small_size 3 3 3 3\
#     --dims 64 128 256 512\
#     --head_dropout 0.1 \
#     --dropout 0.4\
#     --enc_in 1 \
#     --dropout 0.2 \
#     --patience 10 \
#     --use_multi_scale True \
#     --small_kernel_merged True \
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 




# #MICN with Regre

# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Regre_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
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
#     --mode regre\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_3\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

# # #MICN with mean
# seq_len=50
# model_name=MICN
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MICN_Mean_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
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
#     --mode mean\
#     --data custom\
#     --conv_kernel 7 17\
#     --decomp_kernel 25 49\
#     --isometric_kernel 17 49\
#     --task_name  long_term_forecast\
#     --distribution_number _SNR_Level_3\
#     --features S \
#     --seq_len $seq_len \
#     --pred_len $pred_len \
#     --label_len 50\
#     --enc_in 1 \
#     --dec_in 1\
#     --c_out 1\
#     --hidden_dims  256  512\
#     --train_epochs 300\
#     --patience 30 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_CNN/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done

