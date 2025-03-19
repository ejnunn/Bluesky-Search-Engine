import sqlite3
from kafka import KafkaConsumer
import json
from config import KAFKA_BROKER, POSTS_TOPIC, GROUP_ID, DB_PATH
from kafka_utils import create_consumer


def create_table():
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

def consume_and_insert():
    consumer = create_consumer(POSTS_TOPIC, "earliest")

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
            print(f"Inserted post from {author_handle} at {timestamp}")

        except Exception as e:
            print(f"Error inserting data: {e}")
    
    conn.close()

if __name__ == '__main__':
    create_table()
    consume_and_insert()
