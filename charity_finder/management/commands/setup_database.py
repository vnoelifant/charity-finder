from django.core.management.base import BaseCommand
from django.core.management import call_command
from charity_finder.models import Organization, Project 

class Command(BaseCommand):
    help = 'Run migrations and seed the database'

    def handle(self, *args, **kwargs):
        # Run migrations
        self.stdout.write("Running migrations...")
        call_command('migrate')

        # Check if organizations already exist
        if not Organization.objects.exists():
            self.stdout.write("Seeding organizations...")
            call_command('import_organizations', '--model', 'organization')
        else:
            self.stdout.write("Organizations already seeded. Skipping.")

        # Check if projects already exist
        if not Project.objects.exists():
            self.stdout.write("Seeding projects...")
            call_command('import_organizations', '--model', 'project')
        else:
            self.stdout.write("Projects already seeded. Skipping.")

        self.stdout.write("Database setup complete!")
