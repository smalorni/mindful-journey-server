# Generated by Django 4.1.1 on 2022-09-15 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mindfuljourneyapi', '0006_rename_date_event_end_date_event_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(default='2022-01-01'),
        ),
    ]