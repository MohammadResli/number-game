"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers

import core


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['user_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 6}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def validate(self, attrs):
        """Validate Create user."""
        user_name = attrs.get('user_name')
        password = attrs.get('password')

        if not core.models.is_user_name_valid(user_name):
            raise serializers.ValidationError("User name is not valid.")

        if not core.models.is_password_valid(password):
            raise serializers.ValidationError("Password is not valid.")

        return attrs


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    user = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        user = attrs.get('user')
        password = attrs.get('password')
        user_user_name = authenticate(
            request=self.context.get('request'),
            user_name=user.lower(),
            password=password,
        )
        if user_user_name:
            attrs['user'] = user_user_name
            return attrs

        user_name_exists = get_user_model().objects.filter(
            email=user
        ).exists()
        if not user_name_exists:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        user_name = get_user_model().objects.get(
            email=user
        ).user_name

        user_email = authenticate(
            request=self.context.get('request'),
            user_name=user_name,
            password=password,
        )
        if user_email:
            attrs['user'] = user_email
            return attrs

        msg = _('Unable to authenticate with provided credentials.')
        raise serializers.ValidationError(msg, code='authorization')


class ManageUserSerializer(serializers.ModelSerializer):
    """Serializer for the update user object."""
    class Meta:
        model = get_user_model()
        fields = ['password', 'nick_name', 'email']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 6}}
        extra_kwargs = {'email': {'read_only': True}}

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
