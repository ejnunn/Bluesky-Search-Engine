import unittest
from unittest.mock import patch, MagicMock
from backend.data_ingestion import BlueskyAPIClient, KafkaPostProducer

class TestBlueskyAPIClient(unittest.TestCase):
    @patch('data_ingestion.requests.get')
    def test_fetch_posts_success(self, mock_get):
        # Setup a fake response with expected data
        fake_posts = [{"id": 1, "content": "Hello, Bluesky!"}]
        fake_response = MagicMock()
        fake_response.status_code = 200
        fake_response.json.return_value = fake_posts
        mock_get.return_value = fake_response

        client = BlueskyAPIClient("http://fakeurl")
        posts = client.fetch_posts()
        self.assertEqual(posts, fake_posts)
        mock_get.assert_called_with("http://fakeurl")

    @patch('data_ingestion.requests.get')
    def test_fetch_posts_failure(self, mock_get):
        # Setup a fake response that simulates a failed API call
        fake_response = MagicMock()
        fake_response.status_code = 404
        fake_response.raise_for_status.side_effect = Exception("Not Found")
        mock_get.return_value = fake_response

        client = BlueskyAPIClient("http://fakeurl")
        with self.assertRaises(Exception):
            client.fetch_posts()

class TestKafkaPostProducer(unittest.TestCase):
    @patch('data_ingestion.KafkaProducer')
    def test_send_post(self, mock_kafka_producer):
        # Create a fake KafkaProducer instance and simulate the send behavior
        mock_instance = MagicMock()
        fake_future = MagicMock()
        fake_future.get.return_value = "sent"
        mock_instance.send.return_value = fake_future
        mock_kafka_producer.return_value = mock_instance

        producer = KafkaPostProducer(['localhost:9092'], 'test_topic')
        post = {"id": 1, "content": "Test post"}
        result = producer.send_post(post)
        self.assertEqual(result, "sent")
        mock_instance.send.assert_called_with('test_topic', post)

        producer.close()
        mock_instance.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()

