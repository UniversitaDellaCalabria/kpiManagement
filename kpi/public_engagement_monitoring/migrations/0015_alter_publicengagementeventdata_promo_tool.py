# Generated by Django 5.1.3 on 2024-12-23 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_engagement_monitoring',
         '0014_alter_publicengagementevent_operator_validation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicengagementeventdata',
            name='promo_tool',
            field=models.ManyToManyField(blank=True, limit_choices_to={
                                         'is_active': True}, to='public_engagement_monitoring.publicengagementeventpromotool'),
        ),
    ]