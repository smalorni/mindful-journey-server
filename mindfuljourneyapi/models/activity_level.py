from django.db import models

class ActivityLevel(models.Model):
    rating = models.IntegerField()