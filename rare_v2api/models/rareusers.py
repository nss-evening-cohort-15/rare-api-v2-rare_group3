from django.db import models
from django.contrib.auth.models import User

class RareUser(models.Model):
  
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  bio = models.CharField(max_length=500)
  profile_image_url = models.CharField(max_length=500)
  active = models.BooleanField(default=False)
  created_on = models.DateTimeField(auto_now_add=True)