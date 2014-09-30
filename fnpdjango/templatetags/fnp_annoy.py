from django.conf import settings
from django import template
register = template.Library()


@register.simple_tag
def annoy():
    """Annoy people with 1-percent tax plead.

    To use, set FNP_ANNOY to True
    and add fnpdjango/annoy/annoy.{css,js} to your template.
    """
    if getattr(settings, 'FNP_ANNOY', False):
        return template.loader.render_to_string('fnpdjango/annoy.html')
    else:
        return ""
