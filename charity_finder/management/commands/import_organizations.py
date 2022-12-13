import json
import datetime
from pprint import pprint
from django.core.management.base import BaseCommand

from charity_finder.models import Theme, Organization, Country, Project, Region
from charity_finder import charity_api


def insert_active_orgs():
    with open("output_active_orgs.json") as data_file:
        orgs = json.load(data_file)
        # pprint(orgs['organizations']['organization'])
        # print(len(orgs["organizations"]["organization"])) # 3157
        for org_row in orgs["organizations"]["organization"]:
            name = org_row.get("name", "")
            if not name:
                continue
            org, created = Organization.objects.get_or_create(
                name=name,
                org_id=org_row.get("id", 0),
                mission=org_row.get("mission", ""),
                active_projects=org_row.get("activeProjects", 0),
                total_projects=org_row.get("totalProjects", 0),
                ein=org_row.get("ein", ""),
                logo_url=org_row.get("logoUrl", ""),
                address_line1=org_row.get("addressLine1", ""),
                address_line2=org_row.get("addressLine2", ""),
                city=org_row.get("city", ""),
                state=org_row.get("state", ""),
                postal=org_row.get("postal", ""),
                country_home=org_row.get("country", ""),
                url=org_row.get("url", ""),
            )
            if not created:
                print(f"org {name} was already created.")
                continue

            themes = org_row.get("themes")
            if themes is not None:
                matching_themes = get_matching_themes(themes)
                org.themes.add(*matching_themes)

            countries = org_row.get("countries")
            if countries is not None:
                matching_countries = get_matching_countries(countries)
                org.countries.add(*matching_countries)


def get_matching_themes(themes):
    themes_from_json = themes.get("theme", [])
    matching_themes = []

    if isinstance(themes_from_json, dict):
        themes_from_json = [themes_from_json]

    for row in themes_from_json:
        theme, inserted = Theme.objects.get_or_create(
            name=row.get("name", ""),
            theme_id=row.get("id", ""),
        )
        matching_themes.append(theme)
    return matching_themes


def get_matching_countries(countries):
    countries_from_json = countries.get("country", [])
    matching_countries = []

    if isinstance(countries_from_json, dict):
        countries_from_json = [countries_from_json]

    for row in countries_from_json:
        country, inserted = Country.objects.get_or_create(
            name=row.get("name", ""),
            country_code=row.get("iso3166CountryCode", ""),
        )
        matching_countries.append(country)
    return matching_countries


def insert_active_projects():
    with open("output_active_projects.json") as data_file:
        projects = json.load(data_file)
        # org = Organization.objects.all()
        # pprint(projects["projects"]["project"]))
        # print(len(projects["projects"]["project"])) #
        for project_row in projects["projects"]["project"]:
            title = project_row.get("title", "")
            if not title:
                continue
            project, created = Project.objects.get_or_create(
                title=title,
                summary=project_row.get("summary", ""),
                project_id=project_row.get("id", 0),
                project_link=project_row.get("projectLink", ""),
                active=project_row.get("active", ""),
                status=project_row.get("status", ""),
                activities=project_row.get("activities", ""),
                contact_address_1=project_row.get("contactAddress", ""),
                contact_address_2=project_row.get("contactAddress2", ""),
                contact_city=project_row.get("contactCity", ""),
                contact_country=project_row.get("contactCountry", ""),
                contact_name=project_row.get("contactName", ""),
                contact_title=project_row.get("contactTitle", ""),
                contact_postal=project_row.get("contactPostal", ""),
                contact_state=project_row.get("contactState", ""),
                contact_url=project_row.get("contactUrl", ""),
                donation_options=project_row.get("donationOptions", dict),
                funding=project_row.get("funding", 0),
                goal=project_row.get("goal", 0),
                goal_remaining=project_row.get("remaining", 0),
                long_term_impact=project_row.get("longTermImpact", ""),
                need=project_row.get("need", ""),
                number_donations=project_row.get("numberOfDonations", 0),
                number_reports=project_row.get("numberOfReports", ""),
                progress_report_link=project_row.get("progressReportLink", ""),
                latitude=project_row.get("latitude", 0),
                longitude=project_row.get("longitude", 0),
                notice=project_row.get("notice", ""),
            )

            if not created:
                print(f"project {title} was already created.")
                continue

            # parse videos dictionary for video link
            videos = project_row.get("videos").get("video", [])

            if videos is not None:
                if isinstance(videos, dict):
                    videos = [videos]

                videos = videos[0].get("url")

                project.videos = videos
                project.save()

            # parse images dictionary for image link
            images = project_row.get("image").get("imagelink", [])

            if images is not None:
                if isinstance(images, dict):
                    images = [images]

                image = [
                    row.get("url") for row in images if row.get("@size") == "large"
                ][0]

                project.image = image
                project.save()

            # get matching organization from foreign key relationship to Organization model
            org_id = project_row.get("organization").get("id")

            if org_id is not None:
                org = Organization.objects.get(org_id=org_id)
                project.org = org
                project.save()

            # get matching themes from M2M relationship
            themes = project_row.get("themes")

            if themes is not None:
                matching_themes = get_matching_themes(themes)
                project.themes.add(*matching_themes)
                project.save()

            # get primary theme from foreign key relationship to Theme model
            primary_theme = project_row.get("themeName", "")

            if primary_theme is not None:
                theme = Theme.objects.get(name=primary_theme)
                project.primary_theme = theme
                project.save()

            # get matching region from foreign key relationship to Region model
            region = project_row.get("region", "")
            if region is not None:
                region, inserted = Region.objects.get_or_create(name=region)
                project.region = region
                project.save()

            date_format = "%Y-%m-%dT%H:%M:%S"

            approved_date = project_row.get("approvedDate", "")[:19]
            if approved_date is not None:
                approved_date = datetime.datetime.strptime(approved_date, date_format)
                project.approved_date = approved_date
                project.save()
            
            if date_report is not None:

                date_report = project_row.get("dateReport", "")[:19]
                date_report = datetime.datetime.strptime(date_report, date_format)
                project.date_report = date_report

            if modified_date is not None:
                modified_date = project_row.get("modifiedDate", "")[:19]
                modified_date = datetime.datetime.strptime(modified_date, date_format)
                project.modified_date = modified_date
                project.save()


class Command(BaseCommand):
    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
            "--model",
            help="Add model name to seed",
        )

    def handle(self, *args, **options):
        if options["model"] == "org":
            print("Seeding organization data")
            insert_active_orgs()
        elif options["model"] == "project":
            print("Seeding project data")
            insert_active_projects()
        print("Completed")
