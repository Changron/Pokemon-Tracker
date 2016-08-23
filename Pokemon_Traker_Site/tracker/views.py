from django.shortcuts import render
from django.http import HttpResponse
from pokemon.models import Pokemon

# Create your views here.
def tracker(request, pokemonId):
    pokemons = Pokemon.objects.filter(pokemonId = pokemonId)
    return render(request,'tracker/tracker.html',{'pokemons':pokemons, 'pokemonId':pokemonId})
