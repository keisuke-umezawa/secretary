from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)

class Dialogue(models.Model):
    user_name = models.CharField(max_length=10)
    text = models.CharField(max_length=500)

