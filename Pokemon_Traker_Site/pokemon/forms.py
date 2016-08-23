from django.shortcuts import render
from django import forms
from django.forms import ModelForm
from .models import Pokemon
from django.utils.translation import ugettext_lazy as _

class PokemonForm(ModelForm):
    class Meta:
        model = Pokemon
        fields = [
            'objId',
            'created',
            'latitude',
            'longitude',
            'pokemonId'
        ]
        labels = {
            'created': _('time'),
            'latitude': _('latitude'),
            'longitude': _('longitude'),
            'pokemonId': _('No.'),
        }