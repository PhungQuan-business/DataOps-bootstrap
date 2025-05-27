from datetime import datetime, timedelta
import os
# from airflow.models.dag import DAG
from airflow.decorators import dag
from airflow.providers.papermill.operators.papermill import PapermillOperator
from airflow.operators.bash import BashOperator
from airflow.decorators import dag, task, task_group


default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'email_on_failure': False,
    # 'email': ['phunghongquan.business@gmail.com']
}


@dag(
    dag_id='03-Data-Transformation',
    default_args=default_args,
    schedule_interval=None,  # Set to "@daily" or any cron if needed
    start_date=datetime(2025, 5, 21),  # year, month, day
    template_searchpath='/usr/local/airflow/include',
    catchup=False,  # Set true nếu muốn backfill từ past đến hiện tại
    tags=["transform"]
)
def run_transformation_notebook():
    PapermillOperator(
        task_id="run_transformation_notebook",
        input_nb="include/input_notebook/02-data_processing.ipynb",
        output_nb="include/output_notebook/02-data_processing-{{ execution_date.strftime('%Y-%m-%dT%H-%M-%S') }}.ipynb",
        parameters={"execution_date": "{{ execution_date }}"},
        kernel_name="python3"
    )


run_transformation_notebook()
