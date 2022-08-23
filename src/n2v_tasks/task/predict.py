import logging
import os
from glob import glob
from os.path import exists, join

from n2v.models import N2V


def load_model(model_dir, model_name):
    model = N2V(config=None, name=model_name, basedir=model_dir)
    model.load_weights("weights_last.h5")
    return model


def get_files(input_dir, filter, logger=logging):
    files = glob(join(input_dir, filter))
    logger.info(f"Found {len(files)} files.")
    return files


def create_save_dir(output_dir, model_name, logger=logging):
    if exists(output_dir):
        target_dir = join(output_dir, model_name + "_pred")
        os.makedirs(target_dir, exist_ok=True)
        logger.info(f"Predictions will be saved in {target_dir}.")
        return target_dir
    else:
        logger.error(f"{output_dir} does not exist.")
