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

    #paths handling areas with only project names
    path("home/", views.AreaList.as_view(), name= "areas"),
    path('<str:area>/delete_area/',views.AreaDelete.as_view(), name='confirm_delete_area'),
    path('<str:area>/',views.AreaView.as_view(), name='area'),
    
    path('<str:area>/<str:project>/create_project/',views.ProjectCreate.as_view(),name='create_project'),
    path('<str:area>/<str:project>/delete_project/',views.ProjectDelete.as_view(),name='delete_project'),
    path('<str:area>/<str:project>/',views.ProjectView.as_view(),name='project'),
    #path('archive/',name='archive'),
]