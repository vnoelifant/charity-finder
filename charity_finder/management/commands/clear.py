from django.core.management.base import BaseCommand
from charity_finder.models import Theme
from charity_finder import charity_api

def clear_data():
    Theme.objects.all().delete()

class Command(BaseCommand):
    def handle(self, *args, **options):
        clear_data()
        print("completed")


