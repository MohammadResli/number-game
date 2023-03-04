"""
URL mappings for game API.
"""
from django.urls import path

from game import views

app_name = 'game'

urlpatterns = [
    path('create/', views.create_game, name='create'),
    path('games/', views.get_all_games, name='games'),
    path('games/<int:id>', views.get_game_detail, name='games'),
    path('games/<int:id>/move/<int:number>', views.create_move, name='moves'),
]
