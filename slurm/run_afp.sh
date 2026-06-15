


#!/bin/bash

export CUDA_VISIBLE_DEVICES=0

# Create directories if they don't exist

if [ ! -d "./logs" ]; then
    mkdir ./logs
fi

if [ ! -d "./logs/LongForecasting" ]; then
    mkdir ./logs/LongForecasting
fi

if [ ! -d "./logs/LongForecasting/synthetic_Linear_IE" ]; then
    mkdir ./logs/LongForecasting/synthetic_Linear_IE
fi
#Linear model
#checking if predicting each head works or not


# seq_len=100
# model_name=AFP_Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Phase_Mod_Single_Sine_each_head
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generated_Datasets/Phase_Mod_Single_Sine
# for pred_len in 200
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
#       --train_epochs 400 \
#       --itr 1 \
#       --batch_size 128 \
#       --lradj 'TST' \
#       --weight_decay 0.001 \
#       --backcast 0\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done

seq_len=100
model_name=AFP_MLinear
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=MLP_Phase_Mod_Single_Sine_Each_Head
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generated_Datasets/Phase_Mod_Single_Sine
for pred_len in 200
do
    python -u main.py \
      --is_training 1\
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
      --train_epochs 400 \
      --itr 1 \
      --batch_size 128 \
      --lradj 'TST' \
      --weight_decay 0.001 \
      --backcast 0\
      --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
done