# Generated by Django 5.1.4 on 2025-03-04 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public_engagement_monitoring', '0039_alter_publicengagementeventreport_collaborator_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicengagementeventreport',
            name='other_structure',
        ),
    ]
