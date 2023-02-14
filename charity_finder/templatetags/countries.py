import json
from django import template
from charity_finder.models import Country


register = template.Library()


@register.simple_tag
def get_countries():

    countries = Country.objects.all()

    return countries