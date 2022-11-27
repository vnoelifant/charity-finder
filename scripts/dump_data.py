import json
from django.core.management.base import BaseCommand
from charity_finder import charity_api

def dump_charity_data_to_json(output_file, data):
    with open(output_file, "w") as charity_data:
        json.dump(data, charity_data, indent=4, sort_keys=True)

def run():
    # Returns all GlobalGiving themes, under which projects are categorized
    theme_data = charity_api.get_charity_data("/projectservice/themes")
    dump_charity_data_to_json("output_themes.json", theme_data)
    
    org_data = charity_api.get_charity_data("/orgservice/all/organizations/active")
    dump_charity_data_to_json("output_orgs.json", org_data)




