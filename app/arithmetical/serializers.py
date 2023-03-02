"""
Serializers for the arithmetical concept API View.
"""
from core.models import (
    ArithmeticalConceptModel,
    NumberModel,
)
from rest_framework import serializers


class ListArithmeticalConceptSerializer(serializers.ModelSerializer):
    """Serializer for all arithmetical concepts objects."""

    class Meta:
        model = ArithmeticalConceptModel
        fields = ['id', 'name', 'count']
        extra_kwargs = {'id': {'read_only': True}}
        extra_kwargs = {'name': {'read_only': True}}
        extra_kwargs = {'count': {'read_only': True}}


class ListNumberSerializer(serializers.ModelSerializer):
    """Serializer for the number object."""
    count = serializers.SerializerMethodField()

    class Meta:
        model = NumberModel
        fields = ['id', 'name', 'value', 'count']
        extra_kwargs = {'id': {'read_only': True}}
        extra_kwargs = {'name': {'read_only': True}}
        extra_kwargs = {'value': {'read_only': True}}
        extra_kwargs = {'count': {'read_only': True}}

    def get_count(self, obj):
        return obj.arithmetical_concepts.count()


class DetailArithmeticalConceptSerializer(serializers.ModelSerializer):
    """Serializer for detail arithmetical concept object."""
    numbers = ListNumberSerializer(many=True, read_only=True)

    class Meta:
        model = ArithmeticalConceptModel
        fields = ['name', 'description', 'count', 'numbers']
        extra_kwargs = {'name': {'read_only': True}}
        extra_kwargs = {'description': {'read_only': True}}
        extra_kwargs = {'count': {'read_only': True}}
        extra_kwargs = {'numbers': {'read_only': True}}


class ListNumberSerializer(serializers.ModelSerializer):
    """Serializer for all the numbers objects."""
    count = serializers.SerializerMethodField()

    class Meta:
        model = NumberModel
        fields = ['id', 'name', 'value', 'count']
        extra_kwargs = {'id': {'read_only': True}}
        extra_kwargs = {'name': {'read_only': True}}
        extra_kwargs = {'value': {'read_only': True}}
        extra_kwargs = {'count': {'read_only': True}}

    def get_count(self, obj):
        return obj.arithmetical_concepts.count()


class DetailNumberSerializer(serializers.ModelSerializer):
    """Serializer for detail number object."""
    count = serializers.SerializerMethodField()
    arithmetical_concepts = ListArithmeticalConceptSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = NumberModel
        fields = ['name', 'value', 'count', 'arithmetical_concepts']
        extra_kwargs = {'name': {'read_only': True}}
        extra_kwargs = {'value': {'read_only': True}}
        extra_kwargs = {'count': {'read_only': True}}
        extra_kwargs = {'arithmetical_concepts': {'read_only': True}}

    def get_count(self, obj):
        return obj.arithmetical_concepts.count()
