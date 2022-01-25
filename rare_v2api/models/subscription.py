from django.db import models
from .rareuser import RareUser

class Subscription(models.Model):
    follower = models.ForeignKey(RareUser, on_delete=models.CASCADE, related_name = 'following')
    author = models.ForeignKey(RareUser, on_delete=models.CASCADE, related_name= 'followed_by')
    created_on = models.DateTimeField(auto_now_add=True)
    ended_on = models.DateTimeField(null=True)