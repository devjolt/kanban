from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import User

from datetime import datetime
"""
class UserManager(BaseUserManager):
    def create_user(self, email, password = None, active = True, staff = False, superuser = False):
        if not email:
            raise ValueError('Users must have an email')
        if not password:
            raise ValueError('Users must have a password')
        user = self.model(email = self.normalize_email(email))
        user.set_password(password)
        user.staff = staff
        user.superuser = superuser      
        user.active = active     
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password = None):
        user = self.create_user(email, password = password, staff = True)
        return user

    def create_superuser(self, email, password = None):
        user = self.create_user(email, password = password, staff = True, superuser = True)
        return user

class User(AbstractBaseUser):
    email           = models.EmailField(max_length = 255, unique =True, default = 'abc123@domain.ext')
    active          = models.BooleanField(default = True)#can login
    staff           = models.BooleanField(default = False)#staff user non superuser
    superuser       = models.BooleanField(default = False)#superuser
    
    USERNAME_FIELD = 'email' #to set username
    #username and passwor fields are required by default
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return (str(self.id) + ' ' + ' ' + self.email)

    def has_perm(self, perm, obj=None):
        return self.superuser

    def has_module_perms(self, app_label):
        return self.superuser

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_superuser(self):
        return self.superuser
    
    @property
    def is_active(self):
        return self.active
"""
class Item(models.Model):
    user            = models.ForeignKey(User, on_delete = models.CASCADE, default=1)#associated with user
    name            = models.CharField(max_length = 50, default = 'name your item')
    current_column  = models.PositiveIntegerField(default = 1)
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
    columns         = models.ManyToManyField(Column, related_name='columns', blank = True)
    template        = models.BooleanField(default=True)

    def __str__(self):
        return self.name