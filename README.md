
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


## Setup and Running the Pipeline

### Prerequisites

- Docker and Docker Compose installed on your machine.
- Access to an AWS S3 bucket and valid AWS credentials.

### Steps to Set Up and Run

1. **Clone the Repository:**
   - Clone this repository to your local machine.

2. **Build the Docker Image:**
   - Navigate to the directory containing the Dockerfile.
   - Run `docker build -t advertise-pipeline .` to build your Docker image.

3. **Configure Environment Variables:**
   - Set the following environment variables:
     - `AWS_ACCESS_KEY_ID`: Your AWS access key.
     - `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key.
     - `S3_BUCKET_NAME`: The name of your S3 bucket.

4. **Start Kafka and Zookeeper:**
   - Run `docker run -d --name zookeeper --network advertise-net -p 2181:2181 zookeeper`.
   - Run `docker run -d --name kafka --network advertise-net -p 9092:9092 -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 wurstmeister/kafka`.

5. **Run Airflow:**
   - Navigate to the directory with your `docker-compose.yml` file (if using Docker Compose).
   - Run `docker-compose up` to start Airflow.

6. **Access Airflow UI:**
   - Open a web browser and go to `http://localhost:8080`.
   - Trigger the DAG `advertiseX_data_pipeline`.

7. **Monitoring:**
   - Monitor the logs in Airflow UI for any errors or issues.

### Notes

- Ensure that the paths in your configurations are correctly set.
- For a real-world deployment, consider using a managed service for Kafka and Spark, and properly securing your AWS credentials.


## Dependencies

- Apache Kafka
- Apache Spark
- Apache Airflow
- AWS SDK