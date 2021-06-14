from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, RegistrationSerializer


class RegistrationApiView(APIView):
    """Class to register new user"""

    serializer_class = RegistrationSerializer

    def post(self, request: Request) -> Response:
        """Register new user"""
        user = request.data.get("user", {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"user": serializer.data}, status=status.HTTP_201_CREATED
        )


class LoginApiView(APIView):
    """Class to login a user"""

    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        user = request.data.get("user", {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)
