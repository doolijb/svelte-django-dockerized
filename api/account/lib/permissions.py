from rest_framework.permissions import BasePermission
from django.utils.translation import gettext as _
from django.db.models import Model

from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from account.models import User, EmailAddress


class IsSelf(BasePermission):
    """
    Allows access if the user is the same, or if the user owns the object.
    """
    def has_object_permission(self, request, view, obj):
        """
        Returns True if the user is the same, or if the user owns the object.
        Be careful to only extend this list with classes that non staff users
        should be able to access or modify.
        """
        match type(obj):
            case "User":
                return cast("User", obj) ==request.user
            case "EmailAddress":
                return cast("EmailAddress", obj).emailable == request.user
            case _:
                raise TypeError(f"Unexpected type {type(obj)}.")


class IsUnauthenticated(BasePermission):
    message = _('You are already authenticated.')
    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsAdmin(BasePermission):
    """
    Allows access only to admin users.
    """
    message = _('You are not an admin.')
    def has_permission(self, request, view):
        return request.user.is_admin
