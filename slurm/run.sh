
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


# Linear model


# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Phase_Mod_Multi_Sine
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generated_Datasets/Phase_Mod_Multi_Sine/Modulation
# for pred_len in 500
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


# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Phase_Mod_Multi_Sine
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generated_Datasets/Phase_Mod_Multi_Sine/Modulation
# for pred_len in 500
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
#       --backcast 1\
#       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# done


#MLinear

# seq_len=50
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Phase_Mod_Multi_Sine
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generated_Datasets/Phase_Mod_Multi_Sine/Modulation
# for pred_len in 500
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
#     --train_epochs 500\
#     --patience 300 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_MLinear/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# seq_len=50
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Phase_Mod_Multi_Sine_backcast_added_loss
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generated_Datasets/Phase_Mod_Multi_Sine/Modulation
# for pred_len in 500
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
#     --train_epochs 500\
#     --patience 300 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 1\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_MLinear/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 



#checking the performnance with single sine phase modulation

# seq_len=100
# model_name=MLP_Backcast
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Phase_Mod_Single_Sine
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generated_Datasets/Phase_Mod_Single_Sine
# for pred_len in 500
# do
#     python -u main.py \
#     --is_training 1\
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
#     --train_epochs 500\
#     --patience 200 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 1\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_MLinear/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 


# #NoBackcast
# seq_len=100
# model_name=MLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Phase_Mod_Single_Sine
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generated_Datasets/Phase_Mod_Single_Sine
# for pred_len in 500
# do
#     python -u main.py \
#     --is_training 1\
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
#     --train_epochs 500\
#     --patience 200 \
#     --lradj 'TST' \
#     --weight_decay 0.0001\
#     --mlp_dropout 0.3 \
#     --backcast 0\
#     --itr 1 --batch_size 128  --learning_rate 0.0001 | tee logs/LongForecasting/Synthetic_MLinear/$model_name'_'$seq_len'_'$pred_len'_'$data_descriptor'_'revin.txt
# done 

#checking PatchTST performance on Single Sine Phase Modulation

#PatchTST 
seq_len=100
model_name=PatchTST
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=PatchTST_Phase_Mod_Single_Sine
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generated_Datasets/Phase_Mod_Single_Sine
for pred_len in  200 
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
      --features S \
      --target Value \
      --seq_len $seq_len \
      --pred_len $pred_len \
      --task_name long_term_forecast\
      --enc_in 1 \
      --e_layers 3\
      --n_heads 8 \
      --d_model 128 \
      --d_ff 256 \
      --dropout 0.2\
      --fc_dropout 0.2\
      --head_dropout 0.2\
      --patch_len 30\
      --stride 10\
      --train_epochs 300\
      --patience 80\
      --lradj 'TST'\
      --pct_start 0.2\
      --revin 1\
      --decomposition 0\
      --weight_decay 0.0001\
      --backcast 0 \
      --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_PatchTST_Phase/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
done


#checking Linear Model




#now checking with amplitude phase and modulation 



#PatchTST 
# seq_len=100
# model_name=PatchTST
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Phase_Mod_Multi_Sine
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generated_Datasets/Phase_Mod_Multi_Sine/Modulation
# for pred_len in  500 
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
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --task_name long_term_forecast\
#       --enc_in 1 \
#       --e_layers 3\
#       --n_heads 8 \
#       --d_model 128 \
#       --d_ff 256 \
#       --dropout 0.2\
#       --fc_dropout 0.2\
#       --head_dropout 0.2\
#       --patch_len 15\
#       --stride 10\
#       --train_epochs 300\
#       --patience 80\
#       --lradj 'TST'\
#       --pct_start 0.2\
#       --revin 1\
#       --decomposition 0\
#       --weight_decay 0.0001\
#       --backcast 0 \
#       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_PatchTST_Phase/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# done

# seq_len=50 
# model_name=PatchTST
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=MLinear_Phase_Mod_Multi_Sine
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generated_Datasets/Phase_Mod_Multi_Sine/Modulation
# for pred_len in  500 
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
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --task_name long_term_forecast\
#       --enc_in 1 \
#       --e_layers 3\
#       --n_heads 8 \
#       --d_model 128 \
#       --d_ff 256 \
#       --dropout 0.2\
#       --fc_dropout 0.2\
#       --head_dropout 0.2\
#       --patch_len 15\
#       --stride 10\
#       --train_epochs 300\
#       --patience 80\
#       --lradj 'TST'\
#       --pct_start 0.2\
#       --revin 1\
#       --decomposition 0\
#       --weight_decay 0.0001\
#       --backcast 1 \
#       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_PatchTST_Phase/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# done
