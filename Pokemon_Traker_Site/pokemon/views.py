from django.shortcuts import render
from pokemon.forms import PokemonForm, DeletePokemon
from pokemon.models import Pokemon
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
@csrf_exempt
def markPokemon(request):
    if request.method == "POST":
        form = PokemonForm(request.POST)
        if form.is_valid():
            try:
                pokemon = Pokemon.objects.get(objId = form.cleaned_data['objId'])
                return HttpResponse("Existed")
            except ObjectDoesNotExist:
                form.save()
                return HttpResponse("Success")
        else:
            return HttpResponse("Fail")
    else:
        form = PokemonForm()
        return render(request,'pokemon/form.html',{'form':form})

def deletePokemon(request):
    if request.method == 'POST':
        form = DeletePokemon(request.POST)
        if form.is_valid():
            try:
                pokemons = Pokemon.objects.filter(pokemonId = form.cleaned_data['number'])
                pokemons.delete()
                return HttpResponse("Successfully Deleted")
            except:
                return HttpResponse("Error")
    else:
        form = DeletePokemon()
        return render(request,'pokemon/form.html',{'form':form})