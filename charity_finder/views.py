import xmltodict
from django.shortcuts import render
from django.http import HttpResponse
from pprint import pprint
from functools import partial

from charity_finder import charity_api

# Create your views here.
def home(request):

    themes = charity_api.get_charity_data("/themes")

    themes = xmltodict.parse(themes.content)
    print(themes)

    feature_projects = charity_api.get_charity_data("/featured/projects")

    feature_projects = xmltodict.parse(feature_projects.content)
    print(feature_projects)

    context = {"themes": themes, "featured_projects": feature_projects}

    return render(request, "home.html", context)
