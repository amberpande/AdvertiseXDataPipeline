# Kafka Configuration
KAFKA_BROKERS = 'localhost:9092'  # Change as per your Kafka broker setup
KAFKA_TOPIC = 'advertiseX_topic'  # Name of the Kafka topic

# File Paths for Kafka Producer
JSON_FILE_PATH = '/path/to/json_data.json'  # Path to the JSON file for Kafka Producer
CSV_FILE_PATH = '/path/to/csv_data.csv'     # Path to the CSV file for Kafka Producer
AVRO_FILE_PATH = '/path/to/avro_data.avro'  # Path to the Avro file for Kafka Producer
AVRO_SCHEMA_PATH = '/path/to/avro_schema.avsc'  # Path to the Avro schema file

# Spark Job Configuration
SPARK_APP_NAME = 'AdvertiseXDataProcessing'
SPARK_MASTER = 'local[*]'  # Or your cluster's master URL
SPARK_KAFKA_JAR_PATH = '/path/to/spark-sql-kafka-0-10_2.12-3.0.1.jar'  # Path to the Spark Kafka connector JAR
