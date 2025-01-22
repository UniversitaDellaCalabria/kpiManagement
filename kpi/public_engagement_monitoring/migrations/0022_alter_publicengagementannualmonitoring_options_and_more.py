# Generated by Django 5.1.4 on 2025-01-20 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public_engagement_monitoring', '0021_alter_publicengagementannualmonitoring_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='publicengagementannualmonitoring',
            options={'verbose_name': 'Anno di monitoraggio', 'verbose_name_plural': 'Anni di monitoraggio'},
        ),
        migrations.AlterModelOptions(
            name='publicengagementevent',
            options={'verbose_name': 'Iniziativa di Public Engagement', 'verbose_name_plural': 'Iniziative di Public Engagement'},
        ),
        migrations.AlterModelOptions(
            name='publicengagementeventcollaboratortype',
            options={'verbose_name': 'Tipo di collaboratore', 'verbose_name_plural': 'Tipi di collaboratore'},
        ),
        migrations.AlterModelOptions(
            name='publicengagementeventdata',
            options={'verbose_name': 'Dati iniziativa', 'verbose_name_plural': 'Dati iniziative'},
        ),
        migrations.AlterModelOptions(
            name='publicengagementeventpromotool',
            options={'verbose_name': 'Strumento di promozione', 'verbose_name_plural': 'Strumenti di promozione'},
        ),
        migrations.AlterModelOptions(
            name='publicengagementeventrecipient',
            options={'verbose_name': "Destinatario dell'iniziativa", 'verbose_name_plural': 'Destinatari delle iniziative'},
        ),
        migrations.AlterModelOptions(
            name='publicengagementeventreport',
            options={'verbose_name': 'Monitoraggio iniziativa', 'verbose_name_plural': 'Monitoraggio iniziative'},
        ),
        migrations.AlterModelOptions(
            name='publicengagementeventscientificarea',
            options={'verbose_name': 'Area scientifica', 'verbose_name_plural': 'Aree scientifica'},
        ),
        migrations.AlterModelOptions(
            name='publicengagementeventtarget',
            options={'verbose_name': 'Obiettivo iniziative', 'verbose_name_plural': 'Obiettivi iniziative'},
        ),
        migrations.AlterModelOptions(
            name='publicengagementeventtype',
            options={'verbose_name': 'Tipologia iniziativa', 'verbose_name_plural': 'Tipologie iniziative'},
        ),
    ]
