from django.contrib import admin
from charity_finder.models import Theme, Country, Organization


# Register your models here.
# admin.site.register(Theme)
# admin.site.register(Country)
# admin.site.register(Organization)

@admin.register(Theme)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ("name", "theme_id")

@admin.register(Country)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ("name","country_code")

@admin.register(Organization)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ("name","org_id")
    list_filter = ("themes", "country_home")