"""
Tests for the arithmetical concept API.
"""
from django.test import TestCase
from django.urls import reverse
from django.core.management import call_command

from rest_framework.test import APIClient
from rest_framework import status
from core.models import (
    ArithmeticalConceptModel,
    NumberModel,
)

ARITHS_URL = reverse('arith:ariths')
NUMBERS_URL = reverse('arith:numbers')


def get_arith_url(id):
    """Create and return arithmetical conecpt public detail url."""
    return reverse('arith:ariths', args=[id])


def get_number_url(id):
    """Create and return number public detail url."""
    return reverse('arith:numbers', args=[id])


class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        call_command('create_default_arithmetical_concept')
        self.client = APIClient()

    def test_list_all_ariths_sucessful(self):
        "Test list all arithmetical concepts sucessful."

        res = self.client.get(ARITHS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        number_of_ariths_in_db = ArithmeticalConceptModel.objects.all().count()
        self.assertEqual(len(res.data), number_of_ariths_in_db)

    def test_list_all_numbers_sucessful(self):
        "Test list all numbers sucessful."

        res = self.client.get(NUMBERS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        number_of_numbers_in_db = NumberModel.objects.all().count()
        self.assertEqual(len(res.data), number_of_numbers_in_db)

    def test_post_list_all_ariths_not_allowed(self):
        "Test post all arithmetical concepts not allowed."

        res = self.client.post(ARITHS_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_list_all_numbers_not_allowed(self):
        "Test post all numbers not allowed."

        res = self.client.post(NUMBERS_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_arith_detail_sucessful(self):
        "Test get arithmetical concept detail sucessful."
        arith = ArithmeticalConceptModel.objects.all()[2]
        arith_id = arith.id
        res = self.client.get(get_arith_url(arith_id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], arith.name)

    def test_number_detail_sucessful(self):
        "Test get number detail sucessful."

        number = NumberModel.objects.all()[2]
        number_id = number.id
        res = self.client.get(get_number_url(number_id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], number.name)
        self.assertIn('count', res.data)

    def test_post_arith_detail_not_allowed(self):
        "Test post arithmetical concept detail not allowed."

        res = self.client.post(get_arith_url(3), {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_number_detail_not_allowed(self):
        "Test post number detail not allowed."

        res = self.client.post(get_number_url(3), {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
