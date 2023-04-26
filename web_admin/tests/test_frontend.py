import json
import unittest
from fastapi.testclient import TestClient
from fastapi import status
import requests
import psycopg2
from web_admin.frontend import app, TextData, psycopg2, requests
import pytest
import psycopg2
conn = psycopg2.connect(host="db", database="Sentimental_Analysis", user="pgsqldev4", password="enter")


class TestSentimentAnalyzer(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app=app)

    def test_sentiment_analysis(self):
        response = self.client.post("/sentiment", json={"text": "This is a good day."})
        self.assertEqual(response.status_code, 200)
        self.assertFalse("Sentiment: positive" in response.text)

    def test_statistics(self):
        response = self.client.get("/statistics")
        self.assertEqual(response.status_code, 404)
        self.assertFalse("Pos Statements" in response.text)
        self.assertFalse("Neg Statements" in response.text)
        self.assertFalse("Neu Statements" in response.text)
        self.assertFalse("Pos %" in response.text)
        self.assertFalse("Neg %" in response.text)
        self.assertFalse("Neu %" in response.text)
    
    def test_index_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to Sentiment Analyzer", response.content)

    def test_sentiment_analysis_valid_input(self):
        data = {"text": "This is a positive sentence."}
        response = self.client.post('/sentiment', json=data)
        assert response.status_code == 200
        assert response.json()["sentiment"] == "positive"

    def test_edit_sentiment(self):
    # Test case 1: Editing an existing sentiment
     response = self.client.post("/editSentiment/3")
     assert response.status_code == 200

    # Test case 2: Editing a non-existent sentiment
     response = self.client.post("/editSentiment/100")
     assert response.status_code == 404

    # Test case 3: Saving changes to an existing sentiment
     data = {"text": "This is a new text", "sentiment": "neutral", "initial_sentiment": "positive"}
     response = self.client.post("/updateSentiment/3", json=data)
     assert response.status_code == 422

    # Test case 4: Saving changes to a non-existent sentiment
     data = {"text": "This is a new text", "sentiment": "neutral", "initial_sentiment": "positive"}
     response = self.client.post("/updateSentiment/100", json=data)
     assert response.status_code == 422



if __name__ == "__main__":
    unittest.main()
