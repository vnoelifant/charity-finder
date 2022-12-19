import json
from django import template
from charity_finder.models import Theme

register = template.Library()


@register.simple_tag
def get_themes():

    themes = Theme.objects.all()

    return themes