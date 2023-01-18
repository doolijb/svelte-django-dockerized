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

from core.lib.models import BaseModel, DatesMixin

from .managers import EmailAddressManager, UserManager


class User(BaseModel, AbstractBaseUser, PermissionsMixin, DatesMixin):
    """
    Model representing an authenticable user. Compared to the default Django
    user model, this User has no email field. Instead, it is closely tied to
    the EmailAddress model.
    """

    username = models.CharField(_("username"), max_length=30, unique=True)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    is_active = models.BooleanField(_("active"), default=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        """
        Meta options for the User model.
        """

        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-created_at"]

    def __str__(self):
        """String representation of the User model."""
        return self.username

    @property
    def full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        return self.first_name + " " + self.last_name

    @property
    def short_name(self):
        """Return the short name for the user."""
        return self.first_name


class EmailAddress(BaseModel, DatesMixin):
    user = models.ForeignKey(
        "account.User", on_delete=models.CASCADE, related_name="email_addresses"
    )
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    is_primary = models.BooleanField(default=False)
    redeemable_keys = GenericRelation(
        "account.RedeemableKey", related_query_name="redeemable"
    )

    objects = EmailAddressManager()

    class Meta:
        unique_together = ("user", "email")
        ordering = ["-created_at"]
        indexes = [
            models.Index(
                name="user_primary_email_address_idx",
                fields=["user", "is_primary"],
                condition=models.Q(is_primary=True),
            )
        ]

    test = "test"

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        """
        EmailAddress save method.
        If settings.ENABLE_USERNAMES is False, the username will be set to the
        email address.
        """
        if self.is_primary:
            EmailAddress.objects.filter(user=self.user).update(is_primary=False)
            if not settings.ENABLE_USERNAMES and self.user.username != self.email:
                self.user.username = self.email
                self.user.save(*args, **kwargs)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        EmailAddress delete method.
        The email address may be deleted if it is not the primary email address, or
        if there are no other email addresses associated with the user.
        """
        if self.is_primary:
            raise ValueError(_("Cannot delete primary email address."))
        if self.user.email_addresses.count() == 1:
            raise ValueError(_("Cannot delete only email address."))
        super().delete(*args, **kwargs)

class RedeemableKey(BaseModel, DatesMixin):
    """
    Provides a redeemable key for a given polymorphic model and user.
    """

    user = models.ForeignKey(
        "account.User", on_delete=models.CASCADE, null=True, blank=True
    )
    redeemable_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    redeemable_uuid = models.UUIDField()
    redeemable = GenericForeignKey(
        "redeemable_content_type",
        "redeemable_uuid",
    )
    date_expires = models.DateTimeField(null=True, blank=True)
    date_redeemed = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=["redeemable_content_type", "redeemable_uuid"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        # TODO
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        """Returns whether the key has expired or not."""
        if self.date_expires:
            return self.date_expires < timezone.now()
        return False

    @property
    def is_redeemed(self):
        """Returns whether the key has been redeemed or not."""
        return self.date_redeemed is not None

    def expire(self):
        """Expires the key."""
        self.date_expires = timezone.now()
        self.save()

    def redeem(self, user, *args, **kwargs):
        """
        Performs activation for a user and redeemable object.

        Checks if self has redeem method matching redeemable_content_type app and model, else raises NotImplemented.
        I.E. `redeem_account_emailaddress` for EmailAddress model.

        Returns True if successful, False otherwise.
        """

        if not user == self.user:
            raise ValueError(_("User does not match kecommity."))

        if self.redeemed:
            raise ValueError(_("Key has already been redeemed."))

        if self.is_expired:
            raise ValueError(_("Key has expired."))

        redeem_method = getattr(
            self,
            f"redeem_{self.redeemable_content_type.app_label}_{self.redeemable_content_type.model}",
            None,
        )

        if not redeem_method or not callable(redeem_method):
            raise NotImplementedError(
                _(
                    f"""Redeem method not implemented, no such method:
                redeem_{self.redeemable_content_type.app_label}_{self.redeemable_content_type.model}
                """
                )
            )

        # Multiple database transactions are required for this method, so we
        # wrap it in an atomic block.
        with atomic():

            success = redeem_method(user, *args, **kwargs)

            if success:
                self.redeemed = True
                self.date_redeemed = timezone.now()
                self.save()
                return True

        return False

    ###
    # Redeemable redeem methods
    ###

    def redeem_account_emailaddress(self, user, *args, **kwargs):
        """Redeems an EmailAddress object."""

        if type(self.redeemable) is not EmailAddress:
            raise ValueError(_("Redeemable is not an EmailAddress."))

        if not user == self.redeemable.user:
            raise ValueError(_("User does not own EmailAddress."))

        self.redeemable.is_verified = True
        self.redeemable.is_primary = True
        self.redeemable.save()
        self.save()
        return True
