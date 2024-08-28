from pyspark import SparkConf
from pyspark.sql import SparkSession
from delta import *

# sc = spark.sparkContext
# # Set the MinIO access key, secret key, endpoint, and other configurations
# sc._jsc.hadoopConfiguration().set("fs.s3a.access.key", "minio_access_key")
# sc._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "minio_secret_key")
# sc._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "http://localhost:9000")
# sc._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
# sc._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", "false")
# sc._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
# sc._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", "false")
# Read a JSON file from an MinIO bucket using the access key, secret key, 
# and endpoint configured above


conf = SparkConf()
conf.set("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.2.0,io.delta:delta-core_2.12:1.1.0")

spark: SparkSession = SparkSession.builder.config(conf=conf).getOrCreate()
spark.conf.set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
spark.conf.set("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
spark.conf.set("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.TemporaryAWSCredentialsProvider")
spark.conf.set("fs.s3a.access.key", "hVXzKCu1euHas33HWQlS")
spark.conf.set("fs.s3a.secret.key", "1EDaxNrfFCFwVYSr4uzqQJ5a7E0DkoC9d5ANfu0R")
spark.conf.set("fs.s3a.endpoint", "http://localhost:9000")
spark.conf.set("fs.s3a.path.style.access", "true")
spark.conf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
spark.conf.set("fs.s3a.connection.ssl.enabled", "false")
spark.conf.set("fs.s3a.connection.establish.timeout", "5000")
spark.conf.set("fs.s3a.connection.timeout", "10000")

DeltaTable.isDeltaTable(spark, "s3a://delta-lake/layers/")


# import logging
# import os
# from pyspark import SparkContext
# from pyspark.sql import SparkSession
# from pyspark.sql.types import StructType, StructField, LongType, DoubleType, StringType
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# logger = logging.getLogger("MinioSparkJob")
# spark = SparkSession.builder.getOrCreate()
# def load_config(spark_context: SparkContext):
#     spark_context._jsc.hadoopConfiguration().set("fs.s3a.access.key", os.getenv("AWS_ACCESS_KEY_ID", "<Your-MinIO-AccessKey>"))
#     spark_context._jsc.hadoopConfiguration().set("fs.s3a.secret.key",
# os.getenv("AWS_SECRET_ACCESS_KEY", "<Your-MinIO-SecretKey>"))
#     spark_context._jsc.hadoopConfiguration().set("fs.s3a.endpoint", os.getenv("ENDPOINT", "<Your-MinIO-Endpoint>"))
# spark_context._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", "true")
# spark_context._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
# spark_context._jsc.hadoopConfiguration().set("fs.s3a.attempts.maximum", "1")
# spark_context._jsc.hadoopConfiguration().set("fs.s3a.connection.establish.timeout", "5000")
# spark_context._jsc.hadoopConfiguration().set("fs.s3a.connection.timeout", "10000")
# load_config(spark.sparkContext)
# # Define schema for NYC Taxi Data
# schema = StructType([
#     StructField('VendorID', LongType(), True),
#     StructField('tpep_pickup_datetime', StringType(), True),
#     StructField('tpep_dropoff_datetime', StringType(), True),
#     StructField('passenger_count', DoubleType(), True),
#     StructField('trip_distance', DoubleType(), True),
#     StructField('RatecodeID', DoubleType(), True),
#     StructField('store_and_fwd_flag', StringType(), True),
#     StructField('PULocationID', LongType(), True),
#     StructField('DOLocationID', LongType(), True),
#     StructField('payment_type', LongType(), True),
#     StructField('fare_amount', DoubleType(), True),
#     StructField('extra', DoubleType(), True),
#     StructField('mta_tax', DoubleType(), True),
#     StructField('tip_amount', DoubleType(), True),
#     StructField('tolls_amount', DoubleType(), True),
#     StructField('improvement_surcharge', DoubleType(), True),
#     StructField('total_amount', DoubleType(), True)])
# # Read CSV file from MinIO
# df = spark.read.option("header", "true").schema(schema).csv(
#     os.getenv("INPUT_PATH", "s3a://openlake/spark/sample-data/taxi-data.csv"))
# # Filter dataframe based on passenger_count greater than 6
# large_passengers_df = df.filter(df.passenger_count > 6)
# total_rows_count = df.count()
# filtered_rows_count = large_passengers_df.count()
# # File Output Committer is used to write the output to the destination (Not recommended for Production)
# large_passengers_df.write.format("csv").option("header", "true").save(
# os.getenv("OUTPUT_PATH", "s3a://openlake-tmp/spark/nyc/taxis_small"))
# logger.info(f"Total Rows for NYC Taxi Data: {total_rows_count}")
# logger.info(f"Total Rows for Passenger Count > 6: {filtered_rows_count}")