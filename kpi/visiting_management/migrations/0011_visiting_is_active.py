# Generated by Django 4.0.3 on 2022-04-06 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visiting_management', '0010_alter_visiting_end_date_alter_visiting_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='visiting',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]