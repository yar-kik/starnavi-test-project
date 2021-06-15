from django.db.models import Count
from django.db.models.functions import TruncDate
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User
from authentication.serializers import UserActivitySerializer
from blog.models import Like


class BookStatisticsApiView(APIView):
    def get(self, request: Request) -> Response:
        """Analytics about posts likes"""
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")
        likes = (
            Like.objects.filter(created__range=[date_from, date_to])
            .annotate(date=TruncDate("created"))
            .order_by("date")
            .values("date")
            .annotate(total_likes=Count("date"))
        )
        return Response({"analytics": likes}, status=status.HTTP_200_OK)


class UserActivityApiView(APIView):

    serializer_class = UserActivitySerializer

    def get(self, request: Request, user_id: int) -> Response:
        """Return information about user activity"""
        user = get_object_or_404(User, id=user_id)
        serializer = self.serializer_class(user)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)
