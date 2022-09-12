from django.db import models
from django.contrib.auth.models import User

class Meditator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=250)
    location = models.CharField(max_length=250)
    profile_image_url = models.ImageField(
        upload_to='profileImage', height_field=None,
        width_field=None, max_length=None, null=True)
