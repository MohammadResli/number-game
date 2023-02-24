"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            'user_name': 'testuser123',
            'email': 'test@example.com',
            'password': 'testpass123',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(user_name=payload['user_name'])
        self.assertEqual(user.email, payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'user_name': 'testuser123',
            'email': 'test@example.com',
            'password': 'testpass123',
        }
        create_user(**payload)
        payload['user_name'] = 'testnewuser123'
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_with_user_name_exists_error(self):
        """Test error returned if user with user name exists."""
        payload = {
            'user_name': 'testuser123',
            'email': 'test@example.com',
            'password': 'testpass123',
        }
        create_user(**payload)
        payload['email'] = 'test123@example.com'
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_with_invalid_user_name_error(self):
        """Test error returned if user with invalid user name."""

        # test short user_name return bad request.
        payload_short_user_name = {
            'user_name': 'q2',
            'email': 'test1@example.com',
            'password': 'testpass123',
        }
        res = self.client.post(CREATE_USER_URL, payload_short_user_name)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload_short_user_name['email']
        ).exists()
        self.assertFalse(user_exists)

        # test long user_name return bad request.
        payload_long_user_name = {
            'user_name': 'thisistoolongusernamethatshouldnotbevalid',
            'email': 'test2@example.com',
            'password': 'testpass123',
        }
        res = self.client.post(CREATE_USER_URL, payload_long_user_name)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload_long_user_name['email']
        ).exists()
        self.assertFalse(user_exists)

        # test special charecters in user_name return bad request.
        payload_special_charecters_user_name = {
            'user_name': 'invl^idu$er_name',
            'email': 'test3@example.com',
            'password': 'testpass123',
        }
        res = self.client.post(
                CREATE_USER_URL,
                payload_special_charecters_user_name
            )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload_special_charecters_user_name['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_user_with_invalid_password_error(self):
        """Test error returned if user with invalid password."""

        # test short password return bad request.
        payload_short_password = {
            'user_name': 'testusername1',
            'email': 'test1@example.com',
            'password': 'sh0rt',
        }
        res = self.client.post(CREATE_USER_URL, payload_short_password)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload_short_password['email']
        ).exists()
        self.assertFalse(user_exists)

        # test no Engilsh letter password return bad request.
        payload_no_english_letter_password = {
            'user_name': 'testusername2',
            'email': 'test2@example.com',
            'password': '123456',
        }
        res = self.client.post(
                CREATE_USER_URL,
                payload_no_english_letter_password
            )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload_no_english_letter_password['email']
        ).exists()
        self.assertFalse(user_exists)

        # test no digits password return bad request.
        payload_no_digits_password = {
            'user_name': 'testusername3',
            'email': 'test3@example.com',
            'password': 'invalidpassword',
        }
        res = self.client.post(CREATE_USER_URL, payload_no_digits_password)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload_no_digits_password['email']
        ).exists()
        self.assertFalse(user_exists)
