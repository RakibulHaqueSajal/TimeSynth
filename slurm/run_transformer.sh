# # #!/bin/bash

# # export CUDA_VISIBLE_DEVICES=0

# # # Create directories if they don't exist

# # if [ ! -d "./logs" ]; then
# #     mkdir ./logs
# # fi

# # if [ ! -d "./logs/LongForecasting" ]; then
# #     mkdir ./logs/LongForecasting
# # fi

# # if [ ! -d "./logs/LongForecasting/synthetic_Transformer_IE" ]; then
# #     mkdir ./logs/LongForecasting/synthetic_Transformer_IE
# # fi




# # #Drift Harmonic Clean

# # #PatchTST


# # # seq_len=50 
# # # model_name=PatchTST
# # # train_sample_size=70
# # # val_sample_size=10
# # # test_sample_size=20
# # # data_descriptor=PatchTST_Drift_Harmonic_Clean
# # # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
# # # for pred_len in  100 
# # # do
# # #     python -u main.py \
# # #       --is_training 0\
# # #       --train_sample_size $train_sample_size \
# # #       --val_sample_size $val_sample_size \
# # #       --test_sample_size $test_sample_size \
# # #       --root_path $root_path \
# # #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# # #       --model $model_name \
# # #       --data custom \
# # #       --features S \
# # #       --target Value \
# # #       --seq_len $seq_len \
# # #       --pred_len $pred_len \
# # #       --task_name long_term_forecast\
# # #       --enc_in 1 \
# # #       --e_layers 3\
# # #       --n_heads 8 \
# # #       --d_model 256 \
# # #       --d_ff 256 \
# # #       --dropout 0.2\
# # #       --fc_dropout 0.2\
# # #       --head_dropout 0.2\
# # #       --patch_len 15\
# # #       --stride 10\
# # #       --train_epochs 2\
# # #       --patience 80\
# # #       --lradj 'TST'\
# # #       --pct_start 0.2\
# # #       --revin 1\
# # #       --decomposition 0\
# # #       --weight_decay 0.0001\
# # #       --backcast 0 \
# # #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # # done



# # # #Autoformer

# # # seq_len=50 
# # # model_name=Autoformer
# # # train_sample_size=70
# # # val_sample_size=10
# # # test_sample_size=20
# # # data_descriptor=Autoformer_Drift_Harmonic_Clean
# # # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
# # # for pred_len in  100 
# # # do
# # #     python -u main.py \
# # #       --is_training 0\
# # #       --train_sample_size $train_sample_size \
# # #       --val_sample_size $val_sample_size \
# # #       --test_sample_size $test_sample_size \
# # #       --root_path $root_path \
# # #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# # #       --model $model_name \
# # #       --data custom \
# # #       --features S \
# # #       --target Value \
# # #       --seq_len $seq_len \
# # #       --pred_len $pred_len \
# # #       --task_name long_term_forecast\
# # #       --enc_in 1 \
# # #       --e_layers 2\
# # #       --n_heads 8 \
# # #       --d_model 256 \
# # #       --d_ff 256 \
# # #       --dropout 0.2\
# # #       --fc_dropout 0.2\
# # #       --head_dropout 0.2\
# # #       --dec_in 1 \
# # #       --c_out 1\
# # #       --label_len 25\
# # #       --train_epochs 2\
# # #       --patience 80\
# # #       --lradj 'TST'\
# # #       --pct_start 0.2\
# # #       --revin 1\
# # #       --decomposition 0\
# # #       --weight_decay 0.0001\
# # #       --backcast 0 \
# # #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # # done


# # #Transformer

# # # seq_len=50 
# # # model_name=Transformer
# # # train_sample_size=70
# # # val_sample_size=10
# # # test_sample_size=20
# # # data_descriptor=Transformer_Drift_Harmonic_Clean_label_len_in_test
# # # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
# # # for pred_len in  100 
# # # do
# # #     python -u main.py \
# # #       --is_training 0\
# # #       --train_sample_size $train_sample_size \
# # #       --val_sample_size $val_sample_size \
# # #       --test_sample_size $test_sample_size \
# # #       --root_path $root_path \
# # #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# # #       --model $model_name \
# # #       --data custom \
# # #       --features S \
# # #       --target Value \
# # #       --seq_len $seq_len \
# # #       --pred_len $pred_len \
# # #       --task_name long_term_forecast\
# # #       --enc_in 1 \
# # #       --e_layers 2\
# # #       --n_heads 8 \
# # #       --d_model 256 \
# # #       --d_ff 256 \
# # #       --dropout 0.2\
# # #       --fc_dropout 0.2\
# # #       --head_dropout 0.2\
# # #       --dec_in 1 \
# # #       --c_out 1\
# # #       --factor 3\
# # #       --label_len 25\
# # #       --train_epochs 300\
# # #       --patience 30\
# # #       --lradj 'TST'\
# # #       --pct_start 0.2\
# # #       --revin 1\
# # #       --decomposition 0\
# # #       --weight_decay 0.0001\
# # #       --backcast 0 \
# # #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # # done



# # # #Drift Harmonic SNR level-1


# # # #PatchTST


# # # seq_len=50 
# # # model_name=PatchTST
# # # train_sample_size=70
# # # val_sample_size=10
# # # test_sample_size=20
# # # data_descriptor=PatchTST_Drift_Harmonic_SNR_Level_1
# # # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_1
# # # for pred_len in  100 
# # # do
# # #     python -u main.py \
# # #       --is_training 0\
# # #       --train_sample_size $train_sample_size \
# # #       --val_sample_size $val_sample_size \
# # #       --test_sample_size $test_sample_size \
# # #       --root_path $root_path \
# # #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# # #       --model $model_name \
# # #       --data custom \
# # #       --features S \
# # #       --target Value \
# # #       --seq_len $seq_len \
# # #       --pred_len $pred_len \
# # #       --task_name long_term_forecast\
# # #       --enc_in 1 \
# # #       --e_layers 3\
# # #       --n_heads 8 \
# # #       --d_model 256 \
# # #       --d_ff 256 \
# # #       --dropout 0.2\
# # #       --fc_dropout 0.2\
# # #       --head_dropout 0.2\
# # #       --patch_len 15\
# # #       --stride 10\
# # #       --train_epochs 2\
# # #       --patience 80\
# # #       --lradj 'TST'\
# # #       --pct_start 0.2\
# # #       --revin 1\
# # #       --decomposition 0\
# # #       --weight_decay 0.0001\
# # #       --backcast 0 \
# # #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # # done



# # # #Autoformer

