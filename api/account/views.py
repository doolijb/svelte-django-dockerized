# import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import generics, serializers, status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from . import serializers

# from .models import PasswordResetToken
# from .utils import send_confirmation_email


@method_decorator(ensure_csrf_cookie, name="dispatch")
class CSRFTokenAPIView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        return Response(
            status=status.HTTP_201_CREATED, data={"message": "CSRF cookie set"}
        )


class AccountAPIView(generics.GenericAPIView):
    """
    GET view that returns an authenticated user's account details,
    else returns a default unauthenticated account.
    """

    permission_classes = [AllowAny]
    http_method_names = ["get"]

    def get(self, request):
        if (
            request.user.is_authenticated
            or not request.headers.get("Authorization")
            and request.user.is_anonymous
        ):
            serializer = serializers.GETAccountSerializer(request)
            response = Response({"account": serializer.body})
            return response

        return Response(status=status.HTTP_401_UNAUTHORIZED)
