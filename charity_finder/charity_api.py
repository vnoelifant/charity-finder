import os
import json
from pprint import pprint
from functools import partial

import requests
from dotenv import load_dotenv

load_dotenv()

CHARITY_API_KEY = os.environ.get("PROJECT_API_KEY", "")


BASE_URL = "https://api.globalgiving.org/api/public"


def get_charity_data(endpoint):

    """This function returns a JSON object charity data"""
    url = f"{BASE_URL}{endpoint}"

    print("URL: ", url)

    params = {"api_key": CHARITY_API_KEY}

    # https://www.globalgiving.org/api/how-to-use/tutorial/
    headers = {'Accept': 'application/json'}
    # this is not working! - headers = {'Content-Type': 'application/json'}

    response = requests.get(url, params=params, headers=headers)
    return response.json()

def cache_themes(endpoint):
    pass

def cache_orgs(endpoint):
   pass



def main():
    from utils import dump_charity_data_to_json
     # Returns all GlobalGiving themes, under which projects are categorized
    theme_data = get_charity_data("/projectservice/themes")
    dump_charity_data_to_json("themes.json", theme_data)
    
    org_data = get_charity_data("/orgservice/all/organizations/active")
    dump_charity_data_to_json("orgs.json", org_data)

if __name__ == "__main__":
    main()
   
