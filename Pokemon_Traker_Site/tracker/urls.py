from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^(?P<pokemonId>\d+)/$', views.tracker, name='tracker'),
]
