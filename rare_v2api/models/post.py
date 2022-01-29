from django.db import models
from .rareuser import RareUser
from .category import Category

class Post(models.Model):

    user = models.ForeignKey(RareUser, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="post_category")
    publication_date = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField()
    content = models.TextField()
    approved = models.BooleanField(default=False)
