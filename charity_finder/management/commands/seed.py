import os
import json
import requests
from pprint import pprint
from functools import partial
from decouple import config
from django.conf import settings
from django.core.management.base import BaseCommand
from charity_finder.models import Theme

BASE_URL = "https://api.globalgiving.org/api/public"

def get_charity_data(endpoint):

    """This function returns a JSON object charity data"""
    url = f"{BASE_URL}{endpoint}"

    print("URL: ", url)

    params = {"api_key": settings.CHARITY_API_KEY}

    headers = {'Accept': 'application/json'}

    response = requests.get(url, params=params, headers=headers)
    return response.json()


def seed_themes():
    themes = get_charity_data("/projectservice/themes")
    Theme.objects.bulk_create(
        [
            Theme(name=theme["name"], theme_id=theme["id"])
            for theme in themes['themes']['theme']
        ]
    )

def clear_data():
    Theme.objects.all().delete()

class Command(BaseCommand):
    def handle(self, *args, **options):
        seed_themes()
        # clear_data()
        print("completed")



