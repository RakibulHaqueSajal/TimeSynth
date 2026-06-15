
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




# # #Testing Robustness to Noise (Training on Clean - Testing on Noisy)
# # #Drfit Harmonic Signal
# # #Drift Harmonic Testing (Noise-Clean)


# # #Linear
# # seq_len=50
# # model_name=Linear
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Linear_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
# # for pred_len in 100
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #       --features S \
# #       --target Value \
# #       --distribution_number _SNR_Level_0 \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 200 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done





# # # #DLinear

# # seq_len=50
# # model_name=DLinear
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=DLinear_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
# # for pred_len in 100 
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #       --features S \
# #       --distribution_number _SNR_Level_0 \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 300 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done

# # #FITS
# # seq_len=50
# # model_name=FITS
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=FITS_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
# # for pred_len in 100 
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --distribution_number _SNR_Level_0 \
# #       --task_name long_term_forecast \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 300 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --revin 1\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done


# # #Drift Harmonic Testing (SNR_Level1)

# # #Linear
# # seq_len=50
# # model_name=Linear
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Linear_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_1
# # for pred_len in 100
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #       --features S \
# #       --distribution_number _SNR_Level_1 \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 200 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done





# #  #DLinear

# # seq_len=50
# # model_name=DLinear
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=DLinear_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_1
# # for pred_len in 100 
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #       --features S \
# #       --distribution_number _SNR_Level_1\
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 300 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done

# # #FITS
# # seq_len=50
# # model_name=FITS
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=FITS_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_1
# # for pred_len in 100 
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #       --features S \
# #       --target Value \
# #       --distribution_number _SNR_Level_1 \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 300 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --revin 1\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done



# # # #Drift Harmonic Testing (SNR_Level-2)

# # #Linear
# # seq_len=50
# # model_name=Linear
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Linear_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_2
# # for pred_len in 100
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #       --distribution_number _SNR_Level_2 \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 200 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done





# #  #DLinear

# # seq_len=50
# # model_name=DLinear
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=DLinear_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_2
# # for pred_len in 100 
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #       --distribution_number _SNR_Level_2 \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 300 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done

# # #FITS
# # seq_len=50
# # model_name=FITS
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=FITS_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_2
# # for pred_len in 100 
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #       --distribution_number _SNR_Level_2 \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 300 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --revin 1\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done


# # #Drift Harmonic Testing (SNR_Level-3)
# # #Linear
# # seq_len=50
# # model_name=Linear
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Linear_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_3
# # for pred_len in 100
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #       --distribution_number _SNR_Level_3 \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 200 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done





# #  #DLinear

# # seq_len=50
# # model_name=DLinear
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=DLinear_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_3
# # for pred_len in 100 
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #       --distribution_number _SNR_Level_3 \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 300 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done

# # #FITS
# # seq_len=50
# # model_name=FITS
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=FITS_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_3
# # for pred_len in 100 
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --distribution_number _SNR_Level_3 \
# #       --task_name long_term_forecast \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 300 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --revin 1\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done

# # #Single_Phase_Modulation


# # #Linear
# # seq_len=50
# # model_name=Linear
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Linear_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/clean
# # for pred_len in 100
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --distribution_number _SNR_Level_0 \
# #       --task_name long_term_forecast \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 200 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done





# # # #DLinear

# # seq_len=50
# # model_name=DLinear
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=DLinear_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/clean
# # for pred_len in 100 
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --distribution_number _SNR_Level_0 \
# #       --task_name long_term_forecast \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 300 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done

# # #FITS
# # seq_len=50
# # model_name=FITS
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=FITS_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/clean
# # for pred_len in 100 
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #       --features S \
# #       --distribution_number _SNR_Level_0 \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 300 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --revin 1\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done


# # #Drift Harmonic Testing (SNR_Level1)

# # #Linear
# # seq_len=50
# # model_name=Linear
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Linear_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_1
# # for pred_len in 100
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #       --distribution_number _SNR_Level_1 \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 200 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done





# #  #DLinear

# # seq_len=50
# # model_name=DLinear
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=DLinear_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_1
# # for pred_len in 100 
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #       --distribution_number _SNR_Level_1 \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 300 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done

