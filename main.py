import argparse
import os
import torch
import torch.backends
from Experiment.exp_forecast import Exp_Long_Term_Forecast
from Experiment.exp_forecast_test import Exp_Long_Term_Forecast_Test
from Experiment.exp_test_only import Exp_Long_Term_Forecast_Test_Dist
from Experiment.exp_test_only import *
# from Experiment.Exp_stats import Exp_Main
from utils.print_args import print_args
import random
import numpy as np
from utils.str2bool import str2bool
from utils.config import resolve_run, result_dir_for

if __name__ == '__main__':
   
    
    parser = argparse.ArgumentParser(description='TimeSeriesForecasting')
    parser.add_argument('--seed', type=int, default=2021, help='random seed')
    parser.add_argument('--train_sample_size', type=int, default=None, help='random seed')
    parser.add_argument('--test_sample_size', type=int, default=None, help='random seed')
    parser.add_argument('--val_sample_size', type=int, default=None, help='random seed')
   
    # Basic config
    parser.add_argument('--task_name', type=str, required=True, default='long_term_forecast',
                        help='task name, options:[long_term_forecast, short_term_forecast, imputation, classification, anomaly_detection]')
    parser.add_argument('--is_training', type=int, required=True, default=1, help='status')
    parser.add_argument('--model_id', type=str, required=True, default='test', help='model id')
    parser.add_argument('--model', type=str, required=True, default='Autoformer',
                        help='model name, options: [Autoformer, Transformer, TimesNet]')
    parser.add_argument('--random_seed', type=int, default=2021, help='random seed')

    # Data loader
    parser.add_argument('--data', type=str, required=True, default='custom', help='dataset type')
    parser.add_argument('--root_path', type=str, default='./Synthetic_datasets/', help='root path of the data folder')
    # parser.add_argument('--train_files', type=str, nargs='+', default=['train/train_coefficient_0.1.csv', 'train/train_coefficient_0.3.csv', 'train/train_coefficient_0.5.csv'],
    #                     help='list of training files')
    # parser.add_argument('--test_files', type=str, nargs='+', default=['test/test_coefficient_0.2.csv', 'test/test_coefficient_0.6.csv'],
    #                     help='list of testing files')
    parser.add_argument('--features', type=str, default='S',
                        help='forecasting task, options:[M, S, MS]; M:multivariate, S:univariate, MS:multivariate to univariate')
    parser.add_argument('--target', type=str, default='Value', help='target feature in univariate task')
    parser.add_argument('--freq', type=str, default='h', help='frequency of time features encoding')
    parser.add_argument('--checkpoints', type=str, default=None,
                        help='(legacy alias of --checkpoint_dir)')

    # --- P0.2: revision runner -------------------------------------------------
    parser.add_argument('--model_config', type=str, default=None,
                        help='configs/models/<name>.yaml (or a path); sets model hyperparameters')
    parser.add_argument('--paradigm_config', type=str, default=None,
                        help='configs/paradigms/<name>.yaml (or a path); sets data location and windows')
    parser.add_argument('--signal', type=str, default=None, help='signal family key inside the paradigm config')
    parser.add_argument('--condition', type=str, default=None,
                        help='test-only condition key inside the paradigm config (e.g. SNR_3, bucket_p1)')
    parser.add_argument('--model_label', type=str, default=None,
                        help='name used in results/<paradigm>/<signal>/<model_label>/ (default: model, or YAML label)')
    parser.add_argument('--results_dir', type=str, default='./results',
                        help='root of results/{paradigm}/{signal}/{model}/seed{k}/')
    parser.add_argument('--checkpoint_dir', type=str, default='./checkpoints', help='root of checkpoints')
    parser.add_argument('--checkpoint_name', type=str, default=None,
                        help='checkpoint folder name under --checkpoint_dir; default <setting>_seed<k>. '
                             'Use it to evaluate a legacy (paper) checkpoint with --is_training 2')
    parser.add_argument('--seeds', type=int, nargs='+', default=None,
                        help='one run per seed (default: [--seed])')
    parser.add_argument('--train_stride', type=int, default=1, help='window stride for the training split')
    parser.add_argument('--eval_stride', type=int, default=1,
                        help='window stride for val/test splits; seq_len+pred_len gives non-overlapping windows')
    parser.add_argument('--test_drop_last', type=str2bool, default=True,
                        help='drop the last partial test batch (paper behavior). Revision runs use False')
    parser.add_argument('--fs', type=float, default=10.0, help='sampling rate in Hz (recorded in meta)')
    parser.add_argument('--save_legacy_arrays', type=str2bool, default=True,
                        help='also write test_{pred,true}_with_history.npy for the Statistical_Test scripts')
    parser.add_argument('--scale', type=bool, default=False, help='whether to scale the dataset')
    
    # Forecasting task
    parser.add_argument('--seq_len', type=int, default=96, help='input sequence length')
    parser.add_argument('--label_len', type=int, default=0, help='start token length')
    parser.add_argument('--pred_len', type=int, default=96, help='prediction sequence length')
    parser.add_argument('--inverse', action='store_true', help='inverse output data', default=False)
    
    # Optimization
    parser.add_argument('--num_workers', type=int, default=10, help='data loader num workers')
    parser.add_argument('--train_epochs', type=int, default=100, help='train epochs')
    parser.add_argument('--itr', type=int, default=1, help='experiments times')
    parser.add_argument('--batch_size', type=int, default=128, help='batch size of train input data')
    parser.add_argument('--learning_rate', type=float, default=0.0001, help='optimizer learning rate')
    parser.add_argument('--lradj', type=str, default='type1', help='adjust learning rate')
    parser.add_argument('--patience', type=int, default=20, help='early stopping patience')
    parser.add_argument('--pct_start', type=float, default=0.3, help='pct_start')
    parser.add_argument('--use_amp', action='store_true', help='use automatic mixed precision training', default=False)
    parser.add_argument('--use_dtw', type=bool, default=False,
                        help='the controller of using dtw metric (dtw is time consuming, not suggested unless necessary)')
    parser.add_argument('--weight_decay', type=float, default=0.0, help='weight decay value')
 

    #Model
    parser.add_argument('--enc_in', type=int, default=7, help='encoder input size')
    parser.add_argument('--dec_in', type=int, default=7, help='decoder input size')
    parser.add_argument('--individual', action='store_true', default=False, help='Linear: a linear layer for each variate(channel) individually')
    parser.add_argument('--embed', type=str, default='timeF',
                        help='time features encoding, options:[timeF, fixed, learned]')
    parser.add_argument('--patch_len', type=int, default=16, help='patch length')
    parser.add_argument('--stride', type=int, default=8, help='stride')
    parser.add_argument('--fc_dropout', type=float, default=0.05, help='fully connected dropout')
    parser.add_argument('--head_dropout', type=float, default=0.0, help='head dropout')
    parser.add_argument('--padding_patch', default='end', help='None: None; end: padding on the end')
    parser.add_argument('--revin', type=int, default=0, help='RevIN; True 1 False 0')
    parser.add_argument('--affine', type=int, default=0, help='RevIN-affine; True 1 False 0')
    parser.add_argument('--subtract_last', type=int, default=0, help='0: subtract mean; 1: subtract last')
    parser.add_argument('--decomposition', type=int, default=0, help='decomposition; True 1 False 0')
    parser.add_argument('--kernel_size', type=int, default=25, help='decomposition-kernel')
    parser.add_argument('--independent', type=int, default=1, help='independent; True 1 False 0')
    parser.add_argument('--patch',type=int, default=1, help='patch; True 1 False 0')
    parser.add_argument('--d_model', type=int, default=512, help='dimension of model')
    parser.add_argument('--n_heads', type=int, default=8, help='num of heads')
    parser.add_argument('--e_layers', type=int, default=2, help='num of encoder layers')
    parser.add_argument('--d_layers', type=int, default=1, help='num of decoder layers')
    parser.add_argument('--d_ff', type=int, default=2048, help='dimension of fcn')
    parser.add_argument('--dropout', type=float, default=0.1, help='dropout')
    parser.add_argument('--hidden_dims', type=int, nargs='+', default=[128, 256, 128])
    parser.add_argument('--mlp_dropout', type=float, default=0.4, help='MLinear dropout')
    parser.add_argument('--backcast',type=int,default=1,help="if past should be reconstructed or not")
    parser.add_argument('--activation', type=str, default='gelu',help='activation')
    parser.add_argument('--output_attention',action='store_true', help='whether to output attention in ecoder')

    #FLinear
    parser.add_argument('--train_mode', type=int,default=0)
    parser.add_argument('--cut_freq', type=int,default=15)
    parser.add_argument('--base_T', type=int,default=1)
    parser.add_argument('--H_order', type=int,default=2)

    #NBeats
    parser.add_argument('--n_blocks',type=int, default=5)
    parser.add_argument('--hidden_size',type=int, default=256)
    parser.add_argument('--block_type',type=str, choices=['trend','seasonality','generic'],default='seasonality')
    parser.add_argument('--n_layers',type=int, default=4)
    parser.add_argument('--harmonics',type=int, default=8)
    parser.add_argument('--poly_degree',type=int, default=2)
 

   #MICN
    #Number of Scales (Number of conv_kernel, Isometric_kernel_size, number_of_mic_layers,feature_dimension)
    parser.add_argument('--conv_kernel', type=int, nargs='+', default=[17,49], help='downsampling and upsampling convolution kernel_size')
    parser.add_argument('--decomp_kernel', type=int, nargs='+', default=[17,49], help='decomposition kernel_size')
    parser.add_argument('--isometric_kernel', type=int, nargs='+', default=[17,49], help='isometric convolution kernel_size')
    parser.add_argument('--mode', type=str, default='regre', help='different mode of trend prediction block: [regre or mean]')
    parser.add_argument('--c_out', type=int, default=7, help='output size')
    parser.add_argument('--padding', type=int, default=0, help='padding type')


   #TimesNet
    parser.add_argument('--top_k', type=int, default=5, help='for TimesBlock')
    parser.add_argument('--factor', type=int, default=1, help='attn factor')
    parser.add_argument('--num_kernels', type=int, default=6, help='for Inception')


    #ModernTCN
    #ModernTCN
    parser.add_argument('--stem_ratio', type=int, default=2, help='stem ratio')
    parser.add_argument('--downsample_ratio', type=int, default=1, help='downsample_ratio')
    parser.add_argument('--ffn_ratio', type=int, default=2, help='ffn_ratio')
    parser.add_argument('--patch_size', type=int, default=8, help='the patch size')
    parser.add_argument('--patch_stride', type=int, default=4, help='the patch stride')

    parser.add_argument('--num_blocks', nargs='+',type=int, default=[1,1,1,1], help='num_blocks in each stage')
    parser.add_argument('--large_size', nargs='+',type=int, default=[31,29,27,13], help='big kernel size')
    parser.add_argument('--small_size', nargs='+',type=int, default=[5,5,5,5], help='small kernel size for structral reparam')
    parser.add_argument('--dims', nargs='+',type=int, default=[64,128,256,512], help='dmodels in each stage')
    parser.add_argument('--dw_dims', nargs='+',type=int, default=[256,256,256,256])

    parser.add_argument('--small_kernel_merged', type=str2bool, default=False, help='small_kernel has already merged or not')
    parser.add_argument('--call_structural_reparam', type=bool, default=False, help='structural_reparam after training')
    parser.add_argument('--use_multi_scale', type=str2bool, default=True, help='use_multi_scale fusion')



    #Pathformer

    parser.add_argument('--num_nodes', type=int, default=21)
    parser.add_argument('--layer_nums', type=int, default=3)
    parser.add_argument('--k', type=int, default=2, help='choose the Top K patch size at the every layer ')
    parser.add_argument('--num_experts_list', type=list, default=[4, 4, 4])
    parser.add_argument('--patch_size_list', nargs='+', type=int, default=[16,12,8,32,12,8,6,4,8,6,4,2])
    parser.add_argument('--do_predict', action='store_true', help='whether to predict unseen future data')
    parser.add_argument('--drop', type=float, default=0.1, help='dropout ratio')
    parser.add_argument('--residual_connection', type=int, default=0)
    parser.add_argument('--metric', type=str, default='mae')
    parser.add_argument('--batch_norm', type=int, default=0)
    
    #Autformer
    parser.add_argument('--moving_avg', type=int, default=25, help='window size of moving average')


    #Dsitribution_Shift
    parser.add_argument('--distribution_number',type=str, default="_Markov",help="Specify the Distribution")

    # GPU
    parser.add_argument('--use_gpu', type=bool, default=True, help='use gpu')
    parser.add_argument('--gpu', type=int, default=0, help='gpu')
    parser.add_argument('--gpu_type', type=str, default='cuda', help='gpu type')  # cuda or mps
    parser.add_argument('--use_multi_gpu', action='store_true', help='use multiple gpus', default=False)
    parser.add_argument('--devices', type=str, default='0,1,2,3', help='device ids of multile gpus')


    #For Satistical Models
    parser.add_argument('--stat_model',type=bool, default=False, help="Use Statistical Models")
    parser.add_argument('--sample', type=float, default=0.01, help='Sampling percentage, the inference time of ARIMA and SARIMA is too long, you might sample 0.01')

    #For saving the states
    parser.add_argument("--save_gt_state",type=str2bool,default=True,help="Save GT states when the loader provides them")
    
    args = parser.parse_args()

    # P0.2: merge YAML configs (explicit flags win), derive root_path and result labels
    resolve_run(args)
    if args.checkpoints:            # legacy alias
        args.checkpoint_dir = args.checkpoints
    args.checkpoints = args.checkpoint_dir
    if args.seeds is None:
        args.seeds = [args.seed]
    if args.model_id == 'auto':
        args.model_id = '{}_{}_{}_{}_{}'.format(args.model_label, args.seq_len, args.pred_len,
                                                args.paradigm, args.signal)

    #For FITSf
    if args.cut_freq == 0:
        args.cut_freq = int(args.seq_len // args.base_T + 1) * args.H_order + 10
    
    #For MICN Only 
    decomp_kernel = []  # kernel of decomposition operation 
    isometric_kernel = []  # kernel of isometric convolution
    for ii in args.conv_kernel:
        if ii%2 == 0:   # the kernel of decomposition operation must be odd
            decomp_kernel.append(ii+1)
            isometric_kernel.append((args.seq_len + args.pred_len+ii) // ii) 
        else:
            decomp_kernel.append(ii)
            isometric_kernel.append((args.seq_len + args.pred_len+ii-1) // ii) 
    args.isometric_kernel = isometric_kernel  # kernel of isometric convolution
    args.decomp_kernel = decomp_kernel 

    #For Statistial Models 
     

    def _seed_everything(seed):
        random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        np.random.seed(seed)

    _seed_everything(args.seed)


    if torch.cuda.is_available() and args.use_gpu:
        args.device = torch.device('cuda:{}'.format(args.gpu))
        print('Using GPU')
    else:
        args.device = torch.device('cpu')
        print('Using CPU')

    print('Args in experiment:')
   # print_args(args)

    #Exp= Exp_Long_Term_Forecast_MLE
    
    print(args.is_training)

    setting = '{}_{}_{}_{}_{}'.format(args.task_name, args.model_id, args.weight_decay,
                                      args.learning_rate, args.patch_len)

    if args.is_training==1 and args.stat_model==False:
        for seed in args.seeds:
            args.seed = seed
            _seed_everything(seed)
            args.run_dir = result_dir_for(args, seed)
            args.ckpt_name = args.checkpoint_name or f'{setting}_seed{seed}'
            if os.path.exists(os.path.join(args.run_dir, 'pred.npy')):
                print(f'[skip] {args.run_dir} already has pred.npy')
                continue
            Exp = Exp_Long_Term_Forecast
            exp = Exp(args)  # Initialize experiment
            print(f'Starting training seed {seed}')

            print('>>>>>>> Start training: {} >>>>>>>>>>>>>>>>>>>>>>>>>>'.format(args.ckpt_name))
            exp.train(setting)

            print('>>>>>>> Testing: {} <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'.format(args.ckpt_name))
            exp.test(setting)
            
            torch.cuda.empty_cache()
          # exp.plot_model_structure()

    elif args.is_training==2 and args.stat_model==False:
        # test-only: evaluate a trained checkpoint on another condition (noise, shift, markov p)
        for seed in args.seeds:
            args.seed = seed
            _seed_everything(seed)
            args.run_dir = result_dir_for(args, seed)
            args.ckpt_name = args.checkpoint_name or f'{setting}_seed{seed}'
            if os.path.exists(os.path.join(args.run_dir, 'pred.npy')):
                print(f'[skip] {args.run_dir} already has pred.npy')
                continue
            Exp=Exp_Long_Term_Forecast_Test_Dist
            exp=Exp(args)
            exp.test(setting,args.distribution_number,test=1)
            torch.cuda.empty_cache()

        
    # else:
    #     Exp= Exp_Long_Term_Forecast_Test
    #     exp = Exp(args)
    #     setting = '{}_{}_{}_{}_{}'.format(args.task_name, args.model_id,args.weight_decay,args.learning_rate,args.patch_len)
     
    #     print('>>>>>>> Testing: {} <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'.format(setting))
    #     exp.test(setting, test=1)
    #     torch.cuda.empty_cache()

    
    # if args.stat_model:
    #     Exp = Exp_Main
    #     setting = '{}_{}_{}_ft{}_sl{}_pl{}_{}'.format(
    #         args.model_id,
    #         args.model,
    #         args.data,
    #         args.features,
    #         args.seq_len,
    #         args.pred_len, 0)

    #     exp = Exp(args)  # set experiments
    #     print('>>>>>>>testing : {}<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'.format(setting))
    #     exp.test(setting)
       