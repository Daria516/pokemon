from django.shortcuts import render
import requests
from .models import Pokemon, UsersPokemons

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .serializers import UsersPokemonsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from operator import itemgetter



# Create your views here.



def all_pokemons(request):
    url = 'https://pokeapi.co/api/v2/pokemon?limit=1154&offset=0'
    
    r = requests.get(url).json()
    pokemons_data = []
    for pokemon in r["results"]:

        pokemon_info = {
            'name' : pokemon["name"],
            'url' : pokemon["url"],
           }
        pokemon_new = Pokemon(name = pokemon["name"])
        pokemon_new.save()
        pokemons_data.append(pokemon_info)
    paginator = Paginator(pokemons_data, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'pokemons_data' : pokemons_data, 'page_obj': page_obj}
    return render(request, 'pokemon/all.html', context)

def allUsersPokemons(request):
    url = 'http://0.0.0.0:8000/api'
    r = requests.get(url).json()
    result_sorted_by_user = sorted(r, key=itemgetter('user'))
    
    context = {'r': r, 'result_sorted_by_user': result_sorted_by_user}
    return render(request, 'pokemon/allUsersPokemons.html', context)


def details(request, pokemon_id):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}/'
    pokemon_data = requests.get(url.format(pokemon_id=pokemon_id)).json()
    pokemon_info = {
        'name' : pokemon_data["name"],
        'base_experience' : pokemon_data['base_experience'],
        'height' : pokemon_data['height'],
        'weight' : pokemon_data['weight'],
        'past_types' : pokemon_data['past_types'],
        'species' : pokemon_data['species']['name'],
           }
    
    game_indices = []
    for game_index in pokemon_data['game_indices']:
        data = str(game_index['game_index'])+":"+str(game_index['version']['name'])
        game_indices.append(data)
    game_indices_list = ', '.join(game_indices)

    stats = []
    for stat in pokemon_data['stats']:
        data = str(stat['stat']['name'])+":"+str(stat['base_stat'])
        stats.append(data)
    stats_list = ', '.join(stats)

    abilities = []
    for ability in pokemon_data['abilities']:
        abilities.append(ability['ability']['name'])
    abilities_list = ', '.join(abilities)
    
    held_items = []
    for held_item in pokemon_data['held_items']:
        held_items.append(held_item['item']['name'])
    held_items_list = ', '.join(held_items)
    
    image = pokemon_data['sprites']['front_default']
    moves = []
    for move in pokemon_data['moves']:
        moves.append(move['move']['name'])  
    moves_str = ', '.join(moves)  
    forms = []
    for form in pokemon_data['forms']:
        forms.append(form['name'])
    forms_list = ', '.join(forms)

    types = []
    for type in pokemon_data['types']:
        data = 'Slot:'+str(type['slot'])+":"+str(type['type']['name'])
        types.append(data)
    types_list = ', '.join(types)

 
    context = {'types_list': types_list,'forms_list':forms_list, 'moves_str':moves_str, 'stats_list':stats_list, 'image': image, 'pokemon_info' :pokemon_info, 'abilities_list' : abilities_list, 'game_indices_list' : game_indices_list, 'held_items_list': held_items_list }

    return render(request, 'pokemon/detail.html', context)
    

@login_required
def myPokemons(request):
    

    current_user = request.user
    pokemons = UsersPokemons.objects.filter(user=current_user) 
 
    context = {'pokemons' : pokemons}
    return render(request, 'pokemon/mypokemons.html', context)

@login_required
def add_pokemon(request, pokemon_id):
    if UsersPokemons.objects.filter(user=request.user, pokemon=pokemon_id).exists():
        answ = 0
        context = {'answ' : answ}
        return render(request, 'pokemon/add.html', context)
    else:
        new = UsersPokemons.objects.create(user=request.user, pokemon=pokemon_id)
        new.save()
        answ = 1
        context = {'answ' : answ}
        return render(request, 'pokemon/add.html', context)

@login_required
def delete_pokemon(request, pokemon_id):
    if UsersPokemons.objects.filter(user=request.user, pokemon=pokemon_id).exists():
        UsersPokemons.objects.filter(user=request.user, pokemon=pokemon_id).delete()
        answ = 1
        context = {'answ' : answ}
        return render(request, 'pokemon/delete.html', context)
    else:

        answ = 0
        context = {'answ' : answ}
        return render(request, 'pokemon/delete.html', context)


class UsersPokemonsApiView(APIView):


    def get(self, request, *args, **kwargs):
        userspokemons = UsersPokemons.objects.all()
        serializer = UsersPokemonsSerializer(userspokemons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



