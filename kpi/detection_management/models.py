from django.db import models

from organizational_area.models import OrganizationalStructure

class Detection(models.Model):
    code = models.CharField(max_length=10)
    date = models.DateField()
    num = models.FloatField()
    den = models.FloatField()
    value = models.FloatField()

    def __str__(self):
        return '{}-{}-{}-{}-{}'.format(self.code, self.date, self.num, self.den, self.value)
