from uuid import UUID

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from rest_framework import permissions, status
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    DjangoObjectPermissions,
)
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView, Response
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView as BaseTokenObtainPairView,
)
from rest_framework_simplejwt.views import TokenRefreshView as BaseTokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView as BaseTokenVerifyView
from .lib.permissions import IsSelf, IsUnauthenticated

from account.models import EmailAddress, RedeemableKey, User
from .serializers import UserSerializer
from typing import cast, TYPE_CHECKING
from rest_framework.decorators import action

# ModelViewSet for User
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = cast(User, self.request.user)
        self.queryset = self.queryset.filter(id=user.id)
        return super().get_queryset()

    @action(detail=False, methods=["post"])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        match self.action:
            case "list":
                self.permission_classes += [IsAdminUser & DjangoObjectPermissions]
            case "retrieve":
                self.permission_classes += [
                    IsSelf | [IsAdminUser & DjangoObjectPermissions]
                ]
            case "create":
                self.permission_classes += [IsAdminUser & DjangoObjectPermissions]
            case "update":
                self.permission_classes += [
                    IsSelf | [IsAdminUser & DjangoObjectPermissions]
                ]
            case "partial_update":
                self.permission_classes += [
                    IsSelf | [IsAdminUser & DjangoObjectPermissions]
                ]
            case "destroy":
                self.permission_classes += [IsAdminUser & DjangoObjectPermissions]
        return super().get_permissions()
