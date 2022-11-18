import json
from django import template
from charity_finder.models import Theme

register = template.Library()


@register.simple_tag
def get_themes():

    themes = Theme.objects.all()

    theme_names = Theme.objects.values_list('name', flat=True)
    
    return theme_names
