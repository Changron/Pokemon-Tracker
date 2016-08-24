from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.markPokemon, name='markPokemon'),
    url(r'delete/$', views.deletePokemon, name='deletePokemon'),
]
