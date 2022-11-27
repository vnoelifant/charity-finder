from django.conf import settings
from django.db import models
from django_countries.fields import CountryField

# Create your models here.
class Theme(models.Model):
    name = models.CharField(max_length=200)
    theme_id = models.CharField(max_length=200)

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.name}: {self.theme_id}"


class Country(models.Model):
    country = CountryField()

    # def __str__(self):
    #    """String for representing the Model object."""
    #    return f"{self.country.name}: {self.country.code}"


class Org(models.Model):
    name = models.CharField(max_length=200)
    org_id = models.IntegerField()
    mission = models.TextField()
    activeProjects = models.IntegerField()
    totalProjects = models.IntegerField()
    ein = models.CharField(max_length=200)
    logoUrl = models.CharField(max_length=200)
    addressLine1 = models.CharField(max_length=200)
    addressLine2 = models.CharField(max_length=200)
    # City where organization resides.
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    postal = models.CharField(max_length=200)
    # Country where organization resides.
    country = models.CharField(max_length=200)
    # one or more themes for this organization
    themes = models.JSONField()
    url = models.CharField(max_length=200)
    # one or more countries the organization operates in
    countries = models.JSONField()

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.name}: {self.org_id}"
