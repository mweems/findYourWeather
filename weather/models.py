# from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class City(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	current_city = models.CharField(max_length=30, null=True, blank=True)

class CityList(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	city = models.CharField(max_length=30, null=True, blank=True)
