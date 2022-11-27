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
        Org.objects.bulk_create(
            [
                Org(
                    name=org.get("name",""),
                    org_id=org.get("id",0),
                    mission=org.get("mission",""),
                    activeProjects=org.get("activeProjects",0),
                    totalProjects=org.get("totalProjects",0),
                    ein=org.get('ein',""),
                    logoUrl=org.get('logoUrl',""),
                    addressLine1=org.get("addressLine1", ""),
                    addressLine2=org.get("addressLine2",""),
                    # City where organization resides.
                    city=org.get("city",""),
                    state=org.get("state",""),
                    postal=org.get("postal",""),
                    # Country where organization resides.
                    country_home=org.get("country",""),
                    # one or more themes for this organization
                    themes=org.get("themes",""),
                    url=org.get("url",""),
                    # one or more countries the organization operates in
                    countries=org.get("countries",""),
                )
                for org in orgs["organizations"]["organization"]
            ]
        )


class Command(BaseCommand):
    def handle(self, *args, **options):
        #seed_themes()
        seed_active_orgs()
        print("completed")
