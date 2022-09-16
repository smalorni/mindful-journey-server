from django.db import models
from django.contrib.auth.models import User

class PostComment(models.Model):
    # Foreign keys are connected to name of models
    # Specific row will be deleted for on_delete
    # Related names will be combining post and comment
    meditator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_comments")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_comments")
    comment = models.CharField(max_length=250)
    created_on = models.DateField()

    @property
    def readablePostComment_created_on(self):
        return self.created_on.strftime('%m/%d/%y')