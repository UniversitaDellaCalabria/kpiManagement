from django.db import models

from organizational_area.models import OrganizationalStructure
from template.models import CreatedModifiedBy, TimeStampedModel


class PublicEngagement(CreatedModifiedBy, TimeStampedModel):
    subscription_date = models.DateField()
    duration = models.PositiveIntegerField()
    subject = models.TextField()
    structure = models.ForeignKey(OrganizationalStructure,
                                  on_delete=models.PROTECT)
    goal = models.TextField(blank=True, default='')
    requirements_one = models.BooleanField(default=False)
    requirements_two = models.BooleanField(default=False)
    requirements_three = models.BooleanField(default=False)
    note = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{} - {}'.format(self.structure, self.subject)


class PublicEngagementPartner(TimeStampedModel):
    public_engagement = models.ForeignKey(PublicEngagement,
                                          on_delete=models.CASCADE)
    partner = models.ForeignKey(OrganizationalStructure,
                                on_delete=models.PROTECT,
                                limit_choices_to={'is_public_engagement_enabled': True})
    is_head = models.BooleanField(default=False)

    class Meta:
        unique_together = ('public_engagement', 'partner')
        ordering = ('-is_head', 'partner')

    def __str__(self):
        return self.partner.name
