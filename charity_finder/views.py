from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from pprint import pprint
from functools import partial

from charity_finder.models import Theme, Organization, Project
from charity_finder import charity_api

# Create your views here.
def home(request):
    return render(request, "home.html")

def search(request):
    print("REQUEST: ", request.GET)

    themes = request.GET.getlist("themes")
    keyword = request.GET.get("keyword")

    if themes:

        # Get Theme Organizations matching selected theme names
        organizations = Organization.objects.filter(themes__name__in=themes).distinct()

        context = {"orgs_by_theme": organizations, "option": "themes"}

    else:

        # Get Organizations matching search keyword
        orgs_by_keyword = Organization.objects.filter(name__contains=keyword)

        context = {"orgs_by_keyword": orgs_by_keyword, "option": "keyword"}


    return render(request, "orgs_search.html", context)

def get_project_detail(request, org_id):
    project_detail = Project.objects.filter(org__id=org_id)

    context = {
        "project_detail": project_detail,
    }

    return render(request, "project_detail.html", context)
