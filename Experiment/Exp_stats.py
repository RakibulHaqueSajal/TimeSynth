from Data_Loader.data_loader import data_provider
from Experiment.Exp_Basic import Exp_Basic
from utils.tools import EarlyStopping, adjust_learning_rate, visual
from utils.metrics import metric

import numpy as np
import torch
import torch.nn as nn
from torch import optim

import os
import time
import warnings
import matplotlib.pyplot as plt
from Model.Statmodels import *

warnings.filterwarnings('ignore')


class Exp_Main(Exp_Basic):
    def __init__(self, args):
        super(Exp_Main, self).__init__(args)

    def _build_model(self):
        model_dict = {
            'ARIMA': ARIMA,
            'FARIMA': FullARIMA,
            'KALMAN': Kalman3StateDrift
            # 'SARIMA': SArima,
            # 'KALMAN':KalmanForecaster,
            #'Harmonic_KALMAN':HarmonicKalmanForecaster
        }
        model = model_dict[self.args.model](self.args).float()

        return model

    def _get_data(self, flag):
        data_set, data_loader = data_provider(self.args, flag)
        return data_set, data_loader


    def test(self, setting, test=0):
        test_data, test_loader = self._get_data(flag='test')

        # Sample 10% 
        samples = max(int(self.args.sample * self.args.batch_size), 1)

        preds = []
        trues = []
        inputx = []

        # NEW: store history+prediction and history+gt
        preds_with_history = []
        trues_with_history = []

        folder_path = '/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/' + setting + '/'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # choose target dimension convention
        f_dim = -1 if self.args.features == 'MS' else 0

        with torch.no_grad():
            for i, (batch_x, batch_y, batch_x_mark, batch_y_mark) in enumerate(test_loader):
                # move to CPU numpy (stat models expect numpy)
                batch_x = batch_x.float().to(self.device).cpu().numpy()
                batch_y = batch_y.float().to(self.device).cpu().numpy()

                # subsample rows
                batch_x = batch_x[:samples]
                batch_y = batch_y[:samples]

                # history restricted to same feature dims as target
                input_seq = batch_x[:, :, f_dim:]  # [B, hist_len, C]

                # model forward: returns [B, pred_len, D]
                outputs = self.model(batch_x)

                # keep only pred_len and target dims
                outputs = outputs[:, -self.args.pred_len:, f_dim:]
                batch_y = batch_y[:, -self.args.pred_len:, f_dim:]

                pred = outputs
                true = batch_y

                # print('pred shape:', pred.shape, 'true shape:', true.shape)

                # concatenate history + prediction / gt along time dimension
                # shapes: [B, hist_len + pred_len, C]
                pred_with_history = np.concatenate([input_seq, pred], axis=1)
                true_with_history = np.concatenate([input_seq, true], axis=1)

                # print('pred_with_history shape:', pred_with_history.shape, 'true_with_history shape:', true_with_history.shape)

                preds.append(pred)
                trues.append(true)
                inputx.append(batch_x)

                preds_with_history.append(pred_with_history)
                trues_with_history.append(true_with_history)
             
                if i % 20 == 0:
                    # for visualization, just use the (possibly multi-dim) history
                    input_vis = input_seq
                    gt = np.concatenate((input_vis[0, :, -1], true[0, :, -1]), axis=0)
                    pd = np.concatenate((input_vis[0, :, -1], pred[0, :, -1]), axis=0)
                    visual(gt, pd, os.path.join(folder_path, str(i) + '.pdf'))

        preds = np.concatenate(preds, axis=0)  # [N, pred_len, C]
        trues = np.concatenate(trues, axis=0)  # [N, pred_len, C]
        inputx = np.concatenate(inputx, axis=0)

        preds_with_history = np.concatenate(preds_with_history, axis=0)  # [N, hist+pred, C]
        trues_with_history = np.concatenate(trues_with_history, axis=0)  # [N, hist+pred, C]

        folder_path = '/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/' + setting + '/'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        mae, mse, rmse, mape, mspe= metric(preds, trues)
        corr = []
        print('mse:{}, mae:{}'.format(mse, mae))
        f = open("result.txt", 'a')
        f.write(setting + "  \n")
        f.write('mse:{}, mae:{}'.format(mse, mae))
        f.write('\n')
        f.write('\n')
        f.close()

        # save metrics and arrays
        np.save(folder_path + 'metrics.npy', np.array([mae, mse, rmse, mape, mspe]))
        np.save(folder_path + 'pred.npy', preds)
        np.save(folder_path + 'true.npy', trues)

        # NEW: save history+prediction / history+gt
        np.save(folder_path + 'pred_with_history.npy', preds_with_history)
        np.save(folder_path + 'true_with_history.npy', trues_with_history)

        # if you ever need the raw history alone:
        # np.save(folder_path + 'x.npy', inputx)

        return
