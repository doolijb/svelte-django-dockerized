"""
Models for the account app.
"""

import textwrap
from os import truncate
from types import NoneType
from typing import Literal, Optional, cast

from django.apps import apps
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.transaction import atomic
from django.forms import ValidationError
from django.utils import timezone
from django.utils.translation import gettext as _

from core.lib import (
    HasPolymorphicForeignKeys,
    HasSoftDelete,
    HasTimestamps,
    HasUuidId,
    PolymorphicFKRelationship,
    PolymorphicForeignKey,
)

from .lib import (
    EmailAddressManager,
    IsEmailable,
    IsPasswordProtected,
    IsRedeemable,
    PasswordManager,
    UserManager,
    RedeemableKeyManager
)


class User(
    HasUuidId,
    HasTimestamps,
    HasSoftDelete,
    PermissionsMixin,
    IsEmailable,
    IsPasswordProtected,
    models.Model,
):
    """
    Model representing an authenticable user. Compared to the default Django
    user model, this User has no email field. Instead, it is closely tied to
    the EmailAddress model.
    """

    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)

    objects: UserManager = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        """
        Meta options for the User model.
        """
        abstract=False
        verbose_name: str = _("user")
        verbose_name_plural: str = _("users")
        # ordering = ("-created_at",)
        permissions = (
            ("add_superuser", "Can add superuser"),
            ("change_superuser", "Can change superuser"),
            ("delete_superuser", "Can delete superuser"),
            ("view_superuser", "Can view superuser"),
        )

    def __str__(self) -> str:
        """String representation of the User model."""
        return self.username

    @property
    def is_staff(self) -> bool:
        """
        Return True if the user is a member of staff.
        This property has been renamed from is_staff to is_admin.
        This property is to maintain backwards compatibility with Django's
        default User model.
        """
        return self.is_admin

    @property
    def full_name(self) -> str:
        """Return the first_name plus the last_name, with a space in between."""
        return self.first_name + " " + self.last_name

    @property
    def short_name(self) -> str:
        """Return the short name for the user."""
        return self.first_name

    get_username = AbstractBaseUser.get_username
    natural_key = AbstractBaseUser.natural_key
    is_anonymous = AbstractBaseUser.is_anonymous
    is_authenticated = AbstractBaseUser.is_authenticated
    get_session_auth_hash = AbstractBaseUser.get_session_auth_hash
    normalize_username = AbstractBaseUser.normalize_username


class Password(
    HasUuidId, HasTimestamps, HasSoftDelete, HasPolymorphicForeignKeys, models.Model
):
    """
    Model representing a password for a protected object.

    The protected object is identified by a generic foreign key. The protected
    object must implement the IsProtected interface.
    """

    protected = PolymorphicFKRelationship(null=False, on_delete=models.CASCADE, related_name="passwords")
    protected_user = PolymorphicForeignKey(User, protected)
    hash = models.CharField(max_length=128, editable=False)
    objects = PasswordManager()

    class Meta:
        """
        Meta options for the Password model.
        """
        verbose_name: str = _("password")
        verbose_name_plural: str = _("passwords")
        # ordering: list[str] = ["-created_at"]

    def __repr__(self) -> str:
        """String representation of the Password model."""
        protected_str = None
        deleted_str = None
        if self.protected:
            protected_str = f"{self.protected.__class__.__name__}: {self.protected.id}"
        if self.deleted_at:
            deleted_str = f", DELETED"
        return f"<Password: {self.pk}, protected {protected_str}{deleted_str}>"

    def validate(self, password: str) -> bool:
        """
        Check if the given password matches the hash.
        """
        return check_password(password, self.hash)


