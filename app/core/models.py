"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings

from core.utils import NumberToWords
import random


def is_email_valid(email):
    is_valid = True
    if not email:
        is_valid = False
    return is_valid


def is_user_name_valid(user_name):
    is_valid = True
    if len(user_name) < 4 or len(user_name) > 16:
        is_valid = False
    if not user_name.isalnum():
        is_valid = False
    return is_valid


def is_password_valid(password):
    is_valid = True
    if len(password) < 6:
        is_valid = False
    if not any(char.isdigit() for char in password):
        is_valid = False
    if not any(char.isalpha() for char in password):
        is_valid = False
    return is_valid


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, user_name, email, password, **extra_fields):
        """Create, save and return a new user."""

        if not is_user_name_valid(user_name):
            raise ValueError('User name must be valid.')
        if not is_email_valid(email):
            raise ValueError('Email must be valid.')
        if not is_password_valid(password):
            raise ValueError('Password must be valid.')

        user_name_normalized = user_name.lower()
        user = self.model(
            user_name=user_name_normalized,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.nick_name = user_name
        user.save(using=self._db)

        return user

    def create_superuser(self, user_name, email, password, **extra_fields):
        """Create, save and return a superuser."""
        user = self.create_user(user_name, email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    user_name = models.CharField(max_length=16, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    nick_name = models.CharField(max_length=16)
    objects = UserManager()

    USERNAME_FIELD = 'user_name'


class NumberModel(models.Model):
    """Number object."""
    name = models.CharField(max_length=255)
    value = models.IntegerField()

    def save(self, *args, **kwargs):
        self.name = NumberToWords.convert(self.value)
        return super().save(*args, **kwargs)

    def __str__(self):
        ret = f"{self.name} :({self.value}), found in:"
        ret += "{\n"
        for arith in self.arithmetical_concepts.all():
            ret += "    " + arith.name + ',\n'
        ret += "}\n"
        return ret


class ArithmeticalConceptModel(models.Model):
    """Arithmetical Concept object."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=False)
    count = models.IntegerField(default=0)
    numbers = models.ManyToManyField(
        'NumberModel',
        related_name='arithmetical_concepts',
        blank=True
    )

    def add_number(self, number):
        self.numbers.add(number)
        self.count = self.numbers.all().count()
        self.save()
        return self

    def has_number(self, number):
        num_exists = self.numbers.all().filter(
            value=number.value
        ).exists()
        return num_exists

    def __str__(self):
        ret = f"{self.name} has {self.count} numbers."
        ret += "\n Numbers = {"
        for num in self.numbers.all():
            ret += f"{num.value}, "
        ret += "}\n"
        return ret


class GameMoveManager(models.Manager):
    """ Manager for game move."""
    def create(self, game, number):
        "create game move."
        num_exists = game.possible_numbers.all().filter(
            value=number.value,
        ).exists()
        if not num_exists:
            return None
        move = super().create(game=game, number=number)
        game.update_state_with_move(move)
        game.save()
        return move


class GameMoveModel(models.Model):
    """Game move object."""
    game = models.ForeignKey(
        'GameModel',
        on_delete=models.CASCADE,
        related_name='+',
    )
    created_on = models.DateTimeField(auto_now_add=True)
    number = models.ForeignKey(
        'NumberModel',
        on_delete=models.CASCADE,
        related_name='+',
    )
    objects = GameMoveManager()


class GameManager(models.Manager):
    """Manager for games."""
    def create(self, **game_data):
        game = super().create(**game_data)
        game = self.set_hidden_arith(game)
        game = self.add_possible_ariths(game)
        game.save()
        return game

    def set_hidden_arith(self, game):
        arith_count = ArithmeticalConceptModel.objects.all().count()
        arith_index = random.randint(0, arith_count-1)
        hidden_arith = ArithmeticalConceptModel.objects.all()[arith_index]
        game.hidden_arith_concept = hidden_arith
        game = self.add_possible_arith(game, hidden_arith)
        game.save()
        return game

    def add_possible_ariths(self, game):
        arith_count = ArithmeticalConceptModel.objects.all().count()
        arith_ids = list(range(0, arith_count))
        possible_ariths_ids = random.sample(arith_ids, 7)
        for possible_ariths_id in possible_ariths_ids:
            arith_model = ArithmeticalConceptModel.objects.all()
            possible_arith = arith_model[possible_ariths_id]
            game = self.add_possible_arith(game, possible_arith)
        game.save()
        return game

    def add_possible_arith(self, game, arith):
        game.possible_ariths.add(arith)
        for number in arith.numbers.all():
            game = self.add_possible_number(game, number)
        game.save()
        return game

    def add_possible_number(self, game, number):
        game.possible_numbers.add(number)
        game.save()
        return game


class GameModel(models.Model):
    """Game object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_on = models.DateTimeField(auto_now_add=True)
    hidden_arith_concept = models.ForeignKey(
        'ArithmeticalConceptModel',
        on_delete=models.CASCADE,
        related_name='+',
        null=True,
    )
    possible_ariths = models.ManyToManyField(
        'ArithmeticalConceptModel',
        related_name='+',
        blank=True,
    )
    possible_numbers = models.ManyToManyField(
        'NumberModel',
        related_name='+',
        blank=True,
    )
    game_state = models.CharField(max_length=10, default="Runing...")
    objects = GameManager()

    def update_state_with_move(self, move):
        valid_num = self.hidden_arith_concept.has_number(move.number)
        to_delete = []
        for arith in self.possible_ariths.all():
            if valid_num and not arith.has_number(move.number):
                to_delete.append(arith)
            if not valid_num and arith.has_number(move.number):
                to_delete.append(arith)

        for arith in to_delete:
            self.possible_ariths.remove(arith)
        self.save()
        self.possible_numbers.clear()
        for arith in self.possible_ariths.all():
            for number in arith.numbers.all():
                self.possible_numbers.add(number)
        self.save()
        self.update_game_state()

    def update_game_state(self):
        if self.possible_ariths.all().count() == 1:
            self.game_state = 'Win.'
            self.save()
