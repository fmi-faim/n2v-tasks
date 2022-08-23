from prefect import task

from n2v_tasks.task.path_utils import create_output_dir


@task()
def create_output_dir_task(save_data_path, group, user, name):
    return create_output_dir(
        save_data_path=save_data_path, group=group, user=user, name=name
    )
