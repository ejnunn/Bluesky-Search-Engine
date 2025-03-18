from kafka import KafkaConsumer, KafkaProducer
import json

# Kafka configuration
KAFKA_BROKER = 'localhost:9092'
INPUT_TOPIC = 'bluesky-posts'
OUTPUT_TOPIC = 'bluesky-authors'
GROUP_ID = 'bluesky-consumer-group'

actors = set()

def create_consumer():
    return KafkaConsumer(
        INPUT_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        group_id=GROUP_ID,
        auto_offset_reset='earliest',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

def create_producer():
    return KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def process_messages(consumer, producer):
    print(f"Listening for messages on topic: {INPUT_TOPIC}")
    try:
        for message in consumer:
            data = message.value
            if isinstance(data, list) and len(data) >= 1:
                author_handle = data[0]
                # Deduplicate authors
                if author_handle not in actors:
                	actors.add(author_handle)
	                print(f"Extracted author handle: {author_handle}")
	                producer.send(OUTPUT_TOPIC, value=author_handle)
    except KeyboardInterrupt:
        print("Shutting down...")

def main():
    consumer = create_consumer()
    producer = create_producer()
    process_messages(consumer, producer)

if __name__ == "__main__":
    main()
