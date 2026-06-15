#!/bin/bash 
#SBATCH --ntasks=1 
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1 
#SBATCH --open-mode=append 
#SBATCH --time=0-16:30:00 
#SBATCH --mem=96G 
#SBATCH --partition=medvic
#SBATCH --output=log_%J.txt


# Create directories if they don't exist

if [ ! -d "./logs" ]; then
    mkdir ./logs
fi

if [ ! -d "./logs/LongForecasting" ]; then
    mkdir ./logs/LongForecasting
fi

if [ ! -d "./logs/LongForecasting/synthetic_Transformer_IE" ]; then
    mkdir ./logs/LongForecasting/synthetic_Transformer_IE
fi


# #Autformer

# seq_len=50 
# model_name=Autoformer
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Autoformer_Drift_Harmonic_Signal_label_len_train_only
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Drift_Harmonic_Test
# for pred_len in  100 
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
#       --e_layers 2\
#       --n_heads 8 \
#       --d_model 256 \
#       --d_ff 256 \
#       --dropout 0.2\
#       --fc_dropout 0.2\
#       --head_dropout 0.2\
#       --dec_in 1 \
#       --c_out 1\
#       --label_len 25\
#       --train_epochs 300\
#       --patience 30 \
#       --lradj 'TST'\
#       --pct_start 0.2\
#       --revin 1\
#       --decomposition 0\
#       --weight_decay 0.0001\
#       --backcast 0 \
#       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# done




# seq_len=50 
# model_name=Transformer
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Transformer_Drift_Harmonic_Signal_label_len_train_only
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Drift_Harmonic_Test
# for pred_len in  100 
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
#       --e_layers 2\
#       --n_heads 8 \
#       --d_model 256 \
#       --d_ff 256 \
#       --dropout 0.2\
#       --fc_dropout 0.2\
#       --head_dropout 0.2\
#       --dec_in 1 \
#       --c_out 1\
#       --factor 3\
#       --label_len 25\
#       --train_epochs 300\
#       --patience 30 \
#       --lradj 'TST'\
#       --pct_start 0.2\
#       --revin 1\
#       --decomposition 0\
#       --weight_decay 0.0001\
#       --backcast 0 \
#       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# done


#After this point phase modulation only 


#After This point is only for phase modulation
#PatchTST


# seq_len=50 
# model_name=PatchTST
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=PatchTST_ECG_S_Q_Single_Sine_Phase
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/PhaseMod_SingleFreq
# for pred_len in  100 
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
#       --d_model 256 \
#       --d_ff 256 \
#       --dropout 0.2\
#       --fc_dropout 0.2\
#       --head_dropout 0.2\
#       --patch_len 15\
#       --stride 10\
#       --train_epochs 300\
#       --patience 30 \
#       --lradj 'TST'\
#       --pct_start 0.2\
#       --revin 1\
#       --decomposition 0\
#       --weight_decay 0.0001\
#       --backcast 0 \
#       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# done



#Autoformer

# seq_len=50 
# model_name=Autoformer
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Autoformer_ECG_S_Q_Single_Sine_Phase
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/PhaseMod_SingleFreq
# for pred_len in  100 
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
#       --e_layers 2\
#       --n_heads 8 \
#       --d_model 256 \
#       --d_ff 256 \
#       --dropout 0.2\
#       --fc_dropout 0.2\
#       --head_dropout 0.2\
#       --dec_in 1 \
#       --c_out 1\
#       --label_len 25\
#       --train_epochs 300\
#       --patience 30 \
#       --lradj 'TST'\
#       --pct_start 0.2\
#       --revin 1\
#       --decomposition 0\
#       --weight_decay 0.0001\
#       --backcast 0 \
#       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# done


#Transformer

