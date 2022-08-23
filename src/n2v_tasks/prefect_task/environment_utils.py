import json
import os
from os.path import join

import prefect
from airtable import airtable
from prefect import task

from n2v_tasks.task.environment_utils import (
    get_slurm_job_info,
    save_conda_env,
    save_slurm_job_info,
    save_system_information,
)


@task()
def save_conda_env_task(output_dir):
    save_conda_env(output_dir=output_dir, logger=prefect.context.get("logger"))


@task()
def save_system_information_task(output_dir):
    save_system_information(output_dir=output_dir, logger=prefect.context.get("logger"))


@task()
def get_slurm_job_info_task():
    return get_slurm_job_info(
        jobid=os.environ["SLURM_JOB_ID"], logger=prefect.context.get("logger")
    )


@task()
def save_slurm_job_info_task(output_dir, slurm_info_dict):
    save_slurm_job_info(
        output_dir=output_dir,
        slurm_info_dict=slurm_info_dict,
        logger=prefect.context.get("logger"),
    )


@task()
def get_prefect_context_task():
    return {
        "date": prefect.context.get("date").strftime("%Y-%m-%d %H:%M:%S"),
        "flow_id": prefect.context.get("flow_id"),
        "flow_run_id": prefect.context.get("flow_run_id"),
        "flow_run_version": prefect.context.get("flow_run_version"),
        "flow_run_name": prefect.context.get("flow_run_name"),
    }


@task()
def save_prefect_context_task(output_dir, context_dict):
    logger = prefect.context.get("logger")

    outpath = join(output_dir, "prefect-context.json")
    with open(outpath, "w") as f:
        json.dump(context_dict, f, indent=4)

    logger.info(f"Saved prefect context information to {outpath}.")


@task()
def add_to_slurm_flow_run_table_task(
    prefect_context, slurm_info_dict, base_key, table_name, api_key
):
    table = airtable.Table(base_id=base_key, table_name=table_name, api_key=api_key)
    return table.create(
        {
            "slurm-job-id": slurm_info_dict["JobId"],
            "date-gmt": prefect_context["date"],
            "flow_id": prefect_context["flow_id"],
            "flow_run_id": prefect_context["flow_run_id"],
            "flow_run_name": prefect_context["flow_run_name"],
        }
    )
