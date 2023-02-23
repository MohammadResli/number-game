"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_successful(self):
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

    def test_valid_user_name_successful(self):
        """Test user name contains only letters and numbers,
            and the length of the user name is between 4 and 16
        """
        default_password = 'defaultpassword123'
        valid_users_data = [
            ['test1', 'test1@EXAMPLE.com'],
            ['te5ts', 'test2@EXAMPLE.com'],
            ['123Ds', 'test3@EXAMPLE.com'],
            ['u5er', 'Test4@Example.com'],
            ['longusername1234', 'TEST5@EXAMPLE.com'],
            ['a111234567754123', 'test6@example.COM'],
        ]
        for user_name, email in valid_users_data:
            user = get_user_model().objects.create_user(
                user_name=user_name,
                email=email,
                password=default_password
            )
            self.assertEqual(user.user_name, user_name)
            self.assertTrue(user.check_password(default_password))

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                user_name='testusername',
                email='',
                password='test123'
            )

    def test_new_user_without_user_name_raises_error(self):
        """Test that creating a user
        without an user name raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                user_name='',
                email='test@example.com',
                password='test123'
            )

    def test_new_user_without_password_raises_error(self):
        """Test that creating a user without a password raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                user_name='testusername',
                email='test@example.com',
                password=''
            )

    def test_new_user_no_valid_user_name_raises_error(self):
        """Test that creating a user
        with an invalid user name raises ValueError."""

        # test the length of the user name less than 4 raises value error.
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                user_name='q2',
                email='test@example.com',
                password='test123'
            )

        # test the length of the user name greater than 16 raises value error.
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                user_name='thisistoolongusernamethatshouldnotbevalid',
                email='test@example.com',
                password='test123'
            )

        # test the user name contains char
        # that is not englist letter nor digits.
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                user_name='invl^idu$er_name',
                email='test@example.com',
                password='test123'
            )

    def test_new_user_no_valid_password_raises_error(self):
        """Test that creating a user
        with an invalid password raises ValueError."""

        # test the length of the password <= 6 characters raises value error.
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                user_name='testusername',
                email='test@example.com',
                password='sh0rt'
            )

        # test that the password contains at least one English letter.
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                user_name='testusername',
                email='test@example.com',
                password='123456'
            )

        # test that the password contains at least one digits.
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                user_name='testusername',
                email='test@example.com',
                password='invalidpassword'
            )
