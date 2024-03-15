
# AdvertiseX Data Pipeline

This repository contains the data pipeline for AdvertiseX, a digital advertising technology company. The pipeline handles ingestion, processing, and storage of ad impressions, clicks, conversions, and bid requests data.

## Structure

- `producers/`: Kafka producers for ingesting data into Kafka topics.
  - `kafka_producer.py`: Generic Kafka producer script.
- `consumers/`: Kafka consumers for processing data from Kafka topics.
- `data/`: Directory for raw data files (JSON, CSV, Avro).
- `spark_jobs/`: PySpark scripts for data transformation and processing.
- `airflow/`: Contains Airflow DAGs for orchestrating the pipeline.
  - `dags/`: Airflow DAG scripts.
- `config/`: Configuration files for Kafka, AWS, and other services.
  - `config.py`: Contains the config to run the pipeline

## Workflow

1. **Data Ingestion**: Data is ingested from various sources in JSON, CSV, and Avro formats using Kafka producers.
2. **Data Processing**: Ingested data is processed and transformed using PySpark jobs.
3. **Data Storage**: Processed data is stored in AWS S3.
4. **Orchestration**: The entire workflow is orchestrated using Apache Airflow.

## Setup and Usage

- Ensure Kafka, Apache Spark, and Apache Airflow are set up in your environment.
- Configure AWS credentials for accessing S3.
- Place your data files in the respective `data/` subdirectories.
- Update the configuration files in `config/` with your specific settings.
- Run the Airflow DAG to execute the pipeline.

## Dependencies

- Apache Kafka
- Apache Spark
- Apache Airflow
- AWS SDK