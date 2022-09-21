from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'pokemons'

class UsersPokemons(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pokemon = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username