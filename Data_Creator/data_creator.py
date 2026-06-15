import os
import glob
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from torch.utils.data import Dataset



class Dataset_Custom(Dataset):
    def __init__(self,
                 root_path,
                 flag='train',
                 size=None,
                 features='S',
                 target='Value',
                 scale=False,
                 timeenc=0,
                 freq='h',
                 random_sample_size=None,
                 random_seed=42,
                 patch_len=None,               # NEW: add patch_len for warning/padding
                 pad_short_y=False):           # NEW: option to pad y if it's too short
        """
        Parameters:
        - size: [seq_len, label_len, pred_len]
        - patch_len: required only to warn or pad for patch-aligned autoregressive prediction
        - pad_short_y: if True, pads y to pred_len if it's shorter due to boundary
        """
        if size is None:
            self.seq_len, self.label_len, self.pred_len = 96, 24, 24
        else:
            self.seq_len, self.label_len, self.pred_len = size

        self.patch_len = patch_len
        self.pad_short_y = pad_short_y

        assert flag in ['train', 'val', 'test']
        self.flag = flag
        self.features = features
        self.target = target
        self.scale = scale
        self.timeenc = timeenc
        self.freq = freq

        self.root_path = root_path
        self.split_dir = os.path.join(root_path, flag)
        self.random_sample_size = random_sample_size
        self.random_seed = random_seed

        self.__read_data__()

    def __read_data__(self):

        all_files = sorted(glob.glob(os.path.join(self.split_dir, '*.csv')))
        if not all_files:
            raise FileNotFoundError(f"No CSVs found in {self.split_dir}")

        if self.random_sample_size:
            if self.random_sample_size > len(all_files):
                raise ValueError(f"random_sample_size={self.random_sample_size} exceeds available files ({len(all_files)})")
            np.random.seed(self.random_seed)
            selected_files = list(np.random.choice(all_files, size=self.random_sample_size, replace=False))
        else:
            selected_files = all_files

        print(f"[{self.flag}] Using {len(selected_files)} files out of {len(all_files)} total.")

        self.samples = []
        self.scaler = StandardScaler() if self.scale and self.flag == 'train' else None

        all_values = []
        if self.scaler:
            for fp in selected_files:
                df = pd.read_csv(fp, parse_dates=['Time'], index_col='Time')
                values = df[[self.target]].values
                all_values.append(values)
            stacked = np.concatenate(all_values, axis=0)
            self.scaler.fit(stacked)

        for fp in selected_files:
            df = pd.read_csv(fp, parse_dates=['Time'], index_col='Time')
            values = df[[self.target]].values.astype(np.float32)
            if self.scaler:
                values = self.scaler.transform(values)
             
            
            timestamps = df.index.astype(np.int64) / 1e9
    
            timestamps = timestamps.to_numpy().reshape(-1, 1)

            max_start = len(values) - self.seq_len
            if self.flag=='test' or self.flag=='val' or self.flag=='train':
                self.label_len=0
            for i in range(max_start - self.label_len - self.pred_len + 1):
                s_beg = i
                s_end = s_beg + self.seq_len
                r_beg = s_end - self.label_len
                r_end = r_beg + self.label_len + self.pred_len
        
                if r_end > len(values):
                    if self.pad_short_y:
                        pad_len = r_end - len(values)
                        y = np.pad(values[r_beg:], ((0, pad_len), (0,)), mode='constant')
                        y_stamp = np.pad(timestamps[r_beg:], ((0, pad_len), (0,)), mode='constant')
                    else:
                        continue
                else:
                    y = values[r_beg:r_end]
                    y_stamp = timestamps[r_beg:r_end]

                x = values[s_beg:s_end]
                x_stamp = timestamps[s_beg:s_end]

                self.samples.append((x, y, x_stamp, y_stamp))

        print(f"[{self.flag}] Loaded {len(self.samples)} samples.")

        # Optional patch alignment warning
        if self.patch_len is not None and self.pred_len % self.patch_len != 0:
            print(f"[{self.flag}] Warning: pred_len={self.pred_len} is not divisible by patch_len={self.patch_len}. "
                  f"The model's output will be truncated to match pred_len.")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, index):
        return self.samples[index]

    def inverse_transform(self, data):
        if not self.scaler:
            raise RuntimeError("Scaler not defined. Set scale=True during training.")
        return self.scaler.inverse_transform(data)



class TrainDataset_UniformPlusCentered(Dataset):
    def __init__(
        self,
        root_path,
        size=(96, 0, 24),
        target="Value",
        scale=False,
        uniform_stride=1,
        add_uniform=True,
        add_centered=True,
        centered_per_file=40,
        centered_jitter=40,
        centered_history_frac=0.5,
        centered_weight=1.0,
        random_seed=42,
        transition_meta_path=None,  # if None, will default to root_path/train_transitions.csv
    ):
        self.root_path = root_path
        self.split_dir = os.path.join(root_path, "train")

        self.seq_len, self.label_len, self.pred_len = map(int, size)
        self.target = target
        self.scale = bool(scale)

        self.uniform_stride = int(uniform_stride)
        self.add_uniform = bool(add_uniform)
        self.add_centered = bool(add_centered)

        self.centered_per_file = int(centered_per_file)
        self.centered_jitter = int(centered_jitter)
        self.centered_history_frac = float(centered_history_frac)
        self.centered_weight = float(centered_weight)
        self.rng = np.random.RandomState(int(random_seed))

        self.scaler = StandardScaler() if self.scale else None

        # ---- IMPORTANT: these must be DICTS, not strings ----
        self.transition_map = None          # filename -> t_star_idx
        self.transition_map_by_path = None  # abspath(filepath) -> t_star_idx

        # default meta path is in root_path (your case)
        if transition_meta_path is None:
            transition_meta_path = os.path.join(root_path, "train_transitions.csv")

        # load meta if it exists (recommended)
        if transition_meta_path is not None and os.path.exists(transition_meta_path):
            self._load_transition_meta(transition_meta_path)

        # index: list of (fp, start_idx, tag)
        self.samples = []
        self._build_index()

    def _load_transition_meta(self, transition_meta_path):
        meta = pd.read_csv(transition_meta_path)

        required = {"filename", "t_star_idx"}
        missing = required - set(meta.columns)
        if missing:
            raise ValueError(
                f"train_transitions.csv missing columns: {missing}. "
                f"Found columns: {list(meta.columns)}"
            )

        # filename -> idx
        self.transition_map = dict(
            zip(meta["filename"].astype(str), meta["t_star_idx"].astype(int))
        )

        # filepath -> idx (this file has absolute 'filepath', good)
        if "filepath" in meta.columns:
            # normalize to abspath to match glob results robustly
            paths = meta["filepath"].astype(str).apply(lambda p: os.path.abspath(p))
            self.transition_map_by_path = dict(zip(paths, meta["t_star_idx"].astype(int)))
        else:
            self.transition_map_by_path = None

    def _read_csv(self, fp):
        df = pd.read_csv(fp)
        if self.target not in df.columns:
            raise ValueError(f"Missing target column '{self.target}' in {fp}")

        values = df[[self.target]].values.astype(np.float32)
        ts = (df["Time"].to_numpy().astype(np.float32) if "Time" in df.columns
              else np.arange(len(df), dtype=np.float32))
        ts = ts.reshape(-1, 1)

        states = df["State"].to_numpy().astype(int) if "State" in df.columns else None
        return values, ts, states

    def _infer_transition_idx(self, fp, states):
        base = os.path.basename(fp)
        fp_abs = os.path.abspath(fp)

        # 1) filename map
        if self.transition_map is not None and base in self.transition_map:
            return int(self.transition_map[base])

        # 2) filepath map
        if self.transition_map_by_path is not None:
            t = self.transition_map_by_path.get(fp_abs, None)
            if t is not None:
                return int(t)

        # 3) fallback: infer from State column (if present)
        if states is None:
            return None
        change = np.where(states[1:] != states[:-1])[0]
        return None if len(change) == 0 else int(change[0] + 1)

    # --- window logic (same as your existing code) ---
    def _window_end(self, s_beg):
        s_end = s_beg + self.seq_len
        r_beg = s_end - self.label_len
        r_end = r_beg + self.label_len + self.pred_len
        return s_end, r_beg, r_end

    def _is_valid_start(self, s_beg, T):
        _, _, r_end = self._window_end(s_beg)
        return (s_beg >= 0) and (r_end <= T)

    def _fit_scaler(self, files):
        all_vals = []
        for fp in files:
            v, _, _ = self._read_csv(fp)
            all_vals.append(v)
        self.scaler.fit(np.concatenate(all_vals, axis=0))

    def _add_uniform_windows(self, fp, T):
        last = T - (self.seq_len + self.pred_len)
        if last < 0:
            return 0
        cnt = 0
        for s in range(0, last + 1, self.uniform_stride):
            self.samples.append((fp, s, "uniform"))
            cnt += 1
        return cnt

    def _add_centered_windows(self, fp, T, t_star):
        if t_star is None:
            return 0
        ideal = int(round(t_star - self.centered_history_frac * self.seq_len))
        cnt = 0
        for _ in range(self.centered_per_file):
            jitter = self.rng.randint(-self.centered_jitter, self.centered_jitter + 1)
            s = ideal + jitter
            if self._is_valid_start(s, T):
                self.samples.append((fp, s, "centered"))
                cnt += 1

        if self.centered_weight > 1.0 and cnt > 0:
            rep = int(np.floor(self.centered_weight)) - 1
            tail = self.samples[-cnt:]
            for _ in range(rep):
                self.samples.extend(tail)
                cnt += len(tail)
        return cnt

    def _build_index(self):
        files = sorted(glob.glob(os.path.join(self.split_dir, "*.csv")))
        if not files:
            raise FileNotFoundError(f"No CSVs found in {self.split_dir}")

        if self.scaler is not None:
            self._fit_scaler(files)

        uniform_cnt = 0
        centered_cnt = 0

        for fp in files:
            values, _, states = self._read_csv(fp)
            T = len(values)
            t_star = self._infer_transition_idx(fp, states)

            if self.add_uniform:
                uniform_cnt += self._add_uniform_windows(fp, T)
            if self.add_centered:
                centered_cnt += self._add_centered_windows(fp, T, t_star)

        print(f"[train] total_windows={len(self.samples)} | uniform={uniform_cnt}, centered={centered_cnt}")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        fp, s_beg, _tag = self.samples[idx]
        values, ts, _ = self._read_csv(fp)

        if self.scaler is not None:
            values = self.scaler.transform(values).astype(np.float32)

        s_end, r_beg, r_end = self._window_end(s_beg)
        return values[s_beg:s_end], values[r_beg:r_end], ts[s_beg:s_end], ts[r_beg:r_end]

