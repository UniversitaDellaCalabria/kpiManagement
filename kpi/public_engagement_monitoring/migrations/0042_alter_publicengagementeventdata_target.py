# Generated by Django 5.1.7 on 2025-03-17 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_engagement_monitoring', '0041_publicengagementevent_disabled_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicengagementeventdata',
            name='target',
            field=models.ManyToManyField(blank=True, limit_choices_to={'is_active': True}, to='public_engagement_monitoring.publicengagementeventtarget', verbose_name='Sustainable Development Goals (SDGs)'),
        ),
    ]
