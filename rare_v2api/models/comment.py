from django import models


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comment")
    author = models.ForeignKey(RareUser, on_delete="user_comment")
    content = models.CharField(max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)