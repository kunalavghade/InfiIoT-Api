from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from django.contrib.auth.models import User


class Data(models.Model):
    name = models.CharField(max_length=30)
    value = models.IntegerField()
    timestep = models.DateTimeField(auto_now=True)
    owner = ForeignKey(User, on_delete=CASCADE)
    
    def __str__(self):
        return self.name