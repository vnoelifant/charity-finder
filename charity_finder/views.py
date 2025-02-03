import requests
from django.shortcuts import render
from django.utils.encoding import iri_to_uri
from django.utils.http import urlunquote
from django.http import HttpResponse, Http404
from typing import Final, Iterable
from django.db.models import Q

from charity_finder.models import Organization, Project
from .map_visualizer import ProjectMapVisualizer

# Constants for project filtering by funding and region, modifiable by developers for configuration adjustments.
GOAL_MIN: Final[int] = 100_000  # Minimum goal_remaining to include a project in the map
REGION_NAME: Final[str] = "Africa"  # The name of the region to filter projects by
DEFAULT_ORG_PROJ_LOGO = "/static/img/default-logo.jpg" # Name of the default logo image file

def fetch_filtered_projects(goal_min: int = GOAL_MIN, region_name: str = REGION_NAME):
    """
    Fetch and filter projects from the database based on given criteria.
    """
    projects = Project.objects.filter(
        goal_remaining__gte=goal_min, region__name=region_name
    )
    print(f"Filtered {projects.count()} projects for region: {region_name}, min goal: {goal_min}")
    return projects

def calculate_goal_remaining_max(projects: Iterable[Project]) -> float:
    """
    Calculates and returns the maximum goal_remaining value among the provided projects.
    """
    if not projects.exists():
        print("No projects found for goal_remaining calculation.")
        return 0
    return max(project.goal_remaining for project in projects)

def home(request):
    """
    Django view function to render the home page of the application.
    """
    projects = fetch_filtered_projects()
    
    if not projects.exists():
        print("No projects available for map visualization.")
        return render(request, "home.html", {"project_map": None, "error_message": "No projects available to display on the map."})

    goal_remaining_max = calculate_goal_remaining_max(projects)
    
    visualizer = ProjectMapVisualizer()
    visualizer.add_heat_points_and_popups(projects, goal_remaining_max)

    return render(request, "home.html", {"project_map": visualizer.project_map._repr_html_()})


def search(request):
    """
    Renders a search results page for organizations based on a user's query.
    Logs and handles missing organization logos.
    """
    query = request.GET.get("query", "").strip()

    if not query:
        print("❌ Empty search query received.")
        return render(request, "orgs_search.html", {"error_message": "No search query provided."})

    try:
        orgs_by_search = Organization.objects.filter(name__icontains=query)
        print(f"🔍 Search Query: {query} - Found {orgs_by_search.count()} organizations.")

        for org in orgs_by_search:
            if not org.logo_url:
                print(f"⚠️ Missing logo for organization: {org.name}")

        return render(request, "orgs_search.html", {"orgs_by_search": orgs_by_search, "default_logo": DEFAULT_ORG_PROJ_LOGO})

    except Exception as e:
        print(f"❌ Error in search: {e}")
        return render(request, "orgs_search.html", {"error_message": "An error occurred while searching for organizations."})

def discover_orgs(request):
    """
    Renders a page to discover organizations based on user-selected themes or countries.
    Supports filtering by both themes and countries together.
    """
    print("🔍 REQUEST: ", request.GET)

    themes = request.GET.getlist("themes")  # List of selected themes
    countries = request.GET.getlist("countries")  # List of selected countries

    try:
        # Start with all organizations
        organizations = Organization.objects.all()

        # Apply filters dynamically
        if themes and countries:
            organizations = organizations.filter(
                themes__name__in=themes, countries__name__in=countries
            ).distinct()
            print(f"✅ Found {organizations.count()} organizations for themes {themes} in countries {countries}")

        elif themes:
            organizations = organizations.filter(themes__name__in=themes).distinct()
            print(f"✅ Found {organizations.count()} organizations for themes {themes}")

        elif countries:
            organizations = organizations.filter(countries__name__in=countries).distinct()
            print(f"✅ Found {organizations.count()} organizations in countries {countries}")

        else:
            print("⚠️ No filters applied. Showing all organizations.")
        
        # Log missing images for debugging
        for org in organizations:
            if not org.logo_url:
                print(f"⚠️ Missing logo for organization: {org.name}")

        return render(request, "orgs_discover.html", {"orgs_discover": organizations, "default_logo": DEFAULT_ORG_PROJ_LOGO})

    except Exception as e:
        print(f"❌ Error in discover_orgs: {e}")
        return render(request, "orgs_discover.html", {"error_message": "An error occurred while fetching organizations."})

def get_project_detail(request, org_id):
    """
    Renders the detail page for projects associated with a specific organization ID.
    Logs and handles missing project images.
    """
    try:
        project_detail = Project.objects.filter(org_id=org_id)

        if not project_detail.exists():
            print(f"⚠️ No projects found for organization ID: {org_id}")

        for project in project_detail:
            if not project.image:
                print(f"⚠️ Missing image for project: {project.title}")

        return render(request, "project_detail.html", {"project_detail": project_detail, "default_logo": DEFAULT_ORG_PROJ_LOGO})

    except Exception as e:
        print(f"❌ Error in get_project_detail: {e}")
        return render(request, "project_detail.html", {"error_message": "An error occurred while fetching project details."})


def proxy_image(request, image_url=None):
    """
    Fetches and serves an image from an external URL to avoid CORS and ORB restrictions.
    If the image cannot be loaded, serves a default fallback image.
    """

    if not image_url:
        print("No image URL provided, serving default logo.")
        return serve_fallback_image(DEFAULT_ORG_PROJ_LOGO)

    try:
        # Decode the URL before making the request
        decoded_url = urlunquote(image_url)
        print(f"✅ Decoded Image URL: {decoded_url}")

        # Fetch the image from the external URL
        response = requests.get(decoded_url, timeout=5)

        if response.status_code != 200:
            raise Exception(f"Image request failed with status {response.status_code}")

        return HttpResponse(response.content, content_type=response.headers.get("Content-Type", "image/jpeg"))

    except Exception as e:
        print(f"⚠️ Error fetching image: {e}, Serving fallback image.")
        return serve_fallback_image()

def serve_fallback_image(fallback_image_path):
    """Serves the fallback image in case of errors."""
  
    try:
        with open(fallback_image_path, "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    except FileNotFoundError:
        raise Http404("Fallback image not found")