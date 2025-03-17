#!/usr/bin/env python3
import requests
import time
import json
import os
import logging
from kafka import KafkaProducer
from dotenv import load_dotenv
from BlueSkyClient import BlueSkyClient


class KafkaBlueskyPostProducer:
    """Kafka producer for sending Bluesky posts to a designated topic."""

    def __init__(self, kafka_broker: str, topic: str):
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_broker,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = topic

    def send_posts(self, posts: list[dict]) -> None:
        """Send posts one by one to the Kafka topic."""
        for post in posts:
            try:
                self.producer.send(self.topic, post)
            except Exception as e:
                logging.error(f"Failed to send post: {post}. Error. {e}")


def main():
    """
    Main function to wire the API client and Kafka producer together.
    This function can be scheduled to run as a standalone job.
    """
    # Set up Bluesky client
    load_dotenv()
    email = os.getenv("BLUESKY_EMAIL")
    password = os.getenv("BLUESKY_PASSWORD")
    bluesky_client = BlueSkyClient(email, password)

    # Set up Kafka producer
    kafka_broker = "localhost:9092"
    producer = KafkaBlueskyPostProducer(kafka_broker=kafka_broker, topic="bluesky-posts")

    # Continually pull data from Bluesky, filter it and post it to the Kafka broker
    try:
        while True:
            actor = "bicycledutch.bsky.social"
            limit = 5
            feed = bluesky_client.get_actor_feed(actor, limit=limit)
            filtered_feed = bluesky_client.filter_posts(feed)
            producer.send_posts(filtered_feed)
            print(f"Sent {len(filtered_feed)} posts to Kafka broker {kafka_broker} with topic {producer.topic}")
            time.sleep(10)
    except KeyboardInterrupt:
        logging.info("KeyboardInterrupt. Shutting down.")


if __name__ == "__main__":
    main()

