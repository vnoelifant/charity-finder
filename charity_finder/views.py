import xmltodict
from django.shortcuts import render
from django.http import HttpResponse
from pprint import pprint
from functools import partial

from charity_finder import charity_api

# Create your views here.
def home(request):

    themes = charity_api.get_charity_data("/themes")

    themes = xmltodict.parse(themes.content) # returns nested dictionary

    # themes = themes['themes']['theme'] # this returns a list

    # themes_cleaned = {theme["name"]: theme["id"] for theme in themes}
    print("Themes: ", themes)

    feature_projects = charity_api.get_charity_data("/featured/projects")

    feature_projects = xmltodict.parse(feature_projects.content)
    # print("Featured projects: ", feature_projects)

    context = {"themes": themes, "featured_projects": feature_projects}

    return render(request, "home.html", context)
