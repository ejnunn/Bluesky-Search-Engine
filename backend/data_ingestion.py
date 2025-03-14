#!/usr/bin/env python3
import json
import time
import requests
from kafka import KafkaProducer

class BlueskyAPIClient:
    """
    Client to fetch posts from the Bluesky API.
    """
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_posts(self):
        """
        Fetch posts from the API.
        Returns:
            A list of post dictionaries if the request is successful.
        Raises:
            An HTTPError if the API call fails.
        """
        response = requests.get(self.base_url)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

class KafkaPostProducer:
    """
    Kafka producer to send posts to a designated topic.
    """
    def __init__(self, bootstrap_servers, topic):
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = topic

    def send_post(self, post):
        """
        Sends a post to the Kafka topic.
        Args:
            post: The post data (as a dict) to be sent.
        Returns:
            The result of the send operation.
        """
        future = self.producer.send(self.topic, post)
        result = future.get(timeout=60)  # Wait for acknowledgement
        return result

    def close(self):
        """
        Closes the Kafka producer connection.
        """
        self.producer.close()

def main():
    """
    Main function to wire the API client and Kafka producer together.
    This function can be scheduled to run as a standalone job.
    """
    # Simulated Bluesky API endpoint
    api_url = "http://localhost:5000/api/posts"
    # Kafka configuration
    kafka_bootstrap_servers = ['localhost:9092']
    kafka_topic = 'bluesky_posts'

    client = BlueskyAPIClient(api_url)
    producer = KafkaPostProducer(kafka_bootstrap_servers, kafka_topic)

    try:
        posts = client.fetch_posts()
        for post in posts:
            print("Sending post:", post)
            producer.send_post(post)
            time.sleep(1)  # Optional delay between messages
    except Exception as e:
        print("Error occurred:", e)
    finally:
        producer.close()

if __name__ == "__main__":
    main()

