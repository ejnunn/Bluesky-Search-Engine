from kafka import KafkaConsumer, KafkaProducer
import json
from config import KAFKA_BROKER, GROUP_ID

def create_consumer(topic, auto_offset_reset='earliest'):
    """
    Creates a Kafka consumer for a given topic.
    """
    return KafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BROKER,
        group_id=GROUP_ID,
        auto_offset_reset=auto_offset_reset,
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

def create_producer():
    """
    Creates a Kafka producer.
    """
    return KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
