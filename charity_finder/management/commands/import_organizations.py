import json
import datetime
import requests
import xmltodict
from pprint import pprint
from django.core.management.base import BaseCommand

from charity_finder.models import Theme, Organization, Country, Project, Region
from charity_finder import charity_api


def insert_active_orgs():
    with open("output_active_orgs.json") as data_file:
        orgs = json.load(data_file)
        for org_row in orgs["organizations"]["organization"]:
            name = org_row.get("name", "")
            if not name:
                continue
            org, created = Organization.objects.get_or_create(
                name=name,
                org_id=org_row.get("id", 0),
                mission=org_row.get("mission", ""),
                active_projects=org_row.get("activeProjects", 0),
                total_projects=org_row.get("totalProjects", 0),
                ein=org_row.get("ein", ""),
                logo_url=org_row.get("logoUrl", ""),
                address_line1=org_row.get("addressLine1", ""),
                address_line2=org_row.get("addressLine2", ""),
                city=org_row.get("city", ""),
                state=org_row.get("state", ""),
                postal=org_row.get("postal", ""),
                country_home=org_row.get("country", ""),
                url=org_row.get("url", ""),
            )

            if not created:
                print(f"org {name} was already created.")
                continue

            themes = org_row.get("themes")
            if themes is not None:
                matching_themes = get_matching_themes(themes)
                org.themes.add(*matching_themes)

            countries = org_row.get("countries")
            if countries is not None:
                matching_countries = get_matching_countries(countries)
                org.countries.add(*matching_countries)


def get_matching_themes(themes):
    themes_from_json = themes.get("theme", [])
    matching_themes = []

    if isinstance(themes_from_json, dict):
        themes_from_json = [themes_from_json]

    for row in themes_from_json:
        theme, inserted = Theme.objects.get_or_create(
            name=row.get("name", ""),
            theme_id=row.get("id", ""),
        )
        matching_themes.append(theme)
    return matching_themes


def get_matching_countries(countries):
    countries_from_json = countries.get("country", [])
    matching_countries = []

    if isinstance(countries_from_json, dict):
        countries_from_json = [countries_from_json]

    for row in countries_from_json:
        country, inserted = Country.objects.get_or_create(
            name=row.get("name", ""),
            country_code=row.get("iso3166CountryCode", ""),
        )
        matching_countries.append(country)
    return matching_countries


def insert_active_projects():

    # Create organization dictionary to store organization id and object
    organizations = {}
    organization_objs = Organization.objects.values("org_id")

    for organization_obj in organization_objs:
        organizations[organization_obj["org_id"]] = Organization.objects.get(
            org_id=organization_obj["org_id"]
        )

    # print(organizations)

    with open("output_active_projects.json") as data_file:
        projects = json.load(data_file)
        for project_row in projects["projects"]["project"]:
            title = project_row.get("title", "")
            if not title:
                continue
            project, created = Project.objects.get_or_create(
                title=title,
                summary=project_row.get("summary", ""),
                project_id=project_row.get("id", 0),
                project_link=project_row.get("projectLink", ""),
                active=project_row.get("active", ""),
                status=project_row.get("status", ""),
                activities=project_row.get("activities", ""),
                contact_address_1=project_row.get("contactAddress", ""),
                contact_address_2=project_row.get("contactAddress2", ""),
                contact_city=project_row.get("contactCity", ""),
                contact_country=project_row.get("contactCountry", ""),
                contact_name=project_row.get("contactName", ""),
                contact_title=project_row.get("contactTitle", ""),
                contact_postal=project_row.get("contactPostal", ""),
                contact_state=project_row.get("contactState", ""),
                contact_url=project_row.get("contactUrl", ""),
                donation_options=project_row.get("donationOptions", {}),
                funding=project_row.get("funding", 0),
                goal=project_row.get("goal", 0),
                goal_remaining=project_row.get("remaining", 0),
                long_term_impact=project_row.get("longTermImpact", ""),
                need=project_row.get("need", ""),
                number_donations=project_row.get("numberOfDonations", 0),
                number_reports=project_row.get("numberOfReports", ""),
                progress_report_link=project_row.get("progressReportLink", ""),
                latitude=project_row.get("latitude", 0),
                longitude=project_row.get("longitude", 0),
                notice=project_row.get("notice", ""),
            )

            if not created:
                print(f"project {title} was already created.")
                continue

            # parse videos dictionary for video link
            videos = project_row.get("videos")

            if videos is not None:
                video = videos.get("video", [])
                if isinstance(video, dict):
                    video = [video]

                video_url = video[0].get("url", "")

                project.videos = video_url

            # parse images dictionary for image link
            images = project_row.get("image", {}).get("imagelink", [])
            if images is not None:
                if isinstance(images, dict):
                    images = [images]

                image = [
                    row.get("url") for row in images if row.get("@size") == "large"
                ][0]

                project.image = image

            # get matching organization from foreign key relationship to Organization model
            project_orgs = project_row.get("organization")
            if project_orgs is not None:
                project_org_id = project_orgs.get("id", "")
                project_org_id = int(project_org_id)

                if project_org_id:
                    if project_org_id in organizations:
                        print("Found project org ID in dict......", project_org_id)
                        project.org = organizations.get(project_org_id)
                        print(
                            "Project org ID: ",
                            project_org_id,
                            "Project org obj: ",
                            project.org,
                        )

            # get matching themes from M2M relationship
            themes = project_row.get("themes")

            if themes is not None:
                matching_themes = get_matching_themes(themes)
                project.themes.add(*matching_themes)

            # get primary theme from foreign key relationship to Theme model
            primary_theme = project_row.get("themeName", "")

            if primary_theme is not None:
                theme = Theme.objects.get(name=primary_theme)
                project.primary_theme = theme

            # get matching region from foreign key relationship to Region model
            region = project_row.get("region", "")

            if region is not None:
                region, inserted = Region.objects.get_or_create(name=region)
                project.region = region

            date_format = "%Y-%m-%dT%H:%M:%S%z"

            approved_date = project_row.get("approvedDate", "")

            if approved_date:
                approved_date = datetime.datetime.strptime(approved_date, date_format)
                project.approved_date = approved_date

            date_report = project_row.get("dateOfMostRecentReport", "")

            if date_report:
                date_report = datetime.datetime.strptime(date_report, date_format)
                project.date_report = date_report

            modified_date = project_row.get("modifiedDate", "")

            if modified_date:
                modified_date = datetime.datetime.strptime(modified_date, date_format)
                project.modified_date = modified_date

            project.save()


def get_matching_orgs(organization_ids):
    # Dictionary to store project organization ids and matching organization objects
    project_organizations = {}

    for project_org_id in organization_ids:
        try:
            org = Organization.objects.get(
                org_id=project_org_id
            )  # doing this for every loop row
        except Organization.DoesNotExist:
            print("SKIP: cannot find org id", org)
            continue

        project_organizations[project_org_id] = org

    return project_organizations


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


def download_organizations():

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


def download_projects():
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


class Command(BaseCommand):
    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
            "--model",
            help="Add model name to seed",
        )

    def handle(self, *args, **options):
        if options["model"] == "organization":
            print("Downloading latest active organizations")
            download_organizations()
            print("Seeding organization data")
            insert_active_orgs()

        elif options["model"] == "project":
            print("Downloading latest active projects")
            download_projects()
            print("Seeding project data")
            insert_active_projects()
        print("Completed")
