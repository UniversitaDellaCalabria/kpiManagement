# Generated by Django 4.1 on 2022-11-30 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("organizational_area", "0003_alter_organizationalstructureoffice_options"),
        ("public_engagement_management", "0007_alter_publicengagementpartner_partner"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="publicengagementpartner",
            options={"ordering": ("-is_head", "partner")},
        ),
        migrations.AlterField(
            model_name="publicengagement",
            name="structure",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="organizational_area.organizationalstructure",
            ),
        ),
    ]