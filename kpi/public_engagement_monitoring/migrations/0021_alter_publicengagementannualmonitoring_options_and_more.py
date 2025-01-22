# Generated by Django 5.1.4 on 2025-01-20 16:22

import django.db.models.deletion
import public_engagement_monitoring.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizational_area', '0005_alter_organizationalstructureoffice_is_active'),
        ('public_engagement_monitoring', '0020_alter_publicengagementevent_operator_taken_by_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='publicengagementannualmonitoring',
            options={'verbose_name': 'Anno di monitoraggio'},
        ),
        migrations.AlterModelOptions(
            name='publicengagementevent',
            options={'verbose_name': 'Iniziativa di Public Engagement'},
        ),
        migrations.AlterModelOptions(
            name='publicengagementeventcollaboratortype',
            options={'verbose_name': 'Tipo di collaboratore'},
        ),
        migrations.AlterModelOptions(
            name='publicengagementeventdata',
            options={'verbose_name': 'Dati iniziativa'},
        ),
        migrations.AlterModelOptions(
            name='publicengagementeventmethodofexecution',
            options={'verbose_name': 'Modalità di svolgimento'},
        ),
        migrations.AlterModelOptions(
            name='publicengagementeventpromochannel',
            options={'verbose_name': 'Canale di promozione'},
        ),
        migrations.AlterModelOptions(
            name='publicengagementeventpromotool',
            options={'verbose_name': 'Strumento di promozione'},
        ),
        migrations.AlterModelOptions(
            name='publicengagementeventrecipient',
            options={'verbose_name': "Destinatario dell'iniziativa"},
        ),
        migrations.AlterModelOptions(
            name='publicengagementeventreport',
            options={'verbose_name': 'Monitoraggio iniziativa'},
        ),
        migrations.AlterModelOptions(
            name='publicengagementeventscientificarea',
            options={'verbose_name': 'Area scientifica'},
        ),
        migrations.AlterModelOptions(
            name='publicengagementeventtarget',
            options={'verbose_name': 'Obiettivo iniziativa'},
        ),
        migrations.AlterModelOptions(
            name='publicengagementeventtype',
            options={'verbose_name': 'Tipologia iniziativa'},
        ),
        migrations.AlterField(
            model_name='publicengagementevent',
            name='manager_notes',
            field=models.TextField(blank=True, default='', verbose_name='Note validazione manager'),
        ),
        migrations.AlterField(
            model_name='publicengagementevent',
            name='manager_taken_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='manager_taken_by', to=settings.AUTH_USER_MODEL, verbose_name='Presa in carico da manager'),
        ),
        migrations.AlterField(
            model_name='publicengagementevent',
            name='manager_taken_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data presa in carico manager'),
        ),
        migrations.AlterField(
            model_name='publicengagementevent',
            name='manager_validated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='manager_validated_by', to=settings.AUTH_USER_MODEL, verbose_name='Validazione eseguita da manager'),
        ),
        migrations.AlterField(
            model_name='publicengagementevent',
            name='manager_validation_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data validazione manager'),
        ),
        migrations.AlterField(
            model_name='publicengagementevent',
            name='manager_validation_success',
            field=models.BooleanField(default=False, verbose_name='Validazione manager positiva'),
        ),
        migrations.AlterField(
            model_name='publicengagementevent',
            name='operator_notes',
            field=models.TextField(blank=True, default='', verbose_name='Note validazione operatore'),
        ),
        migrations.AlterField(
            model_name='publicengagementevent',
            name='operator_validated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='operator_validated_by', to=settings.AUTH_USER_MODEL, verbose_name='Validazione eseguita da operatore'),
        ),
        migrations.AlterField(
            model_name='publicengagementevent',
            name='operator_validation_success',
            field=models.BooleanField(default=False, verbose_name='Validazione operatore positiva'),
        ),
        migrations.AlterField(
            model_name='publicengagementevent',
            name='patronage_granted',
            field=models.BooleanField(default=False, verbose_name='Patrocinio concesso'),
        ),
        migrations.AlterField(
            model_name='publicengagementevent',
            name='patronage_granted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='patronage_granted_by', to=settings.AUTH_USER_MODEL, verbose_name='Validazione patrocinio eseguita da operatore'),
        ),
        migrations.AlterField(
            model_name='publicengagementevent',
            name='patronage_granted_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data validazione richiesta patrocinio'),
        ),
        migrations.AlterField(
            model_name='publicengagementevent',
            name='patronage_granted_notes',
            field=models.TextField(blank=True, default='', verbose_name='Note concessione patrocinio'),
        ),
        migrations.AlterField(
            model_name='publicengagementevent',
            name='patronage_operator_taken_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='patronage_taken_by', to=settings.AUTH_USER_MODEL, verbose_name='Presa in carico da operatore patrocinio'),
        ),
        migrations.AlterField(
            model_name='publicengagementevent',
            name='patronage_operator_taken_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Data presa in carico operatore patrocinio'),
        ),
        migrations.AlterField(
            model_name='publicengagementevent',
            name='validation_request_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='validation_request_by', to=settings.AUTH_USER_MODEL, verbose_name='Validazione richiesta da'),
        ),
        migrations.AlterField(
            model_name='publicengagementeventdata',
            name='description',
            field=models.TextField(max_length=1500, verbose_name='Breve descrizione'),
        ),
        migrations.AlterField(
            model_name='publicengagementeventdata',
            name='event_type',
            field=models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.CASCADE, to='public_engagement_monitoring.publicengagementeventtype', verbose_name='Tipologia iniziativa'),
        ),
        migrations.AlterField(
            model_name='publicengagementeventdata',
            name='geographical_dimension',
            field=models.CharField(choices=[('Internazionale', 'Internazionale'), ('Nazionale', 'Nazionale'), ('Regionale', 'Regionale'), ('Locale', 'Locale')], default='', max_length=14, verbose_name='Dimensione Geografica'),
        ),
        migrations.AlterField(
            model_name='publicengagementeventdata',
            name='method_of_execution',
            field=models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.PROTECT, to='public_engagement_monitoring.publicengagementeventmethodofexecution', verbose_name='Modalità di svolgimento'),
        ),
        migrations.AlterField(
            model_name='publicengagementeventdata',
            name='organizing_subject',
            field=models.CharField(choices=[('UniCal', 'Università della Calabria (Ateneo, Dipartimento o altra struttura)'), ('Altra università', 'Altra università'), ('Altro ente pubblico', 'Altro ente pubblico'), ('Ente privato', 'Ente privato')], default='', max_length=20, verbose_name='Ente organizzatore principale dell’iniziativa'),
        ),
        migrations.AlterField(
            model_name='publicengagementeventdata',
            name='other_recipients',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Altri destinatari'),
        ),
        migrations.AlterField(
            model_name='publicengagementeventdata',
            name='patronage_requested',
            field=models.BooleanField(default=False, verbose_name='Si richiede il patrocinio del Dipartimento/Centro per  la seguente iniziativa'),
        ),
        migrations.AlterField(
            model_name='publicengagementeventdata',
            name='person',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Nominativi di altro personale UNICAL coinvolto nell’organizzazione/realizzazione dell’iniziativa'),
        ),
        migrations.AlterField(
            model_name='publicengagementeventdata',
            name='poster',
            field=models.FileField(blank=True, null=True, upload_to=public_engagement_monitoring.models._poster_directory_path, verbose_name='Si allega la locandina'),
        ),
        migrations.AlterField(
            model_name='publicengagementeventdata',
            name='promo_channel',
            field=models.ManyToManyField(blank=True, limit_choices_to={'is_active': True}, to='public_engagement_monitoring.publicengagementeventpromochannel', verbose_name='Si richiede che la seguente iniziativa sia promossa sui seguenti canali di comunicazione istituzionale'),
        ),
        migrations.AlterField(
            model_name='publicengagementeventdata',
            name='promo_tool',
            field=models.ManyToManyField(blank=True, limit_choices_to={'is_active': True}, to='public_engagement_monitoring.publicengagementeventpromotool', verbose_name='Si richiede di utilizzare la dicitura e/o il logo del Dipartimento/Centro nei seguenti strumenti di comunicazione'),
        ),
        migrations.AlterField(
            model_name='publicengagementeventdata',
            name='recipient',
            field=models.ManyToManyField(limit_choices_to={'is_active': True}, to='public_engagement_monitoring.publicengagementeventrecipient', verbose_name='Destinatari'),
        ),
        migrations.AlterField(
            model_name='publicengagementeventdata',
            name='target',
            field=models.ManyToManyField(limit_choices_to={'is_active': True}, to='public_engagement_monitoring.publicengagementeventtarget', verbose_name='Obiettivi di Sviluppo Sostenibile'),
        ),
        migrations.AlterField(
            model_name='publicengagementeventreport',
            name='budget',
            field=models.FloatField(verbose_name='Budget complessivo (in Euro)'),
        ),
        migrations.AlterField(
            model_name='publicengagementeventreport',
            name='collaborator_type',
            field=models.ManyToManyField(limit_choices_to={'is_active': True}, to='public_engagement_monitoring.publicengagementeventcollaboratortype', verbose_name='All’organizzazione/gestione dell’iniziativa sono stati coinvolti in qualità di collaboratori'),
        ),
        migrations.AlterField(
            model_name='publicengagementeventreport',
            name='impact_evaluation',
            field=models.BooleanField(default=False, verbose_name='L’iniziativa è accompagnata da un piano per la valutazione d’impatto?'),
        ),
        migrations.AlterField(
            model_name='publicengagementeventreport',
            name='monitoring_activity',
            field=models.BooleanField(default=False, verbose_name='L’iniziativa è accompagnata da attività di monitoraggio (es. raccolta di informazioni sulle attività, sulle presenze, sul gradimento, ecc.)?'),
        ),
        migrations.AlterField(
            model_name='publicengagementeventreport',
            name='notes',
            field=models.TextField(blank=True, default='', verbose_name='Note'),
        ),
        migrations.AlterField(
            model_name='publicengagementeventreport',
            name='other_structure',
            field=models.ManyToManyField(limit_choices_to={'is_active': True, 'is_internal': True, 'is_public_engagement_enabled': True}, to='organizational_area.organizationalstructure', verbose_name='Con quali altre strutture UNICAL (Dipartimenti o Centri) è stata realizzata l’iniziativa?'),
        ),
        migrations.AlterField(
            model_name='publicengagementeventreport',
            name='participants',
            field=models.IntegerField(default=0, verbose_name="Pubblico non accademico partecipante all'iniziativa o pubblico raggiunto attraverso risorse web/social, pubblicazioni divulgative"),
        ),
        migrations.AlterField(
            model_name='publicengagementeventreport',
            name='scientific_area',
            field=models.ManyToManyField(limit_choices_to={'is_active': True}, to='public_engagement_monitoring.publicengagementeventscientificarea', verbose_name='Aree scientifiche'),
        ),
        migrations.AlterField(
            model_name='publicengagementeventreport',
            name='website',
            field=models.URLField(blank=True, null=True, verbose_name='sito web dell’iniziativa'),
        ),
    ]