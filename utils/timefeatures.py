import pandas as pd
import numpy as np
import torch

def build_time_features(batch_size, seq_len, base_time, freq='s'):
    time_index = pd.date_range(start=base_time, periods=seq_len, freq=freq.upper())  # 'S' = seconds
    features = np.stack([
        time_index.month / 12.0,
        time_index.day / 31.0,
        time_index.weekday / 6.0,
        time_index.hour / 23.0,
        time_index.minute / 59.0,
        time_index.second / 59.0
    ], axis=1)  # shape: [seq_len, 6]
    
    features = torch.tensor(features, dtype=torch.float32)  # [L, 6]
    features = features.unsqueeze(0).repeat(batch_size, 1, 1)  # [B, L, 6]
    return features