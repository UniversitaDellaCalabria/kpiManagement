# Generated by Django 4.1 on 2022-12-20 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "public_engagement_management",
            "0015_goal_is_active_alter_publicengagementgoal_goal",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="goal",
            old_name="goal_type",
            new_name="name",
        ),
        migrations.AddField(
            model_name="goal",
            name="description",
            field=models.TextField(default="", null=True),
        ),
    ]
