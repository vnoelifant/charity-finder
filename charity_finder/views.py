import folium
from folium.plugins import HeatMap
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Max
from typing import List, Tuple, Final, Iterable

from charity_finder.models import Theme, Organization, Project
from charity_finder import charity_api
from .map_visualizer import ProjectMapVisualizer

# Constants for project filtering by funding and region, modifiable by developers for configuration adjustments.
GOAL_MIN: Final[int] = 100_000  # Minimum goal_remaining to include a project in the map
REGION_NAME: Final[str] = "Africa"  # The name of the region to filter projects by


def fetch_filtered_projects(goal_min: int = GOAL_MIN, region_name: str = REGION_NAME):
    """
    Fetch and filter projects from the database based on given criteria.

    Args:
        goal_min (int): The minimum remaining goal amount for projects to be included. Defaults to GOAL_MIN.
        region_name (str): The name of the region to filter projects by. Defaults to REGION_NAME.

    Returns:
        Iterable[Project]: A queryset of Project objects that meet the specified criteria.
    """
    projects = Project.objects.filter(
        goal_remaining__gte=goal_min, region__name=region_name
    )
    return projects


def calculate_goal_remaining_max(projects: Iterable[Project]) -> float:
    """
    Calculates and returns the maximum goal_remaining value among the provided projects.

    Args:
        projects (Iterable[Project]): Iterable of projects to calculate the maximum goal_remaining value from.

    Returns:
        float: The maximum goal_remaining value among the provided projects.
    """
    # Calculate the maximum 'goal_remaining' from the iterable of Project instances for normalization purposes.
    return max(project.goal_remaining for project in projects)


def home(request):
    """
    Django view function to render the home page of the application.
    Instantiates ProjectMapVisualizer to create a Folium map object and passes it to the home.html template.

    Args:
        request (HttpRequest): The HTTP request object containing metadata about the request.

    Returns:
        HttpResponse: The HTTP response object used to render the home.html template with the Folium map.
    """
    # Fetching and filtering projects from the database
    projects = fetch_filtered_projects()

    # Calculate the maximum 'goal_remaining' value among projects. This value is later used
    # to normalize project funding goals for comparative purposes in visualization.
    goal_remaining_max = calculate_goal_remaining_max(projects)

    # Instantiate ProjectMapVisualizer
    visualizer = ProjectMapVisualizer()

    # Adding heat points and popups to the map based on the filtered projects
    visualizer.add_heat_points_and_popups(projects, goal_remaining_max)

    # Creating a context dictionary to pass data to the template
    context = {
        "project_map": visualizer.get_map()._repr_html_()
    }  # Get the HTML representation of the Folium map object

    # Rendering the home.html template with the context dictionary
    return render(request, "home.html", context)


def discover_orgs(request):
    """
    Renders a page to discover organizations based on user-selected themes or countries.

    Args:
        request (HttpRequest): The request object containing GET parameters for themes or countries.

    Returns:
        HttpResponse: The HTTP response object with the rendered organization discovery page.
    """
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
    """
    Renders the detail page for projects associated with a specific organization ID.

    Args:
        request (HttpRequest): The request object.
        org_id (int): The ID of the organization to retrieve projects for.

    Returns:
        HttpResponse: The HTTP response object with the rendered project detail page.
    """
    # Retrieve details for projects associated with a given organization ID.
    project_detail = Project.objects.filter(org_id=org_id)
    print("Project detail object: ", project_detail)

    context = {
        "project_detail": project_detail,
    }

    return render(request, "project_detail.html", context)


def search(request):
    """
    Renders a search results page for organizations based on a user's query.

    Args:
        request (HttpRequest): The request object containing a search query in GET parameters.

    Returns:
        HttpResponse: The HTTP response object with the rendered search results page.
    """
    query = request.GET.get("query")

    # Get Organizations matching search query
    orgs_by_search = Organization.objects.filter(name__contains=query)

    context = {"orgs_by_search": orgs_by_search}

    return render(request, "orgs_search.html", context)
