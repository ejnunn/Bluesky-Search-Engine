#!/usr/bin/env python3
import json
import signal
import logging
from kafka import KafkaConsumer, KafkaProducer
from kafka_utils import create_consumer, create_producer
from config import KAFKA_BROKER, POSTS_TOPIC, AUTHORS_TOPIC, GROUP_ID

# In-memory set for deduplication
actors = set()
running = True

def process_messages(consumer, producer):
    """Consumes messages from the posts topic, extracts author handles, and publishes new ones."""
    logging.info(f"Listening for messages on topic: {POSTS_TOPIC}")
    try:
        while running:
            message_pack = consumer.poll(timeout_ms=1000)
            if not message_pack:
                continue
            for tp, messages in message_pack.items():
                for message in messages:
                    data = message.value
                    if isinstance(data, list) and len(data) >= 1:
                        author_handle = data[0]
                        if author_handle not in actors:
                            actors.add(author_handle)
                            logging.info(f"Extracted new author handle: {author_handle}")
                            producer.send(AUTHORS_TOPIC, value=author_handle)
    except Exception as e:
        logging.error(f"Error in process_messages: {e}")
    finally:
        consumer.close()
        producer.close()
        logging.info("Author extractor shutting down.")

def signal_handler(sig, frame):
    """Gracefully shutdown on signal."""
    global running
    logging.info("Received shutdown signal. Shutting down author_extractor service.")
    running = False

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    # Set up graceful shutdown signals
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    consumer = create_consumer(POSTS_TOPIC)
    producer = create_producer()
    process_messages(consumer, producer)

if __name__ == "__main__":
    main()
