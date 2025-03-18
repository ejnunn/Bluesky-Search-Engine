#!/usr/bin/env python3
import json
import time
import signal
import logging
import threading
from kafka import KafkaConsumer, KafkaProducer
from BlueSkyClient import BlueSkyClient
from config import KAFKA_BROKER, POSTS_TOPIC, AUTHORS_TOPIC, GROUP_ID, BLUESKY_EMAIL, BLUESKY_PASSWORD

# Global state and lock
actors = set(["bicycledutch.bsky.social"])
processed_actors = set()
actors_lock = threading.Lock()
running = True

def create_consumer(topic):
    """Creates a Kafka consumer for a given topic."""
    return KafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BROKER,
        group_id=GROUP_ID,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

def create_producer():
    """Creates a Kafka producer."""
    return KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def consume_new_authors():
    """Listens for new authors and adds them to the actors set."""
    consumer = create_consumer(AUTHORS_TOPIC)
    logging.info(f"Listening for new authors on topic: {AUTHORS_TOPIC}")
    try:
        while running:
            message_pack = consumer.poll(timeout_ms=1000)
            if not message_pack:
                continue
            for tp, messages in message_pack.items():
                for message in messages:
                    author_handle = message.value
                    with actors_lock:
                        if author_handle not in actors:
                            actors.add(author_handle)
                            logging.info(f"Added new author: {author_handle}")
    except Exception as e:
        logging.error(f"Error in consume_new_authors: {e}")
    finally:
        consumer.close()
        logging.info("Author consumer shutting down.")

def fetch_and_publish_posts(producer, bluesky_client):
    """Fetches posts for new actors and publishes them to Kafka."""
    global running
    while running:
        with actors_lock:
            new_actors = actors - processed_actors
        if new_actors:
            logging.info(f"Fetching posts from new actors: {new_actors}")
        for actor in list(new_actors):
            limit = 5
            try:
                feed = bluesky_client.get_actor_feed(actor, limit=limit)
                filtered_feed = bluesky_client.filter_posts(feed)
                for post in filtered_feed:
                    producer.send(POSTS_TOPIC, post)
                logging.info(f"Sent {len(filtered_feed)} posts from {actor} to {POSTS_TOPIC}")
                with actors_lock:
                    processed_actors.add(actor)
            except Exception as e:
                logging.error(f"Error fetching posts for {actor}: {e}")
        producer.flush()
        time.sleep(10)
    producer.close()

def signal_handler(sig, frame):
    """Gracefully shutdown on signal."""
    global running
    logging.info("Received shutdown signal. Shutting down data_ingestion service.")
    running = False

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    # Set up graceful shutdown signals
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    if not BLUESKY_EMAIL or not BLUESKY_PASSWORD:
        logging.error("BLUESKY_EMAIL and BLUESKY_PASSWORD must be set in the environment.")
        return

    bluesky_client = BlueSkyClient(BLUESKY_EMAIL, BLUESKY_PASSWORD)
    producer = create_producer()

    # Start consumer thread for new authors
    consumer_thread = threading.Thread(target=consume_new_authors, daemon=True)
    consumer_thread.start()

    # Main loop: fetch posts for new actors
    fetch_and_publish_posts(producer, bluesky_client)

if __name__ == "__main__":
    main()
