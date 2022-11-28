import json
from pprint import pprint
from django.core.management.base import BaseCommand
from charity_finder.models import Theme, Org
from charity_finder import charity_api


def seed_themes():
    themes = charity_api.get_charity_data("/projectservice/themes")
    Theme.objects.bulk_create(
        [
            Theme(name=theme["name"], theme_id=theme["id"])
            for theme in themes["themes"]["theme"]
        ]
    )


def seed_active_orgs():
    with open("output_active_orgs.json") as data_file:
        orgs = json.load(data_file)
        # pprint(orgs['organizations']['organization'])
        for org_row in orgs["organizations"]["organization"]:
            org = Org.objects.create(
                name=org_row.get("name", ""),
                org_id=org_row.get("id", 0),
                mission=org_row.get("mission", ""),
                activeProjects=org_row.get("activeProjects", 0),
                totalProjects=org_row.get("totalProjects", 0),
                ein=org_row.get("ein", ""),
                logoUrl=org_row.get("logoUrl", ""),
                addressLine1=org_row.get("addressLine1", ""),
                addressLine2=org_row.get("addressLine2", ""),
                # City where organization resides.
                city=org_row.get("city", ""),
                state=org_row.get("state", ""),
                postal=org_row.get("postal", ""),
                # Country where organization resides.
                country_home=org_row.get("country", ""),
                # one or more themes for this organization
                url=org_row.get("url", ""),
                # one or more countries the organization operates in
            )
            """
            themes = org_row.get("themes", [])
            if not themes:
                continue
            """

            themes_from_json = org_row["themes"]["theme"]

            matching_themes = []
            for row in themes_from_json:
                theme, inserted = Theme.objects.get_or_create(name=row["name"], theme_id=row["id"])
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
            help="Add model name to seed",
        )

    def handle(self, *args, **options):
        if options["model"] == "theme":
            print("Seeding theme data")
            seed_themes()
        else:
            print("Seeding organization data")
            seed_active_orgs()
        print("completed")
