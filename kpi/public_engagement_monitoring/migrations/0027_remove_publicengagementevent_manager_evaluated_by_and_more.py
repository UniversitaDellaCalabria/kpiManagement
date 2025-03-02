# Generated by Django 5.1.4 on 2025-02-05 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_engagement_monitoring', '0026_remove_publicengagementeventscientificarea_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicengagementevent',
            name='manager_evaluated_by',
        ),
        migrations.RemoveField(
            model_name='publicengagementevent',
            name='manager_evaluation_date',
        ),
        migrations.RemoveField(
            model_name='publicengagementevent',
            name='manager_evaluation_success',
        ),
        migrations.RemoveField(
            model_name='publicengagementevent',
            name='manager_notes',
        ),
        migrations.RemoveField(
            model_name='publicengagementevent',
            name='manager_taken_by',
        ),
        migrations.RemoveField(
            model_name='publicengagementevent',
            name='manager_taken_date',
        ),
        migrations.AddField(
            model_name='publicengagementevent',
            name='created_by_manager',
            field=models.BooleanField(default=False, verbose_name='Creato dal manager'),
        ),
        migrations.AddField(
            model_name='publicengagementevent',
            name='edited_by_manager',
            field=models.BooleanField(default=False, verbose_name='Modificato dal manager'),
        ),
        migrations.AddField(
            model_name='publicengagementeventreport',
            name='edited_by_manager',
            field=models.BooleanField(default=False, verbose_name='Modificato dal manager'),
        ),
        migrations.AlterField(
            model_name='publicengagementeventdata',
            name='description',
            field=models.TextField(help_text='Max 1500 chars', max_length=1500, verbose_name='Short description'),
        ),
        migrations.AlterField(
            model_name='publicengagementeventdata',
            name='project_name',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Project name'),
        ),
    ]
