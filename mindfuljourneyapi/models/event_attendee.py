from django.db import models
from django.contrib.auth.models import User

# This class is joined by event and meditator tables
# Don't need related names on join tables
class EventAttendee(models.Model):
    event = models.ForeignKey("Event", on_delete=models.CASCADE)
    meditator = models.ForeignKey(User, on_delete=models.CASCADE)