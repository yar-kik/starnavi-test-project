from django.db import models

from authentication.models import User


class Post(models.Model):

    title = models.CharField(max_length=100)
    body = models.TextField(max_length=10000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="post_likes", blank=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
