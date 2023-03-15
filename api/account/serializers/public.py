from ctypes import cast
import logging
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from rest_framework import serializers
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils import timezone
from django.db.models import Q
from account.models import User, Password, EmailAddress, RedeemableKey
from django.contrib.auth import login, logout
from account.lib.utils import validate_password


class SessionSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        self.instance = User.objects.filter(
            Q(username=data["username"])
            | Q(email=data["username"])
            ).first()
        if not self.instance:
            raise serializers.ValidationError(_("Invalid username or password."))
        if not self.instance.check_password(data["password"]):
            raise serializers.ValidationError(_("Invalid username or password."))
        return data

    def login(self, *args, **kwargs):
        login(self.context["request"], self.instance)
        return self.instance

    def logout(self, *args, **kwargs):
        logout(self.context["request"])
        self.instance = None
        return None

    def to_representation(self, instance):
        if not instance:
            return {
                "message": "Logged out successfully."
            }
        return UserSerializer(instance).data


class RegisterSerializer(serializers.Serializer):
    takes_context = True

    email = serializers.EmailField(write_only=True)
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not settings.ENABLE_USERNAMES:
            self.fields.pop("username")

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate_password_confirm(self, value):
        if value != self.context["request"].data["password"]:
            raise serializers.ValidationError(_("Passwords do not match."))
        return value

    def validate(self, data):
        return super().validate(data)

    def create(self, validated_data):
        self.instance = User.objects.create_user(
            email=validated_data["email"],
            raw_password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        login(self.context["request"], self.instance)
        return self.instance

    def to_representation(self, instance):
        return {
            "message": _("Registered successfully."),
            "user": UserSerializer(instance, context=self.context).data
        }

class EmailAddressSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, write_only=True)
    is_primary = serializers.BooleanField(required=False, help_text=_("Whether this email address is the primary one. Only one email address can be primary at a time. Ignored on creation."))
    is_verified = serializers.BooleanField(read_only=True)
    emailable = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = EmailAddress
        fields = ("id", "email", "is_primary", "is_verified", "emailable")

    def validate_email(self, value):
        if self.instance and value and self.instance.email != value:
            raise serializers.ValidationError(_("Email cannot be changed."))
        return value

    def validate_is_primary(self, value):
        if not self.instance:
            return False
        return value

    def set_primary(self, *args, **kwargs):
        if self.instance:
            self.instance.set_primary()
        return self.instance

    def validate(self, data):
        if self.instance:
            if self.instance.emailable != self.context["request"].user:
                logging.critical("User {} attempted to set primary email for user {}.".format(
                    self.context["request"].user.id, self.instance.emailable.id
                ))
        return super().validate(data)

    def update(self, instance, validated_data):
        raise NotImplementedError

    def partial_update(self, instance, validated_data):
        raise NotImplementedError


class UserSerializer(serializers.ModelSerializer):

    email_addresses = EmailAddressSerializer(many=True)

    class Meta:
        model = User
        fields = ["id", "username", "email_addresses", "first_name", "last_name", "is_admin"]
        read_only_fields = ["id", "email_addresses", "is_staff"]
        public_fields = ["id", "email_addresses", "first_name", "last_name"]
        if settings.ENABLE_USERNAMES:
            fields.insert(1, "username")
            read_only_fields.insert(1, "username")

    def get_email_addresses(self, obj):
        return EmailAddressSerializer(obj.email_addresses.all(), many=True).data

    def to_representation(self, instance):
        # Limit the available fields if user is not requesting their own data
        if self.context["request"].user != instance:
            for field in self.fields:
                if field not in self.Meta.public_fields:
                    self.fields.pop(field)
        elif self.context["request"].user == instance and not self.context["request"].user.is_admin:
            for field in self.fields:
                if field == "is_admin":
                    self.fields.pop(field)
        return super().to_representation(instance)


class SetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def validate_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError(_("Passwords do not match."))
        return super().validate(data)

    def save(self, *args, **kwargs):
        self.context["request"].user.set_password(self.data["password"])

    def to_representation(self, instance):
        return {"message": _("Password updated.")}


class RedeemKeySerializer(serializers.Serializer):

    key = serializers.ModelField(RedeemableKey.objects.all(), required=False)

    def validate_key(self, value):
        if not value.id:
            raise serializers.ValidationError(_("This key does not exist."))
        if not value.can_redeem:
            raise serializers.ValidationError(_("This key cannot be redeemed."))
        return value

    def validate(self, data):
        self.instance = data["key"]
        self.instance.stage_redeem(
            user=self.context["request"].user
        )
        try:
            data["key"].is_valid()
        except ValueError as e:
            logging.error(e, exc_info=True, extra={"request": self.context["request"]})
            raise serializers.ValidationError("Could not redeem key: {}".format(e))
        return super().validate(data)

    def save(self, **kwargs):
        self.instance.redeem()
        return self.instance

    def to_representation(self, instance):
        return {
            "message": "Key redeemed successfully.",
            "key": instance.key,
            "redeemable_model": str(instance.redeemable_model),
            "redeemable_id": instance.redeemable_id,
        }
