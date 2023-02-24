from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from rest_framework import serializers
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils import timezone
from .models import EmailAddress, RedeemableKey, User


class UserSerializer(serializers.ModelSerializer):

    email_addresses = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email_addresses", "first_name", "last_name", "is_staff"]
        read_only_fields = ["id", "email_addresses", "is_staff"]
        if settings.ENABLE_USERNAMES:
            fields.insert(1, "username")
            read_only_fields.insert(1, "username")

    def get_email_addresses(self, obj):
        return EmailAddressSerializer(obj.email_addresses.all(), many=True).data

    def destroy(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError


class UserAdminSerializer(UserSerializer):
    email_addresses = serializers.SerializerMethodField()

    class Meta:
        model = User
        read_only_fields = ("id",)

    def validate_is_staff(self, value):
        # Only superusers can make users staff.
        if (value and not self.instance) or (
            self.instance
            and value != self.instance.is_staff
            and not self.context["request"].user.is_superuser
        ):
            raise serializers.ValidationError(
                _("You do not have permission to make this user staff.")
            )
        return value

    def validate_is_superuser(self, value):
        # Only superusers can make other users superusers.
        if (value and not self.instance) or (
            self.instance
            and value != self.instance.is_superuser
            and not self.context["request"].user.is_superuser
        ):
            raise serializers.ValidationError(
                _("You do not have permission to make this user a superuser.")
            )
        return value

    def validate_user(self, value):
        # Only superusers can change other users.
        if (
            self.instance
            and value != self.instance
            and not self.context["request"].user.is_superuser
        ):
            raise serializers.ValidationError(
                _("You do not have permission to change this user.")
            )

    def get_email_addresses(self, obj):
        return EmailAddressAdminSerializer(obj.email_addresses.all(), many=True).data


class EmailAddressSerializer(serializers.ModelSerializer):

    email = serializers.EmailField() # TODO, make sure this is not editable

    def validate_email(self, value):
        if self.instance and value and self.instance.email != value:
            raise serializers.ValidationError(_("Email cannot be changed."))
        return value

    def validate_is_primary(self, value):
        if value and not self.instance:
            raise serializers.ValidationError(
                _("New email addresses cannot be primary.")
            )
        if not value and self.instance and self.instance.is_primary:
            raise serializers.ValidationError(
                _("Choose a new primary email address instead.")
            )
        return value

    class Meta:
        model = EmailAddress
        fields = ("id", "email", "is_primary", "verified_at")
        read_only_fields = ("id", "email", "created_at", "verified_at")

    def create(self, *args, **kwargs):
        raise NotImplementedError


class EmailAddressAdminSerializer(EmailAddressSerializer):

    user = serializers.SerializerMethodField()# TODO, make sure this is not editable
    email = serializers.EmailField()# TODO, make sure this is not editable
    create_redeemable_key = serializers.BooleanField(write_only=True, required=False)
    send_verification_email = serializers.BooleanField(write_only=True, required=False)
    is_verified = serializers.BooleanField(required=False)

    def to_internal_value(self, data):
        # If the email address is being verified, set the verified_at field.
        is_verified = data.pop("is_verified", False)
        verified_at = bool(self.instance.verified_at) if self.instance else False
        if is_verified and not verified_at:
            data["verified_at"] = timezone.now()
        if not is_verified and verified_at:
            data["verified_at"] = None
        return super().to_internal_value(data)

    def to_representation(self, instance):
        # Todo, check if is_primary model attribute is being serialized
        return super().to_representation(instance)

    def validate_user(self, value):
        # Only superusers can change other superusers.
        # TODO check if user is superuser
        return value

    def validate(self, data):
        if not self.instance:
            if data.get("is_primary") and not data.get("verified_at"):
                raise serializers.ValidationError(
                    _("Primary email addresses must be verified.")
                )
        return data

    class Meta:
        model = EmailAddress
        fields = ("id", "email", "is_primary", "verified_at", "created_at", "user")
        read_only_fields = ("id", "created_at", "verified_at")
