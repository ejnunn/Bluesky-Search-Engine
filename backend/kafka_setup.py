#!/usr/bin/env python3
import logging
import json
from kafka import KafkaConsumer, KafkaAdminClient
from kafka.admin import NewTopic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_kafka_topic(topic_name, bootstrap_servers, num_partitions=1, replication_factor=1):
    """
    Creates a Kafka topic if it doesn't already exist.
    """
    try:
        admin_client = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
        existing_topics = admin_client.list_topics()
        if topic_name in existing_topics:
            logger.info(f"Topic '{topic_name}' already exists.")
            return
        topic = NewTopic(name=topic_name,
                         num_partitions=num_partitions,
                         replication_factor=replication_factor)
        admin_client.create_topics(new_topics=[topic], validate_only=False)
        logger.info(f"Topic '{topic_name}' created successfully.")
    except Exception as e:
        logger.error(f"Error creating topic '{topic_name}': {e}")

def consume_messages(topic, bootstrap_servers, timeout_ms=1000, max_messages=10):
    """
    Consumes messages from the specified Kafka topic and logs them.
    Returns:
        A list of message values (decoded from JSON).
    """
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    messages = []
    for i, message in enumerate(consumer):
        logger.info(f"Received message: {message.value}")
        messages.append(message.value)
        if i + 1 >= max_messages:
            break
    consumer.close()
    return messages

if __name__ == "__main__":
    # Example usage: ensure topic exists and start consuming messages
    kafka_topic = 'bluesky_posts'
    kafka_bootstrap_servers = ['localhost:9092']

    create_kafka_topic(kafka_topic, kafka_bootstrap_servers)
    logger.info("Starting Kafka consumer...")
    consume_messages(kafka_topic, kafka_bootstrap_servers)

