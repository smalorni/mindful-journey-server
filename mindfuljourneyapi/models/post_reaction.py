from django.db import models

class PostReaction(models.Model):
    # Foreign keys are connected to name of models
    # Specific row will be deleted for on_delete
    # Related name will be post and reaction
    meditator = models.ForeignKey("Meditator", on_delete=models.CASCADE, related_name="post_reactions")
    post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_reactions")
    emoji = models.CharField(max_length=20)