class EmailAddress(HasUuidId, HasTimestamps, IsRedeemable, HasPolymorphicForeignKeys, models.Model):
    emailable = PolymorphicFKRelationship(null=True, on_delete=models.CASCADE, related_name="email_addresses")
    emailable_user = PolymorphicForeignKey(User, emailable)
    email = models.EmailField(unique=True, editable=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    is_primary = models.BooleanField(default=False)

    objects: EmailAddressManager = EmailAddressManager()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._original_is_primary = self.is_primary

    @property
    def is_verified(self) -> bool:
        return bool(self.verified_at)

    class Meta:
        abstract=False
        unique_together: tuple[Literal["user"], Literal["email"]]
        # ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.email

    def save(self, *args, **kwargs) -> None:
        """
        EmailAddress save method.
        If settings.ENABLE_USERNAMES is False, the username will be set to the
        email address.
        """
        with atomic():
            # If has emailable, is set to primary and primary field has changed.
            if self.emailable and self.is_primary and self.is_primary != self._original_is_primary:
                # Set all other email addresses to non-primary.
                query = self.emailable.email_addresses
                if self.pk:
                    query = query.exclude(pk=self.pk)
                query.update(is_primary=False)

                # Update the username if the email address is changed.
                if self.emailable is User and self.emailable.username != self.email and not settings.ENABLE_USERNAMES:
                    User.objects.filter(id=self.emailable.id).update(
                        username=self.email
                    )
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        EmailAddress delete method.
        The email address may be deleted if it is not the primary email address, or
        if there are no other email addresses associated with the user.
        """
        if not self.emailable.email_addresses.exclude(pk=self.pk, is_primary=True).exists():
            raise ValidationError(_("Cannot delete the only email address."))
        super().delete(*args, **kwargs)

    def is_valid_redemption(
        self, user: Optional["User"] = None, *args, **kwargs
    ) -> bool:
        """
        Returns True if the redemption is valid.
        """
        if not user:
            raise ValueError(_("User is required."))
        match type(self.emailable):
            case "User":
                if self.emailable.id != user.id:
                    return False
            case _:
                raise ValueError(_("Not implemented for emailable."))
        return True

    def redeem(self, user: Optional["User"] = None, *args, **kwargs) -> None:
        """
        Redeems the email address.
        """
        self.verified_at = timezone.now()
        self.save()

    def set_primary(self) -> None:
        """
        Sets the email address as the primary email address.
        """
        self.is_primary = True
        self.save()


class RedeemableKey(HasUuidId, HasTimestamps, HasPolymorphicForeignKeys, models.Model):
    """
    Provides a generic way to redeem a redeemable object where a redeemer may or
    may not be required.
    """

    user = models.ForeignKey("account.User", null=True, blank=True, on_delete=models.SET_NULL)
    redeemable = PolymorphicFKRelationship(null=False, on_delete=models.SET_NULL, related_name="redeemable_keys")
    redeemable_user = PolymorphicForeignKey(User, redeemable)
    redeemable_email_address = PolymorphicForeignKey(EmailAddress, redeemable)
    expires_at = models.DateTimeField(null=True, blank=True)
    redeemed_at = models.DateTimeField(null=True, blank=True)

    staged_data = {}
    objects = RedeemableKeyManager()

    class Meta:
        abstract=False
        # ordering = ("-created_at",)

    def __str__(self) -> str:
        return str(self.id)

    @property
    def redeemable_model(self) -> IsRedeemable | NoneType:
        return (
            cast(IsRedeemable, self.redeemable)
            if self.redeemable
            else None
        )

    @property
    def is_redeemed(self) -> bool:
        return bool(self.redeemed_at)

    @property
    def is_expired(self) -> bool:
        """Returns whether the key has expired or not."""
        return self.expires_at < timezone.now() if self.expires_at else False

    @property
    def can_redeem(self) -> bool:
        return not self.is_expired and not self.is_redeemed

    def save(self, *args, **kwargs) -> None:
        # TODO
        super().save(*args, **kwargs)

    def expire(self) -> None:
        """Expires the key."""
        self.expires_at = timezone.now()
        self.save()

    def stage_redemption(
        self, user: Optional["IsRedeemable"] = None, *args, **kwargs
    ) -> None:
        self.staged_data["user"] = user
        self.staged_data["args"] = args
        self.staged_data["kwargs"] = kwargs

    def is_valid(self) -> bool:
        if self.is_expired:
            raise ValueError(_("Key has expired."))
        if self.redeemed_at:
            raise ValueError(_("Key has already been redeemed."))
        if self.user and self.staged_data.get("user") != self.user:
            raise ValueError(_("Key is not valid for this user."))
        return cast(IsRedeemable, self.redeemable).is_valid_redemption(
            **self.staged_data
        )

    def redeem(self, validate=True) -> bool:
        if validate:
            self.is_valid()
        with atomic():
            success: bool = cast(IsRedeemable, self.redeemable).redeem(
                **self.staged_data
            )
            if success:
                self.redeemed_at = timezone.now()
                return True
        return False
