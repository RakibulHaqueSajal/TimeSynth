import comet_ml
from comet_ml import start
from Data_Loader.data_loader import data_provider
from Experiment.Exp_Basic import Exp_Basic
from utils.tools import EarlyStopping, adjust_learning_rate, visual,visual_multivariate_error_distribution,visual_multichannel,visual_relative_error_distribution
from utils.metrics import metric
import torch
import torch.nn as nn
from torch import optim
import os
import time
import warnings
import numpy as np
from utils.dtw_metric import dtw, accelerated_dtw
from utils.augmentation import run_augmentation, run_augmentation_single
from torch.optim import lr_scheduler
from torchview import draw_graph
import matplotlib.pyplot as plt
from utils.loss import hybrid_loss

# Setting Comment Experiments
# experiment = start(
#   api_key="Vr3vky03wyHWTXJTZ6phb4zEF",
#   project_name="time-series-forecasting",
#   workspace="time-series"
# )



warnings.filterwarnings('ignore')


class Exp_Long_Term_Forecast_Test(Exp_Basic):
    def __init__(self, args):
        self.input_size=None
        super(Exp_Long_Term_Forecast_Test, self).__init__(args)

    def _build_model(self):
        model = self.model_dict[self.args.model].Model(self.args).float()

        if self.args.use_multi_gpu and self.args.use_gpu:
            model = nn.DataParallel(model, device_ids=self.args.device_ids)
        return model

    def _get_data(self, flag):
        data_set, data_loader = data_provider(self.args, flag)
        return data_set, data_loader
   
   #Best Weight Decay for MLinear- Shared 0.0167

    def _select_optimizer(self):
        model_optim = optim.Adam(self.model.parameters(), lr=self.args.learning_rate, weight_decay=self.args.weight_decay)
        #model_optim=optim.SGD(self.model.parameters(),lr=self.args.learning_rate,momentum=0.9,weight_decay=self.args.weight_decay)
        return model_optim

    def _select_criterion(self):
        criterion = nn.MSELoss()
       #criterion = hybrid_loss
        return criterion
 
    def test(self, setting, test=0):
        test_data, test_loader = self._get_data(flag='test')
        train_data, train_loader = self._get_data(flag='train')
        val_data, val_loader = self._get_data(flag='val')
        if test:
            print('loading model')
            self.model.load_state_dict(torch.load(os.path.join('/scratch_nvme/Time_Series/AFPForecast/checkpoints/' + setting, 'checkpoint.pth')))
            #self.model.load_state_dict(torch.load(os.path.join('/scratch_hd/Neurips/Synthetic_Data_Testing/checkpoints/' + setting, 'model_last_epoch.pth')))
            
        #Training
        preds = []
        trues = []
        preds_with_history = []
        trues_with_history = []
        print(setting)
        folder_path = './uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/' + setting + '/'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        #For Training
    
        self.model.eval()
        with torch.no_grad():
            for i, (batch_x, batch_y, batch_x_mark, batch_y_mark) in enumerate(train_loader):
                batch_x = batch_x.float().to(self.device)
                batch_y = batch_y.float().to(self.device)
                batch_x_mark = batch_x_mark.float().to(self.device)
                batch_y_mark = batch_y_mark.float().to(self.device)

                input_seq = batch_x.detach().cpu().numpy()
                if train_data.scale and self.args.inverse:
                    shape = input_seq.shape
                    input_seq = train_data.inverse_transform(
                        input_seq.reshape(shape[0]*shape[1], -1)
                    ).reshape(shape)

                # ------------------------
                # choose decoder input / forward path
                # ------------------------
                if "former" in self.args.model.lower():
                    hist_len = batch_x.shape[1]
                    half     = hist_len // 2

                    enc_x      = batch_x[:, :half, :]
                    enc_x_mark = batch_x_mark[:, :half, :]

                    warmup_y      = batch_x[:, half:, :]
                    warmup_y_mark = batch_x_mark[:, half:, :]

                    if self.args.padding == 0:
                        dec_pad = torch.zeros([batch_y.shape[0], self.args.pred_len, batch_y.shape[-1]],
                                              device=self.device)
                    elif self.args.padding == 1:
                        dec_pad = torch.ones([batch_y.shape[0], self.args.pred_len, batch_y.shape[-1]],
                                             device=self.device)
                    else:
                        raise ValueError("Unknown padding option")

                    dec_inp = torch.cat([warmup_y, dec_pad], dim=1).float().to(self.device)

                    if self.args.use_amp:
                        with torch.cuda.amp.autocast():
                            outputs = self.model(enc_x, enc_x_mark, dec_inp, warmup_y_mark)
                    else:
                        outputs = self.model(enc_x, enc_x_mark, dec_inp, warmup_y_mark)

                else:
                    # decoder input
                    dec_inp = torch.zeros_like(batch_y[:, -self.args.pred_len:, :]).float()
                    dec_inp = torch.cat([batch_y[:, :self.args.label_len, :], dec_inp],
                                        dim=1).float().to(self.device)

                    if self.args.use_amp:
                        with torch.cuda.amp.autocast():
                            if any(k in self.args.model for k in ['Linear','TST','Beats','MLP','TCN']):
                                outputs = self.model(batch_x)
                            elif 'FITS' in self.args.model:
                                outputs, low = self.model(batch_x)
                            else:
                                outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)
                    else:
                        if any(k in self.args.model for k in ['Linear','TST','Beats','MLP','TCN']):
                            outputs = self.model(batch_x)
                        elif 'FITS' in self.args.model:
                            outputs, low = self.model(batch_x)
                        else:
                            outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)
                # ---- the rest of your pipeline stays the same
                f_dim = -1 if self.args.features == 'MS' else 0
                input_seq = input_seq[:, :, f_dim:]
                outputs = outputs[:, -self.args.pred_len:, :]
                batch_y = batch_y[:, -self.args.pred_len:, :].to(self.device)

                outputs = outputs.detach().cpu().numpy()
                batch_y = batch_y.detach().cpu().numpy()

                if val_data.scale and self.args.inverse:
                    shape = batch_y.shape
                    if outputs.shape[-1] != batch_y.shape[-1]:
                        outputs = np.tile(outputs, [1, 1, int(batch_y.shape[-1] / outputs.shape[-1])])
                    outputs = val_data.inverse_transform(outputs.reshape(shape[0] * shape[1], -1)).reshape(shape)
                    batch_y = val_data.inverse_transform(batch_y.reshape(shape[0] * shape[1], -1)).reshape(shape)

                outputs = outputs[:, :, f_dim:]
                batch_y = batch_y[:, :, f_dim:]

                pred = outputs
                true = batch_y

                # Concatenate input (history) + prediction
                pred_with_history = np.concatenate([input_seq, pred], axis=1)
                true_with_history = np.concatenate([input_seq, true], axis=1)

                preds.append(pred)
                trues.append(true)
                preds_with_history.append(pred_with_history)
                trues_with_history.append(true_with_history)

                if i % 20 == 0:
                    input = batch_x.detach().cpu().numpy()
                    if val_data.scale and self.args.inverse:
                        shape = input.shape
                        input = val_data.inverse_transform(
                            input.reshape(shape[0] * shape[1], -1)
                        ).reshape(shape)
                    gt = np.concatenate((input[0, :, -1], true[0, :, -1]), axis=0)
                    pd = np.concatenate((input[0, :, -1], pred[0, :, -1]), axis=0)
                    gt_multichannel = np.concatenate((input[0, :, :], true[0, :, :]), axis=0)
                    pd_multichannel = np.concatenate((input[0, :, :], pred[0, :, :]), axis=0)

                
 
        preds = np.concatenate(preds, axis=0)
        trues = np.concatenate(trues, axis=0)
     
        preds = preds.reshape(-1, preds.shape[-2], preds.shape[-1])
        trues = trues.reshape(-1, trues.shape[-2], trues.shape[-1])


        preds_with_history = np.concatenate(preds_with_history, axis=0)
        trues_with_history = np.concatenate(trues_with_history, axis=0)

        np.save(folder_path + 'train_pred_with_history.npy', preds_with_history)
        np.save(folder_path + 'train_true_with_history.npy', trues_with_history)
        
        print("Training")
        print(trues.shape)
        print(preds.shape)
        print(preds_with_history.shape)
        print(trues_with_history.shape)

        # result save
        folder_path = './Train_Test_Validation/' + setting + '/'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        mae, mse, rmse, mape, mspe = metric(preds, trues)
        print('mse:{}, mae:{}'.format(mse, mae))
        f = open(f"result_long_term_forecast.txt", 'a')
        f.write(setting + "  \n")
        f.write('mse:{}, mae:{}'.format(mse, mae))
        f.write('\n')
        f.write('\n')
        f.close()

        np.save(folder_path + 'train_metrics.npy', np.array([mae, mse, rmse, mape, mspe]))
      
        preds = []
        trues = []
        preds_with_history = []
        trues_with_history = []


        #For validation
        self.model.eval()
        with torch.no_grad():
            for i, (batch_x, batch_y, batch_x_mark, batch_y_mark) in enumerate(val_loader):
                batch_x = batch_x.float().to(self.device)
                batch_y = batch_y.float().to(self.device)
                batch_x_mark = batch_x_mark.float().to(self.device)
                batch_y_mark = batch_y_mark.float().to(self.device)

                input_seq = batch_x.detach().cpu().numpy()
                if val_data.scale and self.args.inverse:
                    shape = input_seq.shape
                    input_seq = val_data.inverse_transform(
                        input_seq.reshape(shape[0] * shape[1], -1)
                    ).reshape(shape)

                # ------------------------
                # former vs. other model families
                # ------------------------
                if "former" in self.args.model.lower():
                    # split history into encoder half + warmup half
                    hist_len = batch_x.shape[1]
                    half     = hist_len // 2

                    enc_x      = batch_x[:, :half, :]
                    enc_x_mark = batch_x_mark[:, :half, :]

                    warmup_y      = batch_x[:, half:, :]
                    warmup_y_mark = batch_x_mark[:, half:, :]

                    # padding for prediction horizon
                    if self.args.padding == 0:
                        dec_pad = torch.zeros([batch_y.shape[0], self.args.pred_len, batch_y.shape[-1]],
                                                device=self.device)
                    elif self.args.padding == 1:
                        dec_pad = torch.ones([batch_y.shape[0], self.args.pred_len, batch_y.shape[-1]],
                                                device=self.device)
                    else:
                        raise ValueError("Unknown padding option")

                    # warm-up + prediction padding
                    dec_inp = torch.cat([warmup_y, dec_pad], dim=1).float().to(self.device)

                    # forward
                    if self.args.use_amp:
                        with torch.cuda.amp.autocast():
                            outputs = self.model(enc_x, enc_x_mark, dec_inp, warmup_y_mark)
                    else:
                        outputs = self.model(enc_x, enc_x_mark, dec_inp, warmup_y_mark)

                else:
                    # decoder input for non-former models
                    dec_inp = torch.zeros_like(batch_y[:, -self.args.pred_len:, :]).float()
                    dec_inp = torch.cat([batch_y[:, :self.args.label_len, :], dec_inp],
                                        dim=1).float().to(self.device)

                    # forward (match your training branches)
                    if self.args.use_amp:
                        with torch.cuda.amp.autocast():
                            if any(k in self.args.model for k in ['Linear','TST','Beats','MLP','TCN']):
                                outputs = self.model(batch_x)
                            elif 'FITS' in self.args.model:
                                outputs, low = self.model(batch_x)
                            else:
                                outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)
                    else:
                        if any(k in self.args.model for k in ['Linear','TST','Beats','MLP','TCN']):
                            outputs = self.model(batch_x)
                        elif 'FITS' in self.args.model:
                            outputs, low = self.model(batch_x)
                        else:
                            outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)

                # ---- the rest of your pipeline stays the same
                f_dim = -1 if self.args.features == 'MS' else 0
                input_seq = input_seq[:, :, f_dim:]
                outputs = outputs[:, -self.args.pred_len:, :]
                batch_y = batch_y[:, -self.args.pred_len:, :].to(self.device)

                outputs = outputs.detach().cpu().numpy()
                batch_y = batch_y.detach().cpu().numpy()

                if val_data.scale and self.args.inverse:
                    shape = batch_y.shape
                    if outputs.shape[-1] != batch_y.shape[-1]:
                        outputs = np.tile(outputs, [1, 1, int(batch_y.shape[-1] / outputs.shape[-1])])
                    outputs = val_data.inverse_transform(outputs.reshape(shape[0] * shape[1], -1)).reshape(shape)
                    batch_y = val_data.inverse_transform(batch_y.reshape(shape[0] * shape[1], -1)).reshape(shape)

                outputs = outputs[:, :, f_dim:]
                batch_y = batch_y[:, :, f_dim:]

                pred = outputs
                true = batch_y

                # Concatenate input (history) + prediction
                pred_with_history = np.concatenate([input_seq, pred], axis=1)
                true_with_history = np.concatenate([input_seq, true], axis=1)

                preds.append(pred)
                trues.append(true)
                preds_with_history.append(pred_with_history)
                trues_with_history.append(true_with_history)

                if i % 20 == 0:
                    input = batch_x.detach().cpu().numpy()
                    if val_data.scale and self.args.inverse:
                        shape = input.shape
                        input = val_data.inverse_transform(
                            input.reshape(shape[0] * shape[1], -1)
                        ).reshape(shape)
                    gt = np.concatenate((input[0, :, -1], true[0, :, -1]), axis=0)
                    pd = np.concatenate((input[0, :, -1], pred[0, :, -1]), axis=0)
                    gt_multichannel = np.concatenate((input[0, :, :], true[0, :, :]), axis=0)
                    pd_multichannel = np.concatenate((input[0, :, :], pred[0, :, :]), axis=0)

                

        preds = np.concatenate(preds, axis=0)
        trues = np.concatenate(trues, axis=0)
     
        preds = preds.reshape(-1, preds.shape[-2], preds.shape[-1])
        trues = trues.reshape(-1, trues.shape[-2], trues.shape[-1])


         
        preds_with_history = np.concatenate(preds_with_history, axis=0)
        trues_with_history = np.concatenate(trues_with_history, axis=0)

        np.save(folder_path + 'val_pred_with_history.npy', preds_with_history)
        np.save(folder_path + 'val_true_with_history.npy', trues_with_history)

                
        print("Validation")
        print(trues.shape)
        print(preds.shape)
        print(preds_with_history.shape)
        print(trues_with_history.shape)


        # result save
        folder_path = './Train_Test_Validation/' + setting + '/'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    
        mae, mse, rmse, mape, mspe = metric(preds, trues)
        print('mse:{}, mae:{}'.format(mse, mae))
        f = open(f"result_long_term_forecast.txt", 'a')
        f.write(setting + "  \n")
        f.write('mse:{}, mae:{}'.format(mse, mae))
        f.write('\n')
        f.write('\n')
        f.close()

        np.save(folder_path + 'val_metrics.npy', np.array([mae, mse, rmse, mape, mspe]))
       
        

        #For Testing
        # Testing
        preds = []
        trues = []
        preds_with_history = []
        trues_with_history = []

        self.model.eval()
        with torch.no_grad():
            for i, (batch_x, batch_y, batch_x_mark, batch_y_mark) in enumerate(test_loader):
                batch_x      = batch_x.float().to(self.device)
                batch_y      = batch_y.float().to(self.device)
                batch_x_mark = batch_x_mark.float().to(self.device)
                batch_y_mark = batch_y_mark.float().to(self.device)

                # keep CPU copy of history for saving
                input_seq = batch_x.detach().cpu().numpy()

                # ------------------------
                # former vs other families
                # ------------------------
                if "former" in self.args.model.lower():
                    # split history: encoder half + warmup half
                    hist_len = batch_x.shape[1]
                    half     = hist_len // 2

                    enc_x      = batch_x[:, :half, :]
                    enc_x_mark = batch_x_mark[:, :half, :]

                    warmup_y      = batch_x[:, half:, :]
                    warmup_y_mark = batch_x_mark[:, half:, :]

                    # padding for prediction horizon
                    if self.args.padding == 0:
                        dec_pad = torch.zeros([batch_y.shape[0], self.args.pred_len, batch_y.shape[-1]],
                                                device=self.device)
                    elif self.args.padding == 1:
                        dec_pad = torch.ones([batch_y.shape[0], self.args.pred_len, batch_y.shape[-1]],
                                                device=self.device)
                    else:
                        raise ValueError("Unknown padding option")

                    # warm-up + prediction padding
                    dec_inp = torch.cat([warmup_y, dec_pad], dim=1).float().to(self.device)

                    # forward
                    if self.args.use_amp:
                        with torch.cuda.amp.autocast():
                            outputs = self.model(enc_x, enc_x_mark, dec_inp, warmup_y_mark)
                    else:
                        outputs = self.model(enc_x, enc_x_mark, dec_inp, warmup_y_mark)

                else:
                    # decoder input for non-former models
                    dec_inp = torch.zeros_like(batch_y[:, -self.args.pred_len:, :]).float()
                    dec_inp = torch.cat([batch_y[:, :self.args.label_len, :], dec_inp],
                                        dim=1).float().to(self.device)

                    # forward (mirror your training branches)
                    if self.args.use_amp:
                        with torch.cuda.amp.autocast():
                            if any(k in self.args.model for k in ['Linear','TST','Beats','MLP','TCN']):
                                outputs = self.model(batch_x)
                            elif 'FITS' in self.args.model:
                                outputs, low = self.model(batch_x)
                            else:
                                outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)
                    else:
                        if any(k in self.args.model for k in ['Linear','TST','Beats','MLP','TCN']):
                            outputs = self.model(batch_x)
                        elif 'FITS' in self.args.model:
                            outputs, low = self.model(batch_x)
                        else:
                            outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)

                # ---- post-processing / inverse scaling / save
                f_dim    = -1 if self.args.features == 'MS' else 0
                input_seq = input_seq[:, :, f_dim:]  # keep same channels as final outputs

                outputs = outputs[:, -self.args.pred_len:, :]
                batch_y = batch_y[:, -self.args.pred_len:, :].to(self.device)

                outputs = outputs.detach().cpu().numpy()
                batch_y = batch_y.detach().cpu().numpy()

                if test_data.scale and self.args.inverse:
                    shape = batch_y.shape
                    if outputs.shape[-1] != batch_y.shape[-1]:
                        # tile channels if needed
                        outputs = np.tile(outputs, [1, 1, int(batch_y.shape[-1] / outputs.shape[-1])])
                    outputs = test_data.inverse_transform(outputs.reshape(shape[0]*shape[1], -1)).reshape(shape)
                    batch_y = test_data.inverse_transform(batch_y.reshape(shape[0]*shape[1], -1)).reshape(shape)

                outputs = outputs[:, :, f_dim:]
                batch_y = batch_y[:, :, f_dim:]

                pred = outputs
                true = batch_y

                # Concatenate input (history) + prediction
                pred_with_history = np.concatenate([input_seq, pred], axis=1)
                true_with_history = np.concatenate([input_seq, true], axis=1)

                preds.append(pred)
                trues.append(true)
                preds_with_history.append(pred_with_history)
                trues_with_history.append(true_with_history)

                if i % 20 == 0:
                    input_vis = batch_x.detach().cpu().numpy()
                    if test_data.scale and self.args.inverse:
                        shp = input_vis.shape
                        input_vis = test_data.inverse_transform(input_vis.reshape(shp[0]*shp[1], -1)).reshape(shp)
                    gt = np.concatenate((input_vis[0, :, -1], true[0, :, -1]), axis=0)
                    pd = np.concatenate((input_vis[0, :, -1], pred[0, :, -1]), axis=0)
                    gt_multichannel = np.concatenate((input_vis[0, :, :], true[0, :, :]), axis=0)
                    pd_multichannel = np.concatenate((input_vis[0, :, :], pred[0, :, :]), axis=0)

        # stack & save
        preds = np.concatenate(preds, axis=0)
        trues = np.concatenate(trues, axis=0)

        preds = preds.reshape(-1, preds.shape[-2], preds.shape[-1])
        trues = trues.reshape(-1, trues.shape[-2], trues.shape[-1])

        preds_with_history = np.concatenate(preds_with_history, axis=0)
        trues_with_history = np.concatenate(trues_with_history, axis=0)

        np.save(folder_path + 'test_pred_with_history.npy', preds_with_history)
        np.save(folder_path + 'test_true_with_history.npy', trues_with_history)

        print("Testing")
        print(trues.shape)
        print(preds.shape)
        print(preds_with_history.shape)
        print(trues_with_history.shape)

            
        # result save
        folder_path = './Train_Test_Validation/' + setting + '/'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        
        mae, mse, rmse, mape, mspe = metric(preds, trues)
        print('mse:{}, mae:{}'.format(mse, mae))
        f = open(f"result_long_term_forecast.txt", 'a')
        f.write(setting + "  \n")
        f.write('mse:{}, mae:{}'.format(mse, mae))
        f.write('\n')
        f.write('\n')
        f.close()

        np.save(folder_path + 'test_metrics.npy', np.array([mae, mse, rmse, mape, mspe]))
        
        
        return