# Generated by Django 4.0.6 on 2022-07-28 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('detection_management', '0004_alter_detection_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detection',
            name='code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='detection_management.detectioncode'),
        ),
    ]
