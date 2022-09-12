from django.db import models

class PostComment(models.Model):
    # Foreign keys are connected to name of models
    # Specific row will be deleted for on_delete
    # Related names will be combining post and comment
    meditator = models.ForeignKey("Meditator", on_delete=models.CASCADE, related_name="post_comments")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_comments")
    comment = models.CharField(max_length=250)
    created_on = models.DateField()