# Generated by Django 5.1.4 on 2025-01-20 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public_engagement_monitoring', '0022_alter_publicengagementannualmonitoring_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='publicengagementeventpromochannel',
            options={'verbose_name': 'Canale di promozione', 'verbose_name_plural': 'Canali di promozione'},
        ),
    ]