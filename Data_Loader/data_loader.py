from torch.utils.data import DataLoader
from Data_Creator.data_creator import (
    Dataset_Custom,
    Dataset_Custom_State,
    TrainDataset_UniformPlusCentered,
    TrainDataset_UniformPlusCentered_TwoCP,
    EvalDataset_UniformPlusTagsD,
    EvalDataset_TwoCP_GranularTags,
    EvalDataset_TwoCP_MergedGranularTags
)
from torch.utils.data._utils.collate import default_collate

def collate_with_meta(batch):
    """
    batch items are either:
      (x, y, x_mark, y_mark, meta_dict)
    or  (x, y, x_mark, y_mark)  # fallback

    We collate tensors normally, but keep meta as a python list (so None is allowed).
    """
    if len(batch[0]) == 5:
        x, y, x_mark, y_mark, meta = zip(*batch)  # tuples of length B
        return default_collate(x), default_collate(y), default_collate(x_mark), default_collate(y_mark), list(meta)
    else:
        return default_collate(batch)


data_dict = {
    "custom": Dataset_Custom,  #This is used for normal transition, normal markov probabilit tranisition
    "custom_test":Dataset_Custom_State, #This is for checking if markov probability are maintained in the prediction 
    #"single_train": TrainDataset_UniformPlusCentered,
    "single_train": TrainDataset_UniformPlusCentered_TwoCP, 
    # "single_test": EvalDataset_TwoCP_GranularTags,
    "single_test": EvalDataset_TwoCP_MergedGranularTags,
    # "single_test": EvalDataset_UniformPlusTagsD,

}

