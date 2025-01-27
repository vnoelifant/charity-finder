import pytest
from django.core.management import call_command

from charity_finder.models import Organization

ORG_DATA = "tests/fixtures/org.json"


@pytest.fixture
def load_data():
    call_command("loaddata", ORG_DATA)


def test_homepage(client, db):
    response = client.get("/")
    page_html = response.content.decode()
    assert "Philanthropic Finders" in page_html


def test_org_search(client, db, load_data):
    assert Organization.objects.count() == 3
    response = client.get("/orgs_search/?query=CFK")
    assert response.context["orgs_by_search"].count() == 1


def test_projects_exist(client, db, load_data):
    # TODO: requires project setup + having a project view
    # that raises 404
    response = client.get("/project/1")
    assert response.status_code == 200
    response = client.get("/project/87")
    assert response.status_code == 404
