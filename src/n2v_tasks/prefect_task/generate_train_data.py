from typing import List, Tuple

import numpy as np
import prefect
from prefect import task

from n2v_tasks.task.generate_train_data import extract_patches, save_train_val_data


@task(nout=2)
def extract_patches_task(
    imgs: List[np.array], num_patches_per_img: int, patch_shape: Tuple[int]
):
    return extract_patches(
        imgs=imgs, num_patches_per_img=num_patches_per_img, patch_shape=patch_shape
    )


@task()
def save_train_val_data_task(output_dir, prefix, X, X_val):
    save_train_val_data(
        output_dir=output_dir,
        prefix=prefix,
        X=X,
        X_val=X_val,
        logger=prefect.context.get("logger"),
    )
