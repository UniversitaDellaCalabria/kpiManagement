from django.db import models

from organizational_area.models import OrganizationalStructure
from template.models import CreatedModifiedBy, TimeStampedModel


class PublicEngagement(CreatedModifiedBy, TimeStampedModel):
    subscription_date = models.DateField()
    duration = models.PositiveIntegerField()
    subject = models.TextField(blank=True, default='')
    structure = models.ForeignKey(OrganizationalStructure,
                                  on_delete=models.PROTECT)
    goal = models.TextField(blank=True, default='')
    requirements_one = models.BooleanField(default=True)
    requirements_two = models.BooleanField(default=True)
    requirements_three = models.BooleanField(default=True)
    note = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{}-{}-{}'.format(self.subject, self.structure, self.note)


class PublicEngagementPartner(TimeStampedModel):
    public_engagement = models.ForeignKey(PublicEngagement,
                                          on_delete=models.CASCADE)
    partner = models.ForeignKey(OrganizationalStructure,
                                on_delete=models.PROTECT)
    is_head = models.BooleanField(default=False)

    class Meta:
        unique_together = ('public_engagement', 'partner')
        ordering = ('-is_head', 'partner')

    def __str__(self):
        return self.partner.name
