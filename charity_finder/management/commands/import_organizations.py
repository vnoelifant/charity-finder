import json
from pprint import pprint
from django.core.management.base import BaseCommand
from charity_finder.models import Theme, Organization, Country
from charity_finder import charity_api


def insert_active_orgs():
    with open("output_active_orgs.json") as data_file:
        orgs = json.load(data_file)
        # pprint(orgs['organizations']['organization'])
        # print(len(orgs["organizations"]["organization"])) # 3157
        for org_row in orgs["organizations"]["organization"]:
            name = org_row.get("name", "")
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
        print("Completed")