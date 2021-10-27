from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User

from datetime import datetime

class Item(models.Model):
    """Reside in a column with other items
    """
    user            = models.ForeignKey(User, on_delete = models.CASCADE, default=1)#associated with user
    name            = models.CharField(max_length = 50, default = 'name me!')
    priority        = models.PositiveIntegerField(default = 3)
    date_added      = models.DateTimeField(default=datetime.now)
    blocked         = models.BooleanField(default=False)
    comment         = models.TextField(default='Details...')

    current_column  = models.PositiveIntegerField(default = 1)
    target_date     = models.DateTimeField(blank = True, null = True)
    todo            = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Column(models.Model):
    """Has a position in realtion to other columns (dealt with in views)
    Contains items
    """
    name            = models.CharField(max_length = 50, default = 'name your column')
    position        = models.PositiveIntegerField()
    items           = models.ManyToManyField(Item, related_name='items', blank = True)

    def __str__(self):
        return self.name

class Project(models.Model):
    """Belong to a component row (an area owning many projects)
    Can act as a starting template for other projects, 
    which contain copies the columns of the project (but not the same items).
    Act as a simple action list with two columns (To do, done), indicated by action_list
    Each new area and project gets an action list by default (which may be deleted)
    Action lists and projects differ only in html template formatting
    """
    user            = models.ForeignKey(User, on_delete = models.CASCADE, default=1)#associated with user
    name            = models.CharField(max_length = 50, default = 'name me!')
    priority        = models.PositiveIntegerField(default = 3)
    date_added      = models.DateTimeField(default=datetime.now)

    columns         = models.ManyToManyField(Column, related_name='columns', blank = True)
    template        = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Area(models.Model):
    """template is used to decide whether an instance of this class was created but no longer needed
    After creation, no longer really necessary for Area, but used in Project instances
    """
    user            = models.ForeignKey(User, on_delete = models.CASCADE, default=1)#associated with user
    name            = models.CharField(max_length = 50, default = 'name me!')
    priority        = models.PositiveIntegerField(default = 3)
    date_added      = models.DateTimeField(default=datetime.now)
    
    projects = models.ManyToManyField(Project, related_name='projects', blank = True)  
    
    def __str__(self):
        return self.name

