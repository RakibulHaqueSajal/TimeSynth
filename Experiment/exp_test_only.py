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

def normalize_tags(meta, batch_size):
    """
    Returns list[str] of length batch_size.
    Supports:
    A) meta is dict with key 'tag' -> list/np/torch
    B) meta is list of dicts [{'tag':..}, ...]
    else: unknown
    """
    tags = None

    if isinstance(meta, dict) and "tag" in meta:
        tags = to_pylist(meta["tag"])

    elif isinstance(meta, (list, tuple)) and len(meta) == batch_size:
        # list of dicts
        tags = []
        for m in meta:
            if isinstance(m, dict) and "tag" in m:
                tags.append(m["tag"])
            else:
                tags.append("unknown")

    if tags is None:
        tags = ["unknown"] * batch_size

    # ensure python strings
    out = []
    for t in tags:
        if isinstance(t, (bytes, bytearray)):
            out.append(t.decode())
        else:
            out.append(str(t))
    return out

def safe_tag_filename(tag: str) -> str:
    """Make tag safe for filenames."""
    keep = []
    for ch in tag:
        if ch.isalnum() or ch in ("-", "_", "."):
            keep.append(ch)
        else:
            keep.append("_")
    return "".join(keep)[:120]

class Exp_Long_Term_Forecast_Test_Dist(Exp_Basic):
    def __init__(self, args):
        self.input_size=None
        super(Exp_Long_Term_Forecast_Test_Dist, self).__init__(args)

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
 
    # def test(self, setting, distribution,test=0):
    #     test_data, test_loader = self._get_data(flag='test')
    #     #train_data, train_loader = self._get_data(flag='train')
    #     #val_data, val_loader = self._get_data(flag='val')
    #     if test:
    #         print('loading model')
    #         self.model.load_state_dict(torch.load(os.path.join('/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/checkpoints/' + setting, 'checkpoint.pth')))
    #         #self.model.load_state_dict(torch.load(os.path.join('/scratch_hd/Neurips/Synthetic_Data_Testing/checkpoints/' + setting, 'model_last_epoch.pth')))

    #     #For Testing
    #     # Testing
    #     preds = []
    #     trues = []
    #     preds_with_history = []
    #     trues_with_history = []

    #     self.model.eval()
    #     with torch.no_grad():
    #         for i, batch in enumerate(test_loader):
    #             if len(batch) == 5:
    #                 batch_x, batch_y, batch_x_mark, batch_y_mark, meta = batch
    #             else:
    #                 batch_x, batch_y, batch_x_mark, batch_y_mark = batch
    #                 meta = None
    #             batch_x = batch_x.float().to(self.device)
    #             batch_y = batch_y.float().to(self.device)
    #             batch_x_mark = batch_x_mark.float().to(self.device)
    #             batch_y_mark = batch_y_mark.float().to(self.device)


    #             # keep CPU copy of history for saving
    #             input_seq = batch_x.detach().cpu().numpy()

    #             # ------------------------
    #             # former vs other families
    #             # ------------------------
    #             if "former" in self.args.model.lower():
    #                 # split history: encoder half + warmup half
    #                 hist_len = batch_x.shape[1]
    #                 half     = hist_len // 2

    #                 enc_x      = batch_x[:, :half, :]
    #                 enc_x_mark = batch_x_mark[:, :half, :]

    #                 warmup_y      = batch_x[:, half:, :]
    #                 warmup_y_mark = batch_x_mark[:, half:, :]

    #                 # padding for prediction horizon
    #                 if self.args.padding == 0:
    #                     dec_pad = torch.zeros([batch_y.shape[0], self.args.pred_len, batch_y.shape[-1]],
    #                                             device=self.device)
    #                 elif self.args.padding == 1:
    #                     dec_pad = torch.ones([batch_y.shape[0], self.args.pred_len, batch_y.shape[-1]],
    #                                             device=self.device)
    #                 else:
    #                     raise ValueError("Unknown padding option")

    #                 # warm-up + prediction padding
    #                 dec_inp = torch.cat([warmup_y, dec_pad], dim=1).float().to(self.device)

    #                 # forward
    #                 if self.args.use_amp:
    #                     with torch.cuda.amp.autocast():
    #                         outputs = self.model(enc_x, enc_x_mark, dec_inp, warmup_y_mark)
    #                 else:
    #                     outputs = self.model(enc_x, enc_x_mark, dec_inp, warmup_y_mark)

    #             else:
    #                 # decoder input for non-former models
    #                 dec_inp = torch.zeros_like(batch_y[:, -self.args.pred_len:, :]).float()
    #                 dec_inp = torch.cat([batch_y[:, :self.args.label_len, :], dec_inp],
    #                                     dim=1).float().to(self.device)

    #                 # forward (mirror your training branches)
    #                 if self.args.use_amp:
    #                     with torch.cuda.amp.autocast():
    #                         if any(k in self.args.model for k in ['Linear','TST','Beats','MLP','TCN']):
    #                             outputs = self.model(batch_x)
    #                         elif 'FITS' in self.args.model:
    #                             outputs, low = self.model(batch_x)
    #                         else:
    #                             outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)
    #                 else:
    #                     if any(k in self.args.model for k in ['Linear','TST','Beats','MLP','TCN']):
    #                         outputs = self.model(batch_x)
    #                     elif 'FITS' in self.args.model:
    #                         outputs, low = self.model(batch_x)
    #                     else:
    #                         outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)

    #             # ---- post-processing / inverse scaling / save
    #             f_dim    = -1 if self.args.features == 'MS' else 0
    #             input_seq = input_seq[:, :, f_dim:]  # keep same channels as final outputs

    #             outputs = outputs[:, -self.args.pred_len:, :]
    #             batch_y = batch_y[:, -self.args.pred_len:, :].to(self.device)

    #             outputs = outputs.detach().cpu().numpy()
    #             batch_y = batch_y.detach().cpu().numpy()

    #             if test_data.scale and self.args.inverse:
    #                 shape = batch_y.shape
    #                 if outputs.shape[-1] != batch_y.shape[-1]:
    #                     # tile channels if needed
    #                     outputs = np.tile(outputs, [1, 1, int(batch_y.shape[-1] / outputs.shape[-1])])
    #                 outputs = test_data.inverse_transform(outputs.reshape(shape[0]*shape[1], -1)).reshape(shape)
    #                 batch_y = test_data.inverse_transform(batch_y.reshape(shape[0]*shape[1], -1)).reshape(shape)

    #             outputs = outputs[:, :, f_dim:]
    #             batch_y = batch_y[:, :, f_dim:]

    #             pred = outputs
    #             true = batch_y

    #             # Concatenate input (history) + prediction
    #             pred_with_history = np.concatenate([input_seq, pred], axis=1)
    #             true_with_history = np.concatenate([input_seq, true], axis=1)

    #             preds.append(pred)
    #             trues.append(true)
    #             preds_with_history.append(pred_with_history)
    #             trues_with_history.append(true_with_history)

    #             if i % 20 == 0:
    #                 input_vis = batch_x.detach().cpu().numpy()
    #                 if test_data.scale and self.args.inverse:
    #                     shp = input_vis.shape
    #                     input_vis = test_data.inverse_transform(input_vis.reshape(shp[0]*shp[1], -1)).reshape(shp)
    #                 gt = np.concatenate((input_vis[0, :, -1], true[0, :, -1]), axis=0)
    #                 pd = np.concatenate((input_vis[0, :, -1], pred[0, :, -1]), axis=0)
    #                 gt_multichannel = np.concatenate((input_vis[0, :, :], true[0, :, :]), axis=0)
    #                 pd_multichannel = np.concatenate((input_vis[0, :, :], pred[0, :, :]), axis=0)

    #     # stack & save
    #     preds = np.concatenate(preds, axis=0)
    #     trues = np.concatenate(trues, axis=0)

    #     preds = preds.reshape(-1, preds.shape[-2], preds.shape[-1])
    #     trues = trues.reshape(-1, trues.shape[-2], trues.shape[-1])

    #     preds_with_history = np.concatenate(preds_with_history, axis=0)
    #     trues_with_history = np.concatenate(trues_with_history, axis=0)

    #      # result save
    #     setting=setting+distribution
    #     folder_path = '/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/' + setting + '/'
    #     if not os.path.exists(folder_path):
    #         os.makedirs(folder_path)


    #     np.save(folder_path + 'test_pred_with_history.npy', preds_with_history)
    #     np.save(folder_path + 'test_true_with_history.npy', trues_with_history)
    #     print(folder_path)
    #     print('file_Saved')
        
    #     print(setting)
    #     print("Testing")
    #     print(trues.shape)
    #     print(preds.shape)
    #     print(preds_with_history.shape)
    #     print(trues_with_history.shape)

            
       
        
    #     mae, mse, rmse, mape, mspe = metric(preds, trues)
    #     print('mse:{}, mae:{}'.format(mse, mae))
    #     f = open(f"result_long_term_forecast.txt", 'a')
    #     f.write(setting + "  \n")
    #     f.write('mse:{}, mae:{}'.format(mse, mae))
    #     f.write('\n')
    #     f.write('\n')
    #     f.close()

    #     np.save(folder_path + 'test_metrics.npy', np.array([mae, mse, rmse, mape, mspe]))
        
        
    #     return
    def to_pylist(x):
        """Robust conversion for tags coming as list/np/torch."""
        if x is None:
            return None
        if isinstance(x, (list, tuple)):
            return list(x)
        if isinstance(x, np.ndarray):
            return x.tolist()
        if hasattr(x, "detach"):  # torch tensor
            return x.detach().cpu().tolist()
        return [x]

    def test(self, setting, distribution, test=0):
        test_data, test_loader = self._get_data(flag="test")

        # ------------------------
        # Toggle: save GT state
        # ------------------------
        SAVE_GT_STATE = bool(getattr(self.args, "save_gt_state", True))

        if test:
            print("loading model")
            self.model.load_state_dict(
                torch.load(
                    os.path.join(
                        "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/checkpoints/" + setting,
                        "checkpoint.pth",
                    )
                )
            )

        # Global collections
        preds, trues = [], []
        preds_with_history, trues_with_history = [], []

        # Only used if SAVE_GT_STATE
        true_states = []  # list of [B, H, 1]

        # Tag-wise collections (store WITH HISTORY, as you requested)
        use_tag_eval = (getattr(self.args, "data", "") == "single_test")
        tag_pred_hist = {}  # tag -> list of [1, L+H, C]
        tag_true_hist = {}  # tag -> list of [1, L+H, C]

        self.model.eval()
        with torch.no_grad():
            for i, batch in enumerate(test_loader):

                # -------------------------
                # Unpack batch (4 or 5 items)
                # -------------------------
                if isinstance(batch, (list, tuple)) and len(batch) == 5:
                    batch_x, batch_y, batch_x_mark, batch_y_mark, meta = batch
                else:
                    batch_x, batch_y, batch_x_mark, batch_y_mark = batch
                    meta = None

                # If user wants GT states, meta MUST be a tensor of states
                y_state_true = None
                if SAVE_GT_STATE:
                    if meta is None:
                        raise ValueError(
                            "save_gt_state=True but dataset did not return 5th item (y_state_true)."
                        )
                    y_state_true = meta  # expected torch.Tensor [B, something] or [B, something, 1]

                # Move tensors to device (fixes your device mismatch)
                batch_x      = batch_x.float().to(self.device)
                batch_y      = batch_y.float().to(self.device)
                batch_x_mark = batch_x_mark.float().to(self.device)
                batch_y_mark = batch_y_mark.float().to(self.device)

                if SAVE_GT_STATE:
                    # keep it on device for slicing; dtype doesn't matter much yet
                    if not torch.is_tensor(y_state_true):
                        raise TypeError(
                            f"save_gt_state=True expects meta to be a torch.Tensor, got {type(y_state_true)}"
                        )
                    y_state_true = y_state_true.to(self.device)

                # CPU history copy for saving
                input_seq = batch_x.detach().cpu().numpy()

                # ------------------------
                # Model forward (same logic you had)
                # ------------------------
                if "former" in self.args.model.lower():
                    hist_len = batch_x.shape[1]
                    half = hist_len // 2

                    enc_x      = batch_x[:, :half, :]
                    enc_x_mark = batch_x_mark[:, :half, :]

                    warmup_y      = batch_x[:, half:, :]
                    warmup_y_mark = batch_x_mark[:, half:, :]

                    if self.args.padding == 0:
                        dec_pad = torch.zeros(
                            [batch_y.shape[0], self.args.pred_len, batch_y.shape[-1]],
                            device=self.device
                        )
                    elif self.args.padding == 1:
                        dec_pad = torch.ones(
                            [batch_y.shape[0], self.args.pred_len, batch_y.shape[-1]],
                            device=self.device
                        )
                    else:
                        raise ValueError("Unknown padding option")

                    dec_inp = torch.cat([warmup_y, dec_pad], dim=1).float().to(self.device)

                    if self.args.use_amp:
                        with torch.cuda.amp.autocast():
                            outputs = self.model(enc_x, enc_x_mark, dec_inp, warmup_y_mark)
                    else:
                        outputs = self.model(enc_x, enc_x_mark, dec_inp, warmup_y_mark)

                else:
                    dec_inp = torch.zeros_like(batch_y[:, -self.args.pred_len:, :]).float()
                    dec_inp = torch.cat([batch_y[:, :self.args.label_len, :], dec_inp], dim=1).float().to(self.device)

                    if self.args.use_amp:
                        with torch.cuda.amp.autocast():
                            if any(k in self.args.model for k in ["Linear", "TST", "Beats", "MLP", "TCN"]):
                                outputs = self.model(batch_x)
                            elif "FITS" in self.args.model:
                                outputs, _low = self.model(batch_x)
                            else:
                                outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)
                    else:
                        if any(k in self.args.model for k in ["Linear", "TST", "Beats", "MLP", "TCN"]):
                            outputs = self.model(batch_x)
                        elif "FITS" in self.args.model:
                            outputs, _low = self.model(batch_x)
                        else:
                            outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)

                # ------------------------
                # Post-processing
                # ------------------------
                f_dim = -1 if self.args.features == "MS" else 0
                input_seq = input_seq[:, :, f_dim:]  # keep same channels as outputs

                outputs = outputs[:, -self.args.pred_len:, :]
                batch_y = batch_y[:, -self.args.pred_len:, :]

                # Slice GT state to forecast horizon too (only if enabled)
                if SAVE_GT_STATE:
                    # accept [B, L+H] or [B, L+H, 1] or [B, H] or [B, H, 1]
                    if y_state_true.ndim == 3:
                        y_state_h = y_state_true[:, -self.args.pred_len:, :]
                    else:
                        y_state_h = y_state_true[:, -self.args.pred_len:]
                    if y_state_h.ndim == 2:
                        y_state_h = y_state_h.unsqueeze(-1)  # [B, H, 1]

                outputs_np = outputs.detach().cpu().numpy()
                batch_y_np = batch_y.detach().cpu().numpy()

                # Avoid inverse transform for single_test (because that dataset may not define scaler/scale)
                do_inverse = (
                    (getattr(test_data, "scale", False) is True)
                    and bool(getattr(self.args, "inverse", False))
                    and (getattr(self.args, "data", "") != "single_test")
                    and hasattr(test_data, "inverse_transform")
                )

                if do_inverse:
                    shape = batch_y_np.shape
                    if outputs_np.shape[-1] != batch_y_np.shape[-1]:
                        outputs_np = np.tile(outputs_np, [1, 1, int(batch_y_np.shape[-1] / outputs_np.shape[-1])])

                    outputs_np = test_data.inverse_transform(outputs_np.reshape(shape[0] * shape[1], -1)).reshape(shape)
                    batch_y_np = test_data.inverse_transform(batch_y_np.reshape(shape[0] * shape[1], -1)).reshape(shape)

                outputs_np = outputs_np[:, :, f_dim:]
                batch_y_np = batch_y_np[:, :, f_dim:]

                pred = outputs_np
                true = batch_y_np

                pred_with_hist = np.concatenate([input_seq, pred], axis=1)
                true_with_hist = np.concatenate([input_seq, true], axis=1)

                preds.append(pred)
                trues.append(true)
                preds_with_history.append(pred_with_hist)
                trues_with_history.append(true_with_hist)

                # Save GT states (forecast horizon only)
                if SAVE_GT_STATE:
                    true_states.append(y_state_h.detach().cpu().numpy().astype(np.int64))

                # ------------------------
                # Tag-wise saving WITH HISTORY (ONLY in tag-eval mode)
                # ------------------------
                # IMPORTANT: if SAVE_GT_STATE=True, meta is a tensor, not tags.
                if (not SAVE_GT_STATE) and use_tag_eval and meta is not None:
                    tags = normalize_tags(meta, batch_size=pred.shape[0])
                    for b, tag in enumerate(tags):
                        tag_pred_hist.setdefault(tag, []).append(pred_with_hist[b:b+1])
                        tag_true_hist.setdefault(tag, []).append(true_with_hist[b:b+1])

        # ------------------------
        # Stack globals
        # ------------------------
        preds = np.concatenate(preds, axis=0).reshape(-1, preds[0].shape[-2], preds[0].shape[-1])
        trues = np.concatenate(trues, axis=0).reshape(-1, trues[0].shape[-2], trues[0].shape[-1])

        preds_with_history = np.concatenate(preds_with_history, axis=0)
        trues_with_history = np.concatenate(trues_with_history, axis=0)

        # ------------------------
        # Save outputs
        # ------------------------
        setting = setting + distribution
        folder_path = (
            "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
            + setting
            + "/"
        )
        os.makedirs(folder_path, exist_ok=True)

        np.save(os.path.join(folder_path, "test_pred_with_history.npy"), preds_with_history)
        np.save(os.path.join(folder_path, "test_true_with_history.npy"), trues_with_history)

        if SAVE_GT_STATE:
            true_states = np.concatenate(true_states, axis=0)  # [N, H, 1]
            np.save(os.path.join(folder_path, "test_true_state.npy"), true_states)
            print("Saved test_true_state.npy with shape:", true_states.shape)

        # ------------------------
        # Overall metrics (same as before)
        # ------------------------
        mae, mse, rmse, mape, mspe = metric(preds, trues)
        print(f"mse:{mse}, mae:{mae}")
        np.save(os.path.join(folder_path, "test_metrics.npy"), np.array([mae, mse, rmse, mape, mspe]))

        # ------------------------
        # Tag-wise metrics + SAVE TAG-WISE ARRAYS (WITH HISTORY)
        # (unchanged behavior when SAVE_GT_STATE is False)
        # ------------------------
        if (not SAVE_GT_STATE) and use_tag_eval and len(tag_pred_hist) > 0:
            tag_metrics = {}
            for tag in sorted(tag_pred_hist.keys()):
                P = np.concatenate(tag_pred_hist[tag], axis=0)  # [N, L+H, C]
                T = np.concatenate(tag_true_hist[tag], axis=0)

                L = self.args.seq_len
                p_h = P[:, L:, :]
                t_h = T[:, L:, :]

                mae_t, mse_t, rmse_t, mape_t, mspe_t = metric(p_h, t_h)
                tag_metrics[tag] = [mae_t, mse_t, rmse_t, mape_t, mspe_t]
                print(f"[TAG={tag}] mse={mse_t}, mae={mae_t}, n={P.shape[0]}")

                safe = safe_tag_filename(tag)
                np.save(os.path.join(folder_path, f"tag_{safe}__pred_with_history.npy"), P)
                np.save(os.path.join(folder_path, f"tag_{safe}__true_with_history.npy"), T)

            np.save(os.path.join(folder_path, "test_metrics_by_tag.npy"), tag_metrics, allow_pickle=True)

        # log
        with open("result_long_term_forecast.txt", "a") as f:
            f.write(setting + "\n")
            f.write(f"mse:{mse}, mae:{mae}\n\n")

        print(folder_path)
        print("file_Saved")
        print("Testing")
        print(trues.shape, preds.shape, preds_with_history.shape, trues_with_history.shape)
        return


    # def test(self, setting, distribution, test=0):
    #     test_data, test_loader = self._get_data(flag="test")

    #     if test:
    #         print("loading model")
    #         self.model.load_state_dict(
    #             torch.load(
    #                 os.path.join(
    #                     "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/checkpoints/" + setting,
    #                     "checkpoint.pth",
    #                 )
    #             )
    #         )

    #     # Global collections
    #     preds, trues = [], []
    #     preds_with_history, trues_with_history = [], []

    #     # Tag-wise collections (store WITH HISTORY, as you requested)
    #     use_tag_eval = (getattr(self.args, "data", "") == "single_test")
    #     tag_pred_hist = {}  # tag -> list of [1, L+H, C]
    #     tag_true_hist = {}  # tag -> list of [1, L+H, C]

    #     self.model.eval()
    #     with torch.no_grad():
    #         for i, batch in enumerate(test_loader):

    #             # -------------------------
    #             # Unpack batch (4 or 5 items)
    #             # -------------------------
    #             if isinstance(batch, (list, tuple)) and len(batch) == 5:
    #                 batch_x, batch_y, batch_x_mark, batch_y_mark, meta = batch
    #                 print(meta)
    #             else:
    #                 batch_x, batch_y, batch_x_mark, batch_y_mark = batch
    #                 meta = None

    #             # Move tensors to device (fixes your device mismatch)
    #             batch_x      = batch_x.float().to(self.device)
    #             batch_y      = batch_y.float().to(self.device)
    #             batch_x_mark = batch_x_mark.float().to(self.device)
    #             batch_y_mark = batch_y_mark.float().to(self.device)

    #             # CPU history copy for saving
    #             input_seq = batch_x.detach().cpu().numpy()

    #             # ------------------------
    #             # Model forward (same logic you had)
    #             # ------------------------
    #             if "former" in self.args.model.lower():
    #                 hist_len = batch_x.shape[1]
    #                 half = hist_len // 2

    #                 enc_x      = batch_x[:, :half, :]
    #                 enc_x_mark = batch_x_mark[:, :half, :]

    #                 warmup_y      = batch_x[:, half:, :]
    #                 warmup_y_mark = batch_x_mark[:, half:, :]

    #                 if self.args.padding == 0:
    #                     dec_pad = torch.zeros(
    #                         [batch_y.shape[0], self.args.pred_len, batch_y.shape[-1]],
    #                         device=self.device
    #                     )
    #                 elif self.args.padding == 1:
    #                     dec_pad = torch.ones(
    #                         [batch_y.shape[0], self.args.pred_len, batch_y.shape[-1]],
    #                         device=self.device
    #                     )
    #                 else:
    #                     raise ValueError("Unknown padding option")

    #                 dec_inp = torch.cat([warmup_y, dec_pad], dim=1).float().to(self.device)

    #                 if self.args.use_amp:
    #                     with torch.cuda.amp.autocast():
    #                         outputs = self.model(enc_x, enc_x_mark, dec_inp, warmup_y_mark)
    #                 else:
    #                     outputs = self.model(enc_x, enc_x_mark, dec_inp, warmup_y_mark)

    #             else:
    #                 dec_inp = torch.zeros_like(batch_y[:, -self.args.pred_len:, :]).float()
    #                 dec_inp = torch.cat([batch_y[:, :self.args.label_len, :], dec_inp], dim=1).float().to(self.device)

    #                 if self.args.use_amp:
    #                     with torch.cuda.amp.autocast():
    #                         if any(k in self.args.model for k in ["Linear", "TST", "Beats", "MLP", "TCN"]):
    #                             outputs = self.model(batch_x)
    #                         elif "FITS" in self.args.model:
    #                             outputs, _low = self.model(batch_x)
    #                         else:
    #                             outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)
    #                 else:
    #                     if any(k in self.args.model for k in ["Linear", "TST", "Beats", "MLP", "TCN"]):
    #                         outputs = self.model(batch_x)
    #                     elif "FITS" in self.args.model:
    #                         outputs, _low = self.model(batch_x)
    #                     else:
    #                         outputs = self.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)

    #             # ------------------------
    #             # Post-processing
    #             # ------------------------
    #             f_dim = -1 if self.args.features == "MS" else 0
    #             input_seq = input_seq[:, :, f_dim:]  # keep same channels as outputs

    #             outputs = outputs[:, -self.args.pred_len:, :]
    #             batch_y = batch_y[:, -self.args.pred_len:, :]

    #             outputs = outputs.detach().cpu().numpy()
    #             batch_y = batch_y.detach().cpu().numpy()

    #             # Avoid inverse transform for single_test (because that dataset may not define scaler/scale)
    #             do_inverse = (
    #                 (getattr(test_data, "scale", False) is True)
    #                 and bool(getattr(self.args, "inverse", False))
    #                 and (getattr(self.args, "data", "") != "single_test")
    #                 and hasattr(test_data, "inverse_transform")
    #             )

    #             if do_inverse:
    #                 shape = batch_y.shape
    #                 if outputs.shape[-1] != batch_y.shape[-1]:
    #                     outputs = np.tile(outputs, [1, 1, int(batch_y.shape[-1] / outputs.shape[-1])])

    #                 outputs = test_data.inverse_transform(outputs.reshape(shape[0] * shape[1], -1)).reshape(shape)
    #                 batch_y = test_data.inverse_transform(batch_y.reshape(shape[0] * shape[1], -1)).reshape(shape)

    #             outputs = outputs[:, :, f_dim:]
    #             batch_y = batch_y[:, :, f_dim:]

    #             pred = outputs
    #             true = batch_y

    #             pred_with_hist = np.concatenate([input_seq, pred], axis=1)
    #             true_with_hist = np.concatenate([input_seq, true], axis=1)

    #             preds.append(pred)
    #             trues.append(true)
    #             preds_with_history.append(pred_with_hist)
    #             trues_with_history.append(true_with_hist)

    #             # ------------------------
    #             # Tag-wise saving WITH HISTORY
    #             # ------------------------
    #             if use_tag_eval and meta is not None:
    #                 tags = normalize_tags(meta, batch_size=pred.shape[0])
    #                 for b, tag in enumerate(tags):
    #                     tag_pred_hist.setdefault(tag, []).append(pred_with_hist[b:b+1])
    #                     tag_true_hist.setdefault(tag, []).append(true_with_hist[b:b+1])

    #     # ------------------------
    #     # Stack globals
    #     # ------------------------
    #     preds = np.concatenate(preds, axis=0).reshape(-1, preds[0].shape[-2], preds[0].shape[-1])
    #     trues = np.concatenate(trues, axis=0).reshape(-1, trues[0].shape[-2], trues[0].shape[-1])

    #     preds_with_history = np.concatenate(preds_with_history, axis=0)
    #     trues_with_history = np.concatenate(trues_with_history, axis=0)

    #     # ------------------------
    #     # Save outputs
    #     # ------------------------
    #     setting = setting + distribution
    #     folder_path = (
    #         "/uufs/sci.utah.edu/projects/medvic-lab/Rakib/Time_Series/Time_Series_Forecast/Train_Test_Validation/"
    #         + setting
    #         + "/"
    #     )
    #     os.makedirs(folder_path, exist_ok=True)

    #     np.save(os.path.join(folder_path, "test_pred_with_history.npy"), preds_with_history)
    #     np.save(os.path.join(folder_path, "test_true_with_history.npy"), trues_with_history)

    #     # ------------------------
    #     # Overall metrics (same as before)
    #     # ------------------------
    #     mae, mse, rmse, mape, mspe = metric(preds, trues)
    #     print(f"mse:{mse}, mae:{mae}")
    #     np.save(os.path.join(folder_path, "test_metrics.npy"), np.array([mae, mse, rmse, mape, mspe]))

    #     # ------------------------
    #     # Tag-wise metrics + SAVE TAG-WISE ARRAYS (WITH HISTORY)
    #     # ------------------------
    #     if use_tag_eval and len(tag_pred_hist) > 0:
    #         tag_metrics = {}
    #         for tag in sorted(tag_pred_hist.keys()):
    #             P = np.concatenate(tag_pred_hist[tag], axis=0)  # [N, L+H, C]
    #             T = np.concatenate(tag_true_hist[tag], axis=0)

    #             # metrics must be on forecast horizon only -> slice off history
    #             L = self.args.seq_len
    #             p_h = P[:, L:, :]
    #             t_h = T[:, L:, :]

    #             mae_t, mse_t, rmse_t, mape_t, mspe_t = metric(p_h, t_h)
    #             tag_metrics[tag] = [mae_t, mse_t, rmse_t, mape_t, mspe_t]
    #             print(f"[TAG={tag}] mse={mse_t}, mae={mae_t}, n={P.shape[0]}")

    #             safe = safe_tag_filename(tag)
    #             np.save(os.path.join(folder_path, f"tag_{safe}__pred_with_history.npy"), P)
    #             np.save(os.path.join(folder_path, f"tag_{safe}__true_with_history.npy"), T)

    #         np.save(os.path.join(folder_path, "test_metrics_by_tag.npy"), tag_metrics, allow_pickle=True)

    #     # log
    #     with open("result_long_term_forecast.txt", "a") as f:
    #         f.write(setting + "\n")
    #         f.write(f"mse:{mse}, mae:{mae}\n\n")

    #     print(folder_path)
    #     print("file_Saved")
    #     print("Testing")
    #     print(trues.shape, preds.shape, preds_with_history.shape, trues_with_history.shape)
    #     return
