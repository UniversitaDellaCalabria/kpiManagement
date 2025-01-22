from django.conf import settings


VISITING_OFFICE = getattr(settings, 'VISITING_OFFICE', 'Visiting Management')
VISITING_OFFICE_SLUG = getattr(settings, 'VISITING_OFFICE_SLUG', 'visiting-management')
