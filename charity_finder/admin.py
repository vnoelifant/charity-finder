from django.contrib import admin
from charity_finder.models import Theme, Country, Organization


# Register your models here.
# admin.site.register(Theme)
# admin.site.register(Country)
# admin.site.register(Organization)

@admin.register(Theme)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ("theme_id", "name")

@admin.register(Country)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ("country_code", "name")

@admin.register(Organization)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ("org_id", "name")