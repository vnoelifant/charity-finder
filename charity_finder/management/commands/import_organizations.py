import json
from pprint import pprint
from django.core.management.base import BaseCommand
from charity_finder.models import Theme, Organization
from charity_finder import charity_api


def insert_themes():
    themes = charity_api.get_charity_data("/projectservice/themes")
    Theme.objects.bulk_create(
        [
            Theme(name=theme["name"], theme_id=theme["id"])
            for theme in themes["themes"]["theme"]
        ]
    )


def insert_active_orgs():
    with open("output_active_orgs.json") as data_file:
        orgs = json.load(data_file)
        for org_row in orgs["organizations"]["organization"]:
            org = Organization.objects.create(
                name=org.get("name", ""),
                org_id=org.get("id", 0),
                mission=org.get("mission", ""),
                active_projects=org.get("activeProjects", 0),
                total_projects=org.get("totalProjects", 0),
                ein=org.get("ein", ""),
                logo_url=org.get("logoUrl", ""),
                address_line1=org.get("addressLine1", ""),
                address_line2=org.get("addressLine2", ""),
                city=org.get("city", ""),
                state=org.get("state", ""),
                postal=org.get("postal", ""),
                country_home=org.get("country", ""),
                themes=org.get("themes", ""),
                url=org.get("url", ""),
                countries=org.get("countries", ""),
            )

            themes_from_json = org_row["themes"]["theme"]

            matching_themes = []
            for row in themes_from_json:
                theme, inserted = Theme.objects.get_or_create(
                    name=row["name"], theme_id=row["id"]
                )
                matching_themes.append(theme)

            org.themes.add(*matching_themes)

            # countries=org_row.get("countries", ""),
            # TODO: do same for countries and remove break
            break


class Command(BaseCommand):
    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
            "--model",
            help="Add model name",
        )

    def handle(self, *args, **options):
        if options["model"] == "theme":
            print("Inserting theme data to DB")
            insert_themes()
        elif options["model"] == "org":
            print("Inserting organization data to DB")
            insert_active_orgs()
        print("completed")
