from django.db import models


class PostReaction(models.Model):
    user = models.ForeignKey("rare_v2api.User", on_delete=models.CASCADE, related_name="users_reaction")
    post = models.ForeignKey("rare_v2api.Post", on_delete=models.CASCADE, related_name="post_reaction")
    reaction = models.ForeignKey("rare_v2.Reaction", on_delete=models.CASCADE)
  
