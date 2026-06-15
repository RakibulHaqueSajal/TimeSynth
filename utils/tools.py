import os

import numpy as np
import torch
import matplotlib.pyplot as plt
import pandas as pd
import math
import seaborn as sns

plt.switch_backend('agg')

def compute_model_weight_norm(model):
    total_norm = 0.0
    for param in model.parameters():
        if param.requires_grad:
            total_norm += param.data.norm(2).item() ** 2
    return total_norm ** 0.5

def adjust_learning_rate(optimizer,scheduler,epoch, args):
    # lr = args.learning_rate * (0.2 ** (epoch // 2))
    if args.lradj == 'type1':
        lr_adjust = {epoch: args.learning_rate * (0.5 ** ((epoch - 1) // 1))}
    elif args.lradj == 'type2':
        lr_adjust = {
            2: 5e-5, 4: 1e-5, 6: 5e-6, 8: 1e-6,
            10: 5e-7, 15: 1e-7, 20: 5e-8
        }
    elif args.lradj == 'type3':
        lr_adjust = {epoch: args.learning_rate if epoch < 3 else args.learning_rate * (0.9 ** ((epoch - 3) // 1))}
    elif args.lradj == 'constant':
        lr_adjust = {epoch: args.learning_rate}
    elif args.lradj == "cosine":
        lr_adjust = {epoch: args.learning_rate /2 * (1 + math.cos(epoch / args.train_epochs * math.pi))}
    elif args.lradj == 'TST':
        lr_adjust = {epoch: scheduler.get_last_lr()[0]}
    if epoch in lr_adjust.keys():
        lr = lr_adjust[epoch]
        for param_group in optimizer.param_groups:
            param_group['lr'] = lr
       # print('Updating learning rate to {}'.format(lr))


class EarlyStopping:
    def __init__(self, patience=7, verbose=False, delta=0):
        self.patience = patience
        self.verbose = verbose
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.val_loss_min = np.Inf
        self.delta = delta

    def __call__(self, val_loss, model, path):
        score = -val_loss
        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(val_loss, model, path)
        elif score < self.best_score + self.delta:
            self.counter += 1
            print(f'EarlyStopping counter: {self.counter} out of {self.patience}')
            if self.counter >= self.patience:
                self.early_stop = True
        else:
            self.best_score = score
            self.save_checkpoint(val_loss, model, path)
            self.counter = 0

    def save_checkpoint(self, val_loss, model, path):
        if self.verbose:
            print(f'Validation loss decreased ({self.val_loss_min:.6f} --> {val_loss:.6f}).  Saving model ...')
        torch.save(model.state_dict(), path + '/' + 'checkpoint.pth')
        self.val_loss_min = val_loss


class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class StandardScaler():
    def __init__(self, mean, std):
        self.mean = mean
        self.std = std

    def transform(self, data):
        return (data - self.mean) / self.std

    def inverse_transform(self, data):
        return (data * self.std) + self.mean


def visual_multivariate_error_distribution(true_series, pred_series, name='./pic/multivariate_error_boxplot.pdf'):
    """
    Boxplot of absolute errors across all variables.
    """

    errors = np.mean((true_series - pred_series) ** 2, axis=1)# Mean error per variable across all samples
 
    errors_flatten=np.mean(errors,axis=1)
  
    plt.figure(figsize=(5, 2))
    sns.boxplot(data=errors_flatten)
    plt.title('Error Distribution Across Variables')
    plt.xlabel('Variable Index')
    plt.ylabel('RMSE Error')
    plt.ylim(0,10)
    plt.savefig(name, bbox_inches='tight')

def visual_relative_error_distribution(true_series, pred_series, name='./pic/relative_error_boxplot.pdf'):
    """
    Boxplot of relative errors across all variables.
    """
    # Calculate channel-wise relative error using the formula (true - pred) / true
    # Calculate relative error for each channel
    channelwise_errors = np.mean((np.abs((true_series - pred_series)) / np.abs(true_series)), axis=1)  # Shape: (10784, 7)
    
   
    # Average the relative errors across channels
    average_errors = np.mean(channelwise_errors, axis=1)  # Shape: (10784,)

    # Plotting the boxplot
    plt.figure(figsize=(5,2))
    sns.boxplot(data=average_errors)
    plt.title('Average Relative Error Distribution Across Samples')
    plt.xlabel('Sample Index')
    plt.ylabel('Average Relative Error')
    plt.ylim(0, 10)
    plt.savefig(name, bbox_inches='tight')
    plt.show()


def visual(true, preds=None, name='./pic/test.pdf'):
    """
    Results visualization
    """

    plt.figure()
    plt.plot(true, label='GroundTruth', linewidth=2)
    plt.ylim(-5,5)
    if preds is not None:
        plt.plot(preds, label='Prediction', linewidth=2)
        plt.ylim(-5,5)
    plt.legend()
    plt.savefig(name, bbox_inches='tight')

def visual_multichannel(true, preds=None, name='./pic/test_multichannel.pdf'):
    """
    Results visualization for multiple channels.
    
    Parameters:
    - true: numpy array of shape (timesteps, channels), ground truth values
    - preds: numpy array of shape (timesteps, channels), predicted values (optional)
    - name: path to save the figure
    """
    num_channels = true.shape[-1]  # Number of channels
    plt.figure(figsize=(30, 3 * num_channels))  # Adjust figure size based on channels
     
    for ch in range(num_channels):
        plt.subplot(num_channels, 1, ch + 1)  # Create a separate subplot for each channel
        plt.plot(true[:, ch], label=f'GroundTruth - Channel {ch+1}', linewidth=3, color='blue')
        plt.plot(preds[:, ch], label=f'Prediction - Channel {ch+1}', linewidth=3, color='red')
        plt.ylim(-1.5,4)
       #plt.ylim(min(true[:, ch].min(), preds[:, ch].min()) - 0.5, max(true[:, ch].max(), preds[:, ch].max()) + 0.5)
        plt.legend()
        plt.title(f'Channel {ch+1}')
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(name), exist_ok=True)  # Ensure the directory exists
    plt.savefig(name, bbox_inches='tight')
    plt.show()

# Example

def adjustment(gt, pred):
    anomaly_state = False
    for i in range(len(gt)):
        if gt[i] == 1 and pred[i] == 1 and not anomaly_state:
            anomaly_state = True
            for j in range(i, 0, -1):
                if gt[j] == 0:
                    break
                else:
                    if pred[j] == 0:
                        pred[j] = 1
            for j in range(i, len(gt)):
                if gt[j] == 0:
                    break
                else:
                    if pred[j] == 0:
                        pred[j] = 1
        elif gt[i] == 0:
            anomaly_state = False
        if anomaly_state:
            pred[i] = 1
    return gt, pred


def cal_accuracy(y_pred, y_true):
    return np.mean(y_pred == y_true)