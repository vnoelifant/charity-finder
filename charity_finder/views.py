import folium
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from pprint import pprint
from functools import partial
from folium.plugins import HeatMap

from charity_finder.models import Theme, Organization, Project
from charity_finder import charity_api

# Create your views here.
def home(request):

    m = folium.Map(location=[59.09827437369457, 13.115860356662202], zoom_start=3)

    # TODO: have smaller goals but then limit it to continent or country
    projects = Project.objects.filter(goal_remaining__gte=500_000).values(
        "title", "project_link", "latitude", "longitude", "goal_remaining"
    )

    for project in projects:
        if project["latitude"] and project["longitude"] and project["goal_remaining"]:

            lats_longs = [
                [
                    int(project["latitude"]),
                    int(project["longitude"]),
                    int(project["goal_remaining"]),
                ],
            ]

            title = project["title"]
            url = project["project_link"]

            html = """
                    Project Title: {title} <br>
                    <a href={url}>Project Link</a>
                    """.format(
                title=title, url=url
            )

            iframe = folium.IFrame(html, width=200, height=100)

            popup = folium.Popup(iframe, max_width=200)

            folium.Marker(
                location=[int(project["latitude"]), int(project["longitude"])],
                tooltip="Click to view Project Summary",
                popup=popup,
            ).add_to(m)
            HeatMap(lats_longs).add_to(m)

    m = m._repr_html_()

    context = {
        "m": m,
    }
    return render(request, "home.html", context)


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
