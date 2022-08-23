import json
import logging
import os
import subprocess
from os.path import join

import distro


def save_conda_env(output_dir, logger=logging):
    conda_prefix = os.environ["CONDA_PREFIX"]
    outpath = join(output_dir, "conda-environment.yaml")
    cmd = f"conda list -p {conda_prefix} > {outpath}"
    result = subprocess.run(cmd, shell=True, check=True)
    result.check_returncode()

    logger.info(f"Saved conda-environment to {outpath}.")


def save_system_information(output_dir, logger=logging):
    outpath = join(output_dir, "system-info.json")
    info = distro.info(pretty=True, best=True)
    with open(outpath, "w") as f:
        json.dump(info, f, indent=4)

    logger.info(f"Saved system information to {outpath}.")


def save_slurm_job_info(output_dir, slurm_info_dict, logger=logging):
    outpath = join(output_dir, "slurm-job-info.json")
    with open(outpath, "w") as f:
        json.dump(slurm_info_dict, f, indent=4)

    logger.info(f"Saved slurm job information to {outpath}.")


def get_slurm_job_info(jobid, logger=logging):
    cmd = f"scontrol show jobid --d {jobid} -o"
    result = subprocess.run(cmd, shell=True, check=True, capture_output=True)
    result.check_returncode()

    output = result.stdout.decode("utf-8")
    output_dict = {}
    for i in output.split():
        splitted = i.split("=")
        if len(splitted) > 1:
            output_dict[splitted[0]] = splitted[1]
        else:
            output_dict[splitted[0]] = None

    assert output_dict["JobId"] == str(jobid), logger.error("JobId does not " "match.")

    return output_dict
