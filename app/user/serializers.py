"""
Serializers for the user API View.
"""
from django.contrib.auth import get_user_model

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
