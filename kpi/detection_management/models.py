from django.db import models
from django.core.validators import MinValueValidator

from organizational_area.models import OrganizationalStructure

from template.models import CreatedModifiedBy, TimeStampedModel


class DetectionCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=255)
    note = models.TextField(max_length=1024, default='', blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.code} - {self.description}'


class Detection(CreatedModifiedBy, TimeStampedModel):
    structure = models.ForeignKey(OrganizationalStructure,
                                  on_delete=models.PROTECT,
                                  limit_choices_to={'is_internal': True},)
    code = models.ForeignKey(DetectionCode,
                             on_delete=models.PROTECT)
    reference_date = models.DateField()
    detection_date = models.DateField()
    num = models.FloatField(validators=[MinValueValidator(0.0)],)
    den = models.FloatField(validators=[MinValueValidator(0.1)],)
    value = models.FloatField(validators=[MinValueValidator(0.0)],)
    note = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('structure', 'code', 'reference_date')
        ordering = ['code', '-reference_date']

    def __str__(self):
        return f'{self.code} - {self.reference_date}'
