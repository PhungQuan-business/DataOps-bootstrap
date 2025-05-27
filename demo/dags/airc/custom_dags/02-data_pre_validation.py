from datetime import datetime, timedelta
import os
# from airflow.models.dag import DAG
from airflow.decorators import dag
from airflow.providers.papermill.operators.papermill import PapermillOperator
from airflow.operators.bash import BashOperator
from airflow.decorators import dag, task, task_group
from airc.modules.utlis import _get_minio_connection, _get_minio_object, _minio_object_to_dataframe

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'email_on_failure': False,
    # 'email': ['phunghongquan.business@gmail.com']
}


@dag(
    dag_id='02-Data-Pre-Validation',
    default_args=default_args,
    schedule_interval=None,  # Set to "@daily" or any cron if needed
    start_date=datetime(2025, 5, 21),  # year, month, day
    template_searchpath='/usr/local/airflow/include',
    catchup=False,  # Set true nếu muốn backfill từ past đến hiện tại
    tags=["ingestion", "google_drives"]
)
def pre_validation():

    run_pre_validate_notebook = PapermillOperator(
        task_id="run_data_pre_validation_notebook",
        input_nb="include/input_notebook/01-data_pre_validation.ipynb",
        output_nb="include/output_notebook/01-data_pre_validation-{{ execution_date.strftime('%Y-%m-%dT%H-%M-%S') }}.ipynb",
        parameters={"execution_date": "{{ execution_date }}"},
        kernel_name="python3"
    )

    @task
    def push_data_to_minio():
        minio_client = _get_minio_connection()
        bucket_name = "canada-house"
        found = minio_client.bucket_exists(bucket_name)
        if not found:
            minio_client.make_bucket(bucket_name)
            print("Created bucket", bucket_name)
        else:
            print("Bucket", bucket_name, "already exists")

        DATA_PATH = os.environ.get("DATA_PATH")
        source_file = DATA_PATH+"/canada_house.csv"
        destination_file = 'data/canada_house.csv'
        minio_client.fput_object(
            bucket_name, destination_file, source_file,
        )
        print(
            source_file, "successfully uploaded as object",
            destination_file, "to bucket", bucket_name,
        )

        return 0

    # run_check_notebbok = run_pre_validate_notebook()
    push_to_datalake = push_data_to_minio()

    # run_check_notebbok >> push_to_datalake
    run_pre_validate_notebook >> push_to_datalake


dag = pre_validation()
