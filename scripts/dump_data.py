import json
import requests
import xmltodict
from django.core.management.base import BaseCommand
from charity_finder import charity_api

def dump_charity_data_to_json(output_file, data):
    with open(output_file, "w") as charity_data:
        json.dump(data, charity_data, indent=4, sort_keys=True)

def get_json_data(xml_data):
    with open(xml_data) as xml_file:
        org_json_data = xmltodict.parse(xml_file.read())
    return org_json_data


def run():
    # Get all GlobalGiving themes, under which projects are categorized
    # theme_data = charity_api.get_charity_data("/projectservice/themes")
    # dump_charity_data_to_json("output_themes.json", theme_data)
    
    # Get a download link of all active orgnizations
    org_data = charity_api.get_charity_url_data("/orgservice/all/organizations/active/download")

    # Convert the url file from xml to JSON
    org_json_url = xmltodict.parse(org_data.content)
    dump_charity_data_to_json("output_orgs_url.json", org_json_url)

    # Get the url from JSON
    f = open('output_orgs_url.json')
    url_data = json.load(f)
    url = url_data["download"]["url"]
    response = requests.get(url) 
    
    # Download url data
    with open("output_active_orgs.xml", 'wb') as file:
        file.write(response.content)
    
    # Get all active organizations
    dump_charity_data_to_json("output_active_orgs.json", get_json_data("output_active_orgs.xml"))
   
    





