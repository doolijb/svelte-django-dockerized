from django.db.transaction import atomic
from rest_framework import serializers
from django.conf import settings

from .models import EmailAddress, User


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
            "id",
            "username",
            "first_name",
            "last_name",
            "email_addresses",
        ]
        read_only_fields = [
            "id",
            "username",
        ]

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
                fields += ["username"]   




class EmailAddressSerializer(serializers.ModelSerializer):
    """
    Serializes the email addresses for a user.
    """

    class Meta:
        model = EmailAddress
        fields = [
            "id",
            "is_verified",
            "is_primary",
        ]
        read_only_fields = [
            "id",
            "email",
            "is_verified",
            "is_primary",
        ]

        