# Generated by Django 5.1.4 on 2025-03-05 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_engagement_monitoring', '0040_remove_publicengagementeventreport_other_structure'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicengagementevent',
            name='disabled_notes',
            field=models.TextField(blank=True, default='', verbose_name='Note disabilitazione'),
        ),
    ]
