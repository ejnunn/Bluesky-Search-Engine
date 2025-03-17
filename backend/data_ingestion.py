#!/usr/bin/env python3
import requests
import time
import json
from kafka import KafkaProducer

def get_weather():
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": 51.5,
            "longitude": -0.11,
            "current": "temperature_2m"
        }
    )

    return response.json()


def main():
    """
    Main function to wire the API client and Kafka producer together.
    This function can be scheduled to run as a standalone job.
    """
    producer = KafkaProducer(bootstrap_servers="localhost:9092")

    while True:
        print("\n\nType \"quit\" to exit")
        print("Enter message to be sent:")
        msg = input()
        if msg == "quit":
            print("Exiting...")
            break
        producer.send('test_topic', msg.encode('utf-8'))
        print("Sending msg \"{}\"".format(msg))
        print("Message sent!")

if __name__ == "__main__":
    main()

