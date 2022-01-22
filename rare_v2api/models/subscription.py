from django.db import models

class Subscription(models.Model):
    follower = models.ForeignKey(RareUser, on_delete=models.CASCADE, related_name = 'following')
    author = models.ForeignKey(RareUser, on_delete=models.CASCADE, related_name= 'authors')
    created_on = models.DateTimeField(auto_now_add=True)
    ended_on = models.DateTimeField(auto_now_add=True)
    