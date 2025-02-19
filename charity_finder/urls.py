from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path(
        "project_detail/<int:org_id>/", views.get_project_detail, name="project_detail"
    ),
    path("orgs_discover/", views.discover_orgs, name="orgs_discover"),
    path("orgs_search/", views.search, name="orgs_search"),

    # Proxy image route
    path("proxy-image/<path:image_url>/", views.proxy_image, name="proxy_image"),
]
