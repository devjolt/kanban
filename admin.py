from django.contrib import admin
from .models import Project, Column, Item#,user
#Register your models here.

#admin.site.register(User)
admin.site.register(Project)
admin.site.register(Column)
admin.site.register(Item)