# # # seq_len=50 
# # # model_name=Autoformer
# # # train_sample_size=70
# # # val_sample_size=10
# # # test_sample_size=20
# # # data_descriptor=Autoformer_Drift_Harmonic_SNR_Level_1
# # # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_1
# # # for pred_len in  100 
# # # do
# # #     python -u main.py \
# # #       --is_training 0\
# # #       --train_sample_size $train_sample_size \
# # #       --val_sample_size $val_sample_size \
# # #       --test_sample_size $test_sample_size \
# # #       --root_path $root_path \
# # #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# # #       --model $model_name \
# # #       --data custom \
# # #       --features S \
# # #       --target Value \
# # #       --seq_len $seq_len \
# # #       --pred_len $pred_len \
# # #       --task_name long_term_forecast\
# # #       --enc_in 1 \
# # #       --e_layers 2\
# # #       --n_heads 8 \
# # #       --d_model 256 \
# # #       --d_ff 256 \
# # #       --dropout 0.2\
# # #       --fc_dropout 0.2\
# # #       --head_dropout 0.2\
# # #       --dec_in 1 \
# # #       --c_out 1\
# # #       --label_len 25\
# # #       --train_epochs 2\
# # #       --patience 80\
# # #       --lradj 'TST'\
# # #       --pct_start 0.2\
# # #       --revin 1\
# # #       --decomposition 0\
# # #       --weight_decay 0.0001\
# # #       --backcast 0 \
# # #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # # done


# # # #Transformer

# # # seq_len=50 
# # # model_name=Transformer
# # # train_sample_size=70
# # # val_sample_size=10
# # # test_sample_size=20
# # # data_descriptor=Transformer_Drift_Harmonic_SNR_Level_1
# # # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_1
# # # for pred_len in  100 
# # # do
# # #     python -u main.py \
# # #       --is_training 0\
# # #       --train_sample_size $train_sample_size \
# # #       --val_sample_size $val_sample_size \
# # #       --test_sample_size $test_sample_size \
# # #       --root_path $root_path \
# # #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# # #       --model $model_name \
# # #       --data custom \
# # #       --features S \
# # #       --target Value \
# # #       --seq_len $seq_len \
# # #       --pred_len $pred_len \
# # #       --task_name long_term_forecast\
# # #       --enc_in 1 \
# # #       --e_layers 2\
# # #       --n_heads 8 \
# # #       --d_model 256 \
# # #       --d_ff 256 \
# # #       --dropout 0.2\
# # #       --fc_dropout 0.2\
# # #       --head_dropout 0.2\
# # #       --dec_in 1 \
# # #       --c_out 1\
# # #       --factor 3\
# # #       --label_len 25\
# # #       --train_epochs 2\
# # #       --patience 80\
# # #       --lradj 'TST'\
# # #       --pct_start 0.2\
# # #       --revin 1\
# # #       --decomposition 0\
# # #       --weight_decay 0.0001\
# # #       --backcast 0 \
# # #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # # done


# # # #Drift Harmonic (SNR_Level_2)



# # # #PatchTST


# # # seq_len=50 
# # # model_name=PatchTST
# # # train_sample_size=70
# # # val_sample_size=10
# # # test_sample_size=20
# # # data_descriptor=PatchTST_Drift_Harmonic_SNR_Level_2
# # # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_2
# # # for pred_len in  100 
# # # do
# # #     python -u main.py \
# # #       --is_training 0\
# # #       --train_sample_size $train_sample_size \
# # #       --val_sample_size $val_sample_size \
# # #       --test_sample_size $test_sample_size \
# # #       --root_path $root_path \
# # #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# # #       --model $model_name \
# # #       --data custom \
# # #       --features S \
# # #       --target Value \
# # #       --seq_len $seq_len \
# # #       --pred_len $pred_len \
# # #       --task_name long_term_forecast\
# # #       --enc_in 1 \
# # #       --e_layers 3\
# # #       --n_heads 8 \
# # #       --d_model 256 \
# # #       --d_ff 256 \
# # #       --dropout 0.2\
# # #       --fc_dropout 0.2\
# # #       --head_dropout 0.2\
# # #       --patch_len 15\
# # #       --stride 10\
# # #       --train_epochs 2\
# # #       --patience 80\
# # #       --lradj 'TST'\
# # #       --pct_start 0.2\
# # #       --revin 1\
# # #       --decomposition 0\
# # #       --weight_decay 0.0001\
# # #       --backcast 0 \
# # #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # # done



# # # #Autoformer

# # # seq_len=50 
# # # model_name=Autoformer
# # # train_sample_size=70
# # # val_sample_size=10
# # # test_sample_size=20
# # # data_descriptor=Autoformer_Drift_Harmonic_SNR_Level_2
# # # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_2
# # # for pred_len in  100 
# # # do
# # #     python -u main.py \
# # #       --is_training 0\
# # #       --train_sample_size $train_sample_size \
# # #       --val_sample_size $val_sample_size \
# # #       --test_sample_size $test_sample_size \
# # #       --root_path $root_path \
# # #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# # #       --model $model_name \
# # #       --data custom \
# # #       --features S \
# # #       --target Value \
# # #       --seq_len $seq_len \
# # #       --pred_len $pred_len \
# # #       --task_name long_term_forecast\
# # #       --enc_in 1 \
# # #       --e_layers 2\
# # #       --n_heads 8 \
# # #       --d_model 256 \
# # #       --d_ff 256 \
# # #       --dropout 0.2\
# # #       --fc_dropout 0.2\
# # #       --head_dropout 0.2\
# # #       --dec_in 1 \
# # #       --c_out 1\
# # #       --label_len 25\
# # #       --train_epochs 2\
# # #       --patience 80\
# # #       --lradj 'TST'\
# # #       --pct_start 0.2\
# # #       --revin 1\
# # #       --decomposition 0\
# # #       --weight_decay 0.0001\
# # #       --backcast 0 \
# # #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # # done


# # #Transformer

# # seq_len=50 
# # model_name=Transformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Transformer_Drift_Harmonic_SNR_Level_2
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_2
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #       --is_training 0\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --factor 3\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # # #Drift Harmonic (SNR_Level_3)



# # # #PatchTST