# # #FITS
# # seq_len=50
# # model_name=FITS
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=FITS_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_1
# # for pred_len in 100 
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --distribution_number _SNR_Level_1 \
# #       --task_name long_term_forecast \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 300 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --revin 1\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done



# # #Drift Harmonic Testing (SNR_Level-2)

# # #Linear
# # seq_len=50
# # model_name=Linear
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Linear_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
# # for pred_len in 100
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #       --distribution_number _SNR_Level_2 \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 200 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done





# #  #DLinear

# # seq_len=50
# # model_name=DLinear
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=DLinear_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
# # for pred_len in 100 
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #       --distribution_number _SNR_Level_2 \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 300 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done

# # #FITS
# # seq_len=50
# # model_name=FITS
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=FITS_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
# # for pred_len in 100 
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #       --distribution_number _SNR_Level_2 \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 300 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --revin 1\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done



# # #Drift Harmonic Testing (SNR_Level-3)
# # #Linear
# # seq_len=50
# # model_name=Linear
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Linear_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
# # for pred_len in 100
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #       --distribution_number _SNR_Level_3 \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 200 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done





# #  #DLinear

# # seq_len=50
# # model_name=DLinear
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=DLinear_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
# # for pred_len in 100 
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #       --distribution_number _SNR_Level_3 \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 300 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done

# # #FITS
# # seq_len=50
# # model_name=FITS
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=FITS_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
# # for pred_len in 100 
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #       --distribution_number _SNR_Level_3 \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 300 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --revin 1\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done



# # #Dual Phase Modulation




# # ##Linear
# # seq_len=50
# # model_name=Linear
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Linear_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
# # for pred_len in 100
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --distribution_number _SNR_Level_0 \
# #       --task_name long_term_forecast \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 200 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done





# # # #DLinear

# # seq_len=50
# # model_name=DLinear
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=DLinear_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
# # for pred_len in 100 
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --distribution_number _SNR_Level_0 \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 300 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done

# # #FITS
# # seq_len=50
# # model_name=FITS
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=FITS_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
# # for pred_len in 100 
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #       --distribution_number _SNR_Level_0 \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 300 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --revin 1\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done


# # # #Dual_Phase_Modulation(SNR_Level1)

# # #Linear
# # seq_len=50
# # model_name=Linear
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Linear_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
# # for pred_len in 100
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #       --distribution_number _SNR_Level_1 \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 200 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done





# #  #DLinear

# # seq_len=50
# # model_name=DLinear
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=DLinear_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
# # for pred_len in 100 
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --distribution_number _SNR_Level_1 \
# #       --data custom \
# #       --task_name long_term_forecast \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 300 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done

# # #FITS
# # seq_len=50
# # model_name=FITS
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=FITS_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
# # for pred_len in 100 
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --distribution_number _SNR_Level_1 \
# #       --data custom \
# #       --task_name long_term_forecast \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 300 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --revin 1\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done



# # # #Dual_Phase_Modulation(SNR_Level-2)

# # #Linear
# # seq_len=50
# # model_name=Linear
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Linear_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
# # for pred_len in 100
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #        --distribution_number _SNR_Level_2 \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 200 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done





# #  #DLinear

# # seq_len=50
# # model_name=DLinear
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=DLinear_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
# # for pred_len in 100 
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #       --distribution_number _SNR_Level_2 \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 300 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done

# # #FITS
# # seq_len=50
# # model_name=FITS
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=FITS_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
# # for pred_len in 100 
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #        --distribution_number _SNR_Level_2 \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 300 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --revin 1\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done



# # #Dual_Phase_Modulation(SNR_Level-3)

# # #Linear
# # seq_len=50
# # model_name=Linear
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Linear_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
# # for pred_len in 100
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #       --distribution_number _SNR_Level_3 \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 200 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done





# #  #DLinear

# # seq_len=50
# # model_name=DLinear
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=DLinear_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
# # for pred_len in 100 
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #        --distribution_number _SNR_Level_3 \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 300 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done

