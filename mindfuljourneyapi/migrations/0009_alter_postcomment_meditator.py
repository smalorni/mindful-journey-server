# Generated by Django 4.1.1 on 2022-09-16 20:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mindfuljourneyapi', '0008_alter_event_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcomment',
            name='meditator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comments', to=settings.AUTH_USER_MODEL),
        ),
    ]
