

import torch
import torch.nn as nn 
import math

import pysdtw
import numpy as np

dtw = pysdtw.SoftDTW(gamma=1.0,use_cuda=False)  # gamma controls smoothness

def ncc_loss(pred: torch.Tensor, target: torch.Tensor, eps: float = 1e-6) -> torch.Tensor:
    """
    Normalized Cross‐Correlation Loss supporting:
      - 2D inputs of shape (B, T)
      - 3D inputs of shape (B, T, C)

    Returns a scalar loss = mean_{batch,channel}(1 - NCC).
    """
    if pred.dim() == 2:
        # (B, T)
        # zero‐center along time axis
        pred0   = pred   - pred.mean(dim=1, keepdim=True)
        target0 = target - target.mean(dim=1, keepdim=True)

        # numerator & denominator per sample
        num   = (pred0 * target0).sum(dim=1)  # (B,)
        denom = torch.sqrt((pred0**2).sum(dim=1) *
                           (target0**2).sum(dim=1) + eps)  # (B,)

        ncc = num / (denom + eps)             # (B,)
        loss = 1.0 - ncc
        return loss.mean()

    elif pred.dim() == 3:
        # (B, T, C)
        # zero‐center along time axis (dim=1)
        pred0   = pred   - pred.mean(dim=1, keepdim=True)
        target0 = target - target.mean(dim=1, keepdim=True)

        # numerator & denominator per sample per channel
        # summing over time axis
        num   = (pred0 * target0).sum(dim=1)    # (B, C)
        denom = torch.sqrt((pred0**2).sum(dim=1) *
                           (target0**2).sum(dim=1) + eps)  # (B, C)

        ncc = num / (denom + eps)               # (B, C)
        loss = 1.0 - ncc                        # (B, C)
        return loss.mean()

    else:
        raise ValueError(f"ncc_loss expects 2D or 3D input, got shape {pred.shape}")

def mse_loss(pred, target):
    return torch.mean((pred - target) ** 2)

def frequency_loss(pred, target):
    pred_fft = torch.fft.rfft(pred, dim=-1)
    target_fft = torch.fft.rfft(target, dim=-1)
    return torch.mean(torch.abs(torch.abs(pred_fft) - torch.abs(target_fft)))

def total_variation_loss(x):
    return torch.mean(torch.abs(x[:, 1:] - x[:, :-1]))

def hybrid_loss(pred, target, alpha=1.0, beta=0.5, gamma=0.2):
    loss_mse = mse_loss(pred, target)
    loss_dtw = dtw(pred.cpu(), target.cpu())  # or soft-dtw module

    #convert loss_dtw to tensor
    loss_dtw = torch.tensor(loss_dtw, dtype=torch.float32).to(device='cuda')
    loss_dtw = torch.mean(loss_dtw)
    loss_freq = frequency_loss(pred, target)
    
    return alpha * loss_mse + beta * loss_dtw + gamma * loss_freq

class GaussianNLLLearnable(nn.Module):
    def __init__(self, reduction='mean', eps=1e-6, full=True):
        """
        Gaussian Negative Log Likelihood Loss with learnable variance.
        Args:
            reduction: 'none', 'mean', or 'sum'
            eps: small constant for numerical stability
            full: if True, includes the constant term 0.5*log(2*pi)
        """
        super(GaussianNLLLearnable, self).__init__()
        self.reduction = reduction
        self.eps = eps
        self.full = full

    def forward(self, pred_mean, pred_log_var, target):
        # Convert predicted log variance to variance (ensuring positivity)
        pred_var = torch.exp(pred_log_var) + self.eps
        
        # Compute the per-sample loss
        loss = 0.5 * pred_log_var + (target - pred_mean)**2 / (2 * pred_var)
        if self.full:
            loss = loss + 0.5 * math.log(2 * math.pi)
        
        if self.reduction == 'mean':
            loss = loss.mean()
        elif self.reduction == 'sum':
            loss = loss.sum()
            
        return loss