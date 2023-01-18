from rest_framework import permissions, status
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView, Response
from django.db.transaction import atomic

from account.models import User

from .serializers import CurrentUserSerializer, EmailAddressSerializer


class CurrentUserApiView(APIView):
    @permission_classes([permissions.AllowAny])
    def get(self, request, format=None):
        """
        Shows an authenticated user, if any.
        """

        # Serialize the user
        if request.user.is_authenticated:
            data: dict = User.objects.get(id=request.user.id).serialize_current_user()
        else:
            # This endpoint doesn't determine authentication, so we return an empty object
            data: dict = {}

        return Response(data=data, status=status.HTTP_200_OK)

    @permission_classes([permissions.IsAuthenticated])
    def update(self, request, *args, **kwargs):
        """
        Updates an authenticated user.
        """
        # TODO
        raise NotImplementedError


class CurrentUserEmailAddressesApiView(APIView):
    serializer_class = EmailAddressSerializer

    @permission_classes([permissions.IsAuthenticated])
    def get(self, request, id=None, format=None):
        """
        Shows an authenticated user's email address, if id is provided.
        Lists all authenticated user's email addresses, if id is not provided.
        """
        if id:
            email_address = request.user.email_addresses.get(id=id)
            serializer = self.serializer_class(email_address)
        else:
            serializer = self.serializer_class(request.user.email_addresses, many=True)
        return Response(serializer.data)

    @permission_classes([permissions.IsAuthenticated])
    def post(self, request, format=None):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @permission_classes([permissions.IsAuthenticated])
    def put(self, request, id, format=None):
        """
        Updates an authenticated user's email address.
        """
        email_address = request.user.email_addresses.get(id=id)
        serializer = self.serializer_class(
            email_address, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @permission_classes([permissions.IsAuthenticated])
    def delete(self, request, id, format=None):
        """
        Deletes an authenticated user's email address.
        """
        email_address = request.user.email_addresses.get(id=id)
        email_address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
