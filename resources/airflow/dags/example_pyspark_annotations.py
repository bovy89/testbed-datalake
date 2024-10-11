from datetime import datetime, timedelta

import pandas as pd
from pyspark import SparkContext
from pyspark.sql import SparkSession
from airflow.decorators import dag, task


@dag(
    start_date=datetime(2024, 1, 1),
    schedule=None,
)
def example_pyspark_annotations():
    @task.pyspark(conn_id="spark_default")
    def spark_task(spark: SparkSession, sc: SparkContext):
        spark.sql("SHOW DATABASES").show()

    df = spark_task()

dag = example_pyspark_annotations()
