# Generated by Django 4.0 on 2022-03-22 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visiting_management', '0005_alter_visiting_end_date_alter_visiting_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visiting',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='visiting',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]
