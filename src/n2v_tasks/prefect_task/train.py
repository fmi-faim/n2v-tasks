from prefect import task

from n2v_tasks.task.train import build_model, load_train_data, train_model


@task(nout=2)
def load_train_data_task(train_data: str, val_data: str):
    return load_train_data(train_data=train_data, val_data=val_data)


@task()
def build_model_task(
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
    return build_model(
        output_dir=output_dir,
        model_name=model_name,
        X=X,
        epochs=epochs,
        batch_size=batch_size,
        group=group,
        user=user,
        name=name,
        wandb_project=wandb_project,
        wandb_entity=wandb_entity,
    )


@task()
def train_model_task(model, X, X_val):
    train_model(model=model, X=X, X_val=X_val)
