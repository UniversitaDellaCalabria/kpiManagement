# Generated by Django 5.1.3 on 2024-12-19 19:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public_engagement_monitoring',
         '0007_alter_publicengagementeventdata_event_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='publicengagementevent',
            old_name='referent_organizational_structure',
            new_name='structure',
        ),
    ]