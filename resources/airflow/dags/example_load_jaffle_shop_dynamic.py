from datetime import datetime, timedelta

from pyspark import SparkContext
from pyspark.sql import SparkSession
from airflow.decorators import dag, task
import os
from pathlib import Path


DATABASE_NAME = 'stage'

@dag(
    start_date=datetime(2024, 1, 1),
    schedule=None,
)
def load_jaffle_shop_dynamic():
    @task.pyspark(conn_id="spark_default")
    def create_database(spark: SparkSession, sc: SparkContext):
        spark.sql(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")

    @task.pyspark(conn_id="spark_default")
    def load_data(spark: SparkSession, sc: SparkContext, src_filename='jaffle_shop__customers.json'):
        src_file_path = f"s3a://warehouse/{src_filename}"
        src_filename_noext = Path(src_filename).stem
        table_ref = f"{DATABASE_NAME}.{src_filename_noext}"

        json_df = spark.read.json(src_file_path)
        json_df.writeTo(table_ref).createOrReplace()
        spark.sql(f"DESCRIBE TABLE {table_ref}").show(truncate=False)
        spark.sql(f"SELECT * FROM {table_ref} LIMIT 5").show()

    @task.pyspark(conn_id="spark_default")
    def check_tables(spark: SparkSession, sc: SparkContext):
        spark.sql(f"SHOW TABLES from {DATABASE_NAME}").show()

    src_filename_list = ['jaffle_shop__customers.json', 'jaffle_shop__orders.json', 'jaffle_shop__products.json', 'stripe__payments.json']
    create_database() >> load_data.expand(src_filename=src_filename_list) >> check_tables()

dag = load_jaffle_shop_dynamic()