# # # seq_len=50 
# # # model_name=PatchTST
# # # train_sample_size=70
# # # val_sample_size=10
# # # test_sample_size=20
# # # data_descriptor=PatchTST_Drift_Harmonic_SNR_Level_3
# # # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_3
# # # for pred_len in  100 
# # # do
# # #     python -u main.py \
# # #       --is_training 0\
# # #       --train_sample_size $train_sample_size \
# # #       --val_sample_size $val_sample_size \
# # #       --test_sample_size $test_sample_size \
# # #       --root_path $root_path \
# # #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# # #       --model $model_name \
# # #       --data custom \
# # #       --features S \
# # #       --target Value \
# # #       --seq_len $seq_len \
# # #       --pred_len $pred_len \
# # #       --task_name long_term_forecast\
# # #       --enc_in 1 \
# # #       --e_layers 3\
# # #       --n_heads 8 \
# # #       --d_model 256 \
# # #       --d_ff 256 \
# # #       --dropout 0.2\
# # #       --fc_dropout 0.2\
# # #       --head_dropout 0.2\
# # #       --patch_len 15\
# # #       --stride 10\
# # #       --train_epochs 2\
# # #       --patience 80\
# # #       --lradj 'TST'\
# # #       --pct_start 0.2\
# # #       --revin 1\
# # #       --decomposition 0\
# # #       --weight_decay 0.0001\
# # #       --backcast 0 \
# # #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # # done



# # # #Autoformer

# # # seq_len=50 
# # # model_name=Autoformer
# # # train_sample_size=70
# # # val_sample_size=10
# # # test_sample_size=20
# # # data_descriptor=Autoformer_Drift_Harmonic_SNR_Level_3
# # # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_3
# # # for pred_len in  100 
# # # do
# # #     python -u main.py \
# # #       --is_training 0\
# # #       --train_sample_size $train_sample_size \
# # #       --val_sample_size $val_sample_size \
# # #       --test_sample_size $test_sample_size \
# # #       --root_path $root_path \
# # #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# # #       --model $model_name \
# # #       --data custom \
# # #       --features S \
# # #       --target Value \
# # #       --seq_len $seq_len \
# # #       --pred_len $pred_len \
# # #       --task_name long_term_forecast\
# # #       --enc_in 1 \
# # #       --e_layers 2\
# # #       --n_heads 8 \
# # #       --d_model 256 \
# # #       --d_ff 256 \
# # #       --dropout 0.2\
# # #       --fc_dropout 0.2\
# # #       --head_dropout 0.2\
# # #       --dec_in 1 \
# # #       --c_out 1\
# # #       --label_len 25\
# # #       --train_epochs 2\
# # #       --patience 80\
# # #       --lradj 'TST'\
# # #       --pct_start 0.2\
# # #       --revin 1\
# # #       --decomposition 0\
# # #       --weight_decay 0.0001\
# # #       --backcast 0 \
# # #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # # done


# # # #Transformer

# # # seq_len=50 
# # # model_name=Transformer
# # # train_sample_size=70
# # # val_sample_size=10
# # # test_sample_size=20
# # # data_descriptor=Transformer_Drift_Harmonic_SNR_Level_3
# # # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_3
# # # for pred_len in  100 
# # # do
# # #     python -u main.py \
# # #       --is_training 0\
# # #       --train_sample_size $train_sample_size \
# # #       --val_sample_size $val_sample_size \
# # #       --test_sample_size $test_sample_size \
# # #       --root_path $root_path \
# # #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# # #       --model $model_name \
# # #       --data custom \
# # #       --features S \
# # #       --target Value \
# # #       --seq_len $seq_len \
# # #       --pred_len $pred_len \
# # #       --task_name long_term_forecast\
# # #       --enc_in 1 \
# # #       --e_layers 2\
# # #       --n_heads 8 \
# # #       --d_model 256 \
# # #       --d_ff 256 \
# # #       --dropout 0.2\
# # #       --fc_dropout 0.2\
# # #       --head_dropout 0.2\
# # #       --dec_in 1 \
# # #       --c_out 1\
# # #       --factor 3\
# # #       --label_len 25\
# # #       --train_epochs 2\
# # #       --patience 80\
# # #       --lradj 'TST'\
# # #       --pct_start 0.2\
# # #       --revin 1\
# # #       --decomposition 0\
# # #       --weight_decay 0.0001\
# # #       --backcast 0 \
# # #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # # done



# # #Single Phase Modulation Clean 
# # #PatchTST


# # #Single_Phase_Modulation  Clean

# # #PatchTST


# # # seq_len=50 
# # # model_name=PatchTST
# # # train_sample_size=70
# # # val_sample_size=10
# # # test_sample_size=20
# # # data_descriptor=PatchTST_Single_Phase_Modulation_Clean
# # # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/clean
# # # for pred_len in  100 
# # # do
# # #     python -u main.py \
# # #       --is_training 0\
# # #       --train_sample_size $train_sample_size \
# # #       --val_sample_size $val_sample_size \
# # #       --test_sample_size $test_sample_size \
# # #       --root_path $root_path \
# # #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# # #       --model $model_name \
# # #       --data custom \
# # #       --features S \
# # #       --target Value \
# # #       --seq_len $seq_len \
# # #       --pred_len $pred_len \
# # #       --task_name long_term_forecast\
# # #       --enc_in 1 \
# # #       --e_layers 3\
# # #       --n_heads 8 \
# # #       --d_model 256 \
# # #       --d_ff 256 \
# # #       --dropout 0.2\
# # #       --fc_dropout 0.2\
# # #       --head_dropout 0.2\
# # #       --patch_len 15\
# # #       --stride 10\
# # #       --train_epochs 300\
# # #       --patience 30\
# # #       --lradj 'TST'\
# # #       --pct_start 0.2\
# # #       --revin 1\
# # #       --decomposition 0\
# # #       --weight_decay 0.0001\
# # #       --backcast 0 \
# # #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # # done



# # # #Autoformer

# # # seq_len=50 
# # # model_name=Autoformer
# # # train_sample_size=70
# # # val_sample_size=10
# # # test_sample_size=20
# # # data_descriptor=Autoformer_Single_Phase_Modulation_Clean
# # # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/clean
# # # for pred_len in  100 
# # # do
# # #     python -u main.py \
# # #       --is_training 0\
# # #       --train_sample_size $train_sample_size \
# # #       --val_sample_size $val_sample_size \
# # #       --test_sample_size $test_sample_size \
# # #       --root_path $root_path \
# # #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# # #       --model $model_name \
# # #       --data custom \
# # #       --features S \
# # #       --target Value \
# # #       --seq_len $seq_len \
# # #       --pred_len $pred_len \
# # #       --task_name long_term_forecast\
# # #       --enc_in 1 \
# # #       --e_layers 2\
# # #       --n_heads 8 \
# # #       --d_model 256 \
# # #       --d_ff 256 \
# # #       --dropout 0.2\
# # #       --fc_dropout 0.2\
# # #       --head_dropout 0.2\
# # #       --dec_in 1 \
# # #       --c_out 1\
# # #       --label_len 25\
# # #       --train_epochs 300\
# # #       --patience 30\
# # #       --lradj 'TST'\
# # #       --pct_start 0.2\
# # #       --revin 1\
# # #       --decomposition 0\
# # #       --weight_decay 0.0001\
# # #       --backcast 0 \
# # #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # # done


