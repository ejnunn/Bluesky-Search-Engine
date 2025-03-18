import os
from dotenv import load_dotenv

load_dotenv()

# Kafka configuration
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
POSTS_TOPIC = os.getenv("POSTS_TOPIC", "bluesky-posts")
AUTHORS_TOPIC = os.getenv("AUTHORS_TOPIC", "bluesky-authors")
ACTORS_STATE_TOPIC = os.getenv("ACTORS_STATE_TOPIC", "bluesky-actors-state")
GROUP_ID = os.getenv("GROUP_ID", "bluesky-group")

# BlueSky Credentials
BLUESKY_EMAIL = os.getenv("BLUESKY_EMAIL")
BLUESKY_PASSWORD = os.getenv("BLUESKY_PASSWORD")