class Dataset_Custom_State(Dataset):
    def __init__(self,
                 root_path,
                 flag='train',
                 size=None,
                 features='S',
                 target='Value',
                 scale=False,
                 timeenc=0,
                 freq='h',
                 random_sample_size=None,
                 random_seed=42,
                 patch_len=None,
                 pad_short_y=False):
        if size is None:
            self.seq_len, self.label_len, self.pred_len = 96, 24, 24
        else:
            self.seq_len, self.label_len, self.pred_len = size

        self.patch_len = patch_len
        self.pad_short_y = pad_short_y

        assert flag in ['train', 'val', 'test']
        self.flag = flag
        self.features = features
        self.target = target
        self.scale = scale
        self.timeenc = timeenc
        self.freq = freq

        self.root_path = root_path
        self.split_dir = os.path.join(root_path, flag)
        self.random_sample_size = random_sample_size
        self.random_seed = random_seed

        self.__read_data__()

    def __read_data__(self):

        all_files = sorted(glob.glob(os.path.join(self.split_dir, '*.csv')))
        if not all_files:
            raise FileNotFoundError(f"No CSVs found in {self.split_dir}")

        if self.random_sample_size:
            if self.random_sample_size > len(all_files):
                raise ValueError(f"random_sample_size={self.random_sample_size} exceeds available files ({len(all_files)})")
            np.random.seed(self.random_seed)
            selected_files = list(np.random.choice(all_files, size=self.random_sample_size, replace=False))
        else:
            selected_files = all_files

        print(f"[{self.flag}] Using {len(selected_files)} files out of {len(all_files)} total.")

        self.samples = []
        self.scaler = StandardScaler() if self.scale and self.flag == 'train' else None

        all_values = []
        if self.scaler:
            for fp in selected_files:
                df = pd.read_csv(fp, parse_dates=['Time'], index_col='Time')
                values = df[[self.target]].values
                all_values.append(values)
            stacked = np.concatenate(all_values, axis=0)
            self.scaler.fit(stacked)

        for fp in selected_files:
            df = pd.read_csv(fp, parse_dates=['Time'], index_col='Time')

            # ---- NEW: load state (do NOT scale) ----
            if "State" not in df.columns:
                raise ValueError(f"Missing 'State' column in {fp}. Found: {list(df.columns)}")
            states = df[["State"]].values.astype(np.int64)  # (T,1)

            values = df[[self.target]].values.astype(np.float32)
            if self.scaler:
                values = self.scaler.transform(values)

            timestamps = (df.index.astype(np.int64) / 1e9).to_numpy().reshape(-1, 1)

            max_start = len(values) - self.seq_len

            # keep your behavior
            if self.flag in ['test', 'val', 'train']:
                self.label_len = 0

            for i in range(max_start - self.label_len - self.pred_len + 1):
                s_beg = i
                s_end = s_beg + self.seq_len
                r_beg = s_end - self.label_len
                r_end = r_beg + self.label_len + self.pred_len

                if r_end > len(values):
                    if self.pad_short_y:
                        pad_len = r_end - len(values)

                        y = np.pad(values[r_beg:], ((0, pad_len), (0,)), mode='constant')
                        y_stamp = np.pad(timestamps[r_beg:], ((0, pad_len), (0,)), mode='constant')

                        # ---- NEW: pad y_state_true (use edge so it stays a valid state id) ----
                        y_state_true = np.pad(states[r_beg:], ((0, pad_len), (0,)), mode='edge')
                    else:
                        continue
                else:
                    y = values[r_beg:r_end]
                    y_stamp = timestamps[r_beg:r_end]

                    # ---- NEW: slice states aligned with y ----
                    y_state_true = states[r_beg:r_end]

                x = values[s_beg:s_end]
                x_stamp = timestamps[s_beg:s_end]

                # ---- CHANGED: append y_state_true too ----
                self.samples.append((x, y, x_stamp, y_stamp, y_state_true))

        print(f"[{self.flag}] Loaded {len(self.samples)} samples.")

        if self.patch_len is not None and self.pred_len % self.patch_len != 0:
            print(f"[{self.flag}] Warning: pred_len={self.pred_len} is not divisible by patch_len={self.patch_len}. "
                  f"The model's output will be truncated to match pred_len.")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, index):
        return self.samples[index]

    def inverse_transform(self, data):
        if not self.scaler:
            raise RuntimeError("Scaler not defined. Set scale=True during training.")
        return self.scaler.inverse_transform(data)


class TrainDataset_UniformPlusCentered_TwoCP(Dataset):
    """
    Train dataset for TWO-transition signals (t1, t2), supporting ABA/BAB motifs.

    Adds windows:
      - uniform: sliding windows across file
      - centered_t1: windows whose history boundary is near t1
      - centered_t2: windows whose history boundary is near t2
      - between: windows centered around the segment between t1 and t2 (optional)

    Works with your generator metadata:
      columns expected: filename, t1_idx, t2_idx, motif, regime (optional), no_transition (optional)
    """

    def __init__(
        self,
        root_path,
        size=(96, 0, 24),
        target="Value",
        scale=False,
        uniform_stride=1,
        add_uniform=True,

        # centered around transitions:
        add_centered=True,
        centered_per_file=40,
        centered_jitter=40,
        centered_history_frac=0.5,
        centered_weight=1.0,

        # NEW: centered around BOTH transitions
        center_on=("t1", "t2"),           # any subset of {"t1","t2"}
        per_transition_share=(0.5, 0.5),  # splits centered_per_file between t1 and t2

        # NEW: explicitly sample between transitions
        add_between=False,
        between_per_file=20,
        between_jitter=40,
        between_history_frac=0.5,

        random_seed=42,
        transition_meta_path=None,  # default: root_path/train_transitions.csv
    ):
        self.root_path = root_path
        self.split_dir = os.path.join(root_path, "train")

        self.seq_len, self.label_len, self.pred_len = map(int, size)
        self.target = target
        self.scale = bool(scale)

        self.uniform_stride = int(uniform_stride)
        self.add_uniform = bool(add_uniform)

        self.add_centered = bool(add_centered)
        self.centered_per_file = int(centered_per_file)
        self.centered_jitter = int(centered_jitter)
        self.centered_history_frac = float(centered_history_frac)
        self.centered_weight = float(centered_weight)

        self.center_on = tuple(center_on)
        assert all(x in ("t1", "t2") for x in self.center_on)

        self.per_transition_share = tuple(per_transition_share)
        if len(self.center_on) == 1:
            self.per_transition_share = (1.0,)
        else:
            assert len(self.per_transition_share) == 2
            s = self.per_transition_share[0] + self.per_transition_share[1]
            self.per_transition_share = (
                self.per_transition_share[0] / s,
                self.per_transition_share[1] / s,
            )

        self.add_between = bool(add_between)
        self.between_per_file = int(between_per_file)
        self.between_jitter = int(between_jitter)
        self.between_history_frac = float(between_history_frac)

        self.rng = np.random.RandomState(int(random_seed))
        self.scaler = StandardScaler() if self.scale else None

        # meta maps
        self.meta_by_filename = {}  # filename -> dict(t1,t2,motif,regime,no_transition)
        self.meta_by_path = {}      # abspath -> same dict

        if transition_meta_path is None:
            transition_meta_path = os.path.join(root_path, "train_transitions.csv")
        if transition_meta_path is not None and os.path.exists(transition_meta_path):
            self._load_transition_meta(transition_meta_path)

        self.samples = []  # list of (fp, start_idx, tag)
        self._build_index()

    # -------------------- meta --------------------
    def _load_transition_meta(self, transition_meta_path):
        meta = pd.read_csv(transition_meta_path)

        required = {"filename", "t1_idx", "t2_idx", "motif"}
        missing = required - set(meta.columns)
        if missing:
            raise ValueError(
                f"{os.path.basename(transition_meta_path)} missing columns: {missing}. "
                f"Found columns: {list(meta.columns)}"
            )

        def row_to_dict(r):
            return {
                "t1": int(r["t1_idx"]) if r["t1_idx"] >= 0 else None,
                "t2": int(r["t2_idx"]) if r["t2_idx"] >= 0 else None,
                "motif": str(r["motif"]),
                "regime": str(r["regime"]) if "regime" in meta.columns else None,
                "no_transition": int(r["no_transition"]) if "no_transition" in meta.columns else 0,
            }

        for _, r in meta.iterrows():
            fn = str(r["filename"])
            d = row_to_dict(r)
            self.meta_by_filename[fn] = d

            if "filepath" in meta.columns:
                fp = os.path.abspath(str(r["filepath"]))
                self.meta_by_path[fp] = d

    def _get_two_cps(self, fp):
        base = os.path.basename(fp)
        fp_abs = os.path.abspath(fp)

        d = None
        if base in self.meta_by_filename:
            d = self.meta_by_filename[base]
        elif fp_abs in self.meta_by_path:
            d = self.meta_by_path[fp_abs]

        if d is None:
            return None, None, None  # unknown

        if d.get("no_transition", 0) == 1:
            return None, None, d

        return d.get("t1", None), d.get("t2", None), d

    # -------------------- io --------------------
    def _read_csv(self, fp):
        df = pd.read_csv(fp)
        if self.target not in df.columns:
            raise ValueError(f"Missing target column '{self.target}' in {fp}")

        values = df[[self.target]].values.astype(np.float32)
        ts = (
            df["Time"].to_numpy().astype(np.float32)
            if "Time" in df.columns
            else np.arange(len(df), dtype=np.float32)
        )
        ts = ts.reshape(-1, 1)
        return values, ts

    # -------------------- window helpers --------------------
    def _window_end(self, s_beg):
        s_end = s_beg + self.seq_len
        r_beg = s_end - self.label_len
        r_end = r_beg + self.label_len + self.pred_len
        return s_end, r_beg, r_end

    def _is_valid_start(self, s_beg, T):
        _, _, r_end = self._window_end(s_beg)
        return (s_beg >= 0) and (r_end <= T)

    def _fit_scaler(self, files):
        all_vals = []
        for fp in files:
            v, _ = self._read_csv(fp)
            all_vals.append(v)
        self.scaler.fit(np.concatenate(all_vals, axis=0))

    # -------------------- adding windows --------------------
    def _add_uniform_windows(self, fp, T):
        last = T - (self.seq_len + self.pred_len)
        if last < 0:
            return 0
        cnt = 0
        for s in range(0, last + 1, self.uniform_stride):
            self.samples.append((fp, s, "uniform"))
            cnt += 1
        return cnt

    def _add_centered_around(self, fp, T, t_anchor, tag, history_frac, jitter, n_samples):
        if t_anchor is None:
            return 0
        ideal = int(round(t_anchor - history_frac * self.seq_len))
        cnt = 0
        for _ in range(n_samples):
            j = self.rng.randint(-jitter, jitter + 1)
            s = ideal + j
            if self._is_valid_start(s, T):
                self.samples.append((fp, s, tag))
                cnt += 1
        return cnt

    def _replicate_tail(self, cnt):
        if self.centered_weight <= 1.0 or cnt <= 0:
            return cnt
        rep = int(np.floor(self.centered_weight)) - 1
        tail = self.samples[-cnt:]
        for _ in range(rep):
            self.samples.extend(tail)
            cnt += len(tail)
        return cnt

    # -------------------- build index --------------------
    def _build_index(self):
        files = sorted(glob.glob(os.path.join(self.split_dir, "*.csv")))
        if not files:
            raise FileNotFoundError(f"No CSVs found in {self.split_dir}")

        if self.scaler is not None:
            self._fit_scaler(files)

        uniform_cnt = 0
        centered_cnt = 0
        between_cnt = 0

        for fp in files:
            values, _ = self._read_csv(fp)
            T = len(values)

            # uniform
            if self.add_uniform:
                uniform_cnt += self._add_uniform_windows(fp, T)

            # two CPs from meta
            t1, t2, meta = self._get_two_cps(fp)
            if meta is not None and meta.get("no_transition", 0) == 1:
                continue  # no centered/between for NO_TRANS

            # centered around transitions
            if self.add_centered:
                if len(self.center_on) == 1:
                    n1 = self.centered_per_file
                    anchors = [
                        (
                            t1 if self.center_on[0] == "t1" else t2,
                            f"centered_{self.center_on[0]}",
                            n1,
                        )
                    ]
                else:
                    n1 = int(round(self.centered_per_file * self.per_transition_share[0]))
                    n2 = self.centered_per_file - n1
                    anchors = []
                    if "t1" in self.center_on:
                        anchors.append((t1, "centered_t1", n1))
                    if "t2" in self.center_on:
                        anchors.append((t2, "centered_t2", n2))

                added = 0
                for t_anchor, tag, n_samp in anchors:
                    added += self._add_centered_around(
                        fp,
                        T,
                        t_anchor,
                        tag,
                        history_frac=self.centered_history_frac,
                        jitter=self.centered_jitter,
                        n_samples=n_samp,
                    )
                added = self._replicate_tail(added)
                centered_cnt += added

            # between transitions: put boundary around the middle of (t1,t2)
            if self.add_between and (t1 is not None) and (t2 is not None) and (t2 > t1):
                mid = int(round(0.5 * (t1 + t2)))
                between_cnt += self._add_centered_around(
                    fp,
                    T,
                    mid,
                    "between",
                    history_frac=self.between_history_frac,
                    jitter=self.between_jitter,
                    n_samples=self.between_per_file,
                )

        print(
            f"[train-2cp] total_windows={len(self.samples)} | "
            f"uniform={uniform_cnt}, centered={centered_cnt}, between={between_cnt}"
        )

    # -------------------- torch dataset --------------------
    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        fp, s_beg, tag = self.samples[idx]
        values, ts = self._read_csv(fp)

        if self.scaler is not None:
            values = self.scaler.transform(values).astype(np.float32)

        s_end, r_beg, r_end = self._window_end(s_beg)
        return values[s_beg:s_end], values[r_beg:r_end], ts[s_beg:s_end], ts[r_beg:r_end]


