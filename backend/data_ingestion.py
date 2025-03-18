from kafka import KafkaConsumer, KafkaProducer
import json
import time
import os
import logging
from dotenv import load_dotenv
from BlueSkyClient import BlueSkyClient

# Kafka configuration
KAFKA_BROKER = 'localhost:9092'
POSTS_TOPIC = 'bluesky-posts'
AUTHORS_TOPIC = 'bluesky-authors'
GROUP_ID = 'bluesky-consumer-group'

# Global set to track known authors
actors = set(["bicycledutch.bsky.social"])
processed_actors = set()

def create_consumer(topic):
    """Creates a Kafka consumer for a given topic."""
    return KafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BROKER,
        group_id=GROUP_ID,
        auto_offset_reset='earliest',
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
    print(f"Listening for new authors on topic: {AUTHORS_TOPIC}")
    
    try:
        for message in consumer:
            author_handle = message.value
            if author_handle not in actors:
                actors.add(author_handle)
                print(f"Added new author: {author_handle}")
    except KeyboardInterrupt:
        print("Author consumer shutting down.")

def fetch_and_publish_posts(producer, bluesky_client):
    """Fetches posts for all new actors and publishes them to Kafka."""
    while True:
        new_actors = actors - processed_actors
        print(f"Fetching posts from {new_actors}")
        for actor in list(new_actors):  # Only fetch posts from new actors
            limit = 5
            try:
                feed = bluesky_client.get_actor_feed(actor, limit=limit)
                filtered_feed = bluesky_client.filter_posts(feed)
                for post in filtered_feed:
                    producer.send(POSTS_TOPIC, post)
                print(f"Sent {len(filtered_feed)} posts from {actor} to {POSTS_TOPIC}")
                processed_actors.add(actor)  # Mark actor as processed
            except Exception as e:
                logging.error(f"Error fetching posts for {actor}: {e}")

        time.sleep(10)  # Avoid excessive API calls

def main():
    """Main function to run the author consumer and post producer."""
    load_dotenv()
    email = os.getenv("BLUESKY_EMAIL")
    password = os.getenv("BLUESKY_PASSWORD")
    bluesky_client = BlueSkyClient(email, password)
    
    producer = create_producer()

    # Run consumer in a separate thread
    from threading import Thread
    author_consumer_thread = Thread(target=consume_new_authors, daemon=True)
    author_consumer_thread.start()

    # Start fetching posts
    fetch_and_publish_posts(producer, bluesky_client)

if __name__ == "__main__":
    main()
