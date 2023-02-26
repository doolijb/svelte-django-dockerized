"""
Models for the account app.
"""

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.transaction import atomic
from django.utils import timezone
from django.utils.translation import gettext as _
from typing import Literal, Optional, cast
from django.contrib.auth.hashers import check_password

from core.lib.model_mixins import HasUuidId, HasTimestamps, HasSoftDelete

from .lib.managers import EmailAddressManager, UserManager
from .lib.model_mixins import IsEmailable, IsRedeemable


class User(
    HasUuidId,
    HasTimestamps,
    PermissionsMixin,
    IsEmailable,
    AbstractBaseUser,
    models.Model
):
    """
    Model representing an authenticable user. Compared to the default Django
    user model, this User has no email field. Instead, it is closely tied to
    the EmailAddress model.
    """

    username = models.CharField(_("username"), max_length=30, unique=True)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    is_active = models.BooleanField(_("active"), default=True)
    is_admin = models.BooleanField(_("staff status"), default=False)
    is_superuser = models.BooleanField(_("superuser status"), default=False)

    objects: UserManager = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        """
        Meta options for the User model.
        """

        verbose_name: str = _("user")
        verbose_name_plural: str = _("users")
        ordering = ("-created_at",)
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


class Password(HasUuidId, HasTimestamps, HasSoftDelete, models.Model):
    """
    Model representing a password for a protected object.

    The protected object is identified by a generic foreign key. The protected
    object must implement the IsProtected interface.
    """

    protected_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="protected"
    )
    protected_id = models.UUIDField()
    protected = GenericForeignKey("protected_content_type", "protected_id")
    hash = models.CharField(max_length=128, editable=False)

    objects = EmailAddressManager()

    class Meta:
        """
        Meta options for the Password model.
        """

        verbose_name: str = _("password")
        verbose_name_plural: str = _("passwords")
        # ordering: list[str] = ["-created_at"]

    def __str__(self) -> str:
        """String representation of the Password model."""
        return self.hash

    def validate(self, password: str) -> bool:
        """
        Check if the given password matches the hash.
        """
        return check_password(password, self.hash)


class EmailAddress(HasUuidId, HasTimestamps, IsRedeemable, models.Model):
    emailable_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="emailable"
    )
    emailable_id = models.UUIDField()
    emailable = GenericForeignKey("emailable_content_type", "emailable_id")
    email = models.EmailField(unique=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    is_primary = models.BooleanField(default=False)
    # redeemable_keys = GenericRelation(
    #     "account.RedeemableKey", related_query_name="redeemable"
    # )

    objects: EmailAddressManager = EmailAddressManager()

    @property
    def is_verified(self) -> bool:
        return bool(self.verified_at)

    @property
    def emailable_model(self):
        return self.emailable_content_type.model_class()

    class Meta:
        unique_together: tuple[Literal["user"], Literal["email"]]
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.email

    def save(self, *args, **kwargs) -> None:
        """
        EmailAddress save method.
        If settings.ENABLE_USERNAMES is False, the username will be set to the
        email address.
        """
        with atomic():
            if self.is_primary:
                queryset = EmailAddress.objects.filter(
                        emailable=self.emailable,
                        is_primary=True
                    )
                if self.id:
                    queryset = queryset.exclude(id=self.id)
                queryset.update(is_primary=False)
                if self.emailable_model is User and not settings.ENABLE_USERNAMES:
                    User.objects.filter(id=self.emailable_id).update(username=self.email)
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        EmailAddress delete method.
        The email address may be deleted if it is not the primary email address, or
        if there are no other email addresses associated with the user.
        """
        if self.is_primary:
            raise ValueError(_("Cannot delete primary email address."))
        if self.user.email_addresses.count() == 1:  # type: ignore
            raise ValueError(_("Cannot delete only email address."))
        super().delete(*args, **kwargs)

    def is_valid_redemption(self, user: Optional["User"] = None, *args, **kwargs) -> bool:
        """
        Returns True if the redemption is valid.
        """
        if not user:
            raise ValueError(_("User is required."))
        match self.emailable_model:
            case "User":
                if self.emailable_id != user.id:
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
        self.objects.filter(emailable=self.emailable).update(is_primary=False)

class RedeemableKey(HasUuidId, HasTimestamps, models.Model):
    """
    Provides a generic way to redeem a redeemable object where a redeemer may or
    may not be required.
    """
    app_label = 'auth'

    user = models.ForeignKey("account.User", null=True, on_delete=models.SET_NULL)
    redeemable_content_type = models.ForeignKey(
        ContentType, null=True, on_delete=models.SET_NULL, related_name="redeemable_keys"
    )
    redeemable = GenericForeignKey("redeemable_content_type", "redeemable_uuid")
    expires_at = models.DateTimeField(null=True, blank=True)
    redeemed_at = models.DateTimeField(null=True, blank=True)

    staged_data = {}
    objects = models.Manager()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return str(self.id)

    def save(self, *args, **kwargs) -> None:
        # TODO
        super().save(*args, **kwargs)

    @property
    def redeemable_model(self):
        return self.redeemable_content_type.model_class()

    @property
    def is_redeemed(self) -> bool:
        return bool(self.redeemed_at)

    @property
    def is_expired(self) -> bool:
        """Returns whether the key has expired or not."""
        return self.date_expires < timezone.now()

    @property
    def can_redeem(self) -> bool:
        return not self.is_expired and not self.is_redeemed

    def expire(self) -> None:
        """Expires the key."""
        self.date_expires: timezone.datetime = timezone.now()
        self.save()

    def stage_redemption(self, user: Optional["IsRedeemable"] = None, *args, **kwargs) -> None:
        self.staged_data['user'] = user
        self.staged_data['args'] = args
        self.staged_data['kwargs'] = kwargs

    def is_valid(self) -> bool:
        if self.is_expired:
            raise ValueError(_("Key has expired."))
        if self.redeemed_at:
            raise ValueError(_("Key has already been redeemed."))
        if self.user and self.staged_data.get('user') != self.user:
            raise ValueError(_("Key is not valid for this user."))
        return cast(IsRedeemable, self.redeemable).is_valid_redemption(**self.staged_data)

    def redeem(self, validate=True) -> bool:
        if validate:
            self.is_valid()
        with atomic():
            success: bool = cast(IsRedeemable, self.redeemable).redeem(**self.staged_data)
            if success:
                self.redeemed_at = timezone.now()
                return True
        return False
