from datetime import datetime, timedelta

from pyspark import SparkContext
from pyspark.sql import SparkSession
from airflow.decorators import dag, task
import os
from pathlib import Path


from airflow.providers.amazon.aws.operators.s3 import (
    S3ListOperator
)


DATABASE_NAME = 'bronze'
SOURCE_BUCKET_NAME = 'landing'

@dag(
    start_date=datetime(2024, 1, 1),
    schedule=None,
)
def load_mongo_json():
    @task.pyspark(conn_id="spark_default")
    def create_database(spark: SparkSession, sc: SparkContext):
        spark.sql(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")

    @task.pyspark(conn_id="spark_default")
    def load_data(spark: SparkSession, sc: SparkContext, src_filename=None):
        src_file_path = f"s3a://{SOURCE_BUCKET_NAME}/{src_filename}"
        src_filename_noext = Path(src_filename).stem
        table_ref = f"{DATABASE_NAME}.{src_filename_noext}"

        json_df = spark.read.json(src_file_path)
        json_df.writeTo(table_ref).createOrReplace()
        spark.sql(f"DESCRIBE TABLE {table_ref}").show(truncate=False)
        spark.sql(f"SELECT * FROM {table_ref} LIMIT 5").show()

    @task.pyspark(conn_id="spark_default")
    def check_tables(spark: SparkSession, sc: SparkContext):
        spark.sql(f"SHOW TABLES from {DATABASE_NAME}").show()

    s3_files_list = S3ListOperator(
        task_id='list_3s_files',
        bucket=SOURCE_BUCKET_NAME,
        prefix='mongodb/',
        delimiter='/',
        aws_conn_id='s3_default'
    )

    create_database() >> load_data.expand(src_filename=s3_files_list.output) >> check_tables()

dag = load_mongo_json()
