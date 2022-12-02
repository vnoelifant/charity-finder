from django.core.management.base import BaseCommand
from charity_finder.models import Theme, Organization
from charity_finder import charity_api


def clear_themes():
    Theme.objects.all().delete()


def clear_active_orgs():
    Org.objects.all().delete()


class Command(BaseCommand):
    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
            "--model",
            help="Add model name to clear",
        )

    def handle(self, *args, **options):
        if options["model"] == "theme":
            print("Clearing theme data")
            clear_themes()
        elif options["model"] == "org":
            print("Clearing organization data")
            clear_active_orgs()
        print("completed")
