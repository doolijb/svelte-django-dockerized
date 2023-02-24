from rest_framework.permissions import BasePermission
from django.utils.translation import gettext as _


class IsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsUnauthenticated(BasePermission):
    message = _('You are already authenticated.')
    def has_permission(self, request, view):
        return not request.user.is_authenticated
