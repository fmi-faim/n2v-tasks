import prefect
from prefect import task

from n2v_tasks.task.predict import create_save_dir, get_files, load_model


@task()
def load_model_task(model_dir, model_name):
    return load_model(model_dir=model_dir, model_name=model_name)


@task()
def get_files_task(input_dir, filter):
    return get_files(
        input_dir=input_dir, filter=filter, logger=prefect.context.get("logger")
    )


@task()
def create_save_dir_task(output_dir, model_name):
    return create_save_dir(
        output_dir=output_dir,
        model_name=model_name,
        logger=prefect.context.get("logger"),
    )
