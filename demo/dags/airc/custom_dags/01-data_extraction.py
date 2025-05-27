from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from datetime import datetime


@dag(
    dag_id='01-Extract-Data-From-Google-Drive',
    schedule_interval=None,  # Set to "@daily" or any cron if needed
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["ingestion", "google_drives"]
)
def extract_data_from_gdrive():
    download_task = BashOperator(
        task_id="download_data_using_gdown",
        # bash_command=(
        #     "gdown --folder https://drive.google.com/drive/folders/1-fVKgBVCCn4CZyxQp_tY-Yr3xSwBPb2Y?usp=drive_link "
        #     "-O $AIRFLOW_HOME/include/data/"
        # ),
        bash_command=(
            "gdown --fuzzy https://drive.google.com/file/d/1OWAE1Pu95sVNvtQz4f9_V5pqKVhXK0tm/view?usp=drive_link "
            "-O $AIRFLOW_HOME/include/data/"
        ),
        env={"AIRFLOW_HOME": "/usr/local/airflow"},
        append_env=True,
    )

    download_task  # Explicitly return the task to register it in the DAGs


dag = extract_data_from_gdrive()
