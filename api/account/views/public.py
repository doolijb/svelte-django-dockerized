from typing import cast
from rest_framework.viewsets import GenericViewSet
from account.lib.permissions import IsUnauthenticated
from account.models import User, Password, EmailAddress, RedeemableKey
from account.serializers.public import RegisterSerializer, SessionSerializer, UserSerializer, SetPasswordSerializer, EmailAddressSerializer, RedeemKeySerializer
from rest_framework.permissions import AllowAny
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q


class SessionViewSet(GenericViewSet):
    """
    This viewset is for the user to log in and out of a session.
    """
    serializer_class = SessionSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.login()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['delete'])
    def logout(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.logout()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RegisterViewSet(GenericViewSet):
    serializer_class = RegisterSerializer
    permission_classes = [IsUnauthenticated]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserViewSet(
        CreateModelMixin,
        RetrieveModelMixin,
        UpdateModelMixin,
        GenericViewSet,
    ):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUnauthenticated]

    def get_queryset(self):
        return self.queryset.filter(id=cast(User, self.request.user).id)


class PasswordViewSet(
        GenericViewSet
    ):
    """
    This viewset is for the user to manage their own password.
    """
    queryset = Password.objects.all()
    serializer_class = SetPasswordSerializer
    permission_classes = [AllowAny]

    # @action(detail=False, methods=['post'])
    # def forgot(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


class EmailAddressViewSet(
        CreateModelMixin,
        ListModelMixin,
        UpdateModelMixin,
        RetrieveModelMixin,
        DestroyModelMixin,
        GenericViewSet
    ):
    """
    This viewset is for the user to manage their own email addresses.
    """
    queryset = EmailAddress.objects.all()
    serializer_class = EmailAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(emailable=cast(User, self.request.user))


class RedeemKeyViewSet(GenericViewSet):
    """
    This viewset is for the user to manage their own redeemable keys.
    """
    queryset = RedeemableKey.objects.all()
    serializer_class = RedeemKeySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(
                Q(user=cast(User, self.request.user)) | Q(user__isnull=True)
            )

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
