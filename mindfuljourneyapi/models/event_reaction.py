from django.db import models
from django.contrib.auth.models import User

class EventReaction(models.Model):
    # Foreign keys are connected to name of models
    # Specific row will be deleted for on_delete
    # Related name will be post and reaction
    meditator = models.ForeignKey("Meditator", on_delete=models.CASCADE, related_name="event_reactions")
    event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name="event_reactions")
    emoji = models.CharField(max_length=20)