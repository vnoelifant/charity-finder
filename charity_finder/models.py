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


class Region(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    class Meta:
        verbose_name_plural = "regions"


class Organization(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    type = models.CharField(max_length=200, null=True, blank=True)
    org_id = models.IntegerField(default=0, null=True, blank=True)
    mission = models.TextField(default="", null=True, blank=True)
    active_projects = models.IntegerField(default=0, null=True, blank=True)
    total_projects = models.IntegerField(default=0, null=True, blank=True)
    ein = models.CharField(max_length=200, null=True, blank=True)
    logo_url = models.CharField(max_length=200, null=True, blank=True)
    address_line1 = models.CharField(max_length=200, null=True, blank=True)
    address_line2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    postal = models.CharField(max_length=200, null=True, blank=True)
    country_home = models.CharField(max_length=200, null=True, blank=True)
    themes = models.ManyToManyField(Theme, related_name="themes", blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    countries = models.ManyToManyField(Country, related_name="countries", blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.name}: {self.org_id}"


class Project(models.Model):
    org = models.ForeignKey(
        Organization, on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=200, null=True, blank=True)
    summary = models.TextField(default="", null=True, blank=True)
    project_id = models.IntegerField(default=0, null=True, blank=True)
    project_link = models.CharField(max_length=200, null=True, blank=True)
    active = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=200, null=True, blank=True)
    activities = models.TextField(default="", null=True, blank=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    contact_address_1 = models.CharField(max_length=200, null=True, blank=True)
    contact_address_2 = models.CharField(max_length=200, null=True, blank=True)
    contact_city = models.CharField(max_length=200, null=True, blank=True)
    contact_country = models.CharField(max_length=200, null=True, blank=True)
    contact_name = models.CharField(max_length=200, null=True, blank=True)
    contact_title = models.CharField(max_length=200, null=True, blank=True)
    contact_postal = models.CharField(max_length=200, null=True, blank=True)
    contact_state = models.CharField(max_length=200, null=True, blank=True)
    contact_url = models.CharField(max_length=200, null=True, blank=True)
    countries = models.ManyToManyField(Country, related_name="project_countries", blank=True)
    primary_country = models.ForeignKey(Country, on_delete=models.CASCADE,null=True, blank=True) 
    date_report = models.DateTimeField(null=True, blank=True)
    donation_options = models.JSONField(default=dict, null=True, blank=True)
    funding = models.DecimalField(max_digits=13, decimal_places=2, null=True, blank=True)
    goal = models.DecimalField(max_digits=13, decimal_places=2, null=True, blank=True)
    goal_remaining = models.DecimalField(max_digits=13, decimal_places=2, null=True, blank=True)
    image = models.URLField(max_length = 200, null=True, blank=True)
    long_term_impact = models.TextField(default="", null=True, blank=True)
    need = models.TextField(default="", null=True, blank=True)
    modified_date = models.DateTimeField(null=True, blank=True)
    number_donations = models.IntegerField(default=0, null=True, blank=True)
    number_reports = models.IntegerField(default=0, null=True, blank=True)
    progress_report_link = models.URLField(max_length = 200, null=True, blank=True)
    themes = models.ManyToManyField(Theme, related_name="project_themes", blank=True)
    primary_theme = models.ForeignKey(Theme, on_delete=models.CASCADE,null=True, blank=True) 
    videos = models.URLField(max_length = 200, null=True, blank=True)
    latitude = models.DecimalField(max_digits=13, decimal_places=2)
    longitude = models.DecimalField(max_digits=13, decimal_places=2)
    notice = models.TextField(default="", null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.title}: {self.project_id}"
