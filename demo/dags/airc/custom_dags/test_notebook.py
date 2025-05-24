from datetime import datetime, timedelta

from airflow.models.dag import DAG
from airflow.providers.papermill.operators.papermill import PapermillOperator
from airflow.operators.bash import BashOperator

with DAG(
    dag_id='example_papermill_operator',
    default_args={
        'retries': 0
    },
    schedule='0 0 * * *',
    start_date=datetime(2022, 10, 1),
    template_searchpath='/usr/local/airflow/include/notebook',
    catchup=False
) as dag:

    notebook_task = PapermillOperator(
        task_id="run_example_notebook",
        input_nb="include/input_notebooks/in_notebook.ipynb",
        # output_nb="include/out-{{ execution_date.strftime('%Y-%m-%dT%H-%M-%S') }}.ipynb",
        output_nb="include/output_notebook/out_notebook.ipynb",
        parameters={"execution_date": "{{ execution_date }}"},
        kernel_name="python3"
    )