class EvalDataset_TwoCP_GranularTags(Dataset):
    """
    Eval-only dataset for TWO-transition (t1,t2) sequences with:
      (A) Granular tags around EACH transition (t1 and t2) relative to boundary b=s+L:
            t1_hist_d02, t1_hist_d04, ...   and  t1_fut_d02, ...
            t2_hist_d02, t2_hist_d04, ...   and  t2_fut_d02, ...
      (B) Optional high-level tags:
            {HH/HF/FF}_{dwell_bin}_{motif_bin}  e.g. HH_dwell_d10_motif_ABA
      (C) Optional NO-TRANS baselines:
            no_transition_A / no_transition_B

    Window geometry:
      L = seq_len, H = pred_len, label_len optional
      boundary b = s + L

    Transition offsets returned in meta:
      boundary_offset1 = t1 - b
      boundary_offset2 = t2 - b
    """

    def __init__(
        self,
        root_path,
        flag="test",
        size=(50, 0, 100),              # (seq_len, label_len, pred_len)
        target="Value",
        scale=False,

        # --- granular bins (same idea as your 1-CP eval) ---
        boundary_bins=None,             # e.g. (2,4,6,...,40); if None, build from step/max
        bin_step=2,
        bin_max=20,
        allow_transition_at_boundary=False,  # include d=0 tags (usually False)

        # --- two-cp semantic tags (optional) ---
        add_twoflip_semantic_tags=True,
        dwell_bins=(5, 10, 15, 20, 30, 40),
        placement_modes=("HH", "HF", "FF"),

        # --- selection policy ---
        one_per_tag_per_file=True,
        random_seed=42,
        verbose=True,

        # --- metadata ---
        transition_meta_path=None,      # default: root_path/{flag}_transitions.csv

        # --- no-transition ---
        include_no_transition=True,
        no_transition_one_window_per_file=True,
    ):
        assert flag in ["train", "val", "test"]
        self.root_path = root_path
        self.flag = flag
        self.split_dir = os.path.join(root_path, flag)

        self.seq_len, self.label_len, self.pred_len = map(int, size)
        self.target = target
        self.scale = bool(scale)
        self.scaler = StandardScaler() if self.scale else None

        self.verbose = bool(verbose)
        self.rng = np.random.RandomState(int(random_seed))

        # bins
        if boundary_bins is None:
            if bin_step <= 0 or bin_max <= 0:
                raise ValueError("bin_step and bin_max must be > 0")
            self.boundary_bins = list(range(int(bin_step), int(bin_max) + 1, int(bin_step)))
        else:
            self.boundary_bins = [int(b) for b in boundary_bins]

        if not self.boundary_bins:
            raise ValueError("boundary_bins is empty")
        if self.boundary_bins != sorted(self.boundary_bins):
            raise ValueError("boundary_bins must be sorted ascending")
        if any(b <= 0 for b in self.boundary_bins):
            raise ValueError("All boundary_bins must be > 0 (use allow_transition_at_boundary for d=0)")

        self.allow_transition_at_boundary = bool(allow_transition_at_boundary)

        # semantic tags
        self.add_twoflip_semantic_tags = bool(add_twoflip_semantic_tags)
        self.dwell_bins = [int(x) for x in dwell_bins]
        if self.dwell_bins != sorted(self.dwell_bins):
            raise ValueError("dwell_bins must be sorted ascending")
        self.placement_modes = tuple(placement_modes)
        for m in self.placement_modes:
            if m not in ("HH", "HF", "FF"):
                raise ValueError("placement_modes must be subset of ('HH','HF','FF')")

        # selection
        self.one_per_tag_per_file = bool(one_per_tag_per_file)

        # meta path
        if transition_meta_path is None:
            transition_meta_path = os.path.join(root_path, f"{flag}_transitions.csv")
        self.transition_meta_path = transition_meta_path

        # no-trans
        self.include_no_transition = bool(include_no_transition)
        self.no_transition_one_window_per_file = bool(no_transition_one_window_per_file)

        # meta maps
        self.meta_by_name = {}
        self.meta_by_path = {}

        self._load_transition_map()
        self.samples = []
        self._build_index()

    # ----------------------------- IO -----------------------------
    def _read_csv(self, fp):
        df = pd.read_csv(fp)
        if self.target not in df.columns:
            raise ValueError(f"Missing target column '{self.target}' in {fp}")

        values = df[[self.target]].values.astype(np.float32)

        if "Time" in df.columns:
            try:
                t = pd.to_datetime(df["Time"])
                ts = (t.astype("int64") / 1e9).to_numpy().astype(np.float32)
            except Exception:
                ts = df["Time"].to_numpy().astype(np.float32)
        else:
            ts = np.arange(len(df), dtype=np.float32)
        ts = ts.reshape(-1, 1)

        states = None
        if "State" in df.columns:
            states = df["State"].to_numpy().astype(int)

        return values, ts, states

    # ----------------------- meta loading -------------------------
    def _load_transition_map(self):
        if not os.path.exists(self.transition_meta_path):
            if self.verbose:
                print(f"[{self.flag}] No transition meta found: {self.transition_meta_path}")
            return

        meta = pd.read_csv(self.transition_meta_path)

        # Required for two-cp
        required = {"filename", "t1_idx", "t2_idx"}
        missing = required - set(meta.columns)
        if missing:
            raise ValueError(
                f"Transition CSV must contain {sorted(list(required))}. Missing: {sorted(list(missing))}"
            )

        # motif optional but recommended
        if "motif" not in meta.columns:
            meta["motif"] = "unknown"

        # Keep rows where either:
        # - two-flip: t1>=0, t2>=0
        # - NO_TRANS: motif == "NO_TRANS" or t1<0 and t2<0
        t1f = meta["t1_idx"].astype(float)
        t2f = meta["t2_idx"].astype(float)
        motif = meta["motif"].astype(str)

        valid_twoflip = np.isfinite(t1f) & np.isfinite(t2f) & (t1f >= 0) & (t2f >= 0)
        valid_notrans = np.isfinite(t1f) & np.isfinite(t2f) & ((motif == "NO_TRANS") | ((t1f < 0) & (t2f < 0)))

        mv = meta.loc[valid_twoflip | valid_notrans].copy()
        mv["t1_idx"] = mv["t1_idx"].astype(int)
        mv["t2_idx"] = mv["t2_idx"].astype(int)

        for _, r in mv.iterrows():
            fn = str(r["filename"])
            self.meta_by_name[fn] = r.to_dict()

        if "filepath" in mv.columns:
            for _, r in mv.iterrows():
                fp = os.path.abspath(str(r["filepath"]))
                self.meta_by_path[fp] = r.to_dict()

        if self.verbose:
            print(
                f"[{self.flag}] Loaded transition meta: {self.transition_meta_path} "
                f"(rows={len(meta)}, valid={len(mv)})"
            )

    def _get_twoflip_meta(self, fp, states):
        """
        Returns:
          - two-flip: (t1:int, t2:int, motif:str)
          - no-trans: ("NO_TRANS", None, ab:str in {"A","B"})
          - missing:  (None, None, None)
        """
        base = os.path.basename(fp)
        fp_abs = os.path.abspath(fp)
        row = self.meta_by_name.get(base, None)
        if row is None:
            row = self.meta_by_path.get(fp_abs, None)

        if row is not None:
            motif = str(row.get("motif", "unknown"))
            t1 = int(row["t1_idx"])
            t2 = int(row["t2_idx"])

            if motif == "NO_TRANS" or (t1 < 0 and t2 < 0):
                # infer constant state if available
                state_id = row.get("const_state_id", None)
                if state_id is not None and not (isinstance(state_id, float) and np.isnan(state_id)):
                    state_id = int(state_id)
                else:
                    state_id = None
                    if states is not None and len(states) > 0:
                        state_id = int(states[0])
                ab = "A" if state_id == 0 else "B"
                return "NO_TRANS", None, ab

            return t1, t2, motif

        # fallback: infer from states
        if states is None or len(states) == 0:
            return None, None, None

        ch = np.where(states[1:] != states[:-1])[0] + 1
        if len(ch) == 0:
            ab = "A" if int(states[0]) == 0 else "B"
            return "NO_TRANS", None, ab
        if len(ch) < 2:
            return None, None, None
        t1, t2 = int(ch[0]), int(ch[1])
        motif = "ABA" if int(states[0]) == 0 else "BAB"
        return t1, t2, motif

    # ----------------------- window validity ----------------------
    def _window_end(self, s):
        s_end = s + self.seq_len
        r_beg = s_end - self.label_len
        r_end = r_beg + self.label_len + self.pred_len
        return s_end, r_beg, r_end

    def _valid_start(self, s, T):
        s = int(s)
        _, _, r_end = self._window_end(s)
        return (s >= 0) and (r_end <= T)

    def _append_sample(self, fp, s, tag, t1, t2, motif):
        self.samples.append(
            dict(
                fp=fp,
                s_beg=int(s),
                tag=str(tag),
                t1=int(t1) if t1 is not None else -1,
                t2=int(t2) if t2 is not None else -1,
                motif=str(motif) if motif is not None else None,
            )
        )

    # ------------------------ dwell binning -----------------------
    def _dwell_bin_tag(self, dwell):
        prev = 0
        for b in self.dwell_bins:
            if prev < dwell <= b:
                return f"dwell_d{b:02d}"
            prev = b
        return f"dwell_d{self.dwell_bins[-1]:02d}_plus"

    # ------------------- granular around one anchor ---------------
    def _add_granular_around_anchor(self, fp, T, t_anchor, prefix, t1, t2, motif):
        """
        Creates tags like:
          {prefix}_hist_d02, {prefix}_fut_d02, ...
        where prefix is "t1" or "t2".
        """
        if t_anchor is None:
            return

        L = self.seq_len
        prev = 0

        # boundary b = s + L
        for bmax in self.boundary_bins:
            # hist: t_anchor < b  and prev < (b - t_anchor) <= bmax
            tag_h = f"{prefix}_hist_d{bmax:02d}"
            s_lo = int(t_anchor - L + (prev + 1))
            s_hi = int(t_anchor - L + bmax)

            hist_candidates = []
            for s in range(s_lo, s_hi + 1):
                if not self._valid_start(s, T):
                    continue
                b = s + L
                d = int(b - t_anchor)
                if (t_anchor < b) and (prev < d <= bmax):
                    hist_candidates.append(s)

            if hist_candidates:
                if self.one_per_tag_per_file:
                    s_choice = int(self.rng.choice(hist_candidates))
                    self._append_sample(fp, s_choice, tag_h, t1, t2, motif)
                else:
                    for s_choice in hist_candidates:
                        self._append_sample(fp, int(s_choice), tag_h, t1, t2, motif)

            # fut: b < t_anchor and prev < (t_anchor - b) <= bmax
            tag_f = f"{prefix}_fut_d{bmax:02d}"
            s_lo = int(t_anchor - L - bmax)
            s_hi = int(t_anchor - L - (prev + 1))

            fut_candidates = []
            for s in range(s_lo, s_hi + 1):
                if not self._valid_start(s, T):
                    continue
                b = s + L
                d = int(t_anchor - b)
                if (b < t_anchor) and (prev < d <= bmax):
                    fut_candidates.append(s)

            if fut_candidates:
                if self.one_per_tag_per_file:
                    s_choice = int(self.rng.choice(fut_candidates))
                    self._append_sample(fp, s_choice, tag_f, t1, t2, motif)
                else:
                    for s_choice in fut_candidates:
                        self._append_sample(fp, int(s_choice), tag_f, t1, t2, motif)

            prev = bmax

        # optional boundary case: d=0 when t_anchor == b => s = t_anchor - L
        if self.allow_transition_at_boundary:
            s0 = int(t_anchor - L)
            if self._valid_start(s0, T):
                self._append_sample(fp, s0, f"{prefix}_hist_d00", t1, t2, motif)

    # ------------------- semantic two-flip tags -------------------
    def _add_semantic_twoflip_tags(self, fp, T, t1, t2, motif):
        """
        Adds tags like:
          HH_dwell_d10_motif_ABA
          HF_dwell_d20_motif_BAB
          FF_dwell_d05_motif_ABA
        """
        if t1 is None or t2 is None:
            return
        if not (0 <= int(t1) < int(t2) < T):
            return

        dwell = int(t2 - t1)
        if dwell <= 0:
            return

        dwell_tag = self._dwell_bin_tag(dwell)
        motif_tag = f"motif_{motif}" if motif is not None else "motif_unknown"

        s_min = 0
        s_max = T - (self.seq_len + self.pred_len)
        if s_max < s_min:
            return

        candidates = {"HH": [], "HF": [], "FF": []}
        for s in range(s_min, s_max + 1):
            if not self._valid_start(s, T):
                continue
            b = s + self.seq_len
            if t2 < b:
                candidates["HH"].append(s)
            elif (t1 < b) and (b <= t2):
                candidates["HF"].append(s)
            elif b <= t1:
                candidates["FF"].append(s)

        for placement in self.placement_modes:
            cand = candidates.get(placement, [])
            if not cand:
                continue
            tag = f"{placement}_{dwell_tag}_{motif_tag}"
            if self.one_per_tag_per_file:
                s_choice = int(self.rng.choice(cand))
                self._append_sample(fp, s_choice, tag, t1, t2, motif)
            else:
                for s_choice in cand:
                    self._append_sample(fp, int(s_choice), tag, t1, t2, motif)

    # ------------------- no-transition tags -----------------------
    def _add_no_transition_windows(self, fp, T, ab):
        tag = "no_transition_A" if ab == "A" else "no_transition_B"
        s_min = 0
        s_max = T - (self.seq_len + self.pred_len)
        if s_max < s_min:
            return

        candidates = [s for s in range(s_min, s_max + 1) if self._valid_start(s, T)]
        if not candidates:
            return

        if self.no_transition_one_window_per_file:
            s_choice = int(self.rng.choice(candidates))
            self._append_sample(fp, s_choice, tag, None, None, "NO_TRANS")
        else:
            for s_choice in candidates:
                self._append_sample(fp, int(s_choice), tag, None, None, "NO_TRANS")

    # ------------------- index building --------------------------
    def _fit_scaler(self, files):
        all_vals = []
        for fp in files:
            v, _, _ = self._read_csv(fp)
            all_vals.append(v)
        self.scaler.fit(np.concatenate(all_vals, axis=0))

    def _build_index(self):
        files = sorted(glob.glob(os.path.join(self.split_dir, "*.csv")))
        if not files:
            raise RuntimeError(f"No CSVs found in {self.split_dir}")

        if self.scaler is not None:
            self._fit_scaler(files)

        counts = {}

        for fp in files:
            values, _, states = self._read_csv(fp)
            T = len(values)

            t1, t2, motif = self._get_twoflip_meta(fp, states)

            # NO_TRANS
            if t1 == "NO_TRANS":
                if self.include_no_transition:
                    n0 = len(self.samples)
                    # motif here is actually 'A' or 'B' from _get_twoflip_meta
                    self._add_no_transition_windows(fp, T, motif)
                    for it in self.samples[n0:]:
                        counts[it["tag"]] = counts.get(it["tag"], 0) + 1
                continue

            # require valid two flip
            if t1 is None or t2 is None:
                continue
            if not (0 <= int(t1) < int(t2) < T):
                continue

            # granular tags around t1 and t2
            n0 = len(self.samples)
            self._add_granular_around_anchor(fp, T, int(t1), "t1", int(t1), int(t2), motif)
            self._add_granular_around_anchor(fp, T, int(t2), "t2", int(t1), int(t2), motif)

            # semantic tags (placement × dwell × motif)
            if self.add_twoflip_semantic_tags:
                self._add_semantic_twoflip_tags(fp, T, int(t1), int(t2), motif)

            for it in self.samples[n0:]:
                counts[it["tag"]] = counts.get(it["tag"], 0) + 1

        if self.verbose:
            print(f"[{self.flag}] windows={len(self.samples)} | num_tags={len(counts)}")
            top = sorted(counts.items(), key=lambda x: -x[1])[:40]
            print(f"[{self.flag}] top tags: {top}")

        if len(self.samples) == 0:
            raise RuntimeError(
                "No samples created — check (seq_len, pred_len), boundary bins, and that meta has valid t1/t2."
            )

    # -------------------- torch API ------------------------------
    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        it = self.samples[idx]
        fp, s = it["fp"], int(it["s_beg"])

        values, ts, _ = self._read_csv(fp)
        if self.scaler is not None:
            values = self.scaler.transform(values).astype(np.float32)

        T = len(values)
        s_end, r_beg, r_end = self._window_end(s)
        if (s < 0) or (r_end > T):
            raise IndexError(f"Invalid window: fp={fp}, s={s}, r_end={r_end}, T={T}")

        x = values[s:s_end]
        y = values[r_beg:r_end]
        x_t = ts[s:s_end]
        y_t = ts[r_beg:r_end]

        b = s_end  # boundary
        t1 = int(it["t1"]) if it["t1"] is not None else -1
        t2 = int(it["t2"]) if it["t2"] is not None else -1

        boundary_offset1 = None if t1 < 0 else int(t1 - b)
        boundary_offset2 = None if t2 < 0 else int(t2 - b)
        dwell = 0 if (t1 < 0 or t2 < 0) else int(t2 - t1)

        meta = dict(
            tag=it["tag"],
            filename=os.path.basename(fp),
            filepath=fp,
            motif=it.get("motif", None),
            t1=t1,
            t2=t2,
            dwell=dwell,
            s_beg=s,
            s_end=s_end,
            r_beg=r_beg,
            r_end=r_end,
            boundary_offset1=boundary_offset1,
            boundary_offset2=boundary_offset2,
        )

        return x, y, x_t, y_t, meta






