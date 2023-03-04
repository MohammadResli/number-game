"""
Tests for the game API.
"""
from django.test import TestCase
from django.urls import reverse
from django.core.management import call_command
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status
from core.models import (
    GameModel,
)

GAMES_URL = reverse('game:games')
CREATE_GAME_URL = reverse('game:create')


def get_game_url(id):
    return reverse('game:games', args=[id])


def create_user(**params):
    """Create and return a new user."""
    default_user_sign_up_details = {
            'user_name': 'newuser321',
            'email': 'test312@example.com',
            'password': 'testpass123',
        }
    default_user_sign_up_details.update(params)
    user = get_user_model().objects.create_user(**default_user_sign_up_details)
    return user


def get_create_move_url(id, number):
    return reverse('game:moves', args=[id, number])


class PublicGameApiTests(TestCase):
    """Test the public features of the game API."""

    def setUp(self):
        self.client = APIClient()

    def test_list_all_games_sucessful(self):
        "Test list all games."
        res = self.client.get(GAMES_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_post_all_games_not_allowed(self):
        "Test post to all games is not allowed."
        res = self.client.post(GAMES_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_game_by_id_sucessful(self):
        "Test get game details by id."
        user = create_user()
        call_command('create_default_arithmetical_concept')
        game = GameModel.objects.create(user=user)
        game_id = game.id
        res = self.client.get(get_game_url(game_id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class PrivateGameApiTests(TestCase):
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

    def test_create_game_sucessful(self):
        "Test create game sucessful."
        call_command('create_default_arithmetical_concept')
        res = self.client.post(CREATE_GAME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', res.data)

    def test_create_move_to_game_sucessful(self):
        "Test add move to a game."
        call_command('create_default_arithmetical_concept')
        game = GameModel.objects.create(user=self.user)
        game_id = game.id
        number = game.possible_numbers.all()[0]
        res = self.client.post(get_create_move_url(game_id, number.value), {})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_move_unauthorized(self):
        call_command('create_default_arithmetical_concept')
        user2 = create_user()
        game = GameModel.objects.create(user=user2)
        game_id = game.id
        number = game.possible_numbers.all()[0]
        res = self.client.post(get_create_move_url(game_id, number.value), {})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
