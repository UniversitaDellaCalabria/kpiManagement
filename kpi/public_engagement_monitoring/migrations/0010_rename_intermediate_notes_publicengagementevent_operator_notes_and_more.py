# Generated by Django 5.1.3 on 2024-12-23 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public_engagement_monitoring',
         '0009_alter_publicengagementevent_final_notes_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='publicengagementevent',
            old_name='intermediate_notes',
            new_name='operator_notes',
        ),
        migrations.RenameField(
            model_name='publicengagementevent',
            old_name='intermediate_taken_date',
            new_name='operator_taken_date',
        ),
        migrations.RenameField(
            model_name='publicengagementevent',
            old_name='intermediate_validation_date',
            new_name='operator_validation_date',
        ),
        migrations.RenameField(
            model_name='publicengagementevent',
            old_name='intermediate_validation_success',
            new_name='operator_validation_success',
        ),
    ]