class EvalDataset_TwoCP_MergedGranularTags(Dataset):
    """
    Eval-only dataset for TWO-transition (t1,t2) sequences, BUT you asked to:

      1) Treat t1 and t2 as the "same kind of transition"
         -> we DO NOT output t1_* or t2_* tags.
         -> we output ONLY: hist_dXX / fut_dXX bins (granular distance to boundary),
            where candidates can come from EITHER transition (t1 OR t2).

      2) Add window-level no-transition tags:
         -> win_no_transition_A / win_no_transition_B
            meaning: within the FULL eval window [s : r_end), State never changes.

      3) Drop all high-level semantic tags (HH/HF/FF, dwell, motif).

    Output tags ONLY from this set:
      - win_no_transition_A
      - win_no_transition_B
      - hist_d02, hist_d04, ..., hist_d40  (or whatever bins you specify)
      - fut_d02,  fut_d04,  ..., fut_d40
    """

    def __init__(
        self,
        root_path,
        flag="test",
        size=(50, 0, 100),              # (seq_len, label_len, pred_len)
        target="Value",
        scale=False,

        # ---- bins for distance to boundary ----
        boundary_bins=(2, 4, 6, 10, 12, 15, 20, 30, 40),
        allow_transition_at_boundary=False,   # if True, include d=0 as hist_d00

        # ---- selection policy ----
        one_per_tag_per_file=True,            # IMPORTANT: at most one window per tag per file
        random_seed=42,
        verbose=True,

        # ---- metadata ----
        transition_meta_path=None,            # default: root_path/{flag}_transitions.csv

        # ---- window-level no-transition tags ----
        add_window_no_transition_tags=True,
        window_no_transition_one_per_file=True,
    ):
        assert flag in ["train", "val", "test"]
        self.root_path = root_path
        self.flag = flag
        self.split_dir = os.path.join(root_path, flag)

        self.seq_len, self.label_len, self.pred_len = map(int, size)
        self.target = target

        self.scale = bool(scale)
        if self.scale:
            if StandardScaler is None:
                raise ImportError("scikit-learn is required for scale=True (StandardScaler).")
            self.scaler = StandardScaler()
        else:
            self.scaler = None

        self.verbose = bool(verbose)
        self.rng = np.random.RandomState(int(random_seed))

        self.boundary_bins = [int(b) for b in boundary_bins]
        if not self.boundary_bins:
            raise ValueError("boundary_bins is empty")
        if self.boundary_bins != sorted(self.boundary_bins):
            raise ValueError("boundary_bins must be sorted ascending")
        if any(b < 0 for b in self.boundary_bins):
            raise ValueError("All boundary_bins must be >= 0")
        if any(b == 0 for b in self.boundary_bins) and (not allow_transition_at_boundary):
            raise ValueError("If you include bin 0, set allow_transition_at_boundary=True")

        # We require positive bins for the usual hist/fut; d=0 is optional
        if any(b <= 0 for b in self.boundary_bins) and (0 not in self.boundary_bins):
            raise ValueError("All boundary bins should be > 0 (use allow_transition_at_boundary for d=0)")

        self.allow_transition_at_boundary = bool(allow_transition_at_boundary)
        self.one_per_tag_per_file = bool(one_per_tag_per_file)

        if transition_meta_path is None:
            transition_meta_path = os.path.join(root_path, f"{flag}_transitions.csv")
        self.transition_meta_path = transition_meta_path

        self.add_window_no_transition_tags = bool(add_window_no_transition_tags)
        self.window_no_transition_one_per_file = bool(window_no_transition_one_per_file)

        # meta maps: filename/path -> row dict
        self.meta_by_name = {}
        self.meta_by_path = {}
        self._load_transition_map()

        self.samples = []
        self._build_index()

    # ----------------------------- IO -----------------------------
    def _read_csv(self, fp):
        df = pd.read_csv(fp)
        if self.target not in df.columns:
            raise ValueError(f"Missing target column '{self.target}' in {fp}")

        values = df[[self.target]].values.astype(np.float32)

        if "Time" in df.columns:
            try:
                t = pd.to_datetime(df["Time"])
                ts = (t.astype("int64") / 1e9).to_numpy().astype(np.float32)
            except Exception:
                ts = df["Time"].to_numpy().astype(np.float32)
        else:
            ts = np.arange(len(df), dtype=np.float32)
        ts = ts.reshape(-1, 1)

        states = None
        if "State" in df.columns:
            states = df["State"].to_numpy().astype(int)

        return values, ts, states

    # ----------------------- meta loading -------------------------
    def _load_transition_map(self):
        if not os.path.exists(self.transition_meta_path):
            if self.verbose:
                print(f"[{self.flag}] No transition meta found: {self.transition_meta_path}")
            return

        meta = pd.read_csv(self.transition_meta_path)

        required = {"filename", "t1_idx", "t2_idx"}
        missing = required - set(meta.columns)
        if missing:
            raise ValueError(
                f"Transition CSV must contain {sorted(list(required))}. Missing: {sorted(list(missing))}"
            )

        if "motif" not in meta.columns:
            meta["motif"] = "unknown"

        # Keep rows where either:
        # - two-flip: t1>=0, t2>=0
        # - NO_TRANS: motif == "NO_TRANS" or t1<0 and t2<0
        t1f = meta["t1_idx"].astype(float)
        t2f = meta["t2_idx"].astype(float)
        motif = meta["motif"].astype(str)

        valid_twoflip = np.isfinite(t1f) & np.isfinite(t2f) & (t1f >= 0) & (t2f >= 0)
        valid_notrans = np.isfinite(t1f) & np.isfinite(t2f) & ((motif == "NO_TRANS") | ((t1f < 0) & (t2f < 0)))

        mv = meta.loc[valid_twoflip | valid_notrans].copy()
        mv["t1_idx"] = mv["t1_idx"].astype(int)
        mv["t2_idx"] = mv["t2_idx"].astype(int)

        for _, r in mv.iterrows():
            fn = str(r["filename"])
            self.meta_by_name[fn] = r.to_dict()

        if "filepath" in mv.columns:
            for _, r in mv.iterrows():
                fp = os.path.abspath(str(r["filepath"]))
                self.meta_by_path[fp] = r.to_dict()

        if self.verbose:
            print(
                f"[{self.flag}] Loaded transition meta: {self.transition_meta_path} "
                f"(rows={len(meta)}, valid={len(mv)})"
            )

    def _get_twoflip_meta(self, fp, states):
        """
        Returns:
          - two-flip: (t1:int, t2:int)
          - no-trans: ("NO_TRANS", None, ab:str in {"A","B"})
          - missing:  (None, None, None)
        """
        base = os.path.basename(fp)
        fp_abs = os.path.abspath(fp)

        row = self.meta_by_name.get(base, None)
        if row is None:
            row = self.meta_by_path.get(fp_abs, None)

        if row is not None:
            motif = str(row.get("motif", "unknown"))
            t1 = int(row["t1_idx"])
            t2 = int(row["t2_idx"])

            if motif == "NO_TRANS" or (t1 < 0 and t2 < 0):
                state_id = row.get("const_state_id", None)
                if state_id is not None and not (isinstance(state_id, float) and np.isnan(state_id)):
                    state_id = int(state_id)
                else:
                    state_id = None
                    if states is not None and len(states) > 0:
                        state_id = int(states[0])
                ab = "A" if state_id == 0 else "B"
                return "NO_TRANS", None, ab

            return t1, t2, "TWOFLIP"

        # fallback: infer from states
        if states is None or len(states) == 0:
            return None, None, None

        ch = np.where(states[1:] != states[:-1])[0] + 1
        if len(ch) == 0:
            ab = "A" if int(states[0]) == 0 else "B"
            return "NO_TRANS", None, ab
        if len(ch) < 2:
            return None, None, None

        t1, t2 = int(ch[0]), int(ch[1])
        return t1, t2, "TWOFLIP"

    # ----------------------- window validity ----------------------
    def _window_end(self, s):
        s_end = s + self.seq_len
        r_beg = s_end - self.label_len
        r_end = r_beg + self.label_len + self.pred_len
        return s_end, r_beg, r_end

    def _valid_start(self, s, T):
        s = int(s)
        _, _, r_end = self._window_end(s)
        return (s >= 0) and (r_end <= T)

    def _append_sample(self, fp, s, tag, t1=None, t2=None):
        self.samples.append(
            dict(
                fp=fp,
                s_beg=int(s),
                tag=str(tag),
                t1=int(t1) if t1 is not None else -1,
                t2=int(t2) if t2 is not None else -1,
            )
        )

    # ---------------- NEW: window-level no-transition tags --------
    def _add_window_no_transition_tags(self, fp, T, states):
        """
        Adds:
          - win_no_transition_A if there exists a valid window with constant state 0 in [s:r_end)
          - win_no_transition_B if there exists a valid window with constant state 1 in [s:r_end)
        """
        if states is None:
            return

        s_min = 0
        s_max = T - (self.seq_len + self.pred_len)
        if s_max < s_min:
            return

        cand_A, cand_B = [], []

        for s in range(s_min, s_max + 1):
            if not self._valid_start(s, T):
                continue
            _, _, r_end = self._window_end(s)

            seg = states[int(s):int(r_end)]
            if len(seg) <= 1:
                continue
            if np.any(seg[1:] != seg[:-1]):
                continue  # has transition inside window

            st0 = int(seg[0])
            if st0 == 0:
                cand_A.append(s)
            else:
                cand_B.append(s)

        if cand_A:
            if self.window_no_transition_one_per_file:
                self._append_sample(fp, int(self.rng.choice(cand_A)), "win_no_transition_A")
            else:
                for s in cand_A:
                    self._append_sample(fp, int(s), "win_no_transition_A")

        if cand_B:
            if self.window_no_transition_one_per_file:
                self._append_sample(fp, int(self.rng.choice(cand_B)), "win_no_transition_B")
            else:
                for s in cand_B:
                    self._append_sample(fp, int(s), "win_no_transition_B")

    # ------------- merged granular tags for t1 OR t2 --------------
    def _add_merged_granular_tags(self, fp, T, t1, t2):
        """
        Treats both transitions as "same type".

        For each distance bin bmax, we create exactly these tags:
          - hist_dXX
          - fut_dXX

        Candidates for each tag can come from *either* anchor (t1 OR t2).
        If one_per_tag_per_file=True -> choose one s from union of candidates.
        """
        L = self.seq_len
        anchors = [int(t1), int(t2)]

        prev = 0
        for bmax in self.boundary_bins:
            if bmax == 0 and not self.allow_transition_at_boundary:
                continue

            # union candidates across anchors
            hist_union = []
            fut_union = []

            for t_anchor in anchors:
                # HIST side: t_anchor < b and prev < (b - t_anchor) <= bmax
                s_lo = int(t_anchor - L + (prev + 1))
                s_hi = int(t_anchor - L + bmax)
                for s in range(s_lo, s_hi + 1):
                    if not self._valid_start(s, T):
                        continue
                    b = s + L
                    d = int(b - t_anchor)
                    if (t_anchor < b) and (prev < d <= bmax):
                        hist_union.append(s)

                # FUT side: b < t_anchor and prev < (t_anchor - b) <= bmax
                s_lo = int(t_anchor - L - bmax)
                s_hi = int(t_anchor - L - (prev + 1))
                for s in range(s_lo, s_hi + 1):
                    if not self._valid_start(s, T):
                        continue
                    b = s + L
                    d = int(t_anchor - b)
                    if (b < t_anchor) and (prev < d <= bmax):
                        fut_union.append(s)

                # optional exact boundary: d=0
                if self.allow_transition_at_boundary and (prev == 0) and (0 in self.boundary_bins):
                    s0 = int(t_anchor - L)
                    if self._valid_start(s0, T):
                        # boundary case belongs to "hist_d00" by convention
                        hist_union.append(s0)

            # Deduplicate (important when two anchors contribute same s)
            if hist_union:
                hist_union = sorted(set(hist_union))
            if fut_union:
                fut_union = sorted(set(fut_union))

            # Add tags for this bin
            tag_h = f"hist_d{bmax:02d}"
            tag_f = f"fut_d{bmax:02d}"

            if hist_union:
                if self.one_per_tag_per_file:
                    s_choice = int(self.rng.choice(hist_union))
                    self._append_sample(fp, s_choice, tag_h, t1=t1, t2=t2)
                else:
                    for s_choice in hist_union:
                        self._append_sample(fp, int(s_choice), tag_h, t1=t1, t2=t2)

            if fut_union:
                if self.one_per_tag_per_file:
                    s_choice = int(self.rng.choice(fut_union))
                    self._append_sample(fp, s_choice, tag_f, t1=t1, t2=t2)
                else:
                    for s_choice in fut_union:
                        self._append_sample(fp, int(s_choice), tag_f, t1=t1, t2=t2)

            prev = bmax

    # ------------------- index building --------------------------
    def _fit_scaler(self, files):
        all_vals = []
        for fp in files:
            v, _, _ = self._read_csv(fp)
            all_vals.append(v)
        self.scaler.fit(np.concatenate(all_vals, axis=0))

    def _build_index(self):
        files = sorted(glob.glob(os.path.join(self.split_dir, "*.csv")))
        if not files:
            raise RuntimeError(f"No CSVs found in {self.split_dir}")

        if self.scaler is not None:
            self._fit_scaler(files)

        counts = {}

        for fp in files:
            values, _, states = self._read_csv(fp)
            T = len(values)

            t1, t2, kind = self._get_twoflip_meta(fp, states)

            # Always try to add window-level no-transition tags (if enabled),
            # regardless of whether file is NO_TRANS or TWOFLIP.
            if self.add_window_no_transition_tags:
                n0 = len(self.samples)
                self._add_window_no_transition_tags(fp, T, states)
                for it in self.samples[n0:]:
                    counts[it["tag"]] = counts.get(it["tag"], 0) + 1

            # If file is NO_TRANS, we do NOT add hist/fut distance-to-transition tags
            if t1 == "NO_TRANS":
                continue

            # Need valid t1,t2 for merged granular tags
            if t1 is None or t2 is None:
                continue
            if not (0 <= int(t1) < int(t2) < T):
                continue

            n0 = len(self.samples)
            self._add_merged_granular_tags(fp, T, int(t1), int(t2))
            for it in self.samples[n0:]:
                counts[it["tag"]] = counts.get(it["tag"], 0) + 1

        if self.verbose:
            print(f"[{self.flag}] windows={len(self.samples)} | num_tags={len(counts)}")
            top = sorted(counts.items(), key=lambda x: -x[1])[:50]
            print(f"[{self.flag}] top tags: {top}")

        if len(self.samples) == 0:
            raise RuntimeError(
                "No samples created — check (seq_len, pred_len), boundary_bins, and that State exists."
            )

    # -------------------- torch API ------------------------------
    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        it = self.samples[idx]
        fp, s = it["fp"], int(it["s_beg"])

        values, ts, _ = self._read_csv(fp)
        if self.scaler is not None:
            values = self.scaler.transform(values).astype(np.float32)

        T = len(values)
        s_end, r_beg, r_end = self._window_end(s)
        if (s < 0) or (r_end > T):
            raise IndexError(f"Invalid window: fp={fp}, s={s}, r_end={r_end}, T={T}")

        x = values[s:s_end]
        y = values[r_beg:r_end]
        x_t = ts[s:s_end]
        y_t = ts[r_beg:r_end]

        # Keep meta simple; you said you don't want high-level tags.
        # We still expose t1/t2 and offsets for debugging if needed.
        b = s_end
        t1 = int(it.get("t1", -1))
        t2 = int(it.get("t2", -1))
        boundary_offset1 = None if t1 < 0 else int(t1 - b)
        boundary_offset2 = None if t2 < 0 else int(t2 - b)

        meta = dict(
            tag=it["tag"],
            filename=os.path.basename(fp),
            filepath=fp,
            s_beg=s,
            s_end=s_end,
            r_beg=r_beg,
            r_end=r_end,
            t1=t1,
            t2=t2,
            boundary_offset1=boundary_offset1,
            boundary_offset2=boundary_offset2,
        )
        return x, y, x_t, y_t, meta


