import unittest
from fastapi.testclient import TestClient
from sentimental_analysis.sentiment_analysis import app
import pytest

client = TestClient(app=app)

class TestSentimentAnalysis(unittest.TestCase):

    def test_positive_sentiment(self):
        text_data = {"text": "This is a great day!"}
        response = client.post("/sentiment", json=text_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["sentiment"], "positive")

    def test_negative_sentiment(self):
        text_data = {"text": "I hate this place."}
        response = client.post("/sentiment", json=text_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["sentiment"], "negative")

    def test_neutral_sentiment(self):
        text_data = {"text": "The weather."}
        response = client.post("/sentiment", json=text_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["sentiment"], "neutral")