# seq_len=50 
# model_name=Transformer
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Transformer_ECG_S_Q_Single_Sine_Phase
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/PhaseMod_SingleFreq
# for pred_len in  100 
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
#       --e_layers 2\
#       --n_heads 8 \
#       --d_model 256 \
#       --d_ff 256 \
#       --dropout 0.2\
#       --fc_dropout 0.2\
#       --head_dropout 0.2\
#       --dec_in 1 \
#       --c_out 1\
#       --factor 3\
#       --label_len 25\
#       --train_epochs 300\
#       --patience 30 \
#       --lradj 'TST'\
#       --pct_start 0.2\
#       --revin 1\
#       --decomposition 0\
#       --weight_decay 0.0001\
#       --backcast 0 \
#       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# done



#Dual Sine Wave Phase Modulation
#PatchTST


# seq_len=50 
# model_name=PatchTST
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=PatchTST_ECG_S_Q_Dual_Sine_Phase
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/PhaseMod_TwoFreq
# for pred_len in  100 200 
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
#       --d_model 256 \
#       --d_ff 256 \
#       --dropout 0.2\
#       --fc_dropout 0.2\
#       --head_dropout 0.2\
#       --patch_len 15\
#       --stride 10\
#       --train_epochs 300\
#       --patience 30 \
#       --lradj 'TST'\
#       --pct_start 0.2\
#       --revin 1\
#       --decomposition 0\
#       --weight_decay 0.0001\
#       --backcast 0 \
#       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# done



# #Autoformer

# seq_len=50 
# model_name=Autoformer
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Autoformer_ECG_S_Q_Dual_Sine_Phase
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/PhaseMod_TwoFreq
# for pred_len in  100 200
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
#       --e_layers 2\
#       --n_heads 8 \
#       --d_model 256 \
#       --d_ff 256 \
#       --dropout 0.2\
#       --fc_dropout 0.2\
#       --head_dropout 0.2\
#       --dec_in 1 \
#       --c_out 1\
#       --label_len 25\
#       --train_epochs 300\
#       --patience 30 \
#       --lradj 'TST'\
#       --pct_start 0.2\
#       --revin 1\
#       --decomposition 0\
#       --weight_decay 0.0001\
#       --backcast 0 \
#       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# done


# # #Transformer

# seq_len=50 
# model_name=Transformer
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Transformer_ECG_S_Q_Dual_Sine_Phase
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/PhaseMod_TwoFreq
# for pred_len in  100 200
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
#       --e_layers 2\
#       --n_heads 8 \
#       --d_model 256 \
#       --d_ff 256 \
#       --dropout 0.2\
#       --fc_dropout 0.2\
#       --head_dropout 0.2\
#       --dec_in 1 \
#       --c_out 1\
#       --factor 3\
#       --label_len 25\
#       --train_epochs 300\
#       --patience 30 \
#       --lradj 'TST'\
#       --pct_start 0.2\
#       --revin 1\
#       --decomposition 0\
#       --weight_decay 0.0001\
#       --backcast 0 \
#       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# done






#Drift Harmonic Clean

#PatchTST


# seq_len=50 
# model_name=PatchTST
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=PatchTST_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
# for pred_len in  100 
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
#       --d_model 256 \
#       --d_ff 256 \
#       --dropout 0.2\
#       --fc_dropout 0.2\
#       --head_dropout 0.2\
#       --patch_len 15\
#       --stride 10\
#      --train_epochs 300\
#       --patience 30 \
#       --lradj 'TST'\
#       --pct_start 0.2\
#       --revin 1\
#       --decomposition 0\
#       --weight_decay 0.0001\
#       --backcast 0 \
#       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# done



# #Autoformer

seq_len=50 
model_name=Autoformer
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Autoformer_Drift_Harmonic_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
for pred_len in  100 
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
      --e_layers 2\
      --n_heads 8 \
      --d_model 256 \
      --d_ff 256 \
      --dropout 0.2\
      --fc_dropout 0.2\
      --head_dropout 0.2\
      --dec_in 1 \
      --c_out 1\
      --label_len 25\
     --train_epochs 300\
      --patience 30 \
      --lradj 'TST'\
      --pct_start 0.2\
      --revin 1\
      --decomposition 0\
      --weight_decay 0.0001\
      --backcast 0 \
      --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