# class EvalDataset_UniformPlusTagsD(Dataset):
#     """
#     Eval-only dataset that yields *tagged* windows designed to probe adaptation speed
#     around a single transition point t_star.

#     This dataset is intended for validation/testing after a model is already trained.
#     It samples windows so that the transition occurs a controlled distance away from
#     the history/future boundary (the end of the encoder context).

#     -----------------------
#     Window Geometry
#     -----------------------
#     Let:
#         L = seq_len      (history length given to the model)
#         H = pred_len     (forecast horizon)
#         label_len        (decoder warmup length; kept for compatibility)
#         s                start index of a sample (history begins at s)

#     History window:
#         x = series[s : s+L]
#     Decoder target window (Informer-style):
#         y = series[(s+L-label_len) : (s+L-label_len) + (label_len + H)]
#     Boundary between history and future:
#         b = s + L

#     A transition time t_star is an integer index in the *full series timeline*.

#     -----------------------
#     Tags Produced (ONLY)
#     -----------------------
#     We create tags based on:
#         d = |t_star - b|

#     But we also separate *which side* of the boundary the transition is on.

#     HISTORY-side tags (transition occurs inside history):
#         t_star < b  and  d = b - t_star is in a distance band

#         hist_d05 :  0 < d <=  5
#         hist_d10 :  5 < d <= 10
#         hist_d15 : 10 < d <= 15
#         hist_d20 : 15 < d <= 20

