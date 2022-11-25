import os
import json
from pprint import pprint
from functools import partial

import requests
from dotenv import load_dotenv
from django.conf import settings

load_dotenv()

CHARITY_API_KEY = os.getenv("PROJECT_API_KEY")


BASE_URL = "https://api.globalgiving.org/api/public/projectservice"


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

def main():
    from utils import dump_charity_data_to_json
     # Returns all GlobalGiving themes, under which projects are categorized
    data = get_charity_data("/themes")
    dump_charity_data_to_json("themes.json", data)



if __name__ == "__main__":
    main()
   
