from django import template
from django.utils import timezone


register = template.Library()


@register.simple_tag
def year_list():
    return range(2019, timezone.localdate().year+1)
