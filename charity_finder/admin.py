from django.contrib import admin
from charity_finder.models import Theme, Country, Org

# Register your models here.
admin.site.register(Theme)
admin.site.register(Country)
admin.site.register(Org)
