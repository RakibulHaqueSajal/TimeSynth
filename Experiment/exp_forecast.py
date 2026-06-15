import comet_ml
from comet_ml import start, ExperimentConfig
from Data_Loader.data_loader import data_provider
from Experiment.Exp_Basic import Exp_Basic
from utils.tools import EarlyStopping, adjust_learning_rate, visual,visual_multivariate_error_distribution,visual_multichannel,visual_relative_error_distribution,compute_model_weight_norm
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
from utils.loss import hybrid_loss,ncc_loss


disable_flag=True

disable_comet = ExperimentConfig(disabled=disable_flag)
#Setting Comment Experiments
experiment = start(
  api_key="Vr3vky03wyHWTXJTZ6phb4zEF",
  project_name="Noise_Experiments",
  workspace="time-series",
  experiment_config=disable_comet
)

warnings.filterwarnings('ignore')


class Exp_Long_Term_Forecast(Exp_Basic):
    def __init__(self, args):
        self.input_size=None
        super(Exp_Long_Term_Forecast, self).__init__(args)

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
        model_optim = optim.AdamW(self.model.parameters(), lr=self.args.learning_rate, weight_decay=self.args.weight_decay)
        #model_optim=optim.SGD(self.model.parameters(),lr=self.args.learning_rate,momentum=0.9,weight_decay=self.args.weight_decay)
        return model_optim

    def _select_criterion(self):
        criterion = nn.MSELoss()
       #criterion = hybrid_loss
        #criterion=ncc_loss
        return criterion
 

    def vali(self, vali_data, vali_loader, criterion):
        total_loss = []
        self.model.eval()
        with torch.no_grad():
            for i, (batch_x, batch_y, batch_x_mark, batch_y_mark) in enumerate(vali_loader):
                batch_x = batch_x.float().to(self.device)
                batch_y = batch_y.float()
                batch_x_mark = batch_x_mark.float().to(self.device)
                batch_y_mark = batch_y_mark.float().to(self.device)

                # ==============================
                # Decoder input construction
                # ==============================
                if "former" in self.args.model.lower():
                    # --- split history into encoder/decoder halves ---
                    hist_len = batch_x.shape[1]
                    half = hist_len // 2

                    enc_x = batch_x[:, :half, :]
                    enc_x_mark = batch_x_mark[:, :half, :]

                    warmup_y = batch_x[:, half:, :]
                    warmup_y_mark = batch_x_mark[:, half:, :]

                    dec_pad = torch.zeros([batch_y.shape[0], self.args.pred_len, batch_y.shape[-1]], 
                                            device=self.device)
                    dec_inp = torch.cat([warmup_y, dec_pad], dim=1).float().to(self.device)

                else:
                    # --- default case ---
                    dec_inp = torch.zeros_like(batch_y[:, -self.args.pred_len:, :]).float()
                    dec_inp = torch.cat([batch_y[:, :self.args.label_len, :], dec_inp], dim=1).float().to(self.device)
                    enc_x, enc_x_mark = batch_x, batch_x_mark
                    warmup_y_mark = batch_y_mark

                # ==============================
                # Forward pass
                # ==============================
                if self.args.use_amp:
                    with torch.cuda.amp.autocast():
                        if any(k in self.args.model for k in ["Linear", "TST", "Beats", "MLP", "TCN"]):
                            outputs = self.model(batch_x)
                        elif "FITS" in self.args.model:
                            outputs, low = self.model(batch_x)
                        elif self.args.model == "PathFormer":
                            outputs, balance_loss = self.model(batch_x)
                        elif "former" in self.args.model.lower():
                            outputs = self.model(enc_x, enc_x_mark, dec_inp, warmup_y_mark)
                        else:
                            outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)
                else:
                    if any(k in self.args.model for k in ["Linear", "TST", "Beats", "MLP", "TCN"]):
                        outputs = self.model(batch_x)
                    elif self.args.model == "PathFormer":
                        outputs, balance_loss = self.model(batch_x)
                    elif "FITS" in self.args.model:
                        outputs, low = self.model(batch_x)
                    elif "former" in self.args.model.lower():
                        outputs = self.model(enc_x, enc_x_mark, dec_inp, warmup_y_mark)
                    else:
                        outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)

                # ==============================
                # Loss computation
                # ==============================
                f_dim = -1 if self.args.features == "MS" else 0
                outputs = outputs[:, -self.args.pred_len:, f_dim:]
                batch_y = batch_y[:, -self.args.pred_len:, f_dim:].to(self.device)

                pred = outputs.detach().cpu()
                true = batch_y.detach().cpu()
                loss = criterion(pred, true)
                total_loss.append(loss.item())

        avg_loss = np.average(total_loss)
        self.model.train()
        return avg_loss


  # You can expose this as an argument (args.l1_lambda) too

    def train(self, setting):
        experiment.set_name(f"{setting}")
        experiment.log_parameters(vars(self.args))

        train_data, train_loader = self._get_data(flag='train')
        vali_data, vali_loader = self._get_data(flag='val')
        test_data, test_loader = self._get_data(flag='test')

        path = os.path.join(self.args.checkpoints, setting)
        if not os.path.exists(path):
            os.makedirs(path)

        time_now = time.time()

        train_steps = len(train_loader)
        early_stopping = EarlyStopping(patience=self.args.patience, verbose=True)

        model_optim = self._select_optimizer()
        criterion = self._select_criterion()
        print(train_steps)
        scheduler = lr_scheduler.OneCycleLR(optimizer = model_optim,
                                            steps_per_epoch = train_steps,
                                            pct_start = self.args.pct_start,
                                            epochs = self.args.train_epochs,
                                            max_lr = self.args.learning_rate)

        if self.args.use_amp:
            scaler = torch.cuda.amp.GradScaler()

        for epoch in range(self.args.train_epochs):
            iter_count = 0
            train_loss = []

            self.model.train()
            epoch_time = time.time()
            for i, (batch_x, batch_y, batch_x_mark, batch_y_mark) in enumerate(train_loader):
                iter_count += 1
                model_optim.zero_grad()
                batch_x = batch_x.float().to(self.device)
                batch_y = batch_y.float().to(self.device)
                self.input_size=batch_x.shape
                batch_x_mark = batch_x_mark.float().to(self.device)
                batch_y_mark = batch_y_mark.float().to(self.device)
                
                if "former" in self.args.model.lower():
                    # split history into two halves
                    hist_len = batch_x.shape[1]
                    half = hist_len // 2

                    # first half for encoder
                    enc_x = batch_x[:, :half, :]
                    enc_x_mark = batch_x_mark[:, :half, :]

                    # second half for decoder warm-up
                    warmup_y = batch_x[:, half:, :]
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

                    # run model
                    if self.args.use_amp:
                        with torch.cuda.amp.autocast():
                            outputs = self.model(enc_x, enc_x_mark, dec_inp, warmup_y_mark)
                    else:
                        #import pdb; pdb.set_trace()
                        outputs = self.model(enc_x, enc_x_mark, dec_inp, warmup_y_mark)
                        
                else:
                    # decoder input
                    if self.args.padding==0:
                       dec_inp = torch.zeros([batch_y.shape[0], self.args.pred_len, batch_y.shape[-1]]).float().to(self.device)
                    elif self.args.padding==1:
                       dec_inp = torch.ones([batch_y.shape[0], self.args.pred_len, batch_y.shape[-1]]).float().to(self.device)

                    dec_inp = torch.cat([batch_y[:,:self.args.label_len,:], dec_inp], dim=1).float().to(self.device)

                    # encoder - decoder
                    if self.args.use_amp:
                        with torch.cuda.amp.autocast():
                            if 'Linear' in self.args.model or 'TST' in self.args.model or 'Beats' in self.args.model or 'MLP' in self.args.model or 'TCN' in self.args.model:
                                outputs = self.model(batch_x)
                            elif self.args.model=='PathFormer':
                                outputs, balance_loss = self.model(batch_x)
                            elif 'FITS' in self.args.model:
                                outputs,low=self.model(batch_x)
                            else :
                                outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)
                    else:
                        if 'Linear' in self.args.model or 'TST' in self.args.model or 'Beats' in self.args.model or 'MLP' in self.args.model or 'TCN' in self.args.model:
                            outputs = self.model(batch_x)
                        elif self.args.model=='PathFormer':
                            outputs, balance_loss = self.model(batch_x)
                        elif 'FITS' in self.args.model:
                            outputs,low=self.model(batch_x)
                        else:
                            outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)


                f_dim = -1 if self.args.features == 'MS' else 0
                outputs = outputs[:, -self.args.pred_len:, f_dim:]
                batch_y = batch_y[:, -self.args.pred_len:, f_dim:].to(self.device)
                loss = criterion(outputs, batch_y)
                train_loss.append(loss.item())

                if (i + 1) % 100 == 0:
                    print("\titers: {0}, epoch: {1} | loss: {2:.7f}".format(i + 1, epoch + 1, loss.item()))

                    speed = (time.time() - time_now) / iter_count
                    left_time = speed * ((self.args.train_epochs - epoch) * train_steps - i)
                    print('\tspeed: {:.4f}s/iter; left time: {:.4f}s'.format(speed, left_time))
                    iter_count = 0
                    time_now = time.time()

                if self.args.use_amp:
                    scaler.scale(loss).backward()
                    scaler.step(model_optim)
                    scaler.update()
                else:
                    loss.backward()
                    model_optim.step()
                
                if self.args.lradj == 'TST':
                    adjust_learning_rate(model_optim, scheduler, epoch + 1, self.args)
                    scheduler.step()

            print("Epoch: {} cost time: {}".format(epoch + 1, time.time() - epoch_time))
            train_loss = np.average(train_loss)
            vali_loss = self.vali(vali_data, vali_loader, criterion)
            test_loss = self.vali(test_data, test_loader, criterion)
           # weight_norm = compute_model_weight_norm(self.model)
            #print(f"Epoch {epoch}: Weight Norm = {weight_norm:.4f}")
           # experiment.log_metric("Weight_Norm",weight_norm,epoch=epoch)
            print("Epoch: {0}, Steps: {1} | Train Loss: {2:.7f} Vali Loss: {3:.7f} ".format(
                epoch + 1, train_steps, train_loss, vali_loss))
            #print("Epoch: {0}, Steps: {1} | Train Loss: {2:.7f} Vali Loss: {3:.7f} Test Loss: {4:.7f}".format(
               # epoch + 1, train_steps, train_loss, vali_loss, test_loss))
            experiment.log_metric("Training_Loss", train_loss.item(),epoch=epoch)
            experiment.log_metric("Validation_Loss", vali_loss.item(),epoch=epoch)
            experiment.log_metric("Test_Loss",test_loss.item(),epoch=epoch)
            #experiment.log_metric("Test_Loss",test_loss.item(),epoch=epoch)
            early_stopping(vali_loss, self.model, path)
            if early_stopping.early_stop:
                print("Early stopping")
                break

            if self.args.lradj != 'TST':
                adjust_learning_rate(model_optim, scheduler, epoch + 1, self.args)
            

        best_model_path = path + '/' + 'checkpoint.pth'
        self.model.load_state_dict(torch.load(best_model_path))
        

        last_epoch_model_path = os.path.join(path, 'model_last_epoch.pth')
        torch.save(self.model.state_dict(), last_epoch_model_path)
        print(f"Saved last epoch model to {last_epoch_model_path}")
        return self.model
    

    def plot_model_structure(self,expand_nested=True, save_path=None,device='cuda'):
  
        # Generate model visualization
        model_graph = draw_graph(self.model, input_size=self.input_size, expand_nested=expand_nested, device=device)
        
        # Render the visualization
        if save_path:
            os.makedirs(save_path, exist_ok=True)  # Create directory if it doesn't exist
            file_path = os.path.join(save_path, 'model_visualization')
            model_graph.visual_graph.render(file_path, format='png')
            print(f"Model visualization saved at {file_path}.png")
        else:
            # Display the plot
            model_graph.visual_graph.view()

    def test(self, setting, test=0):
        test_data, test_loader = self._get_data(flag='test')
        if test:
            print('loading model')
            self.model.load_state_dict(
                torch.load(os.path.join('/scratch_hd/Long_Time_Series_Forecasting/checkpoints/' + setting, 'checkpoint.pth'))
            )

        preds, trues = [], []
        print(setting)
        folder_path = './Changing_F1_Mod/' + setting + '/'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        self.model.eval()
        with torch.no_grad():
            for i, (batch_x, batch_y, batch_x_mark, batch_y_mark) in enumerate(test_loader):
                batch_x = batch_x.float().to(self.device)
                batch_y = batch_y.float().to(self.device)
                batch_x_mark = batch_x_mark.float().to(self.device)
                batch_y_mark = batch_y_mark.float().to(self.device)

                # --------------------------
                # Build decoder input
                # --------------------------
                if "former" in self.args.model.lower():
                    # Split history into halves: first half -> encoder, second half -> warm-up
                    hist_len = batch_x.shape[1]
                    half = hist_len // 2

                    enc_x = batch_x[:, :half, :]
                    enc_x_mark = batch_x_mark[:, :half, :]

                    warmup_y = batch_x[:, half:, :]
                    warmup_y_mark = batch_x_mark[:, half:, :]

                    dec_pad = torch.zeros([batch_y.shape[0], self.args.pred_len, batch_y.shape[-1]],
                                        device=self.device, dtype=torch.float32)
                    dec_inp = torch.cat([warmup_y, dec_pad], dim=1)

                    # Forward pass
                    if self.args.use_amp:
                        with torch.cuda.amp.autocast():
                            outputs = self.model(enc_x, enc_x_mark, dec_inp, warmup_y_mark)
                    else:
                        outputs = self.model(enc_x, enc_x_mark, dec_inp, warmup_y_mark)

                else:
                    # Default: use label_len from batch_y as warm-up
                    dec_inp = torch.zeros_like(batch_y[:, -self.args.pred_len:, :]).float()
                    dec_inp = torch.cat([batch_y[:, :self.args.label_len, :], dec_inp], dim=1).float().to(self.device)

                    if self.args.use_amp:
                        with torch.cuda.amp.autocast():
                            if any(k in self.args.model for k in ['Linear', 'TST', 'Beats', 'MLP', 'TCN']):
                                outputs = self.model(batch_x)
                            elif self.args.model == 'PathFormer':
                                outputs, balance_loss = self.model(batch_x)
                            elif 'FITS' in self.args.model:
                                outputs, low = self.model(batch_x)
                            else:
                                outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)
                    else:
                        if any(k in self.args.model for k in ['Linear', 'TST', 'Beats', 'MLP', 'TCN']):
                            outputs = self.model(batch_x)
                        elif self.args.model == 'PathFormer':
                            outputs, balance_loss = self.model(batch_x)
                        elif 'FITS' in self.args.model:
                            outputs, low = self.model(batch_x)
                        else:
                            outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)

                # --------------------------
                # Slice to prediction window
                # --------------------------
                f_dim = -1 if self.args.features == 'MS' else 0
                outputs = outputs[:, -self.args.pred_len:, :]  # keep all channels for inverse, slice f_dim later
                tgt_y = batch_y[:, -self.args.pred_len:, :].to(self.device)

                # --------------------------
                # Move to CPU/NumPy
                # --------------------------
                outputs = outputs.detach().cpu().numpy()
                tgt_y = tgt_y.detach().cpu().numpy()

                # --------------------------
                # Optional inverse transform
                # --------------------------
                if test_data.scale and self.args.inverse:
                    shape = tgt_y.shape
                    if outputs.shape[-1] != tgt_y.shape[-1]:
                        # tile to match multivariate dim if needed
                        outputs = np.tile(outputs, [1, 1, int(tgt_y.shape[-1] / outputs.shape[-1])])
                    outputs = test_data.inverse_transform(outputs.reshape(shape[0] * shape[1], -1)).reshape(shape)
                    tgt_y = test_data.inverse_transform(tgt_y.reshape(shape[0] * shape[1], -1)).reshape(shape)

                # --------------------------
                # Channel selection after inverse
                # --------------------------
                outputs = outputs[:, :, f_dim:]
                tgt_y = tgt_y[:, :, f_dim:]

                preds.append(outputs)
                trues.append(tgt_y)

                # --------------------------
                # Visualization every 20 iters
                # --------------------------
                if i % 20 == 0:
                    raw_input_np = batch_x.detach().cpu().numpy()
                    if test_data.scale and self.args.inverse:
                        shape_in = raw_input_np.shape
                        raw_input_np = test_data.inverse_transform(
                            raw_input_np.reshape(shape_in[0] * shape_in[1], -1)
                        ).reshape(shape_in)

                    # Single-channel concat for quick glance
                    gt = np.concatenate((raw_input_np[0, :, -1], tgt_y[0, :, -1]), axis=0)
                    pd = np.concatenate((raw_input_np[0, :, -1], outputs[0, :, -1]), axis=0)

                    # Multichannel concat
                    gt_multichannel = np.concatenate((raw_input_np[0, :, :], tgt_y[0, :, :]), axis=0)
                    pd_multichannel = np.concatenate((raw_input_np[0, :, :], outputs[0, :, :]), axis=0)

                    if 'traffic' in self.args.model_id or 'electricity' in self.args.model_id:
                        print("too many channels")
                    else:
                        visual_multichannel(
                            gt_multichannel, pd_multichannel,
                            os.path.join(folder_path, f"{i}_Multivariate_plot.pdf")
                        )

        # --------------------------
        # Stack & reshape for metrics
        # --------------------------
        preds = np.concatenate(preds, axis=0)
        trues = np.concatenate(trues, axis=0)

        preds = preds.reshape(-1, preds.shape[-2], preds.shape[-1])
        trues = trues.reshape(-1, trues.shape[-2], trues.shape[-1])

        # Error visualizations
        visual_multivariate_error_distribution(trues, preds, os.path.join(folder_path, "Error.pdf"))
        visual_relative_error_distribution(trues, preds, os.path.join(folder_path, "Relative.pdf"))
        print(trues.shape)
        print(preds.shape)

        # --------------------------
        # Metrics & (optional) DTW
        # --------------------------
        if self.args.use_dtw:
            dtw_list = []
            manhattan_distance = lambda x, y: np.abs(x - y)
            for i in range(preds.shape[0]):
                x = preds[i].reshape(-1, 1)
                y = trues[i].reshape(-1, 1)
                if i % 100 == 0:
                    print("calculating dtw iter:", i)
                d, _, _, _ = accelerated_dtw(x, y, dist=manhattan_distance)
                dtw_list.append(d)
            dtw = np.array(dtw_list).mean()
        else:
            dtw = 'Not calculated'

        mae, mse, rmse, mape, mspe = metric(preds, trues)
        print('mse:{}, mae:{}, dtw:{}'.format(mse, mae, dtw))

        with open("result_long_term_forecast.txt", 'a') as f:
            f.write(setting + "  \n")
            f.write('mse:{}, mae:{}, dtw:{}'.format(mse, mae, dtw))
            f.write('\n\n')

        np.save(os.path.join(folder_path, 'metrics.npy'), np.array([mae, mse, rmse, mape, mspe]))
        np.save(os.path.join(folder_path, 'pred.npy'), preds)
        np.save(os.path.join(folder_path, 'true.npy'), trues)

        return