# # # #Transformer

# # # seq_len=50 
# # # model_name=Transformer
# # # train_sample_size=70
# # # val_sample_size=10
# # # test_sample_size=20
# # # data_descriptor=Transformer_Single_Phase_Modulation_Clean
# # # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/clean
# # # for pred_len in  100 
# # # do
# # #     python -u main.py \
# # #       --is_training 0\
# # #       --train_sample_size $train_sample_size \
# # #       --val_sample_size $val_sample_size \
# # #       --test_sample_size $test_sample_size \
# # #       --root_path $root_path \
# # #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# # #       --model $model_name \
# # #       --data custom \
# # #       --features S \
# # #       --target Value \
# # #       --seq_len $seq_len \
# # #       --pred_len $pred_len \
# # #       --task_name long_term_forecast\
# # #       --enc_in 1 \
# # #       --e_layers 2\
# # #       --n_heads 8 \
# # #       --d_model 256 \
# # #       --d_ff 256 \
# # #       --dropout 0.2\
# # #       --fc_dropout 0.2\
# # #       --head_dropout 0.2\
# # #       --dec_in 1 \
# # #       --c_out 1\
# # #       --factor 3\
# # #       --label_len 25\
# # #       --train_epochs 300\
# # #       --patience 30\
# # #       --lradj 'TST'\
# # #       --pct_start 0.2\
# # #       --revin 1\
# # #       --decomposition 0\
# # #       --weight_decay 0.0001\
# # #       --backcast 0 \
# # #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # # done



# # # #Single_Phase_Modulation  SNR level-1


# # # #PatchTST


# # # seq_len=50 
# # # model_name=PatchTST
# # # train_sample_size=70
# # # val_sample_size=10
# # # test_sample_size=20
# # # data_descriptor=PatchTST_Single_Phase_Modulation_SNR_Level_1
# # # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_1
# # # for pred_len in  100 
# # # do
# # #     python -u main.py \
# # #       --is_training 0\
# # #       --train_sample_size $train_sample_size \
# # #       --val_sample_size $val_sample_size \
# # #       --test_sample_size $test_sample_size \
# # #       --root_path $root_path \
# # #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# # #       --model $model_name \
# # #       --data custom \
# # #       --features S \
# # #       --target Value \
# # #       --seq_len $seq_len \
# # #       --pred_len $pred_len \
# # #       --task_name long_term_forecast\
# # #       --enc_in 1 \
# # #       --e_layers 3\
# # #       --n_heads 8 \
# # #       --d_model 256 \
# # #       --d_ff 256 \
# # #       --dropout 0.2\
# # #       --fc_dropout 0.2\
# # #       --head_dropout 0.2\
# # #       --patch_len 15\
# # #       --stride 10\
# # #       --train_epochs 300\
# # #       --patience 30\
# # #       --lradj 'TST'\
# # #       --pct_start 0.2\
# # #       --revin 1\
# # #       --decomposition 0\
# # #       --weight_decay 0.0001\
# # #       --backcast 0 \
# # #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # # done



# # # #Autoformer

# # # seq_len=50 
# # # model_name=Autoformer
# # # train_sample_size=70
# # # val_sample_size=10
# # # test_sample_size=20
# # # data_descriptor=Autoformer_Single_Phase_Modulation_SNR_Level_1
# # # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_1
# # # for pred_len in  100 
# # # do
# # #     python -u main.py \
# # #       --is_training 0\
# # #       --train_sample_size $train_sample_size \
# # #       --val_sample_size $val_sample_size \
# # #       --test_sample_size $test_sample_size \
# # #       --root_path $root_path \
# # #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# # #       --model $model_name \
# # #       --data custom \
# # #       --features S \
# # #       --target Value \
# # #       --seq_len $seq_len \
# # #       --pred_len $pred_len \
# # #       --task_name long_term_forecast\
# # #       --enc_in 1 \
# # #       --e_layers 2\
# # #       --n_heads 8 \
# # #       --d_model 256 \
# # #       --d_ff 256 \
# # #       --dropout 0.2\
# # #       --fc_dropout 0.2\
# # #       --head_dropout 0.2\
# # #       --dec_in 1 \
# # #       --c_out 1\
# # #       --label_len 25\
# # #       --train_epochs 300\
# # #       --patience 30\
# # #       --lradj 'TST'\
# # #       --pct_start 0.2\
# # #       --revin 1\
# # #       --decomposition 0\
# # #       --weight_decay 0.0001\
# # #       --backcast 0 \
# # #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # # done


# # # #Transformer

# # # seq_len=50 
# # # model_name=Transformer
# # # train_sample_size=70
# # # val_sample_size=10
# # # test_sample_size=20
# # # data_descriptor=Transformer_Single_Phase_Modulation_SNR_Level_1
# # # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_1
# # # for pred_len in  100 
# # # do
# # #     python -u main.py \
# # #       --is_training 0\
# # #       --train_sample_size $train_sample_size \
# # #       --val_sample_size $val_sample_size \
# # #       --test_sample_size $test_sample_size \
# # #       --root_path $root_path \
# # #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# # #       --model $model_name \
# # #       --data custom \
# # #       --features S \
# # #       --target Value \
# # #       --seq_len $seq_len \
# # #       --pred_len $pred_len \
# # #       --task_name long_term_forecast\
# # #       --enc_in 1 \
# # #       --e_layers 2\
# # #       --n_heads 8 \
# # #       --d_model 256 \
# # #       --d_ff 256 \
# # #       --dropout 0.2\
# # #       --fc_dropout 0.2\
# # #       --head_dropout 0.2\
# # #       --dec_in 1 \
# # #       --c_out 1\
# # #       --factor 3\
# # #       --label_len 25\
# # #       --train_epochs 300\
# # #       --patience 30\
# # #       --lradj 'TST'\
# # #       --pct_start 0.2\
# # #       --revin 1\
# # #       --decomposition 0\
# # #       --weight_decay 0.0001\
# # #       --backcast 0 \
# # #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # # done


# # # #Single_Phase_Modulation  (SNR_Level_2)



# # # #PatchTST