done


# #Transformer

seq_len=50 
model_name=Transformer
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Transformer_Drift_Harmonic_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
for pred_len in  100 
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
      --e_layers 2\
      --n_heads 8 \
      --d_model 256 \
      --d_ff 256 \
      --dropout 0.2\
      --fc_dropout 0.2\
      --head_dropout 0.2\
      --dec_in 1 \
      --c_out 1\
      --factor 3\
      --label_len 25\
     --train_epochs 300\
      --patience 30 \
      --lradj 'TST'\
      --pct_start 0.2\
      --revin 1\
      --decomposition 0\
      --weight_decay 0.0001\
      --backcast 0 \
      --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
done



# #Drift Harmonic SNR level-1


# #PatchTST


# seq_len=50 
# model_name=PatchTST
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=PatchTST_Drift_Harmonic_SNR_Level_1
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_1
# for pred_len in  100 
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
#       --d_model 256 \
#       --d_ff 256 \
#       --dropout 0.2\
#       --fc_dropout 0.2\
#       --head_dropout 0.2\
#       --patch_len 15\
#       --stride 10\
#      --train_epochs 300\
#       --patience 30 \
#       --lradj 'TST'\
#       --pct_start 0.2\
#       --revin 1\
#       --decomposition 0\
#       --weight_decay 0.0001\
#       --backcast 0 \
#       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# done



# #Autoformer

seq_len=50 
model_name=Autoformer
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Autoformer_Drift_Harmonic_SNR_Level_1
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_1
for pred_len in  100 
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
      --e_layers 2\
      --n_heads 8 \
      --d_model 256 \
      --d_ff 256 \
      --dropout 0.2\
      --fc_dropout 0.2\
      --head_dropout 0.2\
      --dec_in 1 \
      --c_out 1\
      --label_len 25\
     --train_epochs 300\
      --patience 30 \
      --lradj 'TST'\
      --pct_start 0.2\
      --revin 1\
      --decomposition 0\
      --weight_decay 0.0001\
      --backcast 0 \
      --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
done


# #Transformer

seq_len=50 
model_name=Transformer
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Transformer_Drift_Harmonic_SNR_Level_1
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_1
for pred_len in  100 
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
      --e_layers 2\
      --n_heads 8 \
      --d_model 256 \
      --d_ff 256 \
      --dropout 0.2\
      --fc_dropout 0.2\
      --head_dropout 0.2\
      --dec_in 1 \
      --c_out 1\
      --factor 3\
      --label_len 25\
     --train_epochs 300\
      --patience 30 \
      --lradj 'TST'\
      --pct_start 0.2\
      --revin 1\
      --decomposition 0\
      --weight_decay 0.0001\
      --backcast 0 \
      --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
done


# #Drift Harmonic (SNR_Level_2)



# #PatchTST


# seq_len=50 
# model_name=PatchTST
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=PatchTST_Drift_Harmonic_SNR_Level_2
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_2
# for pred_len in  100 
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
#       --d_model 256 \
#       --d_ff 256 \
#       --dropout 0.2\
#       --fc_dropout 0.2\
#       --head_dropout 0.2\
#       --patch_len 15\
#       --stride 10\
#      --train_epochs 300\
#       --patience 30 \
#       --lradj 'TST'\
#       --pct_start 0.2\
#       --revin 1\
#       --decomposition 0\
#       --weight_decay 0.0001\
#       --backcast 0 \
#       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# done



# #Autoformer

