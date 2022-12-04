from django.conf import settings
from django.db import models

# Create your models here.
class Theme(models.Model):
    name = models.CharField(max_length=200)
    theme_id = models.CharField(max_length=200)

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.name}: {self.theme_id}"

class Country(models.Model):
    name = models.CharField(max_length=200)
    country_code = models.CharField(max_length=200)
    
    def __str__(self):
        """String for representing the Model object."""
        return f"{self.name}: {self.country_code}"
    class Meta:
        verbose_name_plural = "countries"


class Organization(models.Model):
    name = models.CharField(max_length=200,null=True, blank=True)
    org_id = models.IntegerField(default=0,null=True, blank=True)
    mission = models.TextField(default="", null=True, blank=True)
    active_projects = models.IntegerField(default=0,null=True, blank=True)
    total_projects = models.IntegerField(default=0,null=True, blank=True)
    ein = models.CharField(max_length=200,null=True, blank=True)
    logo_url = models.CharField(max_length=200,null=True, blank=True)
    address_line1 = models.CharField(max_length=200,null=True, blank=True)
    address_line2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200,null=True, blank=True)
    state = models.CharField(max_length=200,null=True, blank=True)
    postal = models.CharField(max_length=200,null=True, blank=True)
    country_home = models.CharField(max_length=200,null=True, blank=True)
    themes = models.ManyToManyField(Theme, related_name='themes', blank=True)
    url = models.CharField(max_length=200,null=True, blank=True)
    countries = models.ManyToManyField(Country, related_name='countries',blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.name}: {self.org_id}"

class Project(models.Model):
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200,null=True, blank=True)
    # ...

    def __str__(self):
        return self.name

    
