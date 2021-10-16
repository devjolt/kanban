from django.contrib import admin
from .models import User, Project, Column, Item
#Register your models here.

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Column)
admin.site.register(Item)
