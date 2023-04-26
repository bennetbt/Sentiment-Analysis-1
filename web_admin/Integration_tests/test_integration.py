import json
import unittest
from fastapi.testclient import TestClient
from psycopg2 import connect, extensions, sql
from web_admin.frontend import app

client = TestClient(app=app)

class TestSentimentAnalyzerIntegration(unittest.TestCase):

    def setUp(self):
        self.connection = connect(host="db", database="Sentimental_Analysis", user="pgsqldev4", password="enter")
        self.connection.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.connection.cursor()

        # Create test data in the database
        create_table_query = "CREATE TABLE IF NOT EXISTS sentiment (ID SERIAL PRIMARY KEY, text TEXT NOT NULL, sentiment TEXT NOT NULL, score REAL NOT NULL)"
        self.cursor.execute(create_table_query)
        insert_query = "INSERT INTO sentiment (text, sentiment, score) VALUES ('This is a great day!', 'positive', 0.8)"
        self.cursor.execute(insert_query)
        insert_query = "INSERT INTO sentiment (text, sentiment, score) VALUES ('I hate this place.', 'negative', -0.6)"
        self.cursor.execute(insert_query)

    #def tearDown(self):
        # Clean up the test data from the database
        #delete_query = "DELETE FROM sentiment"
        #self.cursor.execute(delete_query)
        #self.connection.close()

    def test_sentiment_analysis_with_database(self):
        # Test the frontend by submitting a positive text
        data = {"text": "I am happy today"}
        response = client.post("/sentiment", json=data)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("sentiment", response_data)
        self.assertIn("score", response_data)
        self.assertEqual(response_data["sentiment"], "positive")
        self.assertIsInstance(response_data["score"], float)

    def test_sentiment_analysis_with_database(self):
        # Test the frontend by submitting a negative text
        data = {"text": "I am not happy today"}
        response = client.post("/sentiment", json=data)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("sentiment", response_data)
        self.assertIn("score", response_data)
        self.assertEqual(response_data["sentiment"], "negative")
        self.assertIsInstance(response_data["score"], float)

    def test_sentiment_analysis_with_database(self):
        # Test the frontend by submitting a neutral text
        data = {"text": "I am Uday"}
        response = client.post("/sentiment", json=data)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("sentiment", response_data)
        self.assertIn("score", response_data)
        self.assertEqual(response_data["sentiment"], "neutral")
        self.assertIsInstance(response_data["score"], float)


