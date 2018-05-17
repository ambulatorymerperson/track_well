"""test suite for testing track well's server.py"""

import server
import unittest


class MyAppIntegrationTestCase(unittest.TestCase):
    """Examples of integration tests: testing Flask server."""

    def test_index(self):
        client = server.app.test_client()
        result = client.get('/')
        self.assertIn('<h1>Welcome to track well</h1>', result.data)

    def my_stats(self):
        client = server.app.test_client()
        result = client.get('/my_stats')
        self.assertIn('', result.data)    

    def test_favorite_color_form(self):
        client = server.app.test_client()
        result = client.post('/', data={'color': 'blue'})
        self.assertIn('Woah! I like blue, too', result.data)

    
