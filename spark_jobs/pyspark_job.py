from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType
import os

def main():
    # Retrieve AWS credentials and S3 bucket name from environment variables
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    s3_bucket_name = os.environ.get('S3_BUCKET_NAME')

    # Define the schema of the incoming data
    schema = StructType([
        StructField("ad_creative_id", StringType(), True),
        StructField("user_id", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("website", StringType(), True),
        StructField("clicks", IntegerType(), True),
        StructField("conversions", IntegerType(), True)
    ])

    # Initialize Spark Session
    spark = SparkSession.builder \
        .appName("AdvertiseXDataProcessing") \
        .config("spark.hadoop.fs.s3a.access.key", aws_access_key_id) \
        .config("spark.hadoop.fs.s3a.secret.key", aws_secret_access_key) \
        .config("spark.hadoop.fs.s3a.endpoint", "s3.amazonaws.com") \
        .getOrCreate()

    # Read data from Kafka
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "advertiseX_topic") \
        .option("startingOffsets", "earliest") \
        .load()

    # Deserialize JSON data and apply schema
    df = df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")

    # Example Data Transformation
    transformed_df = df.filter(col("clicks") > 0)

    # Write the result to S3
    output_path = f"s3a://{s3_bucket_name}/processed_data/"
    query = transformed_df.writeStream \
        .outputMode("append") \
        .format("parquet") \
        .option("path", output_path) \
        .option("checkpointLocation", "/tmp/checkpoints/") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    main()
