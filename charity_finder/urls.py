from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("orgs_theme/<str:theme_pk>/", views.get_orgs_by_theme, name="orgs_theme"),
]