seq_len=50 
model_name=Autoformer
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Autoformer_Drift_Harmonic_SNR_Level_2
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_2
for pred_len in  100 
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
      --e_layers 2\
      --n_heads 8 \
      --d_model 256 \
      --d_ff 256 \
      --dropout 0.2\
      --fc_dropout 0.2\
      --head_dropout 0.2\
      --dec_in 1 \
      --c_out 1\
      --label_len 25\
     --train_epochs 300\
      --patience 30 \
      --lradj 'TST'\
      --pct_start 0.2\
      --revin 1\
      --decomposition 0\
      --weight_decay 0.0001\
      --backcast 0 \
      --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
done


# #Transformer

seq_len=50 
model_name=Transformer
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Transformer_Drift_Harmonic_SNR_Level_2
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_2
for pred_len in  100 
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
      --e_layers 2\
      --n_heads 8 \
      --d_model 256 \
      --d_ff 256 \
      --dropout 0.2\
      --fc_dropout 0.2\
      --head_dropout 0.2\
      --dec_in 1 \
      --c_out 1\
      --factor 3\
      --label_len 25\
      --train_epochs 2\
      --patience 30 \
      --lradj 'TST'\
      --pct_start 0.2\
      --revin 1\
      --decomposition 0\
      --weight_decay 0.0001\
      --backcast 0 \
      --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
done



# #Drift Harmonic (SNR_Level_3)



# #PatchTST


# seq_len=50 
# model_name=PatchTST
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=PatchTST_Drift_Harmonic_SNR_Level_3
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_3
# for pred_len in  100 
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
#       --d_model 256 \
#       --d_ff 256 \
#       --dropout 0.2\
#       --fc_dropout 0.2\
#       --head_dropout 0.2\
#       --patch_len 15\
#       --stride 10\
#       --train_epochs 300\
#       --patience 30 \
#       --lradj 'TST'\
#       --pct_start 0.2\
#       --revin 1\
#       --decomposition 0\
#       --weight_decay 0.0001\
#       --backcast 0 \
#       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# done



# #Autoformer

seq_len=50 
model_name=Autoformer
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Autoformer_Drift_Harmonic_SNR_Level_3
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_3
for pred_len in  100 
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
      --e_layers 2\
      --n_heads 8 \
      --d_model 256 \
      --d_ff 256 \
      --dropout 0.2\
      --fc_dropout 0.2\
      --head_dropout 0.2\
      --dec_in 1 \
      --c_out 1\
      --label_len 25\
      --train_epochs 300\
      --patience 30 \
      --lradj 'TST'\
      --pct_start 0.2\
      --revin 1\
      --decomposition 0\
      --weight_decay 0.0001\
      --backcast 0 \
      --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
done


#Transformer

seq_len=50 
model_name=Transformer
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Transformer_Drift_Harmonic_SNR_Level_3
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_3
for pred_len in  100 
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
      --e_layers 2\
      --n_heads 8 \
      --d_model 256 \
      --d_ff 256 \
      --dropout 0.2\
      --fc_dropout 0.2\
      --head_dropout 0.2\
      --dec_in 1 \
      --c_out 1\
      --factor 3\
      --label_len 25\
      --train_epochs 300\
      --patience 30 \
      --lradj 'TST'\
      --pct_start 0.2\
      --revin 1\
      --decomposition 0\
      --weight_decay 0.0001\
      --backcast 0 \
      --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
done







#Single_Phase_Modulation



#Single Phase Modulation Clean 
#PatchTST


#Single_Phase_Modulation  Clean

#PatchTST


# seq_len=50 
# model_name=PatchTST
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=PatchTST_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/clean
# for pred_len in  100 
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
#       --d_model 256 \
#       --d_ff 256 \
#       --dropout 0.2\
#       --fc_dropout 0.2\
#       --head_dropout 0.2\
#       --patch_len 15\
#       --stride 10\
#       --train_epochs 300\
#       --patience 30\
#       --lradj 'TST'\
#       --pct_start 0.2\
#       --revin 1\
#       --decomposition 0\
#       --weight_decay 0.0001\
#       --backcast 0 \
#       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# done



# #Autoformer

