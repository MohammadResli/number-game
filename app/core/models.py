"""
Database models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


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
