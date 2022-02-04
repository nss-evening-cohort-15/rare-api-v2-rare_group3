from django.db import models
from django.contrib.auth.models import User


class RareUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="rare_user")
    bio = models.CharField(max_length=500)
    profile_image_url = models.URLField(default="https://upload.wikimedia.org/wikipedia/commons/8/89/Portrait_Placeholder.png")
    active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)