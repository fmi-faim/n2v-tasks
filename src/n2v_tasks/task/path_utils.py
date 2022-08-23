import os
from os.path import join


def create_output_dir(save_data_path, group, user, name):
    output_dir = join(save_data_path, group, user, name)
    os.makedirs(output_dir, exist_ok=True)
    return output_dir
