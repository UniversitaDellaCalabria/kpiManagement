import sys

from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.functional import lazy
from django.utils.translation import gettext_lazy as _
from organizational_area.models import OrganizationalStructure
from template.models import *


def _get_year_choices():
    current_year = datetime.now().year
    return [(year, year) for year in range(2020, current_year + 1)]


_year_choices = _get_year_choices()
if 'makemigrations' in sys.argv or 'migrate' in sys.argv: # pragma: no cover
    _year_choices = [('', '')]


def _poster_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "public-engagement/events/{0}-{1}/{2}".format(instance.event.id,
                                                         instance.title,
                                                         filename)


class PublicEngagementAnnualMonitoring(ActivableModel, CreatedModifiedBy, TimeStampedModel):
    # serve per definire chiudere o aprire le attività di PE in un anno
    year = models.IntegerField(choices=_year_choices, unique=True)

    def __str__(self):
        return str(self.year)


class PublicEngagementEventType(ActivableModel, CreatedModifiedBy, TimeStampedModel):
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.description


class PublicEngagementEvent(ActivableModel, CreatedModifiedBy, TimeStampedModel):
    title = models.CharField(default='', max_length=300)
    start = models.DateTimeField()
    end = models.DateTimeField()
    # dati referente
    referent = models.ForeignKey(get_user_model(),
                                 on_delete=models.PROTECT,
                                 related_name='%(class)s_referent')
    referent_organizational_structure = models.ForeignKey(OrganizationalStructure,
                                                          on_delete=models.PROTECT,
                                                          limit_choices_to={
                                                            "is_internal": True,
                                                            "is_public_engagement_enabled": True,
                                                            "is_active": True
                                                          }
                                                        )
    # pronto per la validazione
    to_validate = models.BooleanField(default=False)
    # dipartimento
    intermediate_taken_date = models.DateField(null=True, blank=True)
    intermediate_validation_date = models.DateField(null=True, blank=True)
    intermediate_validation_success = models.BooleanField(default=False)
    intermediate_notes = models.TextField(default='', blank=False)
    # ateneo
    final_taken_date = models.DateTimeField(null=True, blank=True)
    final_validation_date = models.DateTimeField(null=True, blank=True)
    final_validation_success = models.BooleanField(default=False)
    final_notes = models.TextField(default='', blank=False)

    def __str__(self):
        return f'{self.title} - {self.referent_organizational_structure}'


class PublicEngagementEventMethodOfExecution(ActivableModel, CreatedModifiedBy, TimeStampedModel):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description


class PublicEngagementEventTarget(ActivableModel, CreatedModifiedBy, TimeStampedModel):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description


class PublicEngagementEventPromoChannel(ActivableModel, CreatedModifiedBy, TimeStampedModel):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description


class PublicEngagementEventPromoTool(ActivableModel, CreatedModifiedBy, TimeStampedModel):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description


class PublicEngagementEventRecipient(ActivableModel, CreatedModifiedBy, TimeStampedModel):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description


class PublicEngagementEventData(CreatedModifiedBy, TimeStampedModel):
    event = models.ForeignKey(PublicEngagementEvent,
                              on_delete=models.CASCADE)
    event_type = models.ForeignKey(PublicEngagementEventType,
                                   on_delete=models.CASCADE,
                                   limit_choices_to={"is_active": True})
    description = models.TextField(max_length=1500)
    person = models.ManyToManyField(get_user_model())
    project_scoped = models.BooleanField(default=False)
    project_name = models.CharField(default='', blank=True, max_length=255)
    recipient = models.ManyToManyField(PublicEngagementEventRecipient,
                                       limit_choices_to={'is_active': True},)
    other_recipients = models.CharField(default='', blank=True, max_length=255)
    target = models.ManyToManyField(PublicEngagementEventTarget,
                                    limit_choices_to={'is_active': True},)
    method_of_execution = models.ForeignKey(PublicEngagementEventMethodOfExecution,
                                            on_delete=models.PROTECT,
                                            limit_choices_to={'is_active': True})
    geographical_dimension = models.CharField(
                                choices=[
                                    ('Internazionale', 'Internazionale'),
                                    ('Nazionale', 'Nazionale'),
                                    ('Regionale', 'Regionale'),
                                    ('Locale', 'Locale'),
                                ],
                                max_length=14
                            )
    organizing_subject = models.CharField(
                            choices=[
                                ('UniCal', 'Università della Calabria (Ateneo, Dipartimento o altra struttura)'),
                                ('Altra università', 'Altra università'),
                                ('Altro ente pubblico', 'Altro ente pubblico'),
                                ('Ente privato', 'Ente privato'),
                            ],
                            max_length=20
                        )
    promo_channel = models.ManyToManyField(PublicEngagementEventPromoChannel,
                                           limit_choices_to={'is_active': True})
    patronage_requested = models.BooleanField(default=False)
    promo_tool = models.ManyToManyField(PublicEngagementEventPromoTool,
                                        limit_choices_to={'is_active': True})
    poster = models.FileField(upload_to=_poster_directory_path,
                              null=True, blank=True)
