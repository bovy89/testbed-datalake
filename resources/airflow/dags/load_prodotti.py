from datetime import datetime, timedelta

from pyspark import SparkContext
from pyspark.sql import SparkSession
from airflow.decorators import dag, task


@dag(
    start_date=datetime(2024, 1, 1),
    schedule=None,
)
def load_prodotti():
    @task.pyspark(conn_id="spark_default")
    def create_database(spark: SparkSession, sc: SparkContext):
        spark.sql("CREATE DATABASE IF NOT EXISTS test")

    @task.pyspark(conn_id="spark_default")
    def load_data(spark: SparkSession, sc: SparkContext):
        json_df = spark.read.json("s3a://warehouse/spark_test.json", multiLine=True)
        json_df.writeTo("test.people").createOrReplace()

    @task.pyspark(conn_id="spark_default")
    def describe_table(spark: SparkSession, sc: SparkContext):
        spark.sql("DESCRIBE TABLE test.people").show(truncate=False)

    @task.pyspark(conn_id="spark_default")
    def check_table_content(spark: SparkSession, sc: SparkContext):
        spark.sql("SELECT * FROM test.people LIMIT 5").show()

    create_database() >> load_data() >> [describe_table(), check_table_content()]

dag = load_prodotti()
