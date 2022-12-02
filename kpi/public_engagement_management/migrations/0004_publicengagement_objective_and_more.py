# Generated by Django 4.1.3 on 2022-11-21 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "public_engagement_management",
            "0003_publicengagementpartner_is_head_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="publicengagement",
            name="objective",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="publicengagement",
            name="requirements_one",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="publicengagement",
            name="requirements_three",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="publicengagement",
            name="requirements_two",
            field=models.BooleanField(default=True),
        ),
    ]