# seq_len=50 
# model_name=Autoformer
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Autoformer_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/clean
# for pred_len in  100 
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
#       --e_layers 2\
#       --n_heads 8 \
#       --d_model 256 \
#       --d_ff 256 \
#       --dropout 0.2\
#       --fc_dropout 0.2\
#       --head_dropout 0.2\
#       --dec_in 1 \
#       --c_out 1\
#       --label_len 25\
#       --train_epochs 300\
#       --patience 30\
#       --lradj 'TST'\
#       --pct_start 0.2\
#       --revin 1\
#       --decomposition 0\
#       --weight_decay 0.0001\
#       --backcast 0 \
#       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# done


# #Transformer

# seq_len=50 
# model_name=Transformer
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Transformer_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/clean
# for pred_len in  100 
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
#       --e_layers 2\
#       --n_heads 8 \
#       --d_model 256 \
#       --d_ff 256 \
#       --dropout 0.2\
#       --fc_dropout 0.2\
#       --head_dropout 0.2\
#       --dec_in 1 \
#       --c_out 1\
#       --factor 3\
#       --label_len 25\
#       --train_epochs 300\
#       --patience 30\
#       --lradj 'TST'\
#       --pct_start 0.2\
#       --revin 1\
#       --decomposition 0\
#       --weight_decay 0.0001\
#       --backcast 0 \
#       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# done



# #Single_Phase_Modulation  SNR level-1


# #PatchTST


# seq_len=50 
# model_name=PatchTST
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=PatchTST_Single_Phase_Modulation_SNR_Level_1
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_1
# for pred_len in  100 
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
#       --d_model 256 \
#       --d_ff 256 \
#       --dropout 0.2\
#       --fc_dropout 0.2\
#       --head_dropout 0.2\
#       --patch_len 15\
#       --stride 10\
#       --train_epochs 300\
#       --patience 30\
#       --lradj 'TST'\
#       --pct_start 0.2\
#       --revin 1\
#       --decomposition 0\
#       --weight_decay 0.0001\
#       --backcast 0 \
#       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# done



#Autoformer

seq_len=50 
model_name=Autoformer
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Autoformer_Single_Phase_Modulation_SNR_Level_1
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_1
for pred_len in  100 
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
      --e_layers 2\
      --n_heads 8 \
      --d_model 256 \
      --d_ff 256 \
      --dropout 0.2\
      --fc_dropout 0.2\
      --head_dropout 0.2\
      --dec_in 1 \
      --c_out 1\
      --label_len 25\
      --train_epochs 300\
      --patience 30\
      --lradj 'TST'\
      --pct_start 0.2\
      --revin 1\
      --decomposition 0\
      --weight_decay 0.0001\
      --backcast 0 \
      --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
done


# #Transformer

seq_len=50 
model_name=Transformer
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Transformer_Single_Phase_Modulation_SNR_Level_1
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_1
for pred_len in  100 
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
      --e_layers 2\
      --n_heads 8 \
      --d_model 256 \
      --d_ff 256 \
      --dropout 0.2\
      --fc_dropout 0.2\
      --head_dropout 0.2\
      --dec_in 1 \
      --c_out 1\
      --factor 3\
      --label_len 25\
      --train_epochs 300\
      --patience 30\
      --lradj 'TST'\
      --pct_start 0.2\
      --revin 1\
      --decomposition 0\
      --weight_decay 0.0001\
      --backcast 0 \
      --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
done


# #Single_Phase_Modulation  (SNR_Level_2)



# #PatchTST


# seq_len=50 
# model_name=PatchTST
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=PatchTST_Single_Phase_Modulation_SNR_Level_2
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
# for pred_len in  100 
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
#       --d_model 256 \
#       --d_ff 256 \
#       --dropout 0.2\
#       --fc_dropout 0.2\
#       --head_dropout 0.2\
#       --patch_len 15\
#       --stride 10\
#       --train_epochs 300\
#       --patience 30\
#       --lradj 'TST'\
#       --pct_start 0.2\
#       --revin 1\
#       --decomposition 0\
#       --weight_decay 0.0001\
#       --backcast 0 \
#       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# done



