import logging

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify

from visiting_management import settings as visiting_settings

from . decorators import disable_for_loaddata
from . models import (OrganizationalStructure,
                      OrganizationalStructureOffice)


logger = logging.getLogger(__name__)


@receiver(post_save, sender=OrganizationalStructure)
@disable_for_loaddata
def create_visiting_office(sender, instance, created, **kwargs):
    """
    Help-desk Office created by default
    after Structure is created
    """
    if created and instance.is_internal:
        OrganizationalStructureOffice.objects.create(name=visiting_settings.VISITING_OFFICE,
                                                     slug=visiting_settings.VISITING_OFFICE_SLUG,
                                                     description=visiting_settings.VISITING_OFFICE,
                                                     organizational_structure=instance,
                                                     is_default=False,
                                                     is_active=True)
        # log action
        logger.info('[{}] office {}'
                    ' created in structure {}'.format(timezone.localtime(),
                                                      visiting_settings.VISITING_OFFICE,
                                                      instance))
