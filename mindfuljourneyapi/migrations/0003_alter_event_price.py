# Generated by Django 4.1.1 on 2022-09-09 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mindfuljourneyapi', '0002_remove_event_mediator_event_attendee_event_meditator_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='price',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
    ]
