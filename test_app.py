"""Contains unit tests for the app.py routes."""
import app
from unittest import TestCase
from app import app 
import requests


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

class RegisterTestCase(TestCase):
    """Contains unit tests for the register page."""

    def setUp(self):
        """Create test client, add sample data."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_register(self):
        """Can we get to the register page?"""

        # Get the response object
        response = self.client.get('/register')

        # Check that we got a response
        self.assertEqual(response.status_code, 200)

class ActivityTestCase(TestCase):
    """Contains unit tests for the activity page."""

    def setUp(self):
        """Create test client, add sample data."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_activity(self):
        """Can we get to the activity page?"""

        # Get the response object
        response = self.client.get('/activity')

        # Check that we got a response
        self.assertEqual(response.status_code, 200)

class FavoritesTestCase(TestCase):
    """Contains unit tests for the favorites page."""

    def setUp(self):
        """Create test client, add sample data."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_favorites(self):
        """Do we get redirected to the login page if we're not logged in?"""

        # Get the response object
        response = self.client.get('/favorites')

        # Check that we got a response
        self.assertEqual(response.status_code, 302)

class UploadPhotosTestCase(TestCase):
    """Contains unit tests for the upload photos page."""

    def setUp(self):
        """Create test client, add sample data."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_upload_photos(self):
        """Do we get redirected to the login page if we're not logged in?"""

        # Get the response object
        response = self.client.get('/upload')

        # Check that we got a response
        self.assertEqual(response.status_code, 302)
  
class TestLoginPostRequest(TestCase):
    """Contains unit tests for sending post requests to the login page"""
    def test_send_post_request_to_login_page(self):
        """Test sending a post request to the login page."""
        url = 'https://funseeker.onrender.com/login'
        data = {'username': 'test', 'password': 'testing'}
        response = requests.post(url, data=data)
        self.assertEqual(response.status_code, 200)

class TestRegisterPostRequest(TestCase):
    """Contains unit tests for sending post requests to the register page"""
    def test_send_post_request_to_register_page(self):
        """Test sending a post request to the register page."""
        url = 'https://funseeker.onrender.com/register'
        data = {'username': 'testuser', 'password': 'testing'}
        response = requests.post(url, data=data)
        self.assertEqual(response.status_code, 200)

