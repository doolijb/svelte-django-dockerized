from uuid import UUID

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from rest_framework import permissions, status
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView, Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView as BaseTokenObtainPairView,
)
from rest_framework_simplejwt.views import TokenRefreshView as BaseTokenRefreshView
from rest_framework_simplejwt.views import TokenVerifyView as BaseTokenVerifyView

from .models import EmailAddress, RedeemableKey
from .serializers import CurrentUserSerializer, EmailAddressSerializer

User = get_user_model()

# Create a child of TokenObtainPairView that doesn't require authentication
class TokenObtainPairView(BaseTokenObtainPairView):
    """
    Test!!
    """

    @permission_classes([permissions.AllowAny])
    def post(self, request, *args, **kwargs):
        """
        Creates a token for a user.
        """
        # Should not be authenticated
        if request.user.is_authenticated:
            return Response(
                data={'detail': 'You are already authenticated.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().post(request, *args, **kwargs)


class TokenRefreshView(BaseTokenRefreshView):
    pass


class TokenVerifyView(BaseTokenVerifyView):
    pass


class CurrentUserView(APIView):
    serializer_class = CurrentUserSerializer

    @permission_classes([permissions.AllowAny])
    def get(self, request, format=None):
        """
        Shows an authenticated user, if any.
        """
        data: dict = self.serializer_class(request.user).data
        return Response(data=data, status=status.HTTP_200_OK)

    @permission_classes([permissions.IsAuthenticated])
    def update(self, request, *args, **kwargs):
        """
        Updates an authenticated user.
        """
        # TODO
        raise NotImplementedError


class EmailAddressesView(APIView):
    model = EmailAddress
    serializer_class = EmailAddressSerializer
    queryset = model.objects.all()

    def get_serializer(self, email_address_id: UUID | None = None, **kwargs):
        if self.request:
            kwargs.setdefault('data', {**self.request.data, 'id': email_address_id})  # type: ignore
            kwargs.setdefault('context', {'request': self.request})
            kwargs.setdefault('many', not bool(email_address_id))
            kwargs.setdefault('queryset', self.queryset)
        return self.serializer_class(**kwargs)

    def get(self, request, format=None, email_address_id: UUID | None = None):
        """
        Shows an authenticated user's email address, if id is provided.
        Lists all authenticated user's email addresses, if id is not provided.
        """
        serializer = self.get_serializer(email_address_id=email_address_id)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """
        Creates an email address for an authenticated user.
        """
        serializer = self.get_serializer()
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, format=None, email_address_id: UUID | None = None):
        """
        Updates an authenticated user's email address.
        """
        serializer = self.get_serializer(email_address_id=email_address_id)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, format=None, email_address_id: UUID | None = None):
        """
        Deletes an authenticated user's email address.
        """
        email_address = request.user.email_addresses.get(id=id)
        email_address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RedeemKeyView(APIView):
    @permission_classes([permissions.IsAuthenticated])
    def post(self, request, id: UUID | None = None, format=None):
        """
        Redeems a key for a user.
        """

        redeemable_key = RedeemableKey.objects.get(
            key=request.data['key']
        ).prefetch_related('redeemable')
        success = redeemable_key.redeem(request.user)

        if success:
            data = {
                'message': 'Key redeemed successfully',
                'redeemable_key': {
                    'id': redeemable_key.id,
                    'redeemable_type': redeemable_key.redeemable_type,
                    'redeemable_id': redeemable_key.redeemable_id,
                },
            }
            return Response(data=data, status=status.HTTP_200_OK)
