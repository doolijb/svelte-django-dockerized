from account.models import User, Password, EmailAddress, RedeemableKey
from rest_framework import serializers
from django.utils.translation import gettext as _

class UserAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "deleted_at"]


class PasswordAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = Password
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "deleted_at"]


class EmailAddressAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailAddress
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "deleted_at"]


class RedeemableKeyAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = RedeemableKey
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at", "deleted_at"]
