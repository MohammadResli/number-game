"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        user_name = 'testusername'
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            user_name=user_name,
            email=email,
            password=password,
        )

        self.assertEqual(user.user_name, user_name)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        default_password = 'defaultpassword123'
        sample_users_data = [
            ['test1', 'test1@EXAMPLE.com', 'test1@example.com'],
            ['test2', 'Test2@Example.com', 'Test2@example.com'],
            ['test3', 'TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4', 'test4@example.COM', 'test4@example.com'],
        ]
        for user_name, email, expected in sample_users_data:
            user = get_user_model().objects.create_user(
                user_name=user_name,
                email=email,
                password=default_password
            )
            self.assertEqual(user.email, expected)
