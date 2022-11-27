import os
import json
import requests
from pprint import pprint
from functools import partial
from decouple import config
from django.conf import settings

BASE_URL = "https://api.globalgiving.org/api/public"

def get_charity_data(endpoint):

    """This function returns a JSON object charity data"""
    url = f"{BASE_URL}{endpoint}"

    params = {"api_key": settings.CHARITY_API_KEY}

    headers = {'Accept': 'application/json'}

    response = requests.get(url, params=params, headers=headers)
    return response.json()

   
