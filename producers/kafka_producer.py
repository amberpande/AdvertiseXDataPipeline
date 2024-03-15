import json
import csv
import logging
import avro.schema
import avro.io
import io
from kafka import KafkaProducer, KafkaError
from config.config import KAFKA_BROKERS, KAFKA_TOPIC, JSON_FILE_PATH, CSV_FILE_PATH, AVRO_FILE_PATH, AVRO_SCHEMA_PATH

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to serialize JSON data for Kafka
def json_serializer(data):
    return json.dumps(data).encode('utf-8')

# Create a Kafka producer
def create_kafka_producer():
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKERS,
        value_serializer=json_serializer
    )
    return producer

# Callback for successful message delivery
def on_send_success(record_metadata):
    logging.info(f"Message sent to {record_metadata.topic} [{record_metadata.partition}] @ offset {record_metadata.offset}")

# Callback for failed message delivery
def on_send_error(excp):
    logging.error('Error in sending record', exc_info=excp)

# Send message to Kafka
def send_message(producer, topic, data):
    try:
        producer.send(topic, value=data).add_callback(on_send_success).add_errback(on_send_error)
        producer.flush()
    except KafkaError as e:
        logging.error(f"Failed to send message: {e}")

# Process and send messages from a JSON file
def process_json_file(producer, file_path, topic):
    with open(file_path, 'r') as file:
        for line in file:
            try:
                data = json.loads(line)
                send_message(producer, topic, data)
            except json.JSONDecodeError as e:
                logging.error(f"Error decoding JSON: {e}")

# Process and send messages from a CSV file
def process_csv_file(producer, file_path, topic):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            send_message(producer, topic, row)

# Process and send messages from an Avro file
def process_avro_file(producer, file_path, schema_path, topic):
    schema = avro.schema.parse(open(schema_path, 'rb').read())
    with open(file_path, 'rb') as file:
        reader = avro.datafile.DataFileReader(file, avro.io.DatumReader(schema))
        for record in reader:
            bytes_writer = io.BytesIO()
            encoder = avro.io.BinaryEncoder(bytes_writer)
            datum_writer = avro.io.DatumWriter(schema)
            datum_writer.write(record, encoder)
            send_message(producer, topic, bytes_writer.getvalue())
        producer.flush()

# Main function to run the Kafka producer
def run_kafka_producer():
    producer = create_kafka_producer()
    try:
        process_json_file(producer, JSON_FILE_PATH, KAFKA_TOPIC)
        process_csv_file(producer, CSV_FILE_PATH, KAFKA_TOPIC)
        process_avro_file(producer, AVRO_FILE_PATH, AVRO_SCHEMA_PATH, KAFKA_TOPIC)
    except Exception as e:
        logging.error(f"Exception occurred: {e}")
    finally:
        producer.close()
        logging.info("Kafka Producer closed.")

if __name__ == "__main__":
    run_kafka_producer()
