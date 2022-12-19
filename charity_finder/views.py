from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from pprint import pprint
from functools import partial

from charity_finder.models import Theme, Organization, Project
from charity_finder import charity_api

# Create your views here.
def home(request):
    return render(request, "home.html")


def get_orgs_by_theme(request):

    themes = request.GET.getlist("themes")

    # Get Theme Organizations matching selected theme names
    organizations = Organization.objects.filter(themes__name__in=themes).distinct()

    context = {"orgs_by_theme": organizations}

    return render(request, "orgs_theme.html", context)


def get_project_detail(request, org_id):
    project_detail = Project.objects.filter(org_id=org_id)

    context = {
        "project_detail": project_detail,
    }

    return render(request, "project_detail.html", context)


def search(request):

    query = request.GET.get("query")

    # Get Organizations matching search query
    orgs_by_search = Organization.objects.filter(name__contains=query)

    context = {"orgs_by_search": orgs_by_search}

    return render(request, "orgs_search.html", context)


def heat_map_data(request):
    data = []

    projects = Project.objects.filter(goal_remaining__gte=10000).values("latitude", "longitude", "goal_remaining")

    for project in projects:
        if project['latitude'] and project['longitude'] and project['goal_remaining']:
            row = {
                "lat": float(project['latitude']),
                "lon": float(project['longitude']),
                "goal": project["goal_remaining"],
            }
            data.append(row)
    print(data)

    return JsonResponse({'data': data}, safe=False)


def heat_map(request):
    # TODO: possible use plugin for loading in leaflet lib: https://django-leaflet.readthedocs.io/en/latest/index.html
    return render(request, "heat_map.html", {})
