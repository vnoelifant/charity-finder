import json
from pprint import pprint
from django.core.management.base import BaseCommand
from charity_finder.models import Theme
from charity_finder import charity_api

def seed_themes():
    themes = charity_api.get_charity_data("/projectservice/themes")
    Theme.objects.bulk_create(
        [
            Theme(name=theme["name"], theme_id=theme["id"])
            for theme in themes['themes']['theme']
        ]
    )

def seed_active_orgs():
    with open('output_active_orgs.json') as data_file:    
        orgs = json.load(data_file)
        # pprint(orgs['organizations']['organization'])

class Command(BaseCommand):
    def handle(self, *args, **options):
        # seed_themes()
        seed_active_orgs()
        print("completed")



