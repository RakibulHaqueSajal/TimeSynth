import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class Model(nn.Module):

    # FITS: Frequency Interpolation Time Series Forecasting

    def __init__(self, configs):
        super(Model, self).__init__()
        self.seq_len = configs.seq_len
        self.pred_len = configs.pred_len
        self.individual = configs.individual
        self.channels = configs.enc_in

        self.dominance_freq=configs.cut_freq # 720/24
        self.length_ratio = (self.seq_len + self.pred_len)/self.seq_len

        if self.individual:
            self.freq_upsampler = nn.ModuleList()
            for i in range(self.channels):
                self.freq_upsampler.append(
                    nn.Linear(
                        self.dominance_freq,
                        int(self.dominance_freq * self.length_ratio)
                    )
                )
        else:
            self.freq_upsampler = nn.Linear(
                self.dominance_freq,
                int(self.dominance_freq * self.length_ratio)
            )

    def forward(self, x):
        # RIN
        x_mean = torch.mean(x, dim=1, keepdim=True)
        x = x - x_mean
        x_var=torch.var(x, dim=1, keepdim=True)+ 1e-5
        # print(x_var)
        x = x / torch.sqrt(x_var)

        low_specx = torch.fft.rfft(x, dim=1)
        low_specx[:,self.dominance_freq:]=0 # LPF
        low_specx = low_specx[:,0:self.dominance_freq,:] # LPF
        # print(low_specx.permute(0,2,1))
        real = low_specx.real
        imag = low_specx.imag

        if self.individual:
            up_real = torch.zeros([low_specx.size(0), int(self.dominance_freq * self.length_ratio), low_specx.size(2)], device=low_specx.device)
            up_imag = torch.zeros_like(up_real)
            for i in range(self.channels):
                up_real[:, :, i] = self.freq_upsampler[i](real[:, :, i])
                up_imag[:, :, i] = self.freq_upsampler[i](imag[:, :, i])
            low_specxy_ = torch.complex(up_real, up_imag)
        else:
            up_real = self.freq_upsampler(real.permute(0, 2, 1)).permute(0, 2, 1)
            up_imag = self.freq_upsampler(imag.permute(0, 2, 1)).permute(0, 2, 1)
            low_specxy_ = torch.complex(up_real, up_imag)

        low_specxy = torch.zeros([low_specxy_.size(0),int((self.seq_len+self.pred_len)/2+1),low_specxy_.size(2)],dtype=low_specxy_.dtype).to(low_specxy_.device)
        low_specxy[:,0:low_specxy_.size(1),:]=low_specxy_ # zero padding
        low_xy=torch.fft.irfft(low_specxy, dim=1)
        low_xy=low_xy * self.length_ratio # energy compemsation for the length change
        # dom_x=x-low_x
        
        # dom_xy=self.Dlinear(dom_x)
        # xy=(low_xy+dom_xy) * torch.sqrt(x_var) +x_mean # REVERSE RIN
        xy=(low_xy) * torch.sqrt(x_var) +x_mean
        return xy, low_xy* torch.sqrt(x_var)
