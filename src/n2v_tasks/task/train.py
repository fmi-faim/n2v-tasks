from os.path import join

import numpy as np
import wandb
from n2v.models import N2V, N2VConfig
from wandb.integration.keras import WandbCallback


def load_train_data(train_data: str, val_data: str):
    X = np.load(train_data)["X"]
    X_val = np.load(val_data)["X_val"]

    return X, X_val


def build_model(
    output_dir,
    model_name,
    X,
    epochs,
    batch_size,
    group,
    user,
    name,
    wandb_project,
    wandb_entity,
):
    wandb.init(
        project=wandb_project,
        entity=wandb_entity,
        tags=[group, user],
        name=name + "_" + model_name,
    )
    config = N2VConfig(
        X,
        unet_kern_size=3,
        train_steps_per_epoch=int(X.shape[0] / batch_size),
        train_epochs=epochs,
        train_loss="mse",
        batch_norm=True,
        train_batch_size=batch_size,
        n2v_perc_pix=0.198,
        n2v_patch_shape=(64, 64),
        n2v_manipulator="median",
        blurpool=True,
        skip_skipone=True,
        n2v_neighborhood_radius=2,
    )
    model = N2V(config, model_name, basedir=join(output_dir, "models"))
    model.prepare_for_training(metrics=())
    model.callbacks.append(WandbCallback())
    return model


def train_model(model, X, X_val):
    model.train(X, X_val)
