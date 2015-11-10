import json
from unittest import TestCase
from model import NASDAQNYSE, connect_to_db, db, example_data
from projectOHYEAH import sort_results, run_googlenews_api
from server import app
import server

class SentimentTests(TestCase):
    """Unit tests about the Sentiment analysis sorting."""

    def test_sort_results(self):
        tester_data = {"url" : ["content", "url", "title", "article body", 5, .5, 'pos']}
        expected = ({"url": ["content", "url", "title"]}, {}, [], ['url'], 0, 1, 0)

        self.assertEqual(sort_results(tester_data), expected)

class FlaskTests(TestCase):
    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()

        connect_to_db(app, "sqlite:///")

        db.create_all()
        example_data()

    def test_run_googlenews_api(self):
        """Tests the output of running the google news API."""

        test_search = "Home Depot"
        self.assertEqual(type(run_googlenews_api(test_search)) == type({}), True)

    def test_homepage(self):
        """Tests the result of my homepage"""
        result = self.client.get('/')

        self.assertEqual(result.status_code, 200)
        self.assertIn('<h1>Company Climate</h1>', result.data)

    def test_results_page(self):
        """Tests the result of my results page."""
        result = self.client.get('/results?search=Home Depot')

        self.assertEqual(result.status_code, 200)
        self.assertIn('<title>Company Climate</title>', result.data)

    def test_find_company(self):
        """Can we find an company in the sample data?"""

        apple = NASDAQNYSE.query.filter(NASDAQNYSE.company_name == "Apple").first()
        self.assertEqual(apple.company_name, "Apple")


if __name__ == "__main__":
    import unittest

    unittest.main()