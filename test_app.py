"""Contains unit tests for the app.py routes."""
import unittest as ut
import app
from unittest import TestCase
from app import app 



class LoginTestCase(TestCase):
    """Contains unit tests for the login page."""

    def setUp(self):
        """Create test client, add sample data."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_login(self):
        """Can we get to the login page?"""

        # Get the response object
        response = self.client.get('/login')

        # Check that we got a response
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        """Can we get to the register page?"""

        # Get the response object
        response = self.client.get('/register')

        # Check that we got a response
        self.assertEqual(response.status_code, 200)

    def test_activity(self):
        """Can we get to the activity page?"""

        # Get the response object
        response = self.client.get('/activity')

        # Check that we got a response
        self.assertEqual(response.status_code, 200)

        

