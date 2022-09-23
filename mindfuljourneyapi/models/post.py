from django.db import models
from django.contrib.auth.models import User
class Post(models.Model):
    # Foreign keys are connected to name of models
    # Specific row will be deleted for on_delete
    meditator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey("PostCategory", on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=30, default="null")
    content = models.CharField(max_length=250)
    created_on = models.DateField()
    post_image_url = models.ImageField(
        upload_to='postImage', height_field=None,
        width_field=None, max_length=None, null=True)
    
    @property
    def readable_created_on(self):
        return self.created_on.strftime('%m/%d/%Y')
