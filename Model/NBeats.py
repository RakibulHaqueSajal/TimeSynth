import torch
import torch.nn as nn
import numpy as np

# ----------- Basis Functions -----------

class GenericBasis(nn.Module):
    def __init__(self, backcast_size, forecast_size):
        super().__init__()
        self.backcast_size = backcast_size
        self.forecast_size = forecast_size

    def forward(self, theta):
        return theta[:, :self.backcast_size], theta[:, -self.forecast_size:]


class TrendBasis(nn.Module):
    def __init__(self, degree, backcast_size, forecast_size):
        super().__init__()
        self.p = degree + 1
        t_b = np.stack([np.power(np.arange(backcast_size) / backcast_size, i) for i in range(self.p)])
        t_f = np.stack([np.power(np.arange(forecast_size) / forecast_size, i) for i in range(self.p)])
        self.backcast_time = nn.Parameter(torch.tensor(t_b, dtype=torch.float32), requires_grad=False)
        self.forecast_time = nn.Parameter(torch.tensor(t_f, dtype=torch.float32), requires_grad=False)

    def forward(self, theta):
        backcast = torch.einsum('bp,pt->bt', theta[:, self.p:], self.backcast_time)
        forecast = torch.einsum('bp,pt->bt', theta[:, :self.p], self.forecast_time)
        return backcast, forecast


class SeasonalityBasis(nn.Module):
    def __init__(self, harmonics, backcast_size, forecast_size):
        super().__init__()
        freq = np.arange(1, harmonics + 1)
        b_grid = -2 * np.pi * np.outer(np.arange(backcast_size), freq) / forecast_size
        f_grid = 2 * np.pi * np.outer(np.arange(forecast_size), freq) / forecast_size

        self.b_cos = nn.Parameter(torch.tensor(np.cos(b_grid.T), dtype=torch.float32), requires_grad=False)
        self.b_sin = nn.Parameter(torch.tensor(np.sin(b_grid.T), dtype=torch.float32), requires_grad=False)
        self.f_cos = nn.Parameter(torch.tensor(np.cos(f_grid.T), dtype=torch.float32), requires_grad=False)
        self.f_sin = nn.Parameter(torch.tensor(np.sin(f_grid.T), dtype=torch.float32), requires_grad=False)

    def forward(self, theta):
        p = theta.shape[1] // 4
        b_cos = torch.einsum('bp,pt->bt', theta[:, 2*p:3*p], self.b_cos)
        b_sin = torch.einsum('bp,pt->bt', theta[:, 3*p:], self.b_sin)
        f_cos = torch.einsum('bp,pt->bt', theta[:, 0:p], self.f_cos)
        f_sin = torch.einsum('bp,pt->bt', theta[:, p:2*p], self.f_sin)
        return b_cos + b_sin, f_cos + f_sin

# ----------- N-BEATS Block -----------

class NBeatsBlock(nn.Module):
    def __init__(self, input_size, theta_size, basis_function, layers, layer_size):
        super().__init__()
        self.layers = nn.Sequential(
            *[nn.Sequential(nn.Linear(input_size if i == 0 else layer_size, layer_size), nn.ReLU())
              for i in range(layers)]
        )
        self.theta = nn.Linear(layer_size, theta_size)
        self.basis_function = basis_function

    def forward(self, x):
        x = self.layers(x)
        theta = self.theta(x)
        return self.basis_function(theta)

# ----------- Full N-BEATS Model (Template-Compatible) -----------

class Model(nn.Module):
    """
    N-BEATS: Neural Basis Expansion for interpretable time series forecasting
    """
    def __init__(self, configs):
        super(Model, self).__init__()
        self.seq_len = configs.seq_len
        self.pred_len = configs.pred_len
        self.individual = configs.individual
        self.channels = configs.enc_in
        self.block_type = configs.block_type  # 'trend', 'seasonality', 'generic'
        self.n_blocks = configs.n_blocks
        self.hidden_size = configs.hidden_size
        self.n_layers = configs.n_layers
        self.harmonics = configs.harmonics
        self.poly_degree = configs.poly_degree

        self.blocks = nn.ModuleList()
        theta_size = None

        if self.block_type == 'trend':
            basis_fn = TrendBasis(self.poly_degree, self.seq_len, self.pred_len)
            theta_size = 2 * (self.poly_degree + 1)
        elif self.block_type == 'seasonality':
            basis_fn = SeasonalityBasis(self.harmonics, self.seq_len, self.pred_len)
            theta_size = 4 * self.harmonics
        else:
            basis_fn = GenericBasis(self.seq_len, self.pred_len)
            theta_size = self.seq_len + self.pred_len

        for _ in range(self.n_blocks):
            self.blocks.append(NBeatsBlock(
                input_size=self.seq_len,
                theta_size=theta_size,
                basis_function=basis_fn,
                layers=self.n_layers,
                layer_size=self.hidden_size
            ))

    def forward(self, x):
        # x: [Batch, Input length, Channel]
        x = x.permute(0, 2, 1)  # → [Batch, Channel, Length]
        output = []

        for i in range(self.channels):
            residual = x[:, i, :].flip(dims=(1,))
            forecast = x[:, i, -1:].clone()
            for block in self.blocks:
                backcast, block_forecast = block(residual)
                residual = (residual - backcast)
                forecast = forecast + block_forecast
            output.append(forecast)

        y = torch.stack(output, dim=-1)  # [B, pred_len, C]
        return y