# #Autoformer

seq_len=50 
model_name=Autoformer
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Autoformer_Single_Phase_Modulation_SNR_Level_2
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
for pred_len in  100 
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
      --e_layers 2\
      --n_heads 8 \
      --d_model 256 \
      --d_ff 256 \
      --dropout 0.2\
      --fc_dropout 0.2\
      --head_dropout 0.2\
      --dec_in 1 \
      --c_out 1\
      --label_len 25\
      --train_epochs 300\
      --patience 30\
      --lradj 'TST'\
      --pct_start 0.2\
      --revin 1\
      --decomposition 0\
      --weight_decay 0.0001\
      --backcast 0 \
      --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
done


# #Transformer

seq_len=50 
model_name=Transformer
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Transformer_Single_Phase_Modulation_SNR_Level_2
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
for pred_len in  100 
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
      --e_layers 2\
      --n_heads 8 \
      --d_model 256 \
      --d_ff 256 \
      --dropout 0.2\
      --fc_dropout 0.2\
      --head_dropout 0.2\
      --dec_in 1 \
      --c_out 1\
      --factor 3\
      --label_len 25\
      --train_epochs 300\
      --patience 30\
      --lradj 'TST'\
      --pct_start 0.2\
      --revin 1\
      --decomposition 0\
      --weight_decay 0.0001\
      --backcast 0 \
      --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
done



# #Single_Phase_Modulation  (SNR_Level_3)



# #PatchTST


# seq_len=50 
# model_name=PatchTST
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=PatchTST_Single_Phase_Modulationc_SNR_Level_3
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
# for pred_len in  100 
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
#       --d_model 256 \
#       --d_ff 256 \
#       --dropout 0.2\
#       --fc_dropout 0.2\
#       --head_dropout 0.2\
#       --patch_len 15\
#       --stride 10\
#       --train_epochs 300\
#       --patience 30\
#       --lradj 'TST'\
#       --pct_start 0.2\
#       --revin 1\
#       --decomposition 0\
#       --weight_decay 0.0001\
#       --backcast 0 \
#       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# done



# #Autoformer

seq_len=50 
model_name=Autoformer
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Autoformer_Single_Phase_Modulation_SNR_Level_3
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
for pred_len in  100 
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
      --e_layers 2\
      --n_heads 8 \
      --d_model 256 \
      --d_ff 256 \
      --dropout 0.2\
      --fc_dropout 0.2\
      --head_dropout 0.2\
      --dec_in 1 \
      --c_out 1\
      --label_len 25\
      --train_epochs 2\
      --patience 30\
      --lradj 'TST'\
      --pct_start 0.2\
      --revin 1\
      --decomposition 0\
      --weight_decay 0.0001\
      --backcast 0 \
      --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
done


#Transformer

seq_len=50 
model_name=Transformer
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Transformer_Single_Phase_Modulation_SNR_Level_3
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
for pred_len in  100 
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
      --e_layers 2\
      --n_heads 8 \
      --d_model 256 \
      --d_ff 256 \
      --dropout 0.2\
      --fc_dropout 0.2\
      --head_dropout 0.2\
      --dec_in 1 \
      --c_out 1\
      --factor 3\
      --label_len 25\
      --train_epochs 2\
      --patience 30\
      --lradj 'TST'\
      --pct_start 0.2\
      --revin 1\
      --decomposition 0\
      --weight_decay 0.0001\
      --backcast 0 \
      --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
done



#Dual Phase Modulation


##Dual_Phase_Modulation
##PatchTST