#     FUTURE-side tags (transition occurs inside future):
#         t_star > b  and  d = t_star - b is in a distance band

#         fut_d05  :  0 < d <=  5
#         fut_d10  :  5 < d <= 10
#         fut_d15  : 10 < d <= 15
#         fut_d20  : 15 < d <= 20

#     Notes:
#       - Exact boundary case d=0 (t_star == b) is excluded by design.
#       - If t_star is missing (None), the file contributes no tagged samples.
#       - By default, we create at most ONE window per tag per file (randomly sampled
#         among all valid candidates for that tag).

#     -----------------------
#     Returned by __getitem__
#     -----------------------
#     Returns:
#         x       : (L, 1) float32
#         y       : (label_len + H, 1) float32
#         x_stamp : (L, 1) float32 timestamp (or indices) for x
#         y_stamp : (label_len + H, 1) float32 timestamp (or indices) for y
#         meta    : dict with fields:
#                  - tag
#                  - filename, filepath
#                  - t_star
#                  - s_beg, s_end, r_beg, r_end
#                  - boundary_offset = t_star - (s+L)
#                    (negative => transition in history; positive => in future)
#     """

#     def __init__(
#         self,
#         root_path,
#         flag="test",
#         size=(50, 0, 100),            # (seq_len, label_len, pred_len)
#         target="Value",
#         add_tags=True,
#         scale=False,                  # kept for compatibility (unused)
#         boundary_bins=(5, 10, 15, 20),
#         transition_meta_path=None,
#         random_seed=42,
#         verbose=True,
#     ):
#         assert flag in ["train", "val", "test"]

#         self.root_path = root_path
#         self.flag = flag
#         self.split_dir = os.path.join(root_path, flag)

#         self.seq_len, self.label_len, self.pred_len = map(int, size)
#         self.target = target

#         self.add_tags = bool(add_tags)
#         self.scale = bool(scale)
#         self.verbose = bool(verbose)

#         self.boundary_bins = [int(b) for b in boundary_bins]
#         if self.boundary_bins != sorted(self.boundary_bins):
#             raise ValueError("boundary_bins must be sorted ascending, e.g., (5,10,15,20)")

#         self.rng = np.random.RandomState(int(random_seed))

#         if transition_meta_path is None:
#             transition_meta_path = os.path.join(root_path, f"{flag}_transitions.csv")
#         self.transition_meta_path = transition_meta_path

#         self.transition_map_by_name = None
#         self.transition_map_by_path = None
#         self._load_transition_map()

#         self.samples = []
#         self._build_index()

#     # ------------------------------------------------------------------
#     # Transition metadata
#     # ------------------------------------------------------------------
#     def _load_transition_map(self):
#         """
#         Loads a CSV that maps each file to its transition index t_star.

#         Expected columns:
#           - filename (required): usually the CSV basename (including .csv)
#           - t_star_idx (required): integer transition index
#         Optional:
#           - filepath: full path; used if filename mapping fails

#         If the CSV uses `transition_idx` instead of `t_star_idx`, it is accepted.
#         """
#         if not os.path.exists(self.transition_meta_path):
#             if self.verbose:
#                 print(f"[{self.flag}] No transition meta found: {self.transition_meta_path}")
#             return

#         meta = pd.read_csv(self.transition_meta_path)

#         if "t_star_idx" not in meta.columns:
#             if "transition_idx" in meta.columns:
#                 meta = meta.rename(columns={"transition_idx": "t_star_idx"})
#             else:
#                 raise ValueError("Transition CSV must contain t_star_idx (or transition_idx)")

