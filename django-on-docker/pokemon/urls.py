from django.urls import path
from . import views




urlpatterns = [
    path('', views.all_pokemons, name = 'all'),
    path('details/<pokemon_id>/', views.details, name='details'),
    path('mypokemons/', views.myPokemons, name = 'mypokemon'),
    path('add/<pokemon_id>/', views.add_pokemon, name = 'add'),
    path('delete/<pokemon_id>/', views.delete_pokemon, name = 'delete'),
    path('api', views.UsersPokemonsApiView.as_view()),
    path('alluserspokemons/', views.allUsersPokemons, name = 'alluserspokemons'),
]
