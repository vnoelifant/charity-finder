from django.shortcuts import render
from django.http import HttpResponse
from pprint import pprint
from functools import partial

from charity_finder.models import Theme
from charity_finder import charity_api

# Create your views here.
def home(request):
    try:
        Theme.objects.get(theme_id="edu")
        print("Found data in DB")
    except Theme.DoesNotExist:
        print("Calling API for data, and bulk inserting it")
        themes = charity_api.get_charity_data("/themes")
        # https://docs.djangoproject.com/en/4.1/ref/models/querysets/#bulk-create
        Theme.objects.bulk_create(
            [
                Theme(name=theme["name"], theme_id=theme["id"])
                for theme in themes['themes']['theme']
            ]
        )
        """
        # more DB hits:
        for theme in themes['themes']['theme']:
            Theme.objects.create(name=theme["name"], theme_id=theme["id"])
        """

    themes = Theme.objects.values_list('name','theme_id')
  
    context = {"themes": themes}

    return render(request, "home.html", context)
