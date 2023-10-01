import folium
from folium.plugins import HeatMap
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Max
from typing import List, Tuple, Final

from charity_finder.models import Theme, Organization, Project
from charity_finder import charity_api

def add_heat_points_and_popups(project_map: folium.Map, projects: List[Project], goal_remaining_max) -> None:
    """
    Adds heat points and popups to the given Folium map based on the provided list of projects.
    
    Args:
        project_map (folium.Map): The Folium map object to which heat points and popups will be added.
        projects (List[Project]): A list of project objects containing data for the heat points and popups.
    """
    for project in projects:
        if project.has_map_data:
            # Normalizing the goal_remaining value for the heat map
            goal_norm = float(project.goal_remaining / goal_remaining_max)

            # Creating a list of latitude, longitude, and normalized goal_remaining for the heat point data
            heat_map_data = [[int(project.latitude), int(project.longitude), goal_norm]]

            # Adding a heat point data to the map
            HeatMap(heat_map_data).add_to(project_map)

            # Creating HTML content for the popup with project details
            html = f"""
                    <b>Project Title:</b>{project.title}<br>
                    <a href={project.project_link} target="_blank">Project Link</a><br>
                    <b>Funding Needed:</b>{project.goal_remaining}
                    <b>Funding Weight:</b>{int(project.goal_remaining)}
                    """

            # Creating an iframe with the HTML content and adding it as a popup to the map
            iframe = folium.IFrame(html, width=200, height=100)
            popup = folium.Popup(iframe, max_width=200)
            # Add a clickable marker at a specified location on the map, which displays a popup 
            folium.Marker(
                location=[int(project.latitude), int(project.longitude)],
                tooltip="Click to view Project Summary",
                popup=popup,
            ).add_to(project_map)
            

def get_map() -> folium.Map:
    """
    Creates and returns a Folium heat map object highlighting underserved regions.
    The map is filtered by remaining funding money by Region and normalized data for the heat map.
    The function also adds popups to the map with embedded iframes containing project details.
    
    Returns:
        folium.Map: A Folium map object with heat points and popups based on project data.
    """

    # Constants
    GOAL_LIMIT: Final[int] = 100_000  # Minimum goal_remaining to include a project in the map
    REGION_NAME: Final[str] = "Africa"  # The name of the region to filter projects by
    LAT_LON_INIT: Final[Tuple[float, float]] = (59.09827437369457, 13.115860356662202)  # Initial coordinates for the map
    
    # Fetching and filtering projects from the database
    projects = Project.objects.filter(goal_remaining__gte=GOAL_LIMIT, region__name=REGION_NAME)

    # Finding the maximum goal_remaining value among the filtered projects for normalization
    goal_remaining_max = projects.aggregate(Max("goal_remaining"))["goal_remaining__max"]
    
    # Create a Folium map object centered at the initial latitude and longitude.
    project_map = folium.Map(location=LAT_LON_INIT, zoom_start=3)

    # Adding heat points and popups to the map based on the filtered projects
    add_heat_points_and_popups(project_map, projects, goal_remaining_max)
    
    return project_map


def home(request):
    """
    Django view function to render the home page of the application.
    Calls the get_map function to create a Folium map object and passes it to the home.html template.
    
    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.
        
    Returns:
        HttpResponse: The HTTP response object used to render the home.html template with the Folium map.
    """
    # Creating a Folium map object with the get_map function
    project_map = get_map()
    # Creating a context dictionary to pass data to the template
    
    context = {"project_map": project_map._repr_html_()}  # Get the HTML representation of the Folium map object
    
    # Rendering the home.html template with the context dictionary
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