# # # seq_len=50 
# # # model_name=PatchTST
# # # train_sample_size=70
# # # val_sample_size=10
# # # test_sample_size=20
# # # data_descriptor=PatchTST_Single_Phase_Modulation_SNR_Level_2
# # # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
# # # for pred_len in  100 
# # # do
# # #     python -u main.py \
# # #       --is_training 0\
# # #       --train_sample_size $train_sample_size \
# # #       --val_sample_size $val_sample_size \
# # #       --test_sample_size $test_sample_size \
# # #       --root_path $root_path \
# # #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# # #       --model $model_name \
# # #       --data custom \
# # #       --features S \
# # #       --target Value \
# # #       --seq_len $seq_len \
# # #       --pred_len $pred_len \
# # #       --task_name long_term_forecast\
# # #       --enc_in 1 \
# # #       --e_layers 3\
# # #       --n_heads 8 \
# # #       --d_model 256 \
# # #       --d_ff 256 \
# # #       --dropout 0.2\
# # #       --fc_dropout 0.2\
# # #       --head_dropout 0.2\
# # #       --patch_len 15\
# # #       --stride 10\
# # #       --train_epochs 300\
# # #       --patience 30\
# # #       --lradj 'TST'\
# # #       --pct_start 0.2\
# # #       --revin 1\
# # #       --decomposition 0\
# # #       --weight_decay 0.0001\
# # #       --backcast 0 \
# # #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # # done



# # # #Autoformer

# # # seq_len=50 
# # # model_name=Autoformer
# # # train_sample_size=70
# # # val_sample_size=10
# # # test_sample_size=20
# # # data_descriptor=Autoformer_Single_Phase_Modulation_SNR_Level_2
# # # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
# # # for pred_len in  100 
# # # do
# # #     python -u main.py \
# # #       --is_training 0\
# # #       --train_sample_size $train_sample_size \
# # #       --val_sample_size $val_sample_size \
# # #       --test_sample_size $test_sample_size \
# # #       --root_path $root_path \
# # #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# # #       --model $model_name \
# # #       --data custom \
# # #       --features S \
# # #       --target Value \
# # #       --seq_len $seq_len \
# # #       --pred_len $pred_len \
# # #       --task_name long_term_forecast\
# # #       --enc_in 1 \
# # #       --e_layers 2\
# # #       --n_heads 8 \
# # #       --d_model 256 \
# # #       --d_ff 256 \
# # #       --dropout 0.2\
# # #       --fc_dropout 0.2\
# # #       --head_dropout 0.2\
# # #       --dec_in 1 \
# # #       --c_out 1\
# # #       --label_len 25\
# # #       --train_epochs 300\
# # #       --patience 30\
# # #       --lradj 'TST'\
# # #       --pct_start 0.2\
# # #       --revin 1\
# # #       --decomposition 0\
# # #       --weight_decay 0.0001\
# # #       --backcast 0 \
# # #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # # done


# # # #Transformer

# # # seq_len=50 
# # # model_name=Transformer
# # # train_sample_size=70
# # # val_sample_size=10
# # # test_sample_size=20
# # # data_descriptor=Transformer_Single_Phase_Modulation_SNR_Level_2
# # # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
# # # for pred_len in  100 
# # # do
# # #     python -u main.py \
# # #       --is_training 0\
# # #       --train_sample_size $train_sample_size \
# # #       --val_sample_size $val_sample_size \
# # #       --test_sample_size $test_sample_size \
# # #       --root_path $root_path \
# # #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# # #       --model $model_name \
# # #       --data custom \
# # #       --features S \
# # #       --target Value \
# # #       --seq_len $seq_len \
# # #       --pred_len $pred_len \
# # #       --task_name long_term_forecast\
# # #       --enc_in 1 \
# # #       --e_layers 2\
# # #       --n_heads 8 \
# # #       --d_model 256 \
# # #       --d_ff 256 \
# # #       --dropout 0.2\
# # #       --fc_dropout 0.2\
# # #       --head_dropout 0.2\
# # #       --dec_in 1 \
# # #       --c_out 1\
# # #       --factor 3\
# # #       --label_len 25\
# # #       --train_epochs 300\
# # #       --patience 30\
# # #       --lradj 'TST'\
# # #       --pct_start 0.2\
# # #       --revin 1\
# # #       --decomposition 0\
# # #       --weight_decay 0.0001\
# # #       --backcast 0 \
# # #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # # done



# # # #Single_Phase_Modulation  (SNR_Level_3)



# # # #PatchTST


# # seq_len=50 
# # model_name=PatchTST
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=PatchTST_Single_Phase_Modulationc_SNR_Level_3
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #       --is_training 0\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 3\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --patch_len 15\
# #       --stride 10\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # # # #Autoformer

# # seq_len=50 
# # model_name=Autoformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Autoformer_Single_Phase_Modulation_SNR_Level_3
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #       --is_training 0\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # # #Transformer

# # seq_len=50 
# # model_name=Transformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Transformer_Single_Phase_Modulation_SNR_Level_3
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #       --is_training 0\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --factor 3\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done






# #Dual Phase Modulation






# ##Dual_Phase_Modulation
# ##PatchTST


# # seq_len=50 
# # model_name=PatchTST
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=PatchTST_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 0\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 3\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --patch_len 15\
# #       --stride 10\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # # #Autoformer

# # seq_len=50 
# # model_name=Autoformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Autoformer_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 0\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # # #Transformer

# # seq_len=50 
# # model_name=Transformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Transformer_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 0\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --factor 3\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # # #Dual_Phase_Modulation  SNR level-1


# # # #PatchTST


# # seq_len=50 
# # model_name=PatchTST
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=PatchTST_Dual_Phase_Modulation_SNR_Level_1
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 0\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 3\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --patch_len 15\
# #       --stride 10\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # # #Autoformer

# # seq_len=50 
# # model_name=Autoformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Autoformer_Dual_Phase_Modulation_SNR_Level_1
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 0\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # #Transformer

# # seq_len=50 
# # model_name=Transformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Transformer_Dual_Phase_Modulation_SNR_Level_1
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 0\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --factor 3\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # # #Dual_Phase_Modulation  (SNR_Level_2)



# # # #PatchTST


# # seq_len=50 
# # model_name=PatchTST
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=PatchTST_Dual_Phase_Modulation_SNR_Level_2
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 0\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 3\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --patch_len 15\
# #       --stride 10\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # #Autoformer

# # seq_len=50 
# # model_name=Autoformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Autoformer_Dual_Phase_Modulation_SNR_Level_2
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 0\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # #Transformer

# # seq_len=50 
# # model_name=Transformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Transformer_Dual_Phase_Modulation_SNR_Level_2
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 0\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --factor 3\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # # #Dual_Phase_Modulation  (SNR_Level_3)



# # # #PatchTST


# # seq_len=50 
# # model_name=PatchTST
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=PatchTST_Dual_Phase_Modulationc_SNR_Level_3
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 0\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 3\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --patch_len 15\
# #       --stride 10\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # #Autoformer

