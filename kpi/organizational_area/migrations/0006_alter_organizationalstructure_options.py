# Generated by Django 5.1.4 on 2025-01-22 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizational_area', '0005_alter_organizationalstructureoffice_is_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organizationalstructure',
            options={'ordering': ['name'], 'verbose_name': 'Struttura organizzativa', 'verbose_name_plural': 'Organizational Structures'},
        ),
    ]