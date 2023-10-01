import folium
from folium.plugins import HeatMap
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Avg, Max, Min, Sum
from pprint import pprint
from functools import partial
from typing import Final

from charity_finder.models import Theme, Organization, Project
from charity_finder import charity_api

# Create your views here.
def home(request):

    project_map = get_map()

    context = {
        "project_map": project_map,
    }
    return render(request, "home.html", context)


def get_map():

    # Filtering by remaining funding money by Region
    # TODO:  Include more regions
    GOAL_LIMIT: Final[
        int
    ] = 100_000  # constant marked final, can't assign another value to it
    REGION_NAME: Final[str] = "Africa"
    # Starting Latitude, Longitude coordinates
    LAT_LON_INIT: Final[list] = [59.09827437369457, 13.115860356662202]

    projects = Project.objects.filter(
        goal_remaining__gte=GOAL_LIMIT, region__name=REGION_NAME
    )

    # For normalizing data for heat map
    goal_remaining_max = projects.aggregate(Max("goal_remaining"))

    project_map = folium.Map(location=LAT_LON_INIT, zoom_start=3)

    for project in projects:
        if project.has_map_data:

            # Normalize data for heat map
            goal_norm = float(
                project.goal_remaining / goal_remaining_max["goal_remaining__max"]
            )

            lats_longs = [
                [
                    int(project.latitude),
                    int(project.longitude),
                    goal_norm,
                ],
            ]

            title = project.title
            url = project.project_link
            goal_remaining = int(project.goal_remaining)

            html = f"""
                    <b>Project Title:</b>{title}<br>
                    <a href={url} target="_blank">Project Link</a><br>
                    <b>Funding Needed:</b>{goal_remaining}
                    <b>Funding Weight:</b>{goal_norm}
                   """

            iframe = folium.IFrame(html, width=200, height=100)

            popup = folium.Popup(iframe, max_width=200)

            folium.Marker(
                location=[int(project.latitude), int(project.longitude)],
                tooltip="Click to view Project Summary",
                popup=popup,
            ).add_to(project_map)
            HeatMap(lats_longs).add_to(project_map)

    folium.LayerControl().add_to(project_map)

    project_map = project_map._repr_html_()
    return project_map


def discover_orgs(request):

    print("REQUEST: ", request.GET)
    themes = request.GET.getlist("themes")
    countries = request.GET.getlist("countries")

    if "themes" in request.GET:

        # Get Organizations matching selected theme names
        organizations = Organization.objects.filter(themes__name__in=themes).distinct()

    else:
        # Get Organizations matching selected region names
        organizations = Organization.objects.filter(
            countries__name__in=countries
        ).distinct()

    context = {"orgs_discover": organizations}

    return render(request, "orgs_discover.html", context)


def get_project_detail(request, org_id):
    project_detail = Project.objects.filter(org_id=org_id)
    print("Project detail object: ", project_detail)

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