# # seq_len=50 
# # model_name=Autoformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Autoformer_Dual_Phase_Modulation_SNR_Level_3
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 0\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # #Transformer

# # seq_len=50 
# # model_name=Transformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Transformer_Dual_Phase_Modulation_SNR_Level_3
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 0\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --factor 3\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done









# # ##Distribution_Test

# # #Drift_Harmonic

# # seq_len=50 
# # model_name=PatchTST
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=PatchTST_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.85_1.10
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --distribution_number _Shift_0\
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 3\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --patch_len 15\
# #       --stride 10\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # seq_len=50 
# # model_name=PatchTST
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=PatchTST_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.35_0.60
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --distribution_number _Shift_1\
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 3\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --patch_len 15\
# #       --stride 10\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # seq_len=50 
# # model_name=PatchTST
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=PatchTST_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.60_0.85
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --distribution_number _Shift_2\
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 3\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --patch_len 15\
# #       --stride 10\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # seq_len=50 
# # model_name=PatchTST
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=PatchTST_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_1.10_1.35
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --distribution_number _Shift_3\
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 3\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --patch_len 15\
# #       --stride 10\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # seq_len=50 
# # model_name=PatchTST
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=PatchTST_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_1.35_1.60
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --distribution_number _Shift_4\
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 3\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --patch_len 15\
# #       --stride 10\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # ##Transformer

# # seq_len=50 
# # model_name=Transformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Transformer_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.85_1.10
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --distribution_number _Shift_0\
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --factor 3\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done




# # seq_len=50 
# # model_name=Transformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Transformer_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.35_0.60
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --distribution_number _Shift_1\
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --factor 3\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # seq_len=50 
# # model_name=Transformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Transformer_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.60_0.85
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --distribution_number _Shift_2\
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --factor 3\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # seq_len=50 
# # model_name=Transformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Transformer_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_1.10_1.35
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --distribution_number _Shift_3\
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --factor 3\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done




# # seq_len=50 
# # model_name=Transformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Transformer_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_1.35_1.60
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --distribution_number _Shift_4\
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --factor 3\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # #Autoformer
# # seq_len=50 
# # model_name=Autoformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Autoformer_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.85_1.10
# # for pred_len in  100
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --distribution_number _Shift_0\
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --label_len 25\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # #Autoformer


# # seq_len=50 
# # model_name=Autoformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Autoformer_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.35_0.60
# # for pred_len in  100
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --distribution_number _Shift_1\
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --label_len 25\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done






# # seq_len=50 
# # model_name=Autoformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Autoformer_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_0.60_0.85
# # for pred_len in  100
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --distribution_number _Shift_2\
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --label_len 25\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done

# # seq_len=50 
# # model_name=Autoformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Autoformer_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_1.10_1.35
# # for pred_len in  100
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --distribution_number _Shift_3\
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --label_len 25\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # seq_len=50 
# # model_name=Autoformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Autoformer_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Drift_Harmonic/f_1.35_1.60
# # for pred_len in  100
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --distribution_number _Shift_4\
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --label_len 25\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# #Single_Sine_Phase_Modulation_Distribution_Test



# # seq_len=50 
# # model_name=PatchTST
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=PatchTST_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.680_1.410
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --distribution_number _Shift_0\
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 3\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --patch_len 15\
# #       --stride 10\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # seq_len=50 
# # model_name=PatchTST
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=PatchTST_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.000_0.340
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --distribution_number _Shift_1\
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 3\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --patch_len 15\
# #       --stride 10\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # seq_len=50 
# # model_name=PatchTST
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=PatchTST_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.340_0.680
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --distribution_number _Shift_2\
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 3\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --patch_len 15\
# #       --stride 10\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # seq_len=50 
# # model_name=PatchTST
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=PatchTST_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_1.410_2.140
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --distribution_number _Shift_3\
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 3\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --patch_len 15\
# #       --stride 10\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # seq_len=50 
# # model_name=PatchTST
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=PatchTST_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_2.140_2.880
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --distribution_number _Shift_4\
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 3\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --patch_len 15\
# #       --stride 10\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # ##Transformer

# # seq_len=50 
# # model_name=Transformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Transformer_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.680_1.410
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --distribution_number _Shift_0\
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --factor 3\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done




# # seq_len=50 
# # model_name=Transformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Transformer_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.000_0.340
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --distribution_number _Shift_1\
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --factor 3\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # seq_len=50 
# # model_name=Transformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Transformer_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.340_0.680
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --distribution_number _Shift_2\
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --factor 3\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # seq_len=50 
# # model_name=Transformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Transformer_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_1.410_2.140
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --distribution_number _Shift_3\
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --factor 3\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done




# # seq_len=50 
# # model_name=Transformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Transformer_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_2.140_2.880
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --distribution_number _Shift_4\
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --factor 3\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # #Autoformer
# # seq_len=50 
# # model_name=Autoformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Autoformer_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.680_1.410
# # for pred_len in  100
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --distribution_number _Shift_0\
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --label_len 25\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # #Autoformer


# # seq_len=50 
# # model_name=Autoformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Autoformer_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.000_0.340
# # for pred_len in  100
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --distribution_number _Shift_1\
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --label_len 25\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done






# # seq_len=50 
# # model_name=Autoformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Autoformer_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_0.340_0.680
# # for pred_len in  100
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --distribution_number _Shift_2\
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --label_len 25\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done

# # seq_len=50 
# # model_name=Autoformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Autoformer_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_1.410_2.140
# # for pred_len in  100
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --distribution_number _Shift_3\
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --label_len 25\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # seq_len=50 
# # model_name=Autoformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Autoformer_Single_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_SingleFreq/f_2.140_2.880
# # for pred_len in  100
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --distribution_number _Shift_4\
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --label_len 25\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done

# ##Dual_Phase_Modulation

# ##PatchTST


# # seq_len=50 
# # model_name=PatchTST
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=PatchTST_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.68_1.41__f1_0.68_1.41
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --distribution_number _Shift_0\
# #       --enc_in 1 \
# #       --e_layers 3\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --patch_len 15\
# #       --stride 10\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # # # #Autoformer

# # seq_len=50 
# # model_name=Autoformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Autoformer_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.68_1.41__f1_0.68_1.41
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --distribution_number _Shift_0\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # # # #Transformer

# # seq_len=50 
# # model_name=Transformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Transformer_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.68_1.41__f1_0.68_1.41
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --distribution_number _Shift_0 \
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --factor 3\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # ##SHIFT_1

# # seq_len=50 
# # model_name=PatchTST
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=PatchTST_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.00_0.34__f1_0.00_0.34
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --distribution_number _Shift_1\
# #       --enc_in 1 \
# #       --e_layers 3\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --patch_len 15\
# #       --stride 10\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # # # #Autoformer

