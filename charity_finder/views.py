import requests
from django.shortcuts import render
from urllib.parse import unquote
from django.http import HttpRequest, HttpResponse, Http404
from typing import Final, Dict, Any, Optional
from django.db.models import QuerySet

from charity_finder.models import Organization, Project
from .map_visualizer import ProjectMapVisualizer

# Constants for project filtering by funding and region, modifiable by developers for configuration adjustments.
GOAL_MIN: Final[int] = 100_000  # Minimum goal_remaining to include a project in the map
REGION_NAME: Final[str] = "Africa"  # The name of the region to filter projects by
DEFAULT_ORG_PROJ_LOGO: Final[str] = "/static/img/default-logo.jpg"  # Default logo image file if image not available


def fetch_filtered_projects(goal_min: int = GOAL_MIN, region_name: str = REGION_NAME) -> QuerySet[Project]:
    """
    Fetches and filters projects from the database based on given criteria.

    Args:
        goal_min (int): The minimum remaining goal amount for projects to be included. Defaults to GOAL_MIN.
        region_name (str): The name of the region to filter projects by. Defaults to REGION_NAME.

    Returns:
        QuerySet[Project]: A queryset of Project objects that meet the specified criteria.
    """
    projects = Project.objects.filter(goal_remaining__gte=goal_min, region__name=region_name)
    print(f"Filtered {projects.count()} projects for region: {region_name}, min goal: {goal_min}")
    return projects


def calculate_goal_remaining_max(projects: QuerySet[Project]) -> float:
    """
    Calculates and returns the maximum goal_remaining value among the provided projects.

    Args:
        projects (QuerySet[Project]): QuerySet of projects to calculate the maximum goal_remaining value from.

    Returns:
        float: The maximum goal_remaining value among the provided projects. Returns 0.0 if no projects exist.
    """
    if not projects.exists():
        print("No projects found for goal_remaining calculation.")
        return 0.0
    return max(project.goal_remaining for project in projects)


def home(request: HttpRequest) -> HttpResponse:
    """
    Renders the home page with a project map.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: The rendered home page containing the project map or an error message.
    """
    projects: QuerySet[Project] = fetch_filtered_projects()

    if not projects.exists():
        print("No projects available for map visualization.")
        context: Dict[str, Any] = {
            "project_map": None,
            "error_message": "No projects available to display on the map.",
        }
        return render(request, "home.html", context)

    goal_remaining_max: float = calculate_goal_remaining_max(projects)

    visualizer = ProjectMapVisualizer()
    visualizer.add_heat_points_and_popups(projects, goal_remaining_max)

    context: Dict[str, Any] = {
        "project_map": visualizer.project_map._repr_html_(),
    }

    return render(request, "home.html", context)


def search(request: HttpRequest) -> HttpResponse:
    """
    Renders a search results page for organizations based on a user's query.

    Args:
        request (HttpRequest): The incoming HTTP request containing the search query.

    Returns:
        HttpResponse: The rendered search results page with matching organizations or an error message.
    """
    query: str = request.GET.get("query", "").strip()

    if not query:
        print("❌ Empty search query received.")
        return render(request, "orgs_search.html", {"error_message": "No search query provided."})

    try:
        orgs_by_search: QuerySet[Organization] = Organization.objects.filter(name__icontains=query)
        print(f"🔍 Search Query: {query} - Found {orgs_by_search.count()} organizations.")

        for org in orgs_by_search:
            if not org.logo_url:
                print(f"⚠️ Missing logo for organization: {org.name}")

        return render(
            request,
            "orgs_search.html",
            {"orgs_by_search": orgs_by_search, "default_logo": DEFAULT_ORG_PROJ_LOGO},
        )

    except Exception as e:
        print(f"❌ Error in search: {e}")
        return render(request, "orgs_search.html", {"error_message": "An error occurred while searching for organizations."})


def discover_orgs(request: HttpRequest) -> HttpResponse:
    """
    Renders a page to discover organizations based on user-selected themes or countries.

    Args:
        request (HttpRequest): The incoming HTTP request containing filtering parameters.

    Returns:
        HttpResponse: The rendered page with filtered organizations or an error message.
    """
    print("🔍 REQUEST: ", request.GET)

    themes: list[str] = request.GET.getlist("themes")
    countries: list[str] = request.GET.getlist("countries")

    try:
        organizations: QuerySet[Organization] = Organization.objects.all()

        if themes and countries:
            organizations = organizations.filter(themes__name__in=themes, countries__name__in=countries).distinct()
        elif themes:
            organizations = organizations.filter(themes__name__in=themes).distinct()
        elif countries:
            organizations = organizations.filter(countries__name__in=countries).distinct()

        for org in organizations:
            if not org.logo_url:
                print(f"⚠️ Missing logo for organization: {org.name}")

        return render(
            request,
            "orgs_discover.html",
            {"orgs_discover": organizations, "default_logo": DEFAULT_ORG_PROJ_LOGO},
        )

    except Exception as e:
        print(f"❌ Error in discover_orgs: {e}")
        return render(request, "orgs_discover.html", {"error_message": "An error occurred while fetching organizations."})


def get_project_detail(request: HttpRequest, org_id: int) -> HttpResponse:
    """
    Renders the detail page for projects associated with a specific organization.

    Args:
        request (HttpRequest): The incoming HTTP request.
        org_id (int): The ID of the organization whose projects are being retrieved.

    Returns:
        HttpResponse: The rendered project detail page with project information or an error message.
    """
    try:
        project_detail: QuerySet[Project] = Project.objects.filter(org_id=org_id)

        if not project_detail.exists():
            print(f"⚠️ No projects found for organization ID: {org_id}")

        return render(
            request,
            "project_detail.html",
            {"project_detail": project_detail, "default_logo": DEFAULT_ORG_PROJ_LOGO},
        )

    except Exception as e:
        print(f"❌ Error in get_project_detail: {e}")
        return render(request, "project_detail.html", {"error_message": "An error occurred while fetching project details."})


def proxy_image(request: HttpRequest, image_url: Optional[str] = None) -> HttpResponse:
    """
    Fetches and serves an image from an external URL to avoid CORS and ORB restrictions.

    Args:
        request (HttpRequest): The incoming HTTP request.
        image_url (Optional[str]): The external image URL to fetch.

    Returns:
        HttpResponse: The fetched image if successful, otherwise a fallback image.
    """
    if not image_url:
        return serve_fallback_image(DEFAULT_ORG_PROJ_LOGO)

    try:
        decoded_url: str = unquote(image_url)
        response = requests.get(decoded_url, timeout=5)

        if response.status_code != 200:
            raise Exception(f"Image request failed with status {response.status_code}")

        return HttpResponse(response.content, content_type=response.headers.get("Content-Type", "image/jpeg"))

    except Exception as e:
        print(f"⚠️ Error fetching image: {e}, Serving fallback image.")
        return serve_fallback_image(DEFAULT_ORG_PROJ_LOGO)


def serve_fallback_image(fallback_image_path: str) -> HttpResponse:
    """
    Serves a fallback image in case of errors.

    Args:
        fallback_image_path (str): The path to the fallback image.

    Returns:
        HttpResponse: The fallback image response or an HTTP 404 if missing.
    """
    try:
        with open(fallback_image_path, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except FileNotFoundError:
        raise Http404("Fallback image not found")
