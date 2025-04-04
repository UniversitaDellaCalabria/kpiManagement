# Generated by Django 5.1.3 on 2024-12-16 09:56

import django.db.models.deletion
import public_engagement_monitoring.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizational_area', '0005_alter_organizationalstructureoffice_is_active'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicEngagementAnnualMonitoring',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('year', models.IntegerField(choices=[('', '')], unique=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                 related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                 related_name='%(class)s_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PublicEngagementEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(default='', max_length=300)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('intermediate_taken_date',
                 models.DateTimeField(blank=True, null=True)),
                ('intermediate_validation_date',
                 models.DateTimeField(blank=True, null=True)),
                ('intermediate_validation_success',
                 models.BooleanField(default=False)),
                ('intermediate_notes', models.TextField(default='')),
                ('final_taken_date', models.DateTimeField(blank=True, null=True)),
                ('final_validation_date', models.DateTimeField(blank=True, null=True)),
                ('final_validation_success', models.BooleanField(default=False)),
                ('final_notes', models.TextField(default='')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                 related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                 related_name='%(class)s_modified_by', to=settings.AUTH_USER_MODEL)),
                ('referent', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                 related_name='%(class)s_referent', to=settings.AUTH_USER_MODEL)),
                ('referent_organizational_structure', models.ForeignKey(limit_choices_to={
                 'is_active': True, 'is_internal': True, 'is_public_engagement_enabled': True}, on_delete=django.db.models.deletion.PROTECT, to='organizational_area.organizationalstructure')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PublicEngagementEventMethodOfExecution',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=255)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                 related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                 related_name='%(class)s_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PublicEngagementEventPromoChannel',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=255)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                 related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                 related_name='%(class)s_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PublicEngagementEventPromoTool',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=255)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                 related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                 related_name='%(class)s_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PublicEngagementEventRecipient',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=255)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                 related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                 related_name='%(class)s_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PublicEngagementEventTarget',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=255)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                 related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                 related_name='%(class)s_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PublicEngagementEventType',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=500)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                 related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                 related_name='%(class)s_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PublicEngagementEventData',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(max_length=1500)),
                ('project_scoped', models.BooleanField(default=False)),
                ('project_name', models.CharField(
                    blank=True, default='', max_length=255)),
                ('other_recipients', models.CharField(
                    blank=True, default='', max_length=255)),
                ('geographical_dimension', models.CharField(choices=[('Internazionale', 'Internazionale'), (
                    'Nazionale', 'Nazionale'), ('Regionale', 'Regionale'), ('Locale', 'Locale')], max_length=14)),
                ('organizing_subject', models.CharField(choices=[('UniCal', 'Università della Calabria (Ateneo, Dipartimento o altra struttura)'), (
                    'Altra università', 'Altra università'), ('Altro ente pubblico', 'Altro ente pubblico'), ('Ente privato', 'Ente privato')], max_length=20)),
                ('patronage_requested', models.BooleanField(default=False)),
                ('poster', models.FileField(blank=True, null=True,
                 upload_to=public_engagement_monitoring.models._poster_directory_path)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                 related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 to='public_engagement_monitoring.publicengagementevent')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                 related_name='%(class)s_modified_by', to=settings.AUTH_USER_MODEL)),
                ('person', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('method_of_execution', models.ForeignKey(limit_choices_to={
                 'is_active': True}, on_delete=django.db.models.deletion.PROTECT, to='public_engagement_monitoring.publicengagementeventmethodofexecution')),
                ('promo_channel', models.ManyToManyField(limit_choices_to={
                 'is_active': True}, to='public_engagement_monitoring.publicengagementeventpromochannel')),
                ('promo_tool', models.ManyToManyField(limit_choices_to={
                 'is_active': True}, to='public_engagement_monitoring.publicengagementeventpromotool')),
                ('recipient', models.ManyToManyField(limit_choices_to={
                 'is_active': True}, to='public_engagement_monitoring.publicengagementeventrecipient')),
                ('target', models.ManyToManyField(limit_choices_to={
                 'is_active': True}, to='public_engagement_monitoring.publicengagementeventtarget')),
                ('event_type', models.ForeignKey(limit_choices_to={
                 'is_active': True}, on_delete=django.db.models.deletion.CASCADE, to='public_engagement_monitoring.publicengagementeventtype')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
