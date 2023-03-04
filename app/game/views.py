"""
Views for the game API.
"""
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    NumberModel,
    GameModel,
    GameMoveModel,
)

from game.serializers import (
    ListGamesSerializer,
    GameDetailSerializer,
)


@api_view(['GET'])
def get_all_games(request):
    "Get list of all games."
    games = GameModel.objects.all().order_by('-created_on')
    serializer = ListGamesSerializer(games, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_game(request):
    game = GameModel.objects.create(user=request.user)
    serializer = GameDetailSerializer(game)
    response = Response(serializer.data, status=status.HTTP_201_CREATED)
    return response


@api_view(['GET'])
def get_game_detail(request, id):
    # check if 404
    if not GameModel.objects.filter(id=id).exists():
        return Response({}, status=status.HTTP_404_NOT_FOUND)
    game = GameModel.objects.get(id=id)
    serializer = GameDetailSerializer(game)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_move(request, id, number):
    # check if 404
    if not GameModel.objects.filter(id=id).exists():
        return Response({}, status=status.HTTP_404_NOT_FOUND)
    game = GameModel.objects.get(id=id)
    # test if the user is autherized to create a move for this game.
    if game.user.id != request.user.id:
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)
    # create a move
    number_obj = NumberModel.objects.get(value=number)
    GameMoveModel.objects.create(game=game, number=number_obj)
    game.refresh_from_db()
    serializer = GameDetailSerializer(game)
    response = Response(serializer.data, status=status.HTTP_201_CREATED)
    return response