# seq_len=50 
# model_name=PatchTST
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=PatchTST_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
# for pred_len in  100 
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
#       --d_model 256 \
#       --d_ff 256 \
#       --dropout 0.2\
#       --fc_dropout 0.2\
#       --head_dropout 0.2\
#       --patch_len 15\
#       --stride 10\
#       --train_epochs 300\
#       --patience 30\
#       --lradj 'TST'\
#       --pct_start 0.2\
#       --revin 1\
#       --decomposition 0\
#       --weight_decay 0.0001\
#       --backcast 0 \
#       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# done



# #Autoformer

seq_len=50 
model_name=Autoformer
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Autoformer_Dual_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
for pred_len in  100 
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
      --e_layers 2\
      --n_heads 8 \
      --d_model 256 \
      --d_ff 256 \
      --dropout 0.2\
      --fc_dropout 0.2\
      --head_dropout 0.2\
      --dec_in 1 \
      --c_out 1\
      --label_len 25\
      --train_epochs 300\
      --patience 30\
      --lradj 'TST'\
      --pct_start 0.2\
      --revin 1\
      --decomposition 0\
      --weight_decay 0.0001\
      --backcast 0 \
      --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
done


# #Transformer

seq_len=50 
model_name=Transformer
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Transformer_Dual_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
for pred_len in  100 
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
      --e_layers 2\
      --n_heads 8 \
      --d_model 256 \
      --d_ff 256 \
      --dropout 0.2\
      --fc_dropout 0.2\
      --head_dropout 0.2\
      --dec_in 1 \
      --c_out 1\
      --factor 3\
      --label_len 25\
      --train_epochs 300\
      --patience 30\
      --lradj 'TST'\
      --pct_start 0.2\
      --revin 1\
      --decomposition 0\
      --weight_decay 0.0001\
      --backcast 0 \
      --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
done



# #Dual_Phase_Modulation  SNR level-1


# #PatchTST


# seq_len=50 
# model_name=PatchTST
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=PatchTST_Dual_Phase_Modulation_SNR_Level_1
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
# for pred_len in  100 
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
#       --d_model 256 \
#       --d_ff 256 \
#       --dropout 0.2\
#       --fc_dropout 0.2\
#       --head_dropout 0.2\
#       --patch_len 15\
#       --stride 10\
#       --train_epochs 300\
#       --patience 30\
#       --lradj 'TST'\
#       --pct_start 0.2\
#       --revin 1\
#       --decomposition 0\
#       --weight_decay 0.0001\
#       --backcast 0 \
#       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# done



# #Autoformer

seq_len=50 
model_name=Autoformer
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Autoformer_Dual_Phase_Modulation_SNR_Level_1
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
for pred_len in  100 
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
      --e_layers 2\
      --n_heads 8 \
      --d_model 256 \
      --d_ff 256 \
      --dropout 0.2\
      --fc_dropout 0.2\
      --head_dropout 0.2\
      --dec_in 1 \
      --c_out 1\
      --label_len 25\
      --train_epochs 300\
      --patience 30\
      --lradj 'TST'\
      --pct_start 0.2\
      --revin 1\
      --decomposition 0\
      --weight_decay 0.0001\
      --backcast 0 \
      --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
done


#Transformer

seq_len=50 
model_name=Transformer
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Transformer_Dual_Phase_Modulation_SNR_Level_1
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
for pred_len in  100 
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
      --e_layers 2\
      --n_heads 8 \
      --d_model 256 \
      --d_ff 256 \
      --dropout 0.2\
      --fc_dropout 0.2\
      --head_dropout 0.2\
      --dec_in 1 \
      --c_out 1\
      --factor 3\
      --label_len 25\
      --train_epochs 300\
      --patience 30\
      --lradj 'TST'\
      --pct_start 0.2\
      --revin 1\
      --decomposition 0\
      --weight_decay 0.0001\
      --backcast 0 \
      --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
done


# #Dual_Phase_Modulation  (SNR_Level_2)



# #PatchTST


