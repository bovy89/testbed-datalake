from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.apache.spark.operators.spark_sql import SparkSqlOperator


with DAG('example_sparkoperator',
    start_date=datetime(2024, 1, 1),
    schedule=None,
) as dag:

    create_pippo_db = SparkSqlOperator(
        task_id="spark_create_pippo_db",
        sql="CREATE DATABASE IF NOT EXISTS pippo",
        conn_id='spark_default',
    )

    submit_job = SparkSubmitOperator(
       task_id='submit_job',
       application='/include/pyspark_script.py',
       conn_id='spark_default',
    )

    check_job = SparkSqlOperator(
        task_id="spark_sql_job",
        sql="SHOW DATABASES",
        conn_id='spark_default',
    )

    create_pippo_db >> submit_job >> check_job
