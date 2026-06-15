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

        # RevIN layer
        # if self.revin:
        #     self.revin_layer = RevIN(self.channels, affine=True, subtract_last=False)

        # Handle layer width configuration
        if hasattr(configs, 'hidden_dims'):
            self.hidden_dims = configs.hidden_dims
        else:
            hidden_dim = getattr(configs, 'hidden_dim', 128)
            num_layers = getattr(configs, 'num_layers', 2)
            self.hidden_dims = [hidden_dim] * (num_layers - 1)
        dropout_rate = getattr(configs, 'mlp_dropout', 0.2)

        # Output dim: channels × pred_len (flattened)
        output_dim = self.channels * self.pred_len

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
            # Each variable gets its own MLP: input is seq_len, output is pred_len
            layer_dims = self.hidden_dims + [self.pred_len]
            self.mlps = nn.ModuleList([build_mlp(self.seq_len, layer_dims) for _ in range(self.channels)])
        else:
            # Shared MLP takes full [C x seq_len] and outputs [C x pred_len]
            input_dim = self.seq_len * self.channels
            layer_dims = self.hidden_dims + [output_dim]
            self.shared_mlp = build_mlp(input_dim, layer_dims)

    def forward(self, x):
        # x: [B, L, C]
    
        if self.individual:
            # x: [B, L, C] → [B, C, L]
            x = x.permute(0, 2, 1)
            out = torch.zeros([x.size(0), self.channels, self.pred_len], dtype=x.dtype).to(x.device)
            for i in range(self.channels):
                out[:, i, :] = self.mlps[i](x[:, i, :])
        else:
            # Flatten input: [B, L, C] → [B, C*L]
            x = x.permute(0, 2, 1).contiguous()  # [B, C, L]
            x = x.view(x.size(0), -1)  # [B, C*L]
            out = self.shared_mlp(x)  # [B, C*P]
            out = out.view(x.size(0), self.channels, self.pred_len)

        out = out.permute(0, 2, 1)  # [B, P, C]

        return out



