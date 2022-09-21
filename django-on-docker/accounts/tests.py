from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from collections import OrderedDict

from django.urls import reverse
from pokemon.models import Pokemon, UsersPokemons
from pokemon.views import add_pokemon
# Create your tests here.

class SigninTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', email='test@test.com', password='12345test12345')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='test', password='12345test12345')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='12345test12345')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_pssword(self):
        user = authenticate(username='test', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)



class ChoosePokemonTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', email='test@test.com', password='12345test12345')
        self.user.save()
        self.pokemon  = Pokemon(name='test_pokemon')
        self.pokemon.save()
        self.response = self.client.login(username='test', password='12345test12345')



    def test_userpokemon_add(self):
        response = self.client.post(reverse('add', kwargs={'pokemon_id': self.pokemon}))
        self.assertTrue(UsersPokemons.objects.filter(user=self.user, pokemon=self.pokemon).exists())



