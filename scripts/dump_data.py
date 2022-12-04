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

def get_url_from_json(input_file):
    # Get the url from JSON
    f = open(input_file)
    url_data = json.load(f)
    url = url_data["download"]["url"]
    response = requests.get(url) 
    return response

def download_url_data(output_file, response):
    with open(output_file, 'wb') as file:
        file.write(response.content)

def run():
    # Get all GlobalGiving themes, under which projects are categorized
    # theme_data = charity_api.get_charity_data("/projectservice/themes")
    # dump_charity_data_to_json("output_themes.json", theme_data)
    
    # Get an XML file containing a URL of all active organizations (bulk data download)
    # Note from GlobalGiving's API:
    # Note that only the XML format is available for download. 
    # You may request the URL using JSON, but the URL will always lead to the XML results.
    org_data = charity_api.get_charity_url_data("/orgservice/all/organizations/active/download")

    # Convert the XML URL file to JSON
    org_json_url = xmltodict.parse(org_data.content)
    dump_charity_data_to_json("output_orgs_url.json", org_json_url)

    # Get the bulk organization url response from JSON
    url_response = get_url_from_json('output_orgs_url.json')
    
    # Download bulk organization data to XML file
    download_url_data("output_active_orgs.xml", url_response)
    
    # Dump bulk organization data to JSON file
    dump_charity_data_to_json("output_active_orgs.json", get_json_data("output_active_orgs.xml"))
   
    





