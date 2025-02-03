import requests
from django.shortcuts import render
from django.utils.encoding import iri_to_uri
from django.http import HttpResponse, Http404
from typing import Final, Iterable

from charity_finder.models import Organization, Project
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

    if not projects.exists():
        # Handle the case where no projects are found
        context = {
            "project_map": None,
            "error_message": "No projects available to display on the map.\nPlease check back later.",
        }
        return render(request, "home.html", context)

    # Calculate the maximum 'goal_remaining' value among projects. This value is later used
    # to normalize project funding goals for comparative purposes in visualization.
    goal_remaining_max = calculate_goal_remaining_max(projects)

    # Instantiate ProjectMapVisualizer
    visualizer = ProjectMapVisualizer()

    # Adding heat points and popups to the map based on the filtered projects
    visualizer.add_heat_points_and_popups(projects, goal_remaining_max)

    # Creating a context dictionary to pass data to the template
    context = {
        "project_map": visualizer.project_map._repr_html_()
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

    # Debug: Print logo URLs for each organization
    for organization in organizations:
        print(f"Organization: {organization.name}, Logo URL: {organization.logo_url}")

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
    # print("Project detail object: ", project_detail)

    # Debug: Print image URLs for each project
    for project in project_detail:
        print(f"Project: {project.title}, Image URL: {project.image}")

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

def proxy_image(request, image_url=None):
    """
    Fetches and serves an image from an external URL to avoid CORS and ORB restrictions.
    If the image cannot be loaded, serves a default fallback image.
    """
    fallback_image_path = "static/img/default-logo.jpg"

    # Log the incoming image request
    print(f"Proxy Image Request: {image_url}")

    # If image_url is missing, return fallback
    if not image_url:
        print("No image URL provided, serving default logo.")
        try:
            with open(fallback_image_path, "rb") as f:
                return HttpResponse(f.read(), content_type="image/jpeg")
        except FileNotFoundError:
            raise Http404("Fallback image not found")

    try:
        # Fetch the image from the external URL
        response = requests.get(image_url, timeout=5)

        # Log response status
        print(f"Fetched image from {image_url}, Status Code: {response.status_code}")

        if response.status_code != 200:
            raise Exception(f"Image request failed with status {response.status_code}")

        return HttpResponse(response.content, content_type=response.headers.get("Content-Type", "image/jpeg"))

    except Exception as e:
        print(f"Error fetching image: {e}, Serving fallback image.")

        try:
            with open(fallback_image_path, "rb") as f:
                return HttpResponse(f.read(), content_type="image/jpeg")
        except FileNotFoundError:
            raise Http404("Fallback image not found")