from datetime import datetime, timedelta
import os
from airflow.hooks.base import BaseHook
# from airflow.models.dag import DAG
from airflow.decorators import dag
from airflow.providers.papermill.operators.papermill import PapermillOperator
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import ShortCircuitOperator
from airflow.decorators import dag, task, task_group
from airc.modules.utlis import _get_minio_connection, _get_minio_object, _minio_object_to_dataframe, _get_postgres_connection
import json

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'email_on_failure': False,
    # 'email': ['phunghongquan.business@gmail.com']s
}

DATA_PATH = os.environ.get("DATA_PATH")


@dag(
    dag_id='04-Data-Post-Validation',
    default_args=default_args,
    schedule_interval=None,  # Set to "@daily" or any cron if needed
    start_date=datetime(2025, 5, 21),  # year, month, day
    template_searchpath='/usr/local/airflow/include',
    catchup=False,  # Set true nếu muốn backfill từ past đến hiện tại
    tags=["validation"]
)
def post_validation():

    # @task
    # def data_pre_validation():
    run_pre_validate_notebook = PapermillOperator(
        task_id="run_data_pre_validation_notebook",
        input_nb="include/input_notebook/03-data_post_validation.ipynb",
        output_nb="include/output_notebook/03-data_post_validation-{{ execution_date.strftime('%Y-%m-%dT%H-%M-%S') }}.ipynb",
        parameters={"execution_date": "{{ execution_date }}"},
        kernel_name="python3"
    )

    @task
    def check_validation_result():
        def check_validation_result(validation_result_path: str, min_passed_pct: float = 80.0) -> bool:
            result_path = validation_result_path
            with open(result_path) as f:
                result = json.load(f)

            critical_failed_tests = result.get("critical_failed_tests", 0)
            passed_percentage = result.get("passed_percentage", 0)
            if critical_failed_tests > 0:
                print("❌ Validation failed due to required expectation failure.")
                return False
            if passed_percentage < min_passed_pct:
                print("❌ Validation failed due to insufficient pass percentage.")
                return False

            print("✅ Validation passed. Proceeding with downstream tasks.")
            return True

        ShortCircuitOperator(
            task_id="check_validation_gate",
            python_callable=check_validation_result,
            op_kwargs={
                "validation_result_path": "/tmp/gx_validation_summary.json",
                "min_passed_pct": 80.0,
            }
        )

    run_check_validation_result = check_validation_result()

    @task
    def push_data_to_postgres():
        hook, conn = _get_postgres_connection()
        cursor = conn.cursor()

        # Step 1: Execute SQL from file to create the table
        sql_file_path = "/usr/local/airflow/include/SQL/create_table.sql"
        with open(sql_file_path, 'r') as sql_file:
            create_table_sql = sql_file.read()
        cursor.execute(create_table_sql)
        conn.commit()
        print("table created")

        # Step 2: Load data from CSV into the table
        csv_file_path = f"{DATA_PATH}/cleaned_canada.csv"
        with open(csv_file_path, 'r') as f:
            cursor.copy_expert(
                "COPY cleaned_canada FROM STDIN WITH CSV HEADER DELIMITER ','",
                f
            )

        conn.commit()
        cursor.close()
        conn.close()
        print("Processed data is stored in database")

    # Assign the task
    push_processed_data_to_database = push_data_to_postgres()

    data_analytics_notebook = PapermillOperator(
        task_id="run_data_analytics_notebook",
        input_nb="include/input_notebook/04-EDA.ipynb",
        output_nb="include/output_notebook/04-EDA-{{ execution_date.strftime('%Y-%m-%dT%H-%M-%S') }}.ipynb",
        parameters={"execution_date": "{{ execution_date }}"},
        kernel_name="python3"
    )

    run_pre_validate_notebook >> run_check_validation_result >> [
        data_analytics_notebook, push_processed_data_to_database]


dag = post_validation()
