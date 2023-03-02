"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import (
    NumberModel,
    ArithmeticalConceptModel,
)


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
            self.assertEqual(user.nick_name, user_name)
            self.assertEqual(user.user_name, user_name.lower())
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
                email='test1@example.com',
                password='test123'
            )

        # test the length of the user name greater than 16 raises value error.
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                user_name='thisistoolongusernamethatshouldnotbevalid',
                email='test2@example.com',
                password='test123'
            )

        # test the user name contains char
        # that is not English letter nor digits.
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                user_name='invl^idu$er_name',
                email='test3@example.com',
                password='test123'
            )

    def test_new_user_no_valid_password_raises_error(self):
        """Test that creating a user
        with an invalid password raises ValueError."""

        # test the length of the password <= 6 characters raises value error.
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                user_name='testusername1',
                email='test1@example.com',
                password='sh0rt'
            )

        # test that the password contains at least one English letter.
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                user_name='testusername2',
                email='test2@example.com',
                password='123456'
            )

        # test that the password contains at least one digits.
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                user_name='testusername3',
                email='test3@example.com',
                password='invalidpassword'
            )

    def test_create_super_user(self):
        """Test Creating super user."""
        user = get_user_model().objects.create_superuser(
            user_name='superuser123',
            email='test@example.com',
            password='test124',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_number_sucessful(self):
        """Test Creating a number in Number Model."""
        one = NumberModel.objects.create(value=1)
        self.assertEqual(NumberModel.objects.all().count(), 1)
        self.assertEqual(one.name, 'One')

    def test_create_arithmetical_concept_sucessful(self):
        """Test Creating an arithmetical concept."""
        ArithmeticalConceptModel.objects.create(
            name='Even Numbers',
            description='Numbers that are divisible by 2.',
        )

        self.assertEqual(ArithmeticalConceptModel.objects.all().count(), 1)

    def test_add_number_to_arith_concept_sucessful(self):
        """Test Adding Number to arithmentical Concept."""
        two = NumberModel.objects.create(value=2)
        even_numbers = ArithmeticalConceptModel.objects.create(
            name='Even Numbers',
            description='Numbers that are divisible by 2.',
        )
        even_numbers.add_number(two)

        self.assertEqual(even_numbers.count, 1)
        self.assertEqual(even_numbers.numbers.all().get(value=2), two)
