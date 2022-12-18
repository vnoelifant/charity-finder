from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("project_detail/<int:org_id>/", views.get_project_detail, name="project_detail"),
    path("orgs_search/", views.search, name="orgs_search"),
]