#         if "filename" not in meta.columns:
#             raise ValueError("Transition CSV must contain filename")

#         valid = meta["t_star_idx"].notna() & np.isfinite(meta["t_star_idx"].astype(float))
#         meta_valid = meta.loc[valid].copy()
#         meta_valid["t_star_idx"] = meta_valid["t_star_idx"].astype(int)

#         self.transition_map_by_name = dict(
#             zip(meta_valid["filename"].astype(str), meta_valid["t_star_idx"])
#         )

#         if "filepath" in meta_valid.columns:
#             self.transition_map_by_path = dict(
#                 zip(meta_valid["filepath"].astype(str), meta_valid["t_star_idx"])
#             )

#         if self.verbose:
#             print(
#                 f"[{self.flag}] Loaded transition meta: {self.transition_meta_path} "
#                 f"(rows={len(meta)}, valid_tstar={len(meta_valid)})"
#             )

#     # ------------------------------------------------------------------
#     # CSV reading
#     # ------------------------------------------------------------------
#     def _read_csv(self, fp):
#         """
#         Reads a CSV time series file.

#         Required:
#           - self.target column (default "Value")

#         Optional:
#           - "Time" column (parsed to numeric seconds if possible)
#           - "State" column (used as fallback to infer t_star if meta is absent)

#         Returns:
#           values: (T, 1) float32
#           ts    : (T, 1) float32
#           states: (T,) int or None
#         """
#         df = pd.read_csv(fp)
#         if self.target not in df.columns:
#             raise ValueError(f"Missing target column '{self.target}' in {fp}")

#         values = df[[self.target]].values.astype(np.float32)

#         if "Time" in df.columns:
#             try:
#                 t = pd.to_datetime(df["Time"])
#                 ts = (t.astype("int64") / 1e9).to_numpy().astype(np.float32)
#             except Exception:
#                 ts = df["Time"].to_numpy().astype(np.float32)
#         else:
#             ts = np.arange(len(df), dtype=np.float32)

#         ts = ts.reshape(-1, 1)

#         states = None
#         if "State" in df.columns:
#             states = df["State"].to_numpy().astype(int)

#         return values, ts, states

#     def _infer_transition_idx(self, fp, states):
#         """
#         Retrieves t_star for a given file.

#         Priority:
#           1) transition_map_by_name using basename (with extension)
#           2) transition_map_by_path using full path (if present)
#           3) fallback: infer from `State` column by first change-point

#         Returns:
#           t_star (int) or None
#         """
#         base = os.path.basename(fp)

#         if self.transition_map_by_name is not None:
#             t = self.transition_map_by_name.get(base, None)
#             if t is not None:
#                 return int(t)

#         if self.transition_map_by_path is not None:
#             t = self.transition_map_by_path.get(fp, None)
#             if t is not None:
#                 return int(t)

#         if states is None:
#             return None

#         change = np.where(states[1:] != states[:-1])[0]
#         if len(change) == 0:
#             return None
#         return int(change[0] + 1)

#     # ------------------------------------------------------------------
#     # Window helpers
#     # ------------------------------------------------------------------
#     def _valid_start(self, s, T):
#         """
#         Checks whether start index s yields a valid (x,y) window within the sequence.

#         Uses the Informer-style target window:
#           x: [s, s+L)
#           y: [s+L-label_len, s+L-label_len + label_len+H)

#         Valid iff y end <= T.
#         """
#         s = int(s)
#         s_end = s + self.seq_len
#         r_beg = s_end - self.label_len
#         r_end = r_beg + self.label_len + self.pred_len
#         return (s >= 0) and (r_end <= T)

#     def _append_sample(self, fp, s, tag, t_star):
#         """Adds one sample entry to the index."""
#         self.samples.append(
#             dict(
#                 fp=fp,
#                 s_beg=int(s),
#                 tag=str(tag),
#                 t_star=None if t_star is None else int(t_star),
#             )
#         )

#     # ------------------------------------------------------------------
#     # Tags (hist/fut distance bins ONLY)
#     # ------------------------------------------------------------------
#     def _add_tag_windows(self, fp, T, t_star):
#         """
#         Adds up to one window per tag per file.

#         Key relations:
#           boundary b = s + L

#         HISTORY side (t_star < b):
#           d = b - t_star  in (prev, b]
#           s = (t_star + d) - L  => s in [t_star - L + (prev+1), t_star - L + b]

#         FUTURE side (t_star > b):
#           d = t_star - b  in (prev, b]
#           s = (t_star - d) - L  => s in [t_star - L - b, t_star - L - (prev+1)]
#         """
#         if t_star is None:
#             return

#         L = self.seq_len
#         bins = list(self.boundary_bins)
#         prev = 0

#         def boundary(s):  # b = s + L
#             return s + L

#         for bmax in bins:
#             # -------------------------
#             # HISTORY side: transition in history (t_star < boundary)
#             # d = boundary - t_star in (prev, bmax]
#             # s in [t_star - L + (prev+1), t_star - L + bmax]
#             # -------------------------
#             tag_h = f"hist_d{bmax:02d}"
#             s_lo = int(t_star - L + (prev + 1))
#             s_hi = int(t_star - L + bmax)

#             hist_candidates = []
#             for s in range(s_lo, s_hi + 1):
#                 if not self._valid_start(s, T):
#                     continue
#                 d = int(boundary(s) - t_star)  # positive by construction
#                 if (prev < d) and (d <= bmax):
#                     hist_candidates.append(s)

#             if hist_candidates:
#                 s_choice = int(self.rng.choice(hist_candidates))
#                 self._append_sample(fp, s_choice, tag_h, t_star)

#             # -------------------------
#             # FUTURE side: transition in future (t_star > boundary)
#             # d = t_star - boundary in (prev, bmax]
#             # s in [t_star - L - bmax, t_star - L - (prev+1)]
#             # -------------------------
#             tag_f = f"fut_d{bmax:02d}"
#             s_lo = int(t_star - L - bmax)
#             s_hi = int(t_star - L - (prev + 1))

#             fut_candidates = []
#             for s in range(s_lo, s_hi + 1):
#                 if not self._valid_start(s, T):
#                     continue
#                 d = int(t_star - boundary(s))  # positive by construction
#                 if (prev < d) and (d <= bmax):
#                     fut_candidates.append(s)

#             if fut_candidates:
#                 s_choice = int(self.rng.choice(fut_candidates))
#                 self._append_sample(fp, s_choice, tag_f, t_star)

#             prev = bmax

#     # ------------------------------------------------------------------
#     # Index builder
#     # ------------------------------------------------------------------
#     def _build_index(self):
#         """
#         Builds the list of samples:
#           - for each CSV in split_dir:
#               infer t_star
#               add tagged windows (hist/fut bins)
#         """
#         files = sorted(glob.glob(os.path.join(self.split_dir, "*.csv")))
#         if not files:
#             raise RuntimeError(f"No CSVs found in {self.split_dir}")

#         tag_names = [f"hist_d{b:02d}" for b in self.boundary_bins] + \
#                     [f"fut_d{b:02d}"  for b in self.boundary_bins]
#         counts = {k: 0 for k in tag_names}

#         for fp in files:
#             values, _, states = self._read_csv(fp)
#             T = len(values)
#             t_star = self._infer_transition_idx(fp, states)

#             # if no transition known, contribute nothing
#             if t_star is None:
#                 continue

#             # if transition index is out of file range, skip
#             if not (0 <= int(t_star) < T):
#                 continue

#             if self.add_tags:
#                 n0 = len(self.samples)
#                 self._add_tag_windows(fp, T, int(t_star))
#                 for s in self.samples[n0:]:
#                     counts[s["tag"]] += 1

#         if self.verbose:
#             print(f"[{self.flag}] windows={len(self.samples)} | {counts}")

#         if len(self.samples) == 0:
#             raise RuntimeError(
#                 "No samples created — this means your (seq_len, pred_len) and bins "
#                 "do not yield any valid boundary-near windows for the transitions."
#             )

#     # ------------------------------------------------------------------
#     # PyTorch API
#     # ------------------------------------------------------------------
#     def __len__(self):
#         return len(self.samples)

#     def __getitem__(self, idx):
#         it = self.samples[idx]
#         fp, s = it["fp"], it["s_beg"]

#         values, ts, _ = self._read_csv(fp)
#         T = len(values)

#         s_end = s + self.seq_len
#         r_beg = s_end - self.label_len
#         r_end = r_beg + self.label_len + self.pred_len

#         if (s < 0) or (r_end > T):
#             raise IndexError(f"Invalid window: fp={fp}, s={s}, r_end={r_end}, T={T}")

#         x = values[s:s_end]
#         y = values[r_beg:r_end]
#         x_t = ts[s:s_end]
#         y_t = ts[r_beg:r_end]

#         # boundary_offset = t_star - boundary (negative => in history, positive => in future)
#         boundary_offset = None
#         if it["t_star"] is not None:
#             boundary_offset = int(it["t_star"] - s_end)

#         meta = dict(
#             tag=it["tag"],
#             filename=os.path.basename(fp),
#             filepath=fp,
#             t_star=it["t_star"],
#             s_beg=s,
#             s_end=s_end,
#             r_beg=r_beg,
#             r_end=r_end,
#             boundary_offset=boundary_offset,
#         )

#         return x, y, x_t, y_t, meta


