from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("project_detail/<int:org_id>/", views.get_project_detail, name="project_detail"),
    path("orgs_theme/", views.get_orgs_by_theme, name="orgs_theme"),
    path("orgs_search/", views.search, name="orgs_search"),
    path("heat_map/", views.heat_map, name="heat_map"),
    path("heat_map_data", views.heat_map_data, name="heat_map_data"),
]
