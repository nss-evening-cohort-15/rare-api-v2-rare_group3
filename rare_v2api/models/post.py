from django.db import models


class Post(models.Model):

    user = models.ForeignKey(RareUser, on_delete=models.CASCADE, related_name="post_author")
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="post_category")
    publication_date = models.DateField(max_lenght=50)
    image_url = models.CharField(max_field=500)
    content = models.CharField(max_length=5000)
    approved = models.BooleanField(default=False)
