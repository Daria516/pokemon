from django.contrib import admin
from .models import Pokemon, UsersPokemons

# Register your models here.
admin.site.register(Pokemon)
admin.site.register(UsersPokemons)