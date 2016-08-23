from django.shortcuts import render
from pokemon.forms import PokemonForm
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