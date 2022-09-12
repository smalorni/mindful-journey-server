# Generated by Django 4.1.1 on 2022-09-09 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mindfuljourneyapi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='mediator',
        ),
        migrations.AddField(
            model_name='event',
            name='attendee',
            field=models.ManyToManyField(through='mindfuljourneyapi.EventAttendee', to='mindfuljourneyapi.meditator'),
        ),
        migrations.AddField(
            model_name='event',
            name='meditator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='HostEvent', to='mindfuljourneyapi.meditator'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='tag',
            field=models.ManyToManyField(through='mindfuljourneyapi.EventTag', to='mindfuljourneyapi.tag'),
        ),
    ]