# seq_len=50 
# model_name=PatchTST
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=PatchTST_Dual_Phase_Modulation_SNR_Level_2
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
# for pred_len in  100 
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
#       --d_model 256 \
#       --d_ff 256 \
#       --dropout 0.2\
#       --fc_dropout 0.2\
#       --head_dropout 0.2\
#       --patch_len 15\
#       --stride 10\
#       --train_epochs 300\
#       --patience 30\
#       --lradj 'TST'\
#       --pct_start 0.2\
#       --revin 1\
#       --decomposition 0\
#       --weight_decay 0.0001\
#       --backcast 0 \
#       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# done



#Autoformer

seq_len=50 
model_name=Autoformer
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Autoformer_Dual_Phase_Modulation_SNR_Level_2
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
for pred_len in  100 
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
      --e_layers 2\
      --n_heads 8 \
      --d_model 256 \
      --d_ff 256 \
      --dropout 0.2\
      --fc_dropout 0.2\
      --head_dropout 0.2\
      --dec_in 1 \
      --c_out 1\
      --label_len 25\
      --train_epochs 300\
      --patience 30\
      --lradj 'TST'\
      --pct_start 0.2\
      --revin 1\
      --decomposition 0\
      --weight_decay 0.0001\
      --backcast 0 \
      --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
done


#Transformer

seq_len=50 
model_name=Transformer
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Transformer_Dual_Phase_Modulation_SNR_Level_2
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
for pred_len in  100 
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
      --e_layers 2\
      --n_heads 8 \
      --d_model 256 \
      --d_ff 256 \
      --dropout 0.2\
      --fc_dropout 0.2\
      --head_dropout 0.2\
      --dec_in 1 \
      --c_out 1\
      --factor 3\
      --label_len 25\
      --train_epochs 300\
      --patience 30\
      --lradj 'TST'\
      --pct_start 0.2\
      --revin 1\
      --decomposition 0\
      --weight_decay 0.0001\
      --backcast 0 \
      --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
done



# #Dual_Phase_Modulation  (SNR_Level_3)



# #PatchTST


# seq_len=50 
# model_name=PatchTST
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=PatchTST_Dual_Phase_Modulationc_SNR_Level_3
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
# for pred_len in  100 
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
#       --d_model 256 \
#       --d_ff 256 \
#       --dropout 0.2\
#       --fc_dropout 0.2\
#       --head_dropout 0.2\
#       --patch_len 15\
#       --stride 10\
#       --train_epochs 300\
#       --patience 30\
#       --lradj 'TST'\
#       --pct_start 0.2\
#       --revin 1\
#       --decomposition 0\
#       --weight_decay 0.0001\
#       --backcast 0 \
#       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# done



#Autoformer

seq_len=50 
model_name=Autoformer
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Autoformer_Dual_Phase_Modulation_SNR_Level_3
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
for pred_len in  100 
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
      --e_layers 2\
      --n_heads 8 \
      --d_model 256 \
      --d_ff 256 \
      --dropout 0.2\
      --fc_dropout 0.2\
      --head_dropout 0.2\
      --dec_in 1 \
      --c_out 1\
      --label_len 25\
      --train_epochs 300\
      --patience 30\
      --lradj 'TST'\
      --pct_start 0.2\
      --revin 1\
      --decomposition 0\
      --weight_decay 0.0001\
      --backcast 0 \
      --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
done


#Transformer

seq_len=50 
model_name=Transformer
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Transformer_Dual_Phase_Modulation_SNR_Level_3
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
for pred_len in  100 
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
      --e_layers 2\
      --n_heads 8 \
      --d_model 256 \
      --d_ff 256 \
      --dropout 0.2\
      --fc_dropout 0.2\
      --head_dropout 0.2\
      --dec_in 1 \
      --c_out 1\
      --factor 3\
      --label_len 25\
      --train_epochs 300\
      --patience 30\
      --lradj 'TST'\
      --pct_start 0.2\
      --revin 1\
      --decomposition 0\
      --weight_decay 0.0001\
      --backcast 0 \
      --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
done




















