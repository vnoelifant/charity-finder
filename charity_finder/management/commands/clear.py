from django.core.management.base import BaseCommand
from charity_finder.models import Theme, Organization, Country, Project, Region
from charity_finder import charity_api


def clear_projects():
    Project.objects.all().delete()


def clear_regions():
    Region.objects.all().delete()


def clear_themes():
    Theme.objects.all().delete()


def clear_countries():
    Country.objects.all().delete()


def clear_active_orgs():
    Organization.objects.all().delete()


class Command(BaseCommand):
    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
            "--model",
            help="Specify model to clear, or use 'all' to clear all tables.",
        )

    def handle(self, *args, **options):
        model = options["model"]
        if model == "theme":
            print("Clearing theme data")
            clear_themes()
        elif model == "organization":
            print("Clearing organization data")
            clear_active_orgs()
        elif model == "country":
            print("Clearing country data")
            clear_countries()
        elif model == "project":
            print("Clearing project data")
            clear_projects()
        elif model == "region":
            print("Clearing region data")
            clear_regions()
        elif model == "all":
            print("Clearing all data...")
            clear_projects()
            clear_regions()
            clear_themes()
            clear_countries()
            clear_active_orgs()
        else:
            print("Invalid model specified. Use --model with a valid value.")
        print("Completed")
