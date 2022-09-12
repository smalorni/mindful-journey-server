from django.db import models

class Post(models.Model):
    # Foreign keys are connected to name of models
    # Specific row will be deleted for on_delete
    meditator = models.ForeignKey("Meditator", on_delete=models.CASCADE, related_name="posts")
    category = models.ForeignKey("PostCategory", on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=250)
    created_on = models.DateField()
    post_image_url = models.ImageField(
        upload_to='postImage', height_field=None,
        width_field=None, max_length=None, null=True)
