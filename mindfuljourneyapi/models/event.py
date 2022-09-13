from pyexpat import model
from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    date = models.DateField()
    host = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    event_image_url = models.ImageField(
        upload_to='eventImage', height_field=None,
        width_field=None, max_length=None, null=True)
    activity_level = models.ForeignKey("ActivityLevel", on_delete=models.CASCADE, related_name="event_activity_levels")
    meditator = models.ForeignKey("Meditator", on_delete=models.CASCADE, related_name="HostEvent")
    # Join tables added - many to many relationships, what table it goes through
    attendee = models.ManyToManyField("Meditator", through="EventAttendee")
    tag = models.ManyToManyField("Tag", through="EventTag")