def data_provider(args, flag):
    """
    flag: 'train' | 'val' | 'test' | 'pred'
    args.data:
        - 'single_train' : TrainDataset_UniformPlusCentered (train only)
        - 'single_test'  : EvalDataset_UniformPlusSpecial4 (val/test only) -> uniform + pre/centered/mixed/post
        - 'custom'       : Dataset_Custom (default)
    """
    timeenc = 0 if args.embed != "timeF" else 1
    DataClass = data_dict[args.data]

    # ==========================================================
    # 1) SPECIAL TRAIN LOADER: uniform + centered oversampling
    # ==========================================================
    if args.data=="custom_test":
        dataset = DataClass(
            root_path=args.root_path,
            flag="test",
            size=(args.seq_len, 0, args.pred_len),
            target=args.target,
            scale=False,
        )



    if args.data == "single_train":
        dataset = DataClass(
                root_path=args.root_path,
                size=(args.seq_len, args.label_len, args.pred_len),
                target=args.target,
                scale=args.scale,

                # ---- centered/uniform controls ----
                uniform_stride=getattr(args, "uniform_stride", 1),
                add_uniform=True,
                add_centered=True,
                centered_per_file=getattr(args, "centered_per_file", 120),
                centered_jitter=getattr(args, "centered_jitter", 20),
                centered_history_frac=getattr(args, "centered_history_frac", 0.6),
                centered_weight=getattr(args, "centered_weight", 4.0),
                random_seed=args.seed,

                transition_meta_path=getattr(args, "transition_meta_path", None),
            )

        loader = DataLoader(
                dataset,
                batch_size=args.batch_size,
                shuffle=True,
                num_workers=args.num_workers,
                drop_last=True,
            )
        print(f"{flag} set size: {len(dataset)}")
        return dataset, loader

    # ==========================================================
    # 2) SPECIAL TEST/VAL LOADER: uniform + FOUR special cases
    #    pre / centered / mixed / post  (tagged in meta['tag'])
    # ==========================================================
    if args.data == "single_test":
        if flag not in ["val", "test"]:
            raise ValueError("single_test dataset is intended for val/test only.")

        # dataset = DataClass(
        #     root_path=args.root_path,
        #     flag=flag,
        #     size=(args.seq_len, args.label_len, args.pred_len),
        #     target=args.target,

        #     # --- uniform windows ---
        #     uniform_stride=getattr(args, "uniform_stride", 1),
        #     add_uniform=True,

        #     # --- special 4 windows ---
        #     add_special4=True,
        #     centered_history_frac=getattr(args, "centered_history_frac", 0.6),
        #     pre_margin=getattr(args, "pre_margin", 40),
        #     post_margin=getattr(args, "post_margin", 40),

        #     # --- transition meta ---
        #     transition_meta_path=getattr(args, "transition_meta_path", None),

        #     # optional logging
        #     verbose=getattr(args, "verbose", True),
        # )
        # dataset = EvalDataset_UniformPlusTags(
        #         root_path=args.root_path,
        #         flag="test",
        #         size=(args.seq_len, args.label_len, args.pred_len),
        #         target=args.target,
        #         uniform_stride=1,
        #         add_uniform=True,
        #         add_tags=True,
        #         hist_begin_range=(0.10, 0.20),
        #         hist_mid_range=(0.45, 0.55),
        #         hist_end_range=(0.80, 0.90),
        #         pre_margin=5,
        #         post_margin=5,
        #         transition_meta_path=getattr(args, "transition_meta_path", None)
        # )
        # dataset = EvalDataset_UniformPlusTags9(
        #     root_path=args.root_path,
        #     flag="test",
        #     size=(args.seq_len, args.label_len, args.pred_len),
        #     target=args.target,

        #     uniform_stride=1,
        #     add_uniform=True,
        #     add_tags=True,

        #     # margins only (still used)
        #     pre_margin=5,
        #     post_margin=5,

        #     transition_meta_path=getattr(args, "transition_meta_path", None),
        # )
        # dataset = EvalDataset_UniformPlusTagsD(
        #         root_path=args.root_path,
        #         flag="test",
        #         size=(args.seq_len, args.label_len, args.pred_len),
        #         boundary_bins=(2, 4, 6, 8, 10, 12, 15, 20, 30, 40),
        #         random_seed=42,
        #         verbose=True,
        #         transition_meta_path=getattr(args, "transition_meta_path", None),
        #     )
        # dataset = EvalDataset_TwoCP_MergedGranularTags(
        #     root_path=args.root_path,
        #     flag="test",
        #     size=(args.seq_len, args.label_len, args.pred_len),
        #     target=args.target,
        #     boundary_bins=(2, 4, 6, 8, 10, 12, 15, 20, 30, 40),
        #     add_window_no_transition_tags=True,
        #     window_no_transition_one_per_file=True,
        #     random_seed=42,
        #     transition_meta_path=getattr(args, "transition_meta_path", None),
        # )

        # dataset= EvalDataset_UniformPlusTagsD(
        #     root_path=args.root_path,
        #     flag="test",
        #     size=(args.seq_len, args.label_len, args.pred_len),
        #     target=args.target,
    

        #     # # margins only (still used)
        #     # pre_margin=5,
        #     # post_margin=5,

        #     transition_meta_path=getattr(args, "transition_meta_path", None),
        # )

    
        # dataset=EvalDataset_TwoFlip_AdaptOnly(
        #     root_path=args.root_path,
        #     flag="test",
        #     size=(args.seq_len, args.label_len, args.pred_len),
        #     target=args.target,

        #     strict=True,
        #     verbose=True,

        #     transition_meta_path=getattr(args, "transition_meta_path", None),
        # )

        loader = DataLoader(
            dataset,
            batch_size=args.batch_size,
            shuffle=False,
            num_workers=args.num_workers,
            drop_last=False,
            collate_fn=collate_with_meta,
        )
        print(f"{flag} set size: {len(dataset)}")
        return dataset, loader

    # ==========================================================
    # 3) DEFAULT: Dataset_Custom (your original behavior)
    # ==========================================================
    if flag == "train":
        random_sample_size = args.train_sample_size
        random_seed = args.seed
    elif flag == "val":
        random_sample_size = args.val_sample_size
        random_seed = args.seed
    elif flag == "test":
        random_sample_size = args.test_sample_size
        random_seed = args.seed
    else:
        random_sample_size = 2
        random_seed = 42

    dataset = DataClass(
        root_path=args.root_path,
        flag=flag,
        size=[args.seq_len, args.label_len, args.pred_len],
        features=args.features,
        target=args.target,
        scale=args.scale,
        timeenc=timeenc,
        freq=args.freq,
        random_sample_size=random_sample_size,
        random_seed=random_seed,
    )

    if flag == "train":
        shuffle_flag = True
        drop_last = True
        batch_size = args.batch_size
    elif flag == "val":
        shuffle_flag = False
        drop_last = True
        batch_size = args.batch_size
    elif flag in ["test", "pred"]:
        shuffle_flag = False
        drop_last = (flag == "test")
        batch_size = (1 if flag == "pred" else args.batch_size)
    else:
        raise ValueError(f"Unknown flag: {flag}")

    loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle_flag,
        num_workers=args.num_workers,
        drop_last=drop_last,
    )

    print(f"{flag} set size: {len(dataset)}")
    return dataset, loader
