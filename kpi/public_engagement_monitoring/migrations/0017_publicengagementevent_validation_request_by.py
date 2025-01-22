# Generated by Django 5.1.4 on 2025-01-10 12:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_engagement_monitoring',
         '0016_publicengagementevent_manager_validated_by_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='publicengagementevent',
            name='validation_request_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='validation_request_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