# # #FITS
# # seq_len=50
# # model_name=FITS
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=FITS_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
# # for pred_len in 100 
# # do
# #     python -u main.py \
# #       --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --task_name long_term_forecast \
# #        --distribution_number _SNR_Level_3 \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --enc_in 1 \
# #       --patience 70 \
# #       --train_epochs 300 \
# #       --itr 1 \
# #       --batch_size 128 \
# #       --lradj 'TST' \
# #       --weight_decay 0.001 \
# #       --backcast 0\
# #       --revin 1\
# #       --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Models/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
# # done






# ##SNR_LEVEL_4

# #Drift_Harmonic Testing (SNR_Level-4)
# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_4
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\    --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _SNR_Level_4 \
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


# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_4
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
#        --distribution_number _SNR_Level_4\
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
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_4
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
#        --distribution_number _SNR_Level_4 \
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


# #SNR_LEVEL_5
# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_5
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\    --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _SNR_Level_5\
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


# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_5
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
#        --distribution_number _SNR_Level_5\
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
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_5
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
#        --distribution_number _SNR_Level_5 \
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

# #SNR_LEVEL_6
# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_6
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\    --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _SNR_Level_6\
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


# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Drift_Harmonic_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_6
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
#        --distribution_number _SNR_Level_6\
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
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_6
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
#        --distribution_number _SNR_Level_6\
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






# #Single Phase Modulation (SNR_Level-4)


# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_4
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\    --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _SNR_Level_4 \
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




# ##DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_4
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
#       --distribution_number _SNR_Level_4 \
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
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_4
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
#       --distribution_number _SNR_Level_4 \
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


# #SNR_LEVEL_5

# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_5
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\    --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _SNR_Level_5 \
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




# ##DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_5
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
#       --distribution_number _SNR_Level_5 \
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
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_5
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
#       --distribution_number _SNR_Level_5 \
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


# #SNR_LEVEL_6

# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_6
# for pred_len in 100
# do
#     python -u main.py \
#       --is_training 2\    --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --task_name long_term_forecast \
#       --distribution_number _SNR_Level_6 \
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




# ##DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_6
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
#       --distribution_number _SNR_Level_6 \
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
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_6
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
#       --distribution_number _SNR_Level_6 \
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





# ##Dual Phase Modulation

# #Linear
# seq_len=50
# model_name=Linear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Linear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_4
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
#       --distribution_number _SNR_Level_4 \
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





#  ##DLinear

# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_4
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
#        --distribution_number _SNR_Level_4 \
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
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_4
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
#        --distribution_number _SNR_Level_4 \
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


# ##Generate for _SNR_5
# #Dual Phase Modulation(SNR_Level-5)
# #Linear
#Linear
seq_len=50
model_name=Linear
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Linear_Dual_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_5
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
      --distribution_number _SNR_Level_5 \
      --features S \
      --target Value \
      --seq_len $seq_len \
      --pred_len $pred_len \
      --enc_in 1 \
      --patience 70 \
      --train_epochs 200 \
      --itr 1 \
      --batch_size 128 \
      --lradj 'TST' \
      --weight_decay 0.001 \
      --backcast 0\
      --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
done



# #DLinear
# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_5
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
#        --distribution_number _SNR_Level_5 \
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
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_5
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
#        --distribution_number _SNR_Level_5 \
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




# #SNR_LEVEL_6

# #Dual Phase Modulation(SNR_Level-6)
seq_len=50
model_name=Linear
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=Linear_Dual_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_6
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
      --distribution_number _SNR_Level_6\
      --features S \
      --target Value \
      --seq_len $seq_len \
      --pred_len $pred_len \
      --enc_in 1 \
      --patience 70 \
      --train_epochs 200 \
      --itr 1 \
      --batch_size 128 \
      --lradj 'TST' \
      --weight_decay 0.001 \
      --backcast 0\
      --learning_rate 0.0001| tee logs/LongForecasting/synthetic_Linear_Ph/${model_name}_${seq_len}_${pred_len}_${data_descriptor}_revin_${current_time}.txt
done


# #DLinear
# seq_len=50
# model_name=DLinear
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=DLinear_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_6
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
#        --distribution_number _SNR_Level_6 \
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
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_6
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
#        --distribution_number _SNR_Level_6 \
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
