from kafka import KafkaConsumer
import json
import logging
from config.config import KAFKA_BROKERS, KAFKA_TOPIC

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to deserialize JSON data from Kafka
def json_deserializer(data):
    return json.loads(data.decode('utf-8'))

# Create Kafka Consumer
def create_kafka_consumer(brokers, topic):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=brokers,
        auto_offset_reset='earliest',
        group_id='my-group',
        value_deserializer=json_deserializer
    )
    return consumer

# Process message from Kafka
def process_message(message):
    # Add your processing logic here
    logging.info(f"Received message: {message}")
    # Example: print the message
    print(message)

# Main function to run the Kafka consumer
def run_kafka_consumer():
    consumer = create_kafka_consumer(KAFKA_BROKERS, KAFKA_TOPIC)
    try:
        for message in consumer:
            process_message(message.value)
    except KeyboardInterrupt:
        logging.info("Stopping Kafka Consumer...")
    finally:
        consumer.close()
        logging.info("Kafka Consumer closed.")

if __name__ == "__main__":
    run_kafka_consumer()
