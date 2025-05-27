from airflow import DAG
from airflow.models import Variable
from airflow.hooks.base import BaseHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime
from minio import Minio
from sqlalchemy import create_engine, text
import pandas as pd
import io


def _get_minio_connection():
    conn = BaseHook.get_connection("minio_connection")
    extras = conn.extra_dejson
    minio_endpoint = extras.get("endpoint_url")
    conn_secure = extras.get("secure")
    # print("this is endpoint",minio_endpoint)
    access_key = conn.login
    secret_key = conn.password
    minio_client = Minio(
        endpoint=minio_endpoint,
        access_key=access_key,
        secret_key=secret_key,
        secure=conn_secure
    )
    return minio_client


def _get_postgres_connection():
    hook = PostgresHook(postgres_conn_id="postgres_connection")
    conn = hook.get_conn()

    return hook, conn


def _get_minio_object(BUCKET_NAME, OBJECT_PATH):
    minio_client = _get_minio_connection()
    response = minio_client.get_object(bucket_name=BUCKET_NAME,
                                       object_name=OBJECT_PATH)
    return response


def _minio_object_to_dataframe(minio_object):
    """_summary_

    Args:
        minio_object (_type_): _description_

    Returns:
        _type_: _description_
    """
    df = pd.read_csv(io.BytesIO(minio_object.read()),
                     low_memory=False, index_col=False)
    return df
