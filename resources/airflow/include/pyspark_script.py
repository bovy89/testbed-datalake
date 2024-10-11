from pyspark.sql import SparkSession

def create_database():
    spark = SparkSession.builder.appName("provaprova").getOrCreate()
    # spark = SparkSession.builder.appName("provaprova").enableHiveSupport().getOrCreate()
    # configurations = spark.sparkContext.getConf().getAll()
    # for item in configurations: print(item)
    spark.sql("CREATE DATABASE IF NOT EXISTS provaprova")
    spark.stop()

if __name__ == "__main__":
    create_database()
