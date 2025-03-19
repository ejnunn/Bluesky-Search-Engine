#!/usr/bin/env python3
import json
import time
import signal
import logging
import threading
from kafka import KafkaProducer
from kafka_utils import create_producer
from BlueSkyClient import BlueSkyClient
from config import KAFKA_BROKER, POSTS_TOPIC, GROUP_ID, BLUESKY_EMAIL, BLUESKY_PASSWORD

# Global state and lock
actors = set(["bicycledutch.bsky.social"])
processed_actors = set()
actors_lock = threading.Lock()
running = True

def fetch_and_publish_posts(producer, bluesky_client):
    """Fetches posts for new actors and publishes them to Kafka."""
    global running
    while running:
        with actors_lock:
            new_actors = actors - processed_actors
        if new_actors:
            logging.info(f"Fetching posts from new actors: {new_actors}")
        for actor in list(new_actors):
            limit = 10
            try:
                feed = bluesky_client.get_actor_feed(actor, limit=limit)
                filtered_feed = bluesky_client.filter_posts(feed)
                
                for post in filtered_feed:
                    producer.send(POSTS_TOPIC, post)

                    # Directly add new author_handle to the actors set
                    author_handle = post[0]
                    if author_handle:
                        with actors_lock:
                            if author_handle not in actors:
                                actors.add(author_handle)
                                logging.info(f"Added new author to actors set: {author_handle}")

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

    # Main loop: fetch posts for new actors
    fetch_and_publish_posts(producer, bluesky_client)

if __name__ == "__main__":
    main()
