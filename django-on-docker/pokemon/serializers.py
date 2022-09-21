from .models import UsersPokemons
from rest_framework import serializers


class UsersPokemonsSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    class Meta:
        model = UsersPokemons
        fields = ('user', 'pokemon')
