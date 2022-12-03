import json
from pprint import pprint
from django.core.management.base import BaseCommand
from charity_finder.models import Theme, Organization, Country
from charity_finder import charity_api


"""
def get_matching_data(data_from_json):
    matching_data = []

    for row in data_from_json:
        if data_from_json == "themes_from_json":
            theme, inserted = Theme.objects.get_or_create(name=row["name"], theme_id=row["id"])
            matching_data.append(theme)
        else:
            country, inserted = Country.objects.get_or_create(name=data_from_json["name"], country_code=data_from_json["iso3166CountryCode"])
            matching_data.append(country)

    return matching_data
"""



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
        
            #matching_themes = get_matching_data(themes_from_json)
            matching_themes = []
            
            for row in themes_from_json:
                theme, inserted = Theme.objects.get_or_create(name=row["name"], theme_id=row["id"])
                matching_themes.append(theme)

            org.themes.add(*matching_themes)
           
            countries_from_json = org_row["countries"]["country"]
            #matching_countries = get_matching_data(countries_from_json)
            
            matching_countries = []

            for row in countries_from_json:
            
                country, inserted = Country.objects.get_or_create(name=row["name"], country_code=row["iso3166CountryCode"])
            
                matching_countries.append(country)

            org.countries.add(*matching_countries)


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
