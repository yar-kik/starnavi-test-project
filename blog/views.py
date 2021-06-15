from .models import Like, Post
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
    Get a list of posts or create a new one.
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
    CRUD operations to manage post.
    """

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly & IsAuthor]

    def get(self, request: Request, post_id: int) -> Response:
        post = get_object_or_404(Post, id=post_id)
        serializer = self.serializer_class(post)
        return Response({"post": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request: Request, post_id: int) -> Response:
        post = get_object_or_404(Post, id=post_id)
        self.check_object_permissions(request, post)
        update_data = request.data.get("post")
        serializer = self.serializer_class(
            instance=post, data=update_data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
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
    Like or unlike the post.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, post_id: int) -> Response:
        post = get_object_or_404(Post, id=post_id)
        like = post.likes.filter(user=request.user).all()
        if like:
            like.delete()
            message = {"detail": "Post was unliked"}
        else:
            like = Like.objects.create(user=request.user, post=post)
            post.likes.add(like)
            request.user.likes.add(like)
            message = {"detail": "Post was liked"}
        return Response(message, status=status.HTTP_200_OK)
