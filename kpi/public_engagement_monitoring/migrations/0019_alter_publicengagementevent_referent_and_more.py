# Generated by Django 5.1.4 on 2025-01-17 09:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizational_area', '0005_alter_organizationalstructureoffice_is_active'),
        ('public_engagement_monitoring', '0018_publicengagementevent_patronage_granted_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicengagementevent',
            name='referent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_referent', to=settings.AUTH_USER_MODEL, verbose_name='Referente'),
        ),
        migrations.AlterField(
            model_name='publicengagementevent',
            name='structure',
            field=models.ForeignKey(limit_choices_to={'is_active': True, 'is_internal': True, 'is_public_engagement_enabled': True}, on_delete=django.db.models.deletion.PROTECT, to='organizational_area.organizationalstructure', verbose_name='Struttura'),
        ),
        migrations.AlterField(
            model_name='publicengagementevent',
            name='to_validate',
            field=models.BooleanField(default=False, verbose_name='Richiesta di validazione'),
        ),
    ]
