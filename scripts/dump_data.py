import json
import requests
import xmltodict
from charity_finder import charity_api


def dump_charity_data_to_json(output_file, data):
    with open(output_file, "w") as charity_data:
        json.dump(data, charity_data, indent=4, sort_keys=True)


def get_json_data_from_xml(xml_data):
    with open(xml_data) as xml_file:
        org_json_data = xmltodict.parse(xml_file.read())
    return org_json_data


def get_url_from_json(input_file):
    # Get the url from JSON
    with open(input_file) as f:
        url_data = json.load(f)
        url = url_data["download"]["url"]
        response = requests.get(url)
    return response


def download_bulk_data_to_xml(output_file, response):
    with open(output_file, "wb") as file:
        file.write(response.content)


def run():
    # Get all GlobalGiving themes, under which projects are categorized
    # theme_data = charity_api.get_charity_data("/projectservice/themes")
    # dump_charity_data_to_json("output_themes.json", theme_data)

    # Get an XML file containing a URL of all active organizations (bulk data download)
    # Note from GlobalGiving's API:
    # Note that only the XML format is available for download.
    # You may request the URL using JSON, but the URL will always lead to the XML results.
    org_data = charity_api.get_charity_url_data(
        "/orgservice/all/organizations/active/download"
    )

    # Convert the XML URL file to JSON
    org_file = xmltodict.parse(org_data.content)
    dump_charity_data_to_json("output_orgs_url.json", org_file)

    # Get the bulk organization url from JSON
    org_url = get_url_from_json("output_orgs_url.json")

    # Download bulk organization data to XML file
    download_bulk_data_to_xml("output_active_orgs.xml", org_url)

    # Dump bulk organization data to JSON file
    dump_charity_data_to_json(
        "output_active_orgs.json", get_json_data_from_xml("output_active_orgs.xml")
    )

    # Get an XML file containting a URL of all active projects (bulk data download)
    project_data = charity_api.get_charity_url_data(
        "/projectservice/all/projects/active/download.xml"
    )

    # Convert the XML URL file to JSON
    project_file = xmltodict.parse(project_data.content)
    dump_charity_data_to_json("output_projects_url.json", project_file)

    # Get the bulk project url from JSON
    project_url = get_url_from_json("output_projects_url.json")

    # Download bulk project data to XML file
    download_bulk_data_to_xml("output_active_projects.xml", project_url)

    # Dump bulk project data to JSON file
    dump_charity_data_to_json(
        "output_active_projects.json",
        get_json_data_from_xml("output_active_projects.xml"),
    )
