# Generated by Django 2.1.7 on 2019-02-26 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unical_accounts', '0002_auto_20180806_1205'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['username'],
                     'verbose_name_plural': 'Utenti UNICAL'},
        ),
        migrations.RenameField(
            model_name='user',
            old_name='location',
            new_name='place_of_birth',
        ),
        migrations.RemoveField(
            model_name='user',
            name='matricola',
        ),
        migrations.AddField(
            model_name='user',
            name='matricola_dipendente',
            field=models.CharField(blank=True, help_text='fonte CSA',
                                   max_length=6, null=True, verbose_name='Matricola Dipendente'),
        ),
        migrations.AddField(
            model_name='user',
            name='matricola_studente',
            field=models.CharField(blank=True, help_text='fonte Esse3',
                                   max_length=6, null=True, verbose_name='Matricola Studente'),
        ),
    ]
