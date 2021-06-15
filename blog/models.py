from django.db import models

from authentication.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(max_length=10000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )

    def __str__(self):
        return f"<Post> {self.title} ({self.author.username})"


class Like(models.Model):
    post = models.ForeignKey(
        Post, related_name="likes", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, related_name="likes", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"<Like> {self.user.username} ({self.post.title})"