# # seq_len=50 
# # model_name=Autoformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Autoformer_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.00_0.34__f1_0.00_0.34
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --distribution_number _Shift_1\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # # # #Transformer

# # seq_len=50 
# # model_name=Transformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Transformer_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.00_0.34__f1_0.00_0.34
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --distribution_number _Shift_1 \
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --factor 3\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # #SHIFT_2
# # seq_len=50 
# # model_name=PatchTST
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=PatchTST_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.34_0.68__f1_0.34_0.68
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --distribution_number _Shift_2\
# #       --enc_in 1 \
# #       --e_layers 3\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --patch_len 15\
# #       --stride 10\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # # # #Autoformer

# # seq_len=50 
# # model_name=Autoformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Autoformer_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.34_0.68__f1_0.34_0.68
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --distribution_number _Shift_2\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # # # #Transformer

# # seq_len=50 
# # model_name=Transformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Transformer_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_0.34_0.68__f1_0.34_0.68
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --distribution_number _Shift_2 \
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --factor 3\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # ##SHIFT_3

# # seq_len=50 
# # model_name=PatchTST
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=PatchTST_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_1.41_2.14__f1_1.41_2.14
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --distribution_number _Shift_3\
# #       --enc_in 1 \
# #       --e_layers 3\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --patch_len 15\
# #       --stride 10\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # # # #Autoformer

# # seq_len=50 
# # model_name=Autoformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Autoformer_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_1.41_2.14__f1_1.41_2.14
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --distribution_number _Shift_3\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # # # #Transformer

# # seq_len=50 
# # model_name=Transformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Transformer_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_1.41_2.14__f1_1.41_2.14
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --distribution_number _Shift_3 \
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --factor 3\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # #SHIFT_4
# # seq_len=50 
# # model_name=PatchTST
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=PatchTST_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_2.14_2.88__f1_2.14_2.88
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --distribution_number _Shift_4\
# #       --enc_in 1 \
# #       --e_layers 3\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --patch_len 15\
# #       --stride 10\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # # # #Autoformer

# # seq_len=50 
# # model_name=Autoformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Autoformer_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_2.14_2.88__f1_2.14_2.88
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --distribution_number _Shift_4\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done

# # # # #Transformer

# # seq_len=50 
# # model_name=Transformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Transformer_Dual_Phase_Modulation_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Distribution_Shift/Phasemod_TwoFreq/f0_2.14_2.88__f1_2.14_2.88
# # for pred_len in  100 
# # do
# #     python -u main.py \
# #      --is_training 2\
# #       --train_sample_size $train_sample_size \
# #       --val_sample_size $val_sample_size \
# #       --test_sample_size $test_sample_size \
# #       --root_path $root_path \
# #       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
# #       --model $model_name \
# #       --data custom \
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --distribution_number _Shift_4 \
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --factor 3\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# ##Data Genearation Script


# ##Training on Cleaning and Testing on 

# #Drift Harmonic Clean

# #PatchTST


# # seq_len=50 
# # model_name=PatchTST
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=PatchTST_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
# # for pred_len in  100 
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
# #       --distribution_number _SNR_Level_0\
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 3\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --patch_len 15\
# #       --stride 10\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # #Autoformer

# # seq_len=50 
# # model_name=Autoformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Autoformer_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --distribution_number _SNR_Level_0\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --label_len 25\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # # #Transformer

# # seq_len=50 
# # model_name=Transformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Transformer_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/Clean
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --distribution_number _SNR_Level_0 \
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --factor 3\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 30\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # # #Drift Harmonic SNR level-1


# # # #PatchTST


# # seq_len=50 
# # model_name=PatchTST
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=PatchTST_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_1
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --distribution_number _SNR_Level_1\
# #       --enc_in 1 \
# #       --e_layers 3\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --patch_len 15\
# #       --stride 10\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # #Autoformer

# # seq_len=50 
# # model_name=Autoformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Autoformer_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_1
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --distribution_number _SNR_Level_1\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --label_len 25\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # #Transformer

# # seq_len=50 
# # model_name=Transformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Transformer_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_1
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --distribution_number _SNR_Level_1 \
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --factor 3\
# #       --label_len 25\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # # #Drift Harmonic (SNR_Level_2)



# # #PatchTST


# # seq_len=50 
# # model_name=PatchTST
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=PatchTST_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_2
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --distribution_number _SNR_Level_2\
# #       --enc_in 1 \
# #       --e_layers 3\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --patch_len 15\
# #       --stride 10\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # #Autoformer

# # seq_len=50 
# # model_name=Autoformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Autoformer_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_2
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --distribution_number _SNR_Level_2\
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --label_len 25\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # #Transformer

# # seq_len=50 
# # model_name=Transformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Transformer_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_2
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --distribution_number _SNR_Level_2 \
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --factor 3\
# #       --label_len 25\
# #       --train_epochs 300\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # # #Drift Harmonic (SNR_Level_3)



# # # #PatchTST


# # seq_len=50 
# # model_name=PatchTST
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=PatchTST_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_3
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --distribution_number _SNR_Level_3\
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 3\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --patch_len 15\
# #       --stride 10\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done



# # # #Autoformer

# # seq_len=50 
# # model_name=Autoformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Autoformer_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_3
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --distribution_number _SNR_Level_3\
# #       --task_name long_term_forecast\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --label_len 25\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done


# # #Transformer

# # seq_len=50 
# # model_name=Transformer
# # train_sample_size=70
# # val_sample_size=10
# # test_sample_size=20
# # data_descriptor=Transformer_Drift_Harmonic_Clean
# # root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/Drift_Harmonic_Test/SNR_3
# # for pred_len in  100 
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
# #       --features S \
# #       --target Value \
# #       --seq_len $seq_len \
# #       --pred_len $pred_len \
# #       --task_name long_term_forecast\
# #       --distribution_number _SNR_Level_3\
# #       --enc_in 1 \
# #       --e_layers 2\
# #       --n_heads 8 \
# #       --d_model 256 \
# #       --d_ff 256 \
# #       --dropout 0.2\
# #       --fc_dropout 0.2\
# #       --head_dropout 0.2\
# #       --dec_in 1 \
# #       --c_out 1\
# #       --factor 3\
# #       --label_len 25\
# #       --train_epochs 2\
# #       --patience 80\
# #       --lradj 'TST'\
# #       --pct_start 0.2\
# #       --revin 1\
# #       --decomposition 0\
# #       --weight_decay 0.0001\
# #       --backcast 0 \
# #       --itr 1 --batch_size 128 --learning_rate 0.0001 | tee logs/LongForecasting/synthetic_Transformer_IE/$model_name'_'$model_id_name'_'$seq_len'_'$pred_len.txt
# # done




