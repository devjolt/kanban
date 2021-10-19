from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User

from datetime import datetime

class Item(models.Model):
    user            = models.ForeignKey(User, on_delete = models.CASCADE, default=1)#associated with user
    name            = models.CharField(max_length = 50, default = 'name your item')
    current_column  = models.PositiveIntegerField(default = 1)
    priority        = models.PositiveIntegerField(default = 3)
    date_added      = models.DateTimeField(default=datetime.now)
    target_date     = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return self.name

class Column(models.Model):
    name            = models.CharField(max_length = 50, default = 'name your column')
    position        = models.PositiveIntegerField()
    items           = models.ManyToManyField(Item, related_name='items', blank = True)

    def __str__(self):
        return self.name

class Project(models.Model):
    user            = models.ForeignKey(User, on_delete = models.CASCADE, default=1)#associated with user
    name            = models.CharField(max_length = 50, default = 'name your project')
    priority        = models.PositiveIntegerField(default = 3)
    columns         = models.ManyToManyField(Column, related_name='columns', blank = True)
    template        = models.BooleanField(default=True)

    def __str__(self):
        return self.name