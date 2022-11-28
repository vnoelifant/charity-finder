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
    country = CountryField(blank=True)

    # def __str__(self):
    #    """String for representing the Model object."""
    #    return f"{self.country.name}: {self.country.code}"
    class Meta:
        verbose_name_plural = "countries"


class Org(models.Model):
    name = models.CharField(max_length=200,null=True, blank=True)
    org_id = models.IntegerField(default=0,null=True, blank=True)
    mission = models.TextField(default="", null=True, blank=True)
    activeProjects = models.IntegerField(default=0,null=True, blank=True)
    totalProjects = models.IntegerField(default=0,null=True, blank=True)
    ein = models.CharField(max_length=200,null=True, blank=True)
    logoUrl = models.CharField(max_length=200,null=True, blank=True)
    addressLine1 = models.CharField(max_length=200,null=True, blank=True)
    addressLine2 = models.CharField(max_length=200, null=True, blank=True)
    # City where organization resides.
    city = models.CharField(max_length=200,null=True, blank=True)
    state = models.CharField(max_length=200,null=True, blank=True)
    postal = models.CharField(max_length=200,null=True, blank=True)
    # Country where organization resides.
    country_home = models.CharField(max_length=200,null=True, blank=True)
    # one or more themes for this organization
    themes = models.ManyToManyField(Theme, related_name='themes')
    url = models.CharField(max_length=200,null=True, blank=True)
    # one or more countries the organization operates in
    countries = models.ManyToManyField(Country, related_name='countries')

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.name}: {self.org_id}"


class Project(models.Model):
    org = models.ForeignKey(Org, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200,null=True, blank=True)
    # ...

    def __str__(self):
        return self.name

