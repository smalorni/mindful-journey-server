# Generated by Django 4.1.1 on 2022-09-15 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mindfuljourneyapi', '0007_alter_event_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(),
        ),
    ]
