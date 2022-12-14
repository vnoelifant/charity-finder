from django.contrib import admin
from charity_finder.models import Theme, Country, Organization, Region, Project


# Register your models here.
# admin.site.register(Theme)
# admin.site.register(Country)
# admin.site.register(Organization)


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ("name", "theme_id")


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "country_code",
    )


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "org_id",
    )
    search_fields = ("name",)
    list_filter = (
        "themes",
        "countries",
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project_id",
    )
    search_fields = ("title",)
    list_filter = ("region",)
