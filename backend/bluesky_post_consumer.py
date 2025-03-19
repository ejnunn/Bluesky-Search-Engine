import sqlite3
import logging
from kafka import KafkaConsumer
import json
from config import KAFKA_BROKER, POSTS_TOPIC, GROUP_ID, DB_PATH
from kafka_utils import create_consumer

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def create_table():
    """Create the SQLite table if it doesn't already exist."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author_handle TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                UNIQUE(author_handle, timestamp)
            )
        """)
        conn.commit()
        conn.close()
        logging.info("Successfully ensured posts table exists.")
    except Exception as e:
        logging.error(f"Error creating table: {e}")

def consume_and_insert():
    """Consumes messages from Kafka and inserts them into SQLite."""
    try:
        consumer = create_consumer(POSTS_TOPIC, "earliest")
        logging.info(f"Connected to Kafka topic: {POSTS_TOPIC}")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        for message in consumer:
            try:
                author_handle, content, timestamp = message.value
                cursor.execute("""
                    INSERT INTO posts (author_handle, content, timestamp)
                    VALUES (?, ?, ?)
                    """, (author_handle, content, timestamp))

                conn.commit()
                logging.info(f"Inserted post from {author_handle} at {timestamp}")

            except sqlite3.IntegrityError:
                logging.warning(f"Duplicate post skipped: {author_handle} at {timestamp}")
            except Exception as e:
                logging.error(f"Error inserting data: {e}")
        
        conn.close()

    except Exception as e:
        logging.error(f"Error setting up Kafka consumer or SQLite connection: {e}")

if __name__ == '__main__':
    logging.info("Starting bluesky_post_ingest service.")
    create_table()
    consume_and_insert()
