"""
URL mappings for arith API.
"""
from django.urls import path

from arithmetical import views

app_name = 'arith'

urlpatterns = [
    path('ariths/', views.get_all_arithmetical_concepts, name='ariths'),
    path(
            'ariths/<int:id>/',
            views.get_arithmetical_concept_detail,
            name='ariths',
        ),
    path('numbers/', views.get_all_numbers, name='numbers'),
    path('numbers/<int:id>/', views.get_number_detail, name='numbers'),
]
