from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from rest_framework import serializers

from .models import EmailAddress, RedeemableKey

User = get_user_model()


# Serializer to grab the authenticated user or return a generic unauthenticated user object
class CurrentUserSerializer(serializers.ModelSerializer):
    """
    Serializes the authenticated user with their email addresses, or returns a generic unauthenticated user object.
    """

    instance: EmailAddress
    email_addresses = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email_addresses',
        ]
        read_only_fields = [
            'id',
            'username',
        ]

    def get_email_addresses(self, instance):
        """
        Return the email addresses for the authenticated user.
        """
        return EmailAddressSerializer(instance.email_addresses.all(), many=True).data

    def to_representation(self, instance):
        """
        Return the authenticated user or an empty object.
        This is done because this serializer should not used to determine authentication.
        """
        return super().to_representation(instance) if instance.is_authenticated else {}


class RegisteredUserSerializer(serializers.CreateOnlyDefault):
    """
    Serializes a registered user.
    """

    email_address = serializers.EmailField()

    instance: EmailAddress

    class Meta:
        model = User
        fields = []
        if settings.ENABLE_USERNAMES:
            fields += ['username']


# class EmailAddressesSerializer(serializers.ModelSerializer):
#     """
#     Serializes email addresses.
#     """

#     class Meta:
#         model = EmailAddress
#         fields = [
#             "id",
#             "email",
#             "is_verified",
#             "is_primary",
#         ]
#         read_only_fields = [
#             "id",
#             "email",
#             "is_verified",
#             "is_primary",
#         ]


class EmailAddressSerializer(serializers.ModelSerializer):
    """
    Serializes an email address.
    """

    takes_context = True

    def __init__(self, *args, **kwargs):
        """
        Initialize the serializer.
        """
        super().__init__(*args, **kwargs)
        self.request = self.context.get('request')

    class Meta:
        model = EmailAddress
        fields = [
            'id',
            'email',
            'is_verified',
            'is_primary',
        ]
        read_only_fields = [
            'id',
            'email',
            'is_verified',
            'is_primary',
            'user',
        ]

    def create(self, validated_data):
        """
        Create an email address.
        Must be staff with the "account.add_emailaddress" permission.
        """
        email_address = EmailAddress.objects.create(**validated_data)
        email_address.send_verification_email(self.request)
        return email_address
