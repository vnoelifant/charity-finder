from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Run migrations and seed the database'

    def handle(self, *args, **kwargs):
        # Run migrations
        self.stdout.write("Running migrations...")
        call_command('migrate')

        # Seed the database
        self.stdout.write("Seeding organizations...")
        call_command('import_organizations', '--model', 'organization')

        self.stdout.write("Seeding projects...")
        call_command('import_organizations', '--model', 'project')

        self.stdout.write("Database setup complete!")