# ##Single_Phase_Modulation

# # #Single Phase Modulation Clean 
# # #PatchTST


# # #Single_Phase_Modulation  Clean

# # #PatchTST


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
#       --is_training 2\
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
#       --distribution_number _SNR_Level_0\
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
#       --is_training 2\
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
#       --distribution_number _SNR_Level_0\
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
#       --is_training 2\
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
#       --distribution_number _SNR_Level_0 \
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
# data_descriptor=PatchTST_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_1
# for pred_len in  100 
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
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --task_name long_term_forecast\
#       --distribution_number _SNR_Level_1\
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
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_1
# for pred_len in  100 
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
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --task_name long_term_forecast\
#       --enc_in 1 \
#       --distribution_number _SNR_Level_1\
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
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_1
# for pred_len in  100 
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
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --task_name long_term_forecast\
#       --distribution_number _SNR_Level_1 \
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


# #Single_Phase_Modulation  (SNR_Level_2)



# #PatchTST


# seq_len=50 
# model_name=PatchTST
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=PatchTST_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
# for pred_len in  100 
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
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --task_name long_term_forecast\
#       --distribution_number _SNR_Level_2\
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
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
# for pred_len in  100 
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
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --task_name long_term_forecast\
#       --distribution_number _SNR_Level_2\
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
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_2
# for pred_len in  100 
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
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --task_name long_term_forecast\
#       --distribution_number _SNR_Level_2\
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



# # #Single_Phase_Modulation  (SNR_Level_3)



# # #PatchTST


seq_len=50 
model_name=PatchTST
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=PatchTST_Single_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
for pred_len in  100 
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
      --features S \
      --target Value \
      --seq_len $seq_len \
      --pred_len $pred_len \
      --task_name long_term_forecast\
      --enc_in 1 \
      --distribution_number _SNR_Level_3\
      --e_layers 3\
      --n_heads 8 \
      --d_model 256 \
      --d_ff 256 \
      --dropout 0.2\
      --fc_dropout 0.2\
      --head_dropout 0.2\
      --patch_len 15\
      --stride 10\
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



# # # #Autoformer

# seq_len=50 
# model_name=Autoformer
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Autoformer_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
# for pred_len in  100 
# do
#     python -u main.py \
#       --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --distribution_number _SNR_Level_3\
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


# # #Transformer

# seq_len=50 
# model_name=Transformer
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Transformer_Single_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_SingleFreq/SNR_3
# for pred_len in  100 
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
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --distribution_number _SNR_Level_3\
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







# ####Dual_Phase_Modulation
# ##PatchTST


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
#      --is_training 2\
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
#       --distribution_number _SNR_Level_0\
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



# # #Autoformer

# seq_len=50 
# model_name=Autoformer
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Autoformer_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
# for pred_len in  100 
# do
#     python -u main.py \
#      --is_training 2\
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
#       --distribution_number _SNR_Level_0\
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


# # #Transformer

# seq_len=50 
# model_name=Transformer
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Transformer_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/clean
# for pred_len in  100 
# do
#     python -u main.py \
#      --is_training 2\
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
#       --distribution_number _SNR_Level_0 \
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



# # #Dual_Phase_Modulation  SNR level-1


# # #PatchTST


# seq_len=50 
# model_name=PatchTST
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=PatchTST_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
# for pred_len in  100 
# do
#     python -u main.py \
#      --is_training 2\
#       --train_sample_size $train_sample_size \
#       --val_sample_size $val_sample_size \
#       --test_sample_size $test_sample_size \
#       --root_path $root_path \
#       --model_id ${model_name}_${seq_len}_${pred_len}_${data_descriptor}_${train_sample_size}_${val_sample_size}_${test_sample_size} \
#       --model $model_name \
#       --data custom \
#       --features S \
#       --distribution_number _SNR_Level_1\
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



# # #Autoformer

# seq_len=50 
# model_name=Autoformer
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Autoformer_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
# for pred_len in  100 
# do
#     python -u main.py \
#      --is_training 2\
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
#       --distribution_number _SNR_Level_1\
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
# data_descriptor=Transformer_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_1
# for pred_len in  100 
# do
#     python -u main.py \
#      --is_training 2\
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
#       --distribution_number _SNR_Level_1\
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


# # #Dual_Phase_Modulation  (SNR_Level_2)



# # #PatchTST


# seq_len=50 
# model_name=PatchTST
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=PatchTST_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
# for pred_len in  100 
# do
#     python -u main.py \
#      --is_training 2\
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
#       --distribution_number _SNR_Level_2\
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
# data_descriptor=Autoformer_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
# for pred_len in  100 
# do
#     python -u main.py \
#      --is_training 2\
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
#       --distribution_number _SNR_Level_2\
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
# data_descriptor=Transformer_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_2
# for pred_len in  100 
# do
#     python -u main.py \
#      --is_training 2\
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
#       --distribution_number _SNR_Level_2\
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



# # #Dual_Phase_Modulation  (SNR_Level_3)



# # #PatchTST


seq_len=50 
model_name=PatchTST
train_sample_size=70
val_sample_size=10
test_sample_size=20
data_descriptor=PatchTST_Dual_Phase_Modulation_Clean
root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
for pred_len in  100 
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
      --features S \
      --target Value \
      --seq_len $seq_len \
      --pred_len $pred_len \
      --task_name long_term_forecast\
      --distribution_number _SNR_Level_3\
      --enc_in 1 \
      --e_layers 3\
      --n_heads 8 \
      --d_model 256 \
      --d_ff 256 \
      --dropout 0.2\
      --fc_dropout 0.2\
      --head_dropout 0.2\
      --patch_len 15\
      --stride 10\
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



# #Autoformer

# seq_len=50 
# model_name=Autoformer
# train_sample_size=70
# val_sample_size=10
# test_sample_size=20
# data_descriptor=Autoformer_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
# for pred_len in  100 
# do
#     python -u main.py \
#      --is_training 2\
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
#       --distribution_number _SNR_Level_3\
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
# data_descriptor=Transformer_Dual_Phase_Modulation_Clean
# root_path=/scratch_nvme/Time_Series/Bio-Synthesize/Generation_Synthesized_Bio_Signals/Noise/PhaseMod_TwoFreq/SNR_3
# for pred_len in  100 
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
#       --features S \
#       --target Value \
#       --seq_len $seq_len \
#       --pred_len $pred_len \
#       --task_name long_term_forecast\
#       --distribution_number _SNR_Level_3\
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




