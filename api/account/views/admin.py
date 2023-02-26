
from rest_framework.permissions import (
    IsAuthenticated,
    DjangoObjectPermissions,
)
from rest_framework.viewsets import ModelViewSet

from account.lib.permissions import IsAdmin

from account.models import User, Password, EmailAddress, RedeemableKey
from account.serializers.admin import UserAdminSerializer, PasswordAdminSerializer, EmailAddressAdminSerializer, RedeemableKeyAdminSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [IsAuthenticated & IsAdmin & DjangoObjectPermissions]

class PasswordViewSet(ModelViewSet):
    queryset = Password.objects.all()
    serializer_class = PasswordAdminSerializer
    permission_classes = [IsAuthenticated & IsAdmin & DjangoObjectPermissions]

class EmailAddressViewSet(ModelViewSet):
    queryset = EmailAddress.objects.all()
    serializer_class = EmailAddressAdminSerializer
    permission_classes = [IsAuthenticated & IsAdmin & DjangoObjectPermissions]

class RedeemableKeyViewSet(ModelViewSet):
    queryset = RedeemableKey.objects.all()
    serializer_class = RedeemableKeyAdminSerializer
    permission_classes = [IsAuthenticated & IsAdmin & DjangoObjectPermissions]
