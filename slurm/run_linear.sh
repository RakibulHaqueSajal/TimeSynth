
#!/bin/bash

export CUDA_VISIBLE_DEVICES=0

# Create directories if they don't exist

if [ ! -d "./logs" ]; then
    mkdir ./logs
fi

if [ ! -d "./logs/LongForecasting" ]; then
    mkdir ./logs/LongForecasting
fi

if [ ! -d "./logs/LongForecasting/synthetic_Linear_Models" ]; then
    mkdir ./logs/LongForecasting/synthetic_Linear_Models
fi


#Drift Harmonic Testing (Noise-Clean)


# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





# # #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done


# #Drift Harmonic Testing (SNR_Level1)

# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Drift_Harmonic_SNR_level_1
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_1
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





#  #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Drift_Harmonic_SNR_level_1
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Drift_Harmonic_SNR_level_1
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done



# #Drift Harmonic Testing (SNR_Level-2)

# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Drift_Harmonic_SNR_level_2
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_2
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





#  #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Drift_Harmonic_SNR_level_2
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Drift_Harmonic_SNR_level_2
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done


# #Drift Harmonic Testing (SNR_Level-3)
# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Drift_Harmonic_SNR_level_3
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_3
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





#  #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Drift_Harmonic_SNR_level_3
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Drift_Harmonic_SNR_level_3
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done



#Phase_Modulation_Clean


#Phase_Modulation Clean (Noise-Clean)


#Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/clean
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





# # #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/clean
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/clean
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done


# #Drift Harmonic Testing (SNR_Level1)

# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Single_Phase_Modulation_SNR_level_1
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_1
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





#  #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Single_Phase_Modulation_SNR_level_1
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Single_Phase_Modulation_SNR_level_1
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done



# #Drift Harmonic Testing (SNR_Level-2)

# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Single_Phase_Modulation_SNR_level_2
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





#  #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Single_Phase_Modulation_SNR_level_2
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Single_Phase_Modulation_SNR_level_2
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done



# #Drift Harmonic Testing (SNR_Level-3)
# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Single_Phase_Modulation_SNR_level_3
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





#  #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Single_Phase_Modulation_SNR_level_3
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Single_Phase_Modulation_SNR_level_3
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done


#Dual_Sine_Phase_Modulation
#Dual_Phase_Modulation_Clean


#Dual_Phase_Modulation Clean (Noise-Clean)


#Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





# # #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done


# #Dual_Phase_Modulation(SNR_Level1)

# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Dual_Phase_Modulation_SNR_level_1
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





#  #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Dual_Phase_Modulation_SNR_level_1
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Dual_Phase_Modulation_SNR_level_1
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done



# #Dual_Phase_Modulation(SNR_Level-2)

# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Dual_Phase_Modulation_SNR_level_2
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





#  #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Dual_Phase_Modulation_SNR_level_2
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
seq_len=50
model_name=FITS
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=FITS_Dual_Phase_Modulation_SNR_level_2
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
for pred_len in 100 
do
    python -u main.py \
      --is_training 0\
      --train_sample_size $train_sample_size \
      --val_sample_size $val_sample_size \
      --test_sample_size $test_sample_size \
      --root_path $root_path \
      --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
      --model $model_name \
      --data custom \
      --task_name long_term_forecast \
      --features S \
      --target Value \
      --seq_len $seq_len \
      --pred_len $pred_len \
      --enc_in 1 \
      --patience 70 \
      --train_epochs 300 \
      --itr 1 \
      --batch_size 128 \
      --lradj 'TST' \
      --weight_decay 0.001 \
      --backcast 0\
      --revin 1\
      --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
done



# #Dual_Phase_Modulation(SNR_Level-3)

# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Dual_Phase_Modulation_SNR_level_3
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





#  #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Dual_Phase_Modulation_SNR_level_3
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 0\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

#FITS
seq_len=50
model_name=FITS
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=FITS_Dual_Phase_Modulation_SNR_level_3
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
for pred_len in 100 
do
    python -u main.py \
      --is_training 0\
      --train_sample_size $train_sample_size \
      --val_sample_size $val_sample_size \
      --test_sample_size $test_sample_size \
      --root_path $root_path \
      --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
      --model $model_name \
      --data custom \
      --task_name long_term_forecast \
      --features S \
      --target Value \
      --seq_len $seq_len \
      --pred_len $pred_len \
      --enc_in 1 \
      --patience 70 \
      --train_epochs 300 \
      --itr 1 \
      --batch_size 128 \
      --lradj 'TST' \
      --weight_decay 0.001 \
      --backcast 0\
      --revin 1\
      --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
done








###Distribution_Shift_Check_in_Drift_Harmonic

##Linear



# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.85_1.10
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_0\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# ##Shift_1

# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.35_0.60
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_1\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done


# ## Shift_2

# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.60_0.85
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_2\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done



# ## Shift_3

# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_1.10_1.35
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_3\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done


# ## Shift_4



# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_1.35_1.60
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_4\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done


###DLinear 


# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.85_1.10
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_0\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# ##Shift_1

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.35_0.60
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_1\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done


# ## Shift_2

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.60_0.85
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_2\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done



# ## Shift_3

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_1.10_1.35
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_3\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done


# ## Shift_4



# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_1.35_1.60
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_4\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done



##FITS

##Shift-0

# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.85_1.10
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_0\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done



# #Shift_1
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.35_0.60
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_1\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #Shift_1
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.60_0.85
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_2\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done




# #Shift_2
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_1.10_1.35
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_3\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done




# #Shift_3
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_1.35_1.60
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_4\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done



#Distribution check

#Single Phase Modulation



##Linear



# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.680_1.410
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_0\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# ##Shift_1

# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.000_0.340
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_1\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done


# ## Shift_2

# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.340_0.680
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_2\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done



# ## Shift_3

# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_1.410_2.140
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_3\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done


# ## Shift_4



# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_2.140_2.880
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_4\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done


# ##DLinear 


# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.680_1.410
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_0\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# ##Shift_1

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.000_0.340
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_1\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done


# ## Shift_2

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.340_0.680
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_2\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done



## Shift_3

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_1.410_2.140
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_3\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done


# ## Shift_4



# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_2.140_2.880
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_4\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done



# #FITS

# #Shift-0

# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.680_1.410
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_0\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done



# #Shift_1
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.000_0.340
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_1\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #Shift_1
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.340_0.680
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_2\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done




# #Shift_2
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_1.410_2.140
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_3\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done




# #Shift_4
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_2.140_2.880
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _Shift_4\
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done



##Dual_Phase_Modulation Shift





# ##Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.68_1.41__f1_0.68_1.41
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --distribution_number _Shift_0 \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





# # #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.68_1.41__f1_0.68_1.41
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --distribution_number _Shift_0 \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.68_1.41__f1_0.68_1.41
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _Shift_0 \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done






# ##SHIFt_1


# ##Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.00_0.34__f1_0.00_0.34
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --distribution_number _Shift_1\
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done


# ##DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.00_0.34__f1_0.00_0.34
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --distribution_number _Shift_1 \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.00_0.34__f1_0.00_0.34
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _Shift_1 \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done


# ##SHIFT_2_



# ##Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.34_0.68__f1_0.34_0.68
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --distribution_number _Shift_2\
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done


# ##DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.34_0.68__f1_0.34_0.68
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --distribution_number _Shift_2 \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.34_0.68__f1_0.34_0.68
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _Shift_2 \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





# ##SHIFT_3

# ##Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_1.41_2.14__f1_1.41_2.14
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --distribution_number _Shift_3 \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





# # #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_1.41_2.14__f1_1.41_2.14
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --distribution_number _Shift_3 \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_1.41_2.14__f1_1.41_2.14
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _Shift_3 \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done


# #SHIFT_4


# ##Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_2.14_2.88__f1_2.14_2.88
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --distribution_number _Shift_4 \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





# # #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_2.14_2.88__f1_2.14_2.88
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --distribution_number _Shift_4 \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_2.14_2.88__f1_2.14_2.88
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _Shift_4 \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done
































#Testing Robustness to Noise (Training on Clean - Testing on Noisy)
#Drfit Harmonic Signal
#Drift Harmonic Testing (Noise-Clean)


# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _SNR_Level_0 \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





# # #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --distribution_number _SNR_Level_0 \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --distribution_number _SNR_Level_0 \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done


# #Drift Harmonic Testing (SNR_Level1)

# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_1
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --distribution_number _SNR_Level_1 \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





#  #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --distribution_number _SNR_Level_1\
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --distribution_number _SNR_Level_1 \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done



# # #Drift Harmonic Testing (SNR_Level-2)

# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_2
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _SNR_Level_2 \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





#  #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _SNR_Level_2 \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _SNR_Level_2 \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done


# #Drift Harmonic Testing (SNR_Level-3)
# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_3
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _SNR_Level_3 \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





#  #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _SNR_Level_3 \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --distribution_number _SNR_Level_3 \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

#Single_Phase_Modulation


#Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/clean
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --distribution_number _SNR_Level_0 \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





# # #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/clean
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --distribution_number _SNR_Level_0 \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/clean
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --distribution_number _SNR_Level_0 \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done


# #Drift Harmonic Testing (SNR_Level1)

# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_1
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _SNR_Level_1 \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





#  #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _SNR_Level_1 \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --distribution_number _SNR_Level_1 \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done



# #Drift Harmonic Testing (SNR_Level-2)

# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _SNR_Level_2 \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





#  #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _SNR_Level_2 \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _SNR_Level_2 \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done



# #Drift Harmonic Testing (SNR_Level-3)
# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _SNR_Level_3 \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





#  #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _SNR_Level_3 \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _SNR_Level_3 \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done



##Dual Phase Modulation




###Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --distribution_number _SNR_Level_0 \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





# # #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --distribution_number _SNR_Level_0 \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _SNR_Level_0 \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done


# # #Dual_Phase_Modulation(SNR_Level1)

# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _SNR_Level_1 \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





#  #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --distribution_number _SNR_Level_1 \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --distribution_number _SNR_Level_1 \
#       --data custom \
#       --task_name long_term_forecast \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done



# # #Dual_Phase_Modulation(SNR_Level-2)

# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#        --distribution_number _SNR_Level_2 \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





#  #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _SNR_Level_2 \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

# #FITS
# seq_len=50
# model_name=FITS
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=FITS_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#        --distribution_number _SNR_Level_2 \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --revin 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done



# #Dual_Phase_Modulation(SNR_Level-3)

# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _SNR_Level_3 \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 200 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done





#  #DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
# for pred_len in 100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#        --distribution_number _SNR_Level_3 \
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --enc_in 1 \
#       --patience 70 \
#       --train_epochs 300 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

#FITS
seq_len=50
model_name=FITS
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=FITS_Dual_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
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
      --data custom \
      --task_name long_term_forecast \
       --distribution_number _SNR_Level_3 \
      --features S \
      --target Value \
      --seq_len $seq_len \
      --pred_len $pred_len \
      --enc_in 1 \
      --patience 70 \
      --train_epochs 300 \
      --itr 1 \
      --batch_size 128 \
      --lradj 'TST' \
      --weight_decay 0.001 \
      --backcast 0\
      --revin 1\
      --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
done


