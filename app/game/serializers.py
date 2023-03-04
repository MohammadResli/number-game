"""
Serializers for the game API View.
"""
from core.models import (
    GameModel,
    GameMoveModel,
)
from arithmetical.serializers import (
    ListNumberSerializer,
    ListArithmeticalConceptSerializer,
)


from user.serializers import (
    UserPublicProfileSerializer,
)
from rest_framework import serializers


class ListGamesSerializer(serializers.ModelSerializer):
    """Serializer for all games objects."""
    user = UserPublicProfileSerializer(read_only=True)
    state = serializers.SerializerMethodField()

    class Meta:
        model = GameModel
        fields = ['id', 'user', 'state']
        extra_kwargs = {'id': {'read_only': True}}
        extra_kwargs = {'user': {'read_only': True}}
        extra_kwargs = {'state': {'read_only': True}}

    def get_state(self, obj):
        return obj.game_state


class GameDetailSerializer(serializers.ModelSerializer):
    """Serializer for creating new game."""
    user = UserPublicProfileSerializer(read_only=True)
    state = serializers.SerializerMethodField()
    moves = serializers.SerializerMethodField()
    possible_numbers = ListNumberSerializer(many=True)
    possible_ariths = ListArithmeticalConceptSerializer(many=True)

    class Meta:
        model = GameModel
        fields = ['id', 'user', 'state', 'created_on',
                  'possible_numbers', 'possible_ariths', 'moves']
        extra_kwargs = {'id': {'read_only': True}}
        extra_kwargs = {'user': {'read_only': True}}
        extra_kwargs = {'state': {'read_only': True}}
        extra_kwargs = {'created_on': {'read_only': True}}
        extra_kwargs = {'possible_numbers': {'read_only': True}}
        extra_kwargs = {'possible_ariths': {'read_only': True}}
        extra_kwargs = {'moves': {'read_only': True}}

    def get_state(self, obj):
        return obj.game_state

    def get_moves(self, obj):
        moves = []
        moves_query_set = GameMoveModel.objects.filter(
            game=obj,
        ).order_by('-created_on')
        for move in moves_query_set.all():
            move_obj = {
                "number": move.number.value,
                "created_on": move.created_on,
                'in_hidden': obj.hidden_arith_concept.has_number(move.number),
            }
            moves.append(move_obj)
        return moves
