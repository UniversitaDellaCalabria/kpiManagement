# Generated by Django 5.1.4 on 2025-01-14 07:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_engagement_monitoring', '0017_publicengagementevent_validation_request_by'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='publicengagementevent',
            name='patronage_granted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='publicengagementevent',
            name='patronage_granted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='patronage_granted_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='publicengagementevent',
            name='patronage_granted_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='publicengagementevent',
            name='patronage_granted_notes',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='publicengagementevent',
            name='patronage_operator_taken_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='patronage_taken_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='publicengagementevent',
            name='patronage_operator_taken_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]