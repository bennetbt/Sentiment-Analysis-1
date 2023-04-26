import json
import unittest
from fastapi.testclient import TestClient
from fastapi import status
import requests
import psycopg2
from web.frontend import app, TextData, psycopg2, requests
import pytest
import psycopg2
conn = psycopg2.connect(host="db", database="Sentimental_Analysis", user="pgsqldev4", password="enter")


class TestSentimentAnalyzer(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app=app)

    def test_index_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to Sentiment Analyzer", response.content)

    def test_sentiment_analysis(self):
        data = {"text": "I am happy today"}
        response = self.client.post("/sentiment", json=data)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("sentiment", response_data)
        self.assertIn("score", response_data)
        self.assertEqual(response_data["sentiment"], "positive")
        self.assertIsInstance(response_data["score"], float)

    #def test_delete_history(self):
        #response = self.client.post("/sentiment/1")
       # self.assertEqual(response.status_code, 303)  # redirect status code
       # self.assertEqual(response.headers["location"], "http://localhost:1172")
        

if __name__ == "__main__":
    unittest.main()
