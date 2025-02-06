import unittest
import sys
import os

# Ensure WebPage package is discoverable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from WebPage.Week1 import application  # Import your Flask application instance

class BasicTests(unittest.TestCase):

    def setUp(self):
        application.testing = True
        self.app = application.test_client()

    def tearDown(self):
        pass

    def test_homepage(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
