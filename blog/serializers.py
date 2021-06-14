from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """Class for news posts serialization/deserialization"""

    total_likes = serializers.SerializerMethodField(read_only=True)

    def get_total_likes(self, post: Post) -> int:
        return post.likes.count()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "body",
            "created",
            "updated",
            "total_likes",
            "author",
        )
        read_only_fields = (
            "id",
            "created",
            "updated",
            "author",
            "total_likes",
        )
