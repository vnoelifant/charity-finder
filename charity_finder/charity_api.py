import os
import json
import xmltodict
from pprint import pprint
from functools import partial
# from utils import dump_charity_data_to_json

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PROJECT_API_KEY")
BASE_URL = "https://api.globalgiving.org/api/public/projectservice"


def get_charity_data(endpoint):

    """This function returns a JSON object charity data"""
    url = f"{BASE_URL}{endpoint}"

    print("URL: ", url)

    params = {"api_key": API_KEY}

    response = requests.get(url, params=params)

    return response

    # TODO: DEBUG JSON Decode error when lines below uncommented

    # headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    # response = requests.get(url, params=params, headers=headers)

    # return response.json()


if __name__ == "__main__":
    # Returns all GlobalGiving themes, under which projects are categorized
    data = get_charity_data("/themes")

    data = xmltodict.parse(data.content)
    print(data)
    dump_charity_data_to_json("output.json", data)
