import logging
from os.path import join
from typing import List, Tuple

import numpy as np
from n2v.internals.N2V_DataGenerator import N2V_DataGenerator


def extract_patches(
    imgs: List[np.array], num_patches_per_img: int, patch_shape: Tuple[int]
):
    datagen = N2V_DataGenerator()
    split = int(min(max(len(imgs) * 0.1, 1), 500))
    X_val = datagen.generate_patches_from_list(
        imgs[:split],
        num_patches_per_img=num_patches_per_img,
        shape=patch_shape,
        augment=False,
    )
    X = datagen.generate_patches_from_list(
        imgs[split:], num_patches_per_img=num_patches_per_img, shape=patch_shape
    )

    return X, X_val


def save_train_val_data(output_dir, prefix, X, X_val, logger=logging):
    logger.info(f"Training data shape: {X.shape}")
    logger.info(f"Validation data shape: {X_val.shape}")

    train_data_path = join(output_dir, prefix + "_n2v_2D_train.npz")
    np.savez(train_data_path, X=X)
    logger.info(f"Saved train data to: {train_data_path}")

    val_data_path = join(output_dir, prefix + "_n2v_2D_val.npz")
    np.savez(val_data_path, X_val=X_val)
    logger.info(f"Saved validation data to: {val_data_path}")
