from .models import Post
from .permissions import IsAuthor
from .serializers import PostSerializer
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


class ListPostApiView(APIView):
    """
    Class to get a list of posts or create a new one.
    """

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request: Request) -> Response:
        post = request.data.get("post")
        serializer = self.serializer_class(data=post)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
        return Response(
            {"post": serializer.data}, status=status.HTTP_201_CREATED
        )

    def get(self, request: Request) -> Response:
        posts = Post.objects.all()
        serializer = self.serializer_class(posts, many=True)
        return Response({"posts": serializer.data}, status=status.HTTP_200_OK)


class PostApiView(APIView):
    """
    Class for CRUD operations to manage post.
    """

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly & IsAuthor]

    def get(self, request: Request, post_id: int) -> Response:
        post = get_object_or_404(Post, id=post_id)
        serializer = self.serializer_class(post)
        return Response({"post": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request: Request, post_id: int) -> Response:
        post = get_object_or_404(Post, id=post_id)
        self.check_object_permissions(request, post_id)
        update_data = request.data.get("post")
        serializer = self.serializer_class(
            instance=post, data=update_data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
        return Response({"post": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request: Request, post_id: int) -> Response:
        post = get_object_or_404(Post, id=post_id)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(
            {"detail": "Deleted successfully"}, status=status.HTTP_200_OK
        )


class LikeApiView(APIView):
    """
    Class to like/dislike the post
    """

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, post_id: int) -> Response:
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            message = {"detail": "Post was liked"}
        else:
            post.likes.add(request.user)
            message = {"detail": "Post was disliked"}
        return Response(message, status=status.HTTP_200_OK)
