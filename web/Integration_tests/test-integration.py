import json
import unittest
from fastapi.testclient import TestClient
from psycopg2 import connect, extensions, sql
from web.frontend import app
from sentimental_analysis.sentiment_analysis import app as backend_app

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
        # Test the frontend by submitting a new text
        data = {"text": "I am happy today"}
        response = client.post("/sentiment", json=data)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("sentiment", response_data)
        self.assertIn("score", response_data)
        self.assertEqual(response_data["sentiment"], "positive")
        self.assertIsInstance(response_data["score"], float)

        # Test the backend by getting the sentiment analysis history
        backend_client = TestClient(app=backend_app)
        response = backend_client.get("/sentiment_history")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIsInstance(response_data, list)
        self.assertEqual(len(response_data), 2)

        # Test the frontend by deleting a text from the history
        history_id = response_data[0]["ID"]
        response = client.post(f"/sentiment/{history_id}")
        self.assertEqual(response.status_code, 303)  # redirect status code
        self.assertEqual(response.headers["location"], "http://testserver/")

        # Test the backend by checking that the deleted text is not in the history anymore
        response = backend_client.get("/sentiment_history")
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIsInstance(response_data, list)
        self.assertEqual(len(response_data), 1)
        self.assertNotEqual(response_data[0]["ID"], history_id)
