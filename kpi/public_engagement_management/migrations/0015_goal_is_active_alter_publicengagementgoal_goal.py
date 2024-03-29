# Generated by Django 4.1 on 2022-12-20 08:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("public_engagement_management", "0014_alter_publicengagement_note_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="goal",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="publicengagementgoal",
            name="goal",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="public_engagement_management.goal",
            ),
        ),
    ]
