# Generated by Django 4.1.3 on 2022-11-21 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("organizational_area", "0001_initial"),
        ("public_engagement_management", "0002_remove_partner_city"),
    ]

    operations = [
        migrations.AddField(
            model_name="publicengagementpartner",
            name="is_head",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="publicengagementpartner",
            name="partner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="organizational_area.organizationalstructure",
            ),
        ),
        migrations.DeleteModel(
            name="Partner",
        ),
    ]
