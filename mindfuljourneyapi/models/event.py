from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    host = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    event_image_url = models.ImageField(
        upload_to='eventImage', height_field=None,
        width_field=None, max_length=None, null=True)
    activity_level = models.ForeignKey("ActivityLevel", on_delete=models.CASCADE, related_name="event_activity_levels")
    meditator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="HostEvent")
    # Join tables added - many to many relationships, what table it goes through
    attendee = models.ManyToManyField(User, through="EventAttendee")

    @property
    def readable_start_date(self):
        return self.start_date.strftime('%m/%d/%y')

    @property
    def readable_end_date(self):
        return self.end_date.strftime('%m/%d/%y')

    @property
    def attending(self):
        return self.__attending
    
    @attending.setter
    def attending(self, value):
        self.__attending = value