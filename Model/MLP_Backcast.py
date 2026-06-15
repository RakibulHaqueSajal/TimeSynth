import torch
import torch.nn as nn

class Model(nn.Module):
    def __init__(self, configs):
        super(Model, self).__init__()
        self.seq_len = configs.seq_len
        self.pred_len = configs.pred_len
        self.channels = configs.enc_in
        self.individual = configs.individual
        self.revin = configs.revin

        # Total output dim for shared MLP: (seq_len + pred_len) × channels
        self.total_len = self.seq_len + self.pred_len
        self.output_dim = self.channels * self.total_len

        if hasattr(configs, 'hidden_dims'):
            self.hidden_dims = configs.hidden_dims
        else:
            hidden_dim = getattr(configs, 'hidden_dim', 128)
            num_layers = getattr(configs, 'num_layers', 2)
            self.hidden_dims = [hidden_dim] * (num_layers - 1)
        dropout_rate = getattr(configs, 'mlp_dropout', 0.2)

        def build_mlp(in_dim, dims):
            layers = []
            for dim in dims[:-1]:
                layers.append(nn.Linear(in_dim, dim))
                layers.append(nn.ReLU())
                layers.append(nn.Dropout(dropout_rate))
                in_dim = dim
            layers.append(nn.Linear(in_dim, dims[-1]))
            return nn.Sequential(*layers)

        if self.individual:
            # Each channel has its own MLP → outputs [seq_len + pred_len]
            layer_dims = self.hidden_dims + [self.total_len]
            self.mlps = nn.ModuleList([build_mlp(self.seq_len, layer_dims) for _ in range(self.channels)])
        else:
            input_dim = self.seq_len * self.channels
            layer_dims = self.hidden_dims + [self.output_dim]
            self.shared_mlp = build_mlp(input_dim, layer_dims)

    def forward(self, x):
        # x: [B, seq_len, C]

        if self.individual:
            # x: [B, C, seq_len]
            x = x.permute(0, 2, 1)
            out = torch.zeros([x.size(0), self.channels, self.total_len], dtype=x.dtype).to(x.device)
            for i in range(self.channels):
                out[:, i, :] = self.mlps[i](x[:, i, :])  # [B, total_len]
        else:
            # x: [B, seq_len, C] → [B, C, seq_len]
            x = x.permute(0, 2, 1).contiguous()
            x = x.view(x.size(0), -1)  # [B, C * seq_len]
            out = self.shared_mlp(x)   # [B, C * total_len]
            out = out.view(x.size(0), self.channels, self.total_len)

        # Split: [B, C, total_len] → backcast [B, seq_len, C], forecast [B, pred_len, C]
        backcast = out[:, :, :self.seq_len].permute(0, 2, 1)   # [B, seq_len, C]
        forecast = out[:, :, self.seq_len:].permute(0, 2, 1)   # [B, pred_len, C]

        return backcast, forecast