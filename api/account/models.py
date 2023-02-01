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
from typing import Any, Optional, Type, TypeVar, Literal, Generic, Union, cast

from core.lib.models import AbstractModel
from core.lib.model_mixins import HasUuidId, HasTimestamps

from .lib.managers import EmailAddressManager, UserManager
from .lib.model_mixins import IsRedeemable, IsRedeemer
from .lib.enums import EmailConfirmedChoices


class User(AbstractBaseUser, HasUuidId, HasTimestamps, PermissionsMixin, IsRedeemer):
    """
    Model representing an authenticable user. Compared to the default Django
    user model, this User has no email field. Instead, it is closely tied to
    the EmailAddress model.
    """

    username = models.CharField(_('username'), max_length=30, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_active = models.BooleanField(_('active'), default=True)

    objects: UserManager = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        """
        Meta options for the User model.
        """

        verbose_name: str = _('user')
        verbose_name_plural: str = _('users')
        ordering: list[str] = ['-created_at']

    def __str__(self) -> str:
        """String representation of the User model."""
        return self.username

    @property
    def full_name(self) -> str:
        """Return the first_name plus the last_name, with a space in between."""
        return self.first_name + ' ' + self.last_name

    @property
    def short_name(self) -> str:
        """Return the short name for the user."""
        return self.first_name


class EmailAddress(AbstractModel, HasUuidId, HasTimestamps, IsRedeemable):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='email_addresses'
    )
    email = models.EmailField(unique=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    is_primary = models.BooleanField(default=False)
    redeemable_keys = GenericRelation(
        'account.RedeemableKey', related_query_name='redeemable'
    )

    objects: EmailAddressManager = EmailAddressManager()

    class Meta:
        unique_together: tuple[Literal['user'], Literal['email']]
        ordering: tuple[Literal['-created_at']]
        indexes: tuple[models.Index] = (
            models.Index(
                name='user_primary_email_address_idx',
                fields=('user', 'is_primary',),
                condition=models.Q(is_primary=True),
            ),
        )

    def __str__(self) -> str:
        return self.email

    def save(self, *args, **kwargs) -> None:
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
            raise ValueError(_('Cannot delete primary email address.'))
        if self.user.email_addresses.count() == 1: # type: ignore
            raise ValueError(_('Cannot delete only email address.'))
        super().delete(*args, **kwargs)

    def redeem_by_redeemer(self, redeemer:"IsRedeemable", *args, **kwargs) -> bool:
        match type(redeemer):
            case User.__class__:
                self.confirmed_at=timezone.now()
                self.save()
                return True
            case _:
                raise ValueError(_(f'Redeemer type {type(redeemer)} not supported.'))


class RedeemableKey(AbstractModel, HasUuidId, HasTimestamps):
    """
    Provides a redeemable key for a given polymorphic model and user.
    """

    redeemer_content_type = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE, related_name='redeemer_keys')
    redeemer_uuid = models.UUIDField(null=True)
    redeemer = GenericForeignKey('redeemer_content_type','redeemer_uuid')
    redeemable_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='redeemable_keys')
    redeemable_uuid = models.UUIDField()
    redeemable = GenericForeignKey('redeemable_content_type','redeemable_uuid')
    expires_at = models.DateTimeField(null=True, blank=True)
    redeemed_at = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()

    class Meta:
        indexes: list[models.Index] = [
            models.Index(fields=['redeemable_content_type', 'redeemable_uuid']),
        ]
        ordering: list[str] = ['-created_at']

    def __str__(self) -> str:
        return str(self.id)

    def save(self, *args, **kwargs) -> None:
        # TODO
        super().save(*args, **kwargs)

    @property
    def is_expired(self) -> bool:
        """Returns whether the key has expired or not."""
        return self.date_expires < timezone.now()


    def expire(self) -> None:
        """Expires the key."""
        self.date_expires: timezone.datetime = timezone.now()
        self.save()

    def redeem(self, *args, **kwargs) -> bool:
        """
        Performs activation on the redeemable.

        @return: True if activation was successful, False otherwise.
        """
        if self.redeemed_at:
            raise ValueError(_('Key has already been redeemed.'))
        if self.is_expired:
            raise ValueError(_('Key has expired.'))
        with atomic():
            success: bool = cast(IsRedeemable, self.redeemable).redeem(key=self, *args, **kwargs);
            if success:
                self.redeemed_at=timezone.now()
                return True
        return False

    def redeem_by_redeemer(self, key:"RedeemableKey", redeemer:"IsRedeemer", *args, **kwargs) -> bool:
        """
        Performs activation on the redeemable on behalf of a redeemer.

        @return: True if activation was successful, False otherwise.
        """
        if self.redeemed_at:
            raise ValueError(_('Key has already been redeemed.'))
        if self.is_expired:
            raise ValueError(_('Key has expired.'))
        if not self.redeemer == redeemer:
            raise ValueError(_('Redeemer does not own key.'))
        with atomic():
            success: bool = cast(IsRedeemable, self.redeemable).redeem_by_redeemer(key=self, redeemer=redeemer, *args, **kwargs);
            if success:
                self.redeemed_at=timezone.now()
                self.save()
                return True
        return False
