from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Pokemon(models.Model):
    objId = models.CharField(max_length=200)
    created = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    pokemonId = models.IntegerField()
    def __unicode__(self):
        return u'%s' % self.pokemonId