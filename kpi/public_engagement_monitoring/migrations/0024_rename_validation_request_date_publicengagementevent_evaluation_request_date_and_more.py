# Generated by Django 5.1.4 on 2025-01-22 09:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_engagement_monitoring', '0023_alter_publicengagementeventpromochannel_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='publicengagementevent',
            old_name='validation_request_date',
            new_name='evaluation_request_date',
        ),
        migrations.RenameField(
            model_name='publicengagementevent',
            old_name='manager_validation_date',
            new_name='manager_evaluation_date',
        ),
        migrations.RenameField(
            model_name='publicengagementevent',
            old_name='manager_validation_success',
            new_name='manager_evaluation_success',
        ),
        migrations.RenameField(
            model_name='publicengagementevent',
            old_name='operator_validation_date',
            new_name='operator_evaluation_date',
        ),
        migrations.RenameField(
            model_name='publicengagementevent',
            old_name='operator_validation_success',
            new_name='operator_evaluation_success',
        ),
        migrations.RenameField(
            model_name='publicengagementevent',
            old_name='to_validate',
            new_name='to_evaluate',
        ),
        migrations.RemoveField(
            model_name='publicengagementevent',
            name='manager_validated_by',
        ),
        migrations.RemoveField(
            model_name='publicengagementevent',
            name='operator_validated_by',
        ),
        migrations.RemoveField(
            model_name='publicengagementevent',
            name='validation_request_by',
        ),
        migrations.AddField(
            model_name='publicengagementevent',
            name='evaluation_request_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='evaluation_request_by', to=settings.AUTH_USER_MODEL, verbose_name='Validazione richiesta da'),
        ),
        migrations.AddField(
            model_name='publicengagementevent',
            name='manager_evaluated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='manager_evaluated_by', to=settings.AUTH_USER_MODEL, verbose_name='Validazione eseguita da manager'),
        ),
        migrations.AddField(
            model_name='publicengagementevent',
            name='operator_evaluated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='operator_evaluated_by', to=settings.AUTH_USER_MODEL, verbose_name='Validazione eseguita da operatore'),
        ),
    ]