class EvalDataset_UniformPlusTagsD(Dataset):
    """
    Eval-only dataset that yields tagged windows around a single transition t_star,
    PLUS two extra *window-level* tags:

      - win_no_transition_A : the entire (history+future target) window has constant State==0
      - win_no_transition_B : the entire (history+future target) window has constant State==1

    NOTE: These window-level tags are NOT about "no transition in the whole file".
          They are about "no transition inside THIS specific window".

    Tags (transition-distance, per file, at most one window per tag):
      hist_d05, hist_d10, ...   (t_star in history)
      fut_d05,  fut_d10,  ...   (t_star in future)

    Window-level tags (per file, at most one per A and one per B, unless you disable one-per-file):
      win_no_transition_A
      win_no_transition_B
    """

    def __init__(
        self,
        root_path,
        flag="test",
        size=(50, 0, 100),            # (seq_len, label_len, pred_len)
        target="Value",
        add_tags=True,
        boundary_bins=(5, 10, 15, 20),
        transition_meta_path=None,
        random_seed=42,
        verbose=True,

        # ---------------- NEW ----------------
        add_window_no_transition_tags=True,
        window_no_transition_one_per_file=True,
        # -------------------------------------
    ):
        assert flag in ["train", "val", "test"]

        self.root_path = root_path
        self.flag = flag
        self.split_dir = os.path.join(root_path, flag)

        self.seq_len, self.label_len, self.pred_len = map(int, size)
        self.target = target

        self.add_tags = bool(add_tags)
        self.verbose = bool(verbose)

        self.boundary_bins = [int(b) for b in boundary_bins]
        if self.boundary_bins != sorted(self.boundary_bins):
            raise ValueError("boundary_bins must be sorted ascending, e.g., (5,10,15,20)")

        self.rng = np.random.RandomState(int(random_seed))

        if transition_meta_path is None:
            transition_meta_path = os.path.join(root_path, f"{flag}_transitions.csv")
        self.transition_meta_path = transition_meta_path

        # transition maps
        self.transition_map_by_name = None
        self.transition_map_by_path = None
        self._load_transition_map()

        # NEW: window-level no-transition tags
        self.add_window_no_transition_tags = bool(add_window_no_transition_tags)
        self.window_no_transition_one_per_file = bool(window_no_transition_one_per_file)

        self.samples = []
        self._build_index()

    # ------------------------------------------------------------------
    # Transition metadata
    # ------------------------------------------------------------------
    def _load_transition_map(self):
        if not os.path.exists(self.transition_meta_path):
            if self.verbose:
                print(f"[{self.flag}] No transition meta found: {self.transition_meta_path}")
            return

        meta = pd.read_csv(self.transition_meta_path)

        if "t_star_idx" not in meta.columns:
            if "transition_idx" in meta.columns:
                meta = meta.rename(columns={"transition_idx": "t_star_idx"})
            else:
                raise ValueError("Transition CSV must contain t_star_idx (or transition_idx)")

        if "filename" not in meta.columns:
            raise ValueError("Transition CSV must contain filename")

        valid = meta["t_star_idx"].notna() & np.isfinite(meta["t_star_idx"].astype(float))
        meta_valid = meta.loc[valid].copy()
        meta_valid["t_star_idx"] = meta_valid["t_star_idx"].astype(int)

        self.transition_map_by_name = dict(
            zip(meta_valid["filename"].astype(str), meta_valid["t_star_idx"])
        )

        if "filepath" in meta_valid.columns:
            self.transition_map_by_path = dict(
                zip(meta_valid["filepath"].astype(str), meta_valid["t_star_idx"])
            )

        if self.verbose:
            print(
                f"[{self.flag}] Loaded transition meta: {self.transition_meta_path} "
                f"(rows={len(meta)}, valid_tstar={len(meta_valid)})"
            )

    # ------------------------------------------------------------------
    # CSV reading
    # ------------------------------------------------------------------
    def _read_csv(self, fp):
        df = pd.read_csv(fp)
        if self.target not in df.columns:
            raise ValueError(f"Missing target column '{self.target}' in {fp}")

        values = df[[self.target]].values.astype(np.float32)

        if "Time" in df.columns:
            try:
                t = pd.to_datetime(df["Time"])
                ts = (t.astype("int64") / 1e9).to_numpy().astype(np.float32)
            except Exception:
                ts = df["Time"].to_numpy().astype(np.float32)
        else:
            ts = np.arange(len(df), dtype=np.float32)

        ts = ts.reshape(-1, 1)

        states = None
        if "State" in df.columns:
            states = df["State"].to_numpy().astype(int)

        return values, ts, states

    def _infer_transition_idx(self, fp, states):
        base = os.path.basename(fp)

        if self.transition_map_by_name is not None:
            t = self.transition_map_by_name.get(base, None)
            if t is not None:
                return int(t)

        if self.transition_map_by_path is not None:
            t = self.transition_map_by_path.get(fp, None)
            if t is not None:
                return int(t)

        # fallback: infer from state changes in the whole file
        if states is None:
            return None
        change = np.where(states[1:] != states[:-1])[0]
        if len(change) == 0:
            return None
        return int(change[0] + 1)

    # ------------------------------------------------------------------
    # Window helpers
    # ------------------------------------------------------------------
    def _window_endpoints(self, s):
        s = int(s)
        s_end = s + self.seq_len
        r_beg = s_end - self.label_len
        r_end = r_beg + self.label_len + self.pred_len
        return s_end, r_beg, r_end

    def _valid_start(self, s, T):
        s_end, r_beg, r_end = self._window_endpoints(s)
        return (s >= 0) and (r_end <= T)

    def _append_sample(self, fp, s, tag, t_star):
        self.samples.append(
            dict(
                fp=fp,
                s_beg=int(s),
                tag=str(tag),
                t_star=None if t_star is None else int(t_star),
            )
        )

    # ------------------------------------------------------------------
    # Transition-distance tags (hist/fut bins)
    # ------------------------------------------------------------------
    def _add_transition_distance_tag_windows(self, fp, T, t_star):
        """
        Adds up to one window per {hist_dXX, fut_dXX} tag for this file.
        """
        if t_star is None:
            return

        L = self.seq_len
        prev = 0

        def boundary(s):
            return s + L

        for bmax in self.boundary_bins:
            # HISTORY side: d = (s+L) - t_star in (prev, bmax]
            tag_h = f"hist_d{bmax:02d}"
            s_lo = int(t_star - L + (prev + 1))
            s_hi = int(t_star - L + bmax)

            hist_candidates = []
            for s in range(s_lo, s_hi + 1):
                if not self._valid_start(s, T):
                    continue
                d = int(boundary(s) - t_star)
                if (prev < d) and (d <= bmax):
                    hist_candidates.append(s)

            if hist_candidates:
                s_choice = int(self.rng.choice(hist_candidates))
                self._append_sample(fp, s_choice, tag_h, t_star)

            # FUTURE side: d = t_star - (s+L) in (prev, bmax]
            tag_f = f"fut_d{bmax:02d}"
            s_lo = int(t_star - L - bmax)
            s_hi = int(t_star - L - (prev + 1))

            fut_candidates = []
            for s in range(s_lo, s_hi + 1):
                if not self._valid_start(s, T):
                    continue
                d = int(t_star - boundary(s))
                if (prev < d) and (d <= bmax):
                    fut_candidates.append(s)

            if fut_candidates:
                s_choice = int(self.rng.choice(fut_candidates))
                self._append_sample(fp, s_choice, tag_f, t_star)

            prev = bmax

    # ------------------------------------------------------------------
    # NEW: window-level no-transition tags (within [s, r_end))
    # ------------------------------------------------------------------
    def _add_window_no_transition_tags(self, fp, T, states):
        """
        Adds:
          - win_no_transition_A if exists at least one valid window with constant state 0
          - win_no_transition_B if exists at least one valid window with constant state 1

        Decision is per-window, scanning states[s:r_end].
        """
        if states is None:
            return

        # valid start range (fast bound)
        s_min = 0
        s_max = T - (self.seq_len + self.pred_len)  # label_len=0 typical; _valid_start will enforce exact
        if s_max < s_min:
            return

        cand_A, cand_B = [], []

        for s in range(s_min, s_max + 1):
            if not self._valid_start(s, T):
                continue
            _, _, r_end = self._window_endpoints(s)

            seg = states[int(s):int(r_end)]
            if len(seg) <= 1:
                continue

            # if any change -> not a "no-transition window"
            if np.any(seg[1:] != seg[:-1]):
                continue

            # constant
            st0 = int(seg[0])
            if st0 == 0:
                cand_A.append(s)
            else:
                cand_B.append(s)

        if cand_A:
            if self.window_no_transition_one_per_file:
                self._append_sample(fp, int(self.rng.choice(cand_A)), "win_no_transition_A", t_star=None)
            else:
                for s in cand_A:
                    self._append_sample(fp, int(s), "win_no_transition_A", t_star=None)

        if cand_B:
            if self.window_no_transition_one_per_file:
                self._append_sample(fp, int(self.rng.choice(cand_B)), "win_no_transition_B", t_star=None)
            else:
                for s in cand_B:
                    self._append_sample(fp, int(s), "win_no_transition_B", t_star=None)

    # ------------------------------------------------------------------
    # Index builder
    # ------------------------------------------------------------------
    def _build_index(self):
        files = sorted(glob.glob(os.path.join(self.split_dir, "*.csv")))
        if not files:
            raise RuntimeError(f"No CSVs found in {self.split_dir}")

        # for debug print
        base_tag_names = (
            [f"hist_d{b:02d}" for b in self.boundary_bins] +
            [f"fut_d{b:02d}"  for b in self.boundary_bins]
        )
        if self.add_window_no_transition_tags:
            base_tag_names += ["win_no_transition_A", "win_no_transition_B"]

        counts = {k: 0 for k in base_tag_names}

        for fp in files:
            values, _, states = self._read_csv(fp)
            T = len(values)

            # 1) transition-distance tags (need t_star)
            t_star = self._infer_transition_idx(fp, states)
            if self.add_tags and (t_star is not None) and (0 <= int(t_star) < T):
                n0 = len(self.samples)
                self._add_transition_distance_tag_windows(fp, T, int(t_star))
                for it in self.samples[n0:]:
                    counts[it["tag"]] = counts.get(it["tag"], 0) + 1

            # 2) window-level no-transition tags (do NOT need t_star)
            if self.add_window_no_transition_tags:
                n0 = len(self.samples)
                self._add_window_no_transition_tags(fp, T, states)
                for it in self.samples[n0:]:
                    counts[it["tag"]] = counts.get(it["tag"], 0) + 1

        if self.verbose:
            print(f"[{self.flag}] windows={len(self.samples)} | {counts}")

        if len(self.samples) == 0:
            raise RuntimeError(
                "No samples created — check (seq_len, pred_len), boundary_bins, "
                "and whether 'State' exists for window-level tags."
            )

    # ------------------------------------------------------------------
    # PyTorch API
    # ------------------------------------------------------------------
    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        it = self.samples[idx]
        fp, s = it["fp"], it["s_beg"]

        values, ts, _ = self._read_csv(fp)
        T = len(values)

        s_end, r_beg, r_end = self._window_endpoints(s)

        if (s < 0) or (r_end > T):
            raise IndexError(f"Invalid window: fp={fp}, s={s}, r_end={r_end}, T={T}")

        x = values[s:s_end]
        y = values[r_beg:r_end]
        x_t = ts[s:s_end]
        y_t = ts[r_beg:r_end]

        boundary_offset = None
        if it["t_star"] is not None:
            boundary_offset = int(it["t_star"] - s_end)

        meta = dict(
            tag=it["tag"],
            filename=os.path.basename(fp),
            filepath=fp,
            t_star=it["t_star"],
            s_beg=int(s),
            s_end=int(s_end),
            r_beg=int(r_beg),
            r_end=int(r_end),
            boundary_offset=boundary_offset,
        )

        return x, y, x_t, y_t, meta