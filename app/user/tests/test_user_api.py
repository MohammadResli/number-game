"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


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

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_signup_details = {
            'user_name': 'testUser123',
            'email': 'test@example.com',
            'password': 'pass123',
        }
        create_user(**user_signup_details)

        # payload contains email.
        payload_with_email = {
            'user': user_signup_details['email'],
            'password': user_signup_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload_with_email)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        # payload contains user_name
        payload_with_user_name = {
            'user': user_signup_details['user_name'],
            'password': user_signup_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload_with_user_name)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        user_signup_details = {
            'user_name': 'testuser123',
            'email': 'test@example.com',
            'password': 'pass123',
        }
        create_user(**user_signup_details)

        # payload contains email.
        payload_with_email_bad_password = {
            'user': user_signup_details['email'],
            'password': 'badpassword123',
        }
        res = self.client.post(TOKEN_URL, payload_with_email_bad_password)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # payload contains user name.
        payload_with_user_name_bad_password = {
            'user': user_signup_details['user_name'],
            'password': 'badpassword123',
        }
        res = self.client.post(TOKEN_URL, payload_with_user_name_bad_password)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a no password returns an error."""
        user_signup_details = {
            'user_name': 'testuser123',
            'email': 'test@example.com',
            'password': 'pass123',
        }
        create_user(**user_signup_details)

        # payload contains email with no password.
        payload_email_with_no_password = {
            'user': user_signup_details['email'],
        }
        res = self.client.post(TOKEN_URL, payload_email_with_no_password)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # payload contains user name with no password.
        payload_use_name_with_no_password = {
            'user': user_signup_details['user_name'],
        }
        res = self.client.post(TOKEN_URL, payload_use_name_with_no_password)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_not_signup_user(self):
        """Test posting token for not regestered user returns an error."""
        user_signup_details = {
            'user_name': 'testuser123',
            'email': 'test@example.com',
            'password': 'pass123',
        }
        # payload contains email with no password.
        payload_with_email = {
            'user': user_signup_details['email'],
            'password': user_signup_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload_with_email)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # payload contains user name with no password.
        payload_with_user_name = {
            'user': user_signup_details['email'],
            'password': user_signup_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload_with_user_name)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        "Test authoentication is required for users."
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        user_signup_details = {
            'user_name': 'testUser123',
            'email': 'test@example.com',
            'password': 'pass123',
        }
        self.user = create_user(**user_signup_details)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('email', res.data)
        self.assertEqual(res.data['email'], self.user.email)

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the me endpoint."""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_password(self):
        """Test updating the user password for the authenticated user."""
        payload_update = {
            'password': 'newpassword123'
        }

        res = self.client.patch(ME_URL, payload_update)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload_update['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_user_email_not_allowed(self):
        """Test updating the user email not allowed."""
        payload_update = {
            'email': 'newemail@example.com'
        }

        res = self.client.patch(ME_URL, payload_update)
        self.user.refresh_from_db()
        self.assertNotEqual(res.data['email'], payload_update['email'])
        self.assertEqual(self.user.email, 'test@example.com')
