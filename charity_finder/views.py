from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from pprint import pprint
from functools import partial

from charity_finder.models import Theme, Organization, Project
from charity_finder import charity_api

# Create your views here.
def home(request):
    return render(request, "home.html")


def get_orgs_by_theme(request, theme_pk):
    organizations = Organization.objects.filter(themes__id=theme_pk)
    print("Theme pk: ", theme_pk)
   
    context = {
      "orgs_by_theme": organizations
    }

    return render(request, "orgs_theme.html" , context)



