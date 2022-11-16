import os
import json
from pprint import pprint
from functools import partial
# from utils import dump_charity_data_to_json

import requests
from dotenv import load_dotenv
from django.conf import settings

load_dotenv()

BASE_URL = "https://api.globalgiving.org/api/public/projectservice"


def get_charity_data(endpoint):

    """This function returns a JSON object charity data"""
    url = f"{BASE_URL}{endpoint}"

    print("URL: ", url)

    params = {"api_key": settings.CHARITY_API_KEY}

    # https://www.globalgiving.org/api/how-to-use/tutorial/
    headers = {'Accept': 'application/json'}
    # this is not working! - headers = {'Content-Type': 'application/json'}

    response = requests.get(url, params=params, headers=headers)
    return response.json()


if __name__ == "__main__":
    # Returns all GlobalGiving themes, under which projects are categorized
    data = get_charity_data("/themes")
    print(data)
    #dump_charity_data_to_json("output.json", data)
