from django.urls import path, include
from django.conf.urls import url

from . import views
#from .views import AssetValueViewset

app_name = 'kanban_app'

urlpatterns = [
    path("", views.Landing.as_view(), name='landing'),
    
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name= "logout"),

    path("home/", views.ProjectList.as_view(), name= "home"),

    path('<str:project_name>/project/', views.project_view, name='project_view'),
    path('<str:project_name>/create_project/', views.create_project, name='create_project')
]