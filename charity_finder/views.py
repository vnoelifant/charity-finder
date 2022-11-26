from django.shortcuts import render
from django.http import HttpResponse
from pprint import pprint
from functools import partial

from charity_finder.models import Theme
from charity_finder import charity_api

# Create your views here.
def home(request):
    return render(request, "home.html")


def get_orgs_by_theme():

  pass


