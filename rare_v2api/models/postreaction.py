from django.db import models
from .rareuser import RareUser
from .post import Post
from .reaction import Reaction

class PostReaction(models.Model):
    user = models.ForeignKey(RareUser, on_delete=models.CASCADE, related_name="post_reactions")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_reactions")
    reaction = models.ForeignKey(Reaction, on_delete=models.CASCADE, related_name="post_reactions")