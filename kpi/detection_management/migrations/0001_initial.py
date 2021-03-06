# Generated by Django 4.0.6 on 2022-07-28 10:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizational_area', '0003_alter_organizationalstructureoffice_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DetectionCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('description', models.CharField(max_length=255)),
                ('note', models.TextField(blank=True, default='', max_length=1024)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Detection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('reference_date', models.DateField()),
                ('detaction_date', models.DateField()),
                ('num', models.FloatField()),
                ('den', models.FloatField()),
                ('value', models.FloatField()),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='detection_management.detectioncode')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_modified_by', to=settings.AUTH_USER_MODEL)),
                ('structure', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organizational_area.organizationalstructure')),
            ],
            options={
                'unique_together': {('structure', 'code', 'reference_date')},
            },
        ),
    ]
