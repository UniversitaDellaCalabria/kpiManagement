from django import template
from django.conf import settings
from django.utils import timezone


register = template.Library()


@register.simple_tag
def year_list():
    return range(2019, timezone.localdate().year+1)


@register.simple_tag
def settings_value(name, **kwargs):
    value = getattr(settings, name, None)
    if value and kwargs: return value.format(**kwargs)
    return value
