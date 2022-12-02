import json
from pprint import pprint
from django.core.management.base import BaseCommand
from charity_finder.models import Theme, Organization
from charity_finder import charity_api


def get_matching_data(data_from_json):
    matching_data = []

    for row in data_from_json:
        type, inserted = (
            Theme.objects.get_or_create(
                name=row.get("name", ""), theme_id=row.get("id", "")
            )
            if data_from_json == "themes_from_json"
            else Theme.objects.get_or_create(
                name=row.get("name", ""), country_code=row.get("iso3166CountryCode", "")
            )
        )

        print("Dict data: ", row)

        matching_data.append(type)

    return matching_data


def insert_active_orgs():
    with open("output_active_orgs.json") as data_file:
        orgs = json.load(data_file)
        # pprint(orgs['organizations']['organization'])
        for org_row in orgs["organizations"]["organization"]:
            org = Organization.objects.create(
                name=org_row.get("name", ""),
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
            """
            themes = org_row.get("themes", [])
            if not themes:
                continue
            """

            themes_from_json = org_row["themes"]["theme"]

            countries_from_json = org_row["countries"]["country"]

            matching_themes = get_matching_data(themes_from_json)

            org.themes.add(*matching_themes)

            # countries=org_row.get("countries", ""),
            matching_countries = get_matching_data(countries_from_json)

            org.themes.add(*matching_countries)


class Command(BaseCommand):
    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
            "--model",
            help="Add model name to seed",
        )

    def handle(self, *args, **options):
        if options["model"] == "org":
            print("Seeding organization data")
            insert_active_orgs()
        print("completed")
