import os
import json
import requests
from pprint import pprint
from functools import partial
from decouple import config

BASE_URL = "https://api.globalgiving.org/api/public"

CHARITY_API_KEY = config("PROJECT_API_KEY")


def get_charity_data(endpoint):

    """This function returns a JSON object charity data"""
    url = f"{BASE_URL}{endpoint}"

    print("URL: ", url)

    params = {"api_key": CHARITY_API_KEY}

    headers = {'Accept': 'application/json'}

    response = requests.get(url, params=params, headers=headers)
    return response.json()

def main():
    from utils import dump_charity_data_to_json
    # Returns all GlobalGiving themes, under which projects are categorized
    # theme_data = get_charity_data("/projectservice/themes")
    # dump_charity_data_to_json("themes.json", theme_data)
    
    # org_data = get_charity_data("/orgservice/all/organizations/active")
    # dump_charity_data_to_json("orgs.json", org_data)

if __name__ == "__main__":
    main()
   
