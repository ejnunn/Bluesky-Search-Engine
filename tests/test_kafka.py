import unittest
from unittest.mock import patch, MagicMock
import json
from backend.kafka_setup import create_kafka_topic, consume_messages
from backend.data_ingestion import KafkaPostProducer

class TestKafkaSetup(unittest.TestCase):
    @patch('backend.kafka_setup.KafkaAdminClient')
    def test_create_kafka_topic_already_exists(self, mock_admin_client):
        # Simulate that the topic already exists.
        mock_instance = MagicMock()
        mock_instance.list_topics.return_value = ['bluesky_posts']
        mock_admin_client.return_value = mock_instance

        create_kafka_topic('bluesky_posts', ['localhost:9092'])
        mock_instance.create_topics.assert_not_called()

    @patch('backend.kafka_setup.KafkaAdminClient')
    def test_create_kafka_topic_creates_new_topic(self, mock_admin_client):
        # Simulate that the topic does not exist.
        mock_instance = MagicMock()
        mock_instance.list_topics.return_value = []
        mock_admin_client.return_value = mock_instance

        create_kafka_topic('bluesky_posts', ['localhost:9092'])
        mock_instance.create_topics.assert_called_once()

    @patch('backend.kafka_setup.KafkaConsumer')
    def test_consume_messages(self, mock_kafka_consumer):
        # Simulate KafkaConsumer returning a predefined message.
        fake_message = MagicMock()
        fake_message.value = json.dumps({"id": 1, "content": "Test post"}).encode('utf-8')
        mock_consumer_instance = MagicMock()
        mock_consumer_instance.__iter__.return_value = [fake_message] * 3
        mock_kafka_consumer.return_value = mock_consumer_instance

        messages = consume_messages('bluesky_posts', ['localhost:9092'], max_messages=2)
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0], {"id": 1, "content": "Test post"})
        mock_consumer_instance.close.assert_called_once()

class TestKafkaIntegration(unittest.TestCase):
    @patch('backend.kafka_setup.KafkaAdminClient')
    @patch('backend.kafka_setup.KafkaConsumer')
    @patch('backend.data_ingestion.KafkaProducer')
    def test_producer_consumer_integration(self, mock_kafka_producer, mock_kafka_consumer, mock_admin_client):
        # Set up a fake Kafka producer to simulate message production.
        mock_producer_instance = MagicMock()
        fake_future = MagicMock()
        fake_future.get.return_value = "sent"
        mock_producer_instance.send.return_value = fake_future
        mock_kafka_producer.return_value = mock_producer_instance

        producer = KafkaPostProducer(['localhost:9092'], 'bluesky_posts')
        post = {"id": 1, "content": "Integration Test Post"}
        result = producer.send_post(post)
        self.assertEqual(result, "sent")
        mock_producer_instance.send.assert_called_with('bluesky_posts', post)

        # Set up a fake Kafka consumer to simulate message consumption.
        fake_message = MagicMock()
        fake_message.value = json.dumps(post).encode('utf-8')
        mock_consumer_instance = MagicMock()
        mock_consumer_instance.__iter__.return_value = [fake_message]
        mock_kafka_consumer.return_value = mock_consumer_instance

        messages = consume_messages('bluesky_posts', ['localhost:9092'], max_messages=1)
        self.assertEqual(messages[0], post)
        mock_consumer_instance.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()

