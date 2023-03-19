from abc import abstractmethod
from django.db import models
from typing import TYPE_CHECKING, Optional
from account.lib.managers import PasswordManager, EmailAddressManager, RedeemableKeyManager
from account.lib.querysets import EmailAddressQuerySet

if TYPE_CHECKING:
    from account.models import User, Password, EmailAddress



class IsRedeemable(models.Model):
    """
    Mixin that adds support for RedeemableKey to a model.
    Adds the GenericRedeemable type to the model.
    """

    class Meta:
        abstract = True

    redeemable_keys: "RedeemableKeyManager"

    @abstractmethod
    def get_is_redeemed(self) -> bool:
        """
        Return True if the model instance has been redeemed.
        """
        raise NotImplementedError

    @abstractmethod
    def is_valid_redemption(self, user: Optional["User"] = None, *args, **kwargs) -> bool:
        """
        Validate that redemption is possible with the given parameters.
        """
        raise NotImplementedError

    @abstractmethod
    def redeem(self, user: Optional["User"] = None, *args, **kwargs) -> bool:
        """
        Redeem the model instance.
        """
        raise NotImplementedError


class IsPasswordProtected(models.Model):
    """
    Mixin that adds support for Password to a model.
    Adds the IsPasswordProtected type to the model.
    """

    class Meta:
        abstract = True

    _password: Optional["Password"] = None
    passwords: "PasswordManager"

    def get_password(self) -> Optional["Password"]:
        """
        Returns the most recent password for the user.
        """
        from account.models import Password
        if self._password and self._password.deleted_at is None:
            return self._password
        self._password = Password.objects.filter(protected=self, deleted_at__isnull=True).first()
        return self._password


    def set_password(self, value: str) -> None:
        """
        Sets the user's password.
        """
        # Delete any existing passwords for this user
        for password in self.passwords.all():
            password.delete()

        from account.models import Password

        # Create a new password
        self._password = Password.objects.create(protected=self, raw_password=value)

    def delete_password(self) -> None:
        """
        Deletes the user's password.
        """
        # Delete any existing passwords for this user
        Password.objects.filter(deleted_at__isnull=True, protected=self).delete()
        _password = None

    def set_unusable_password(self) -> None:
        """
        Sets a value that will never be a valid hash.
        """
        self.delete_password()

    def refresh_from_db(self, using=None, fields=None, **kwargs):
        _password = None
        super().refresh_from_db(using, fields, **kwargs)

    password = property(get_password, set_password, delete_password)

    def check_password(self, raw_password: str) -> bool:
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        if self.password:
            return self.password.validate(raw_password)
        return False


class IsEmailable(models.Model):
    """
    Mixin that adds support for EmailAddress to a model.
    """

    class Meta:
        abstract = True

    _primary_email_address: Optional["EmailAddress"] = None
    email_addresses = EmailAddressManager()

    def get_primary_email_address(self) -> Optional["EmailAddress"]:
        """
        Returns the primary email address for the emailable.
        """
        if self._primary_email_address:
            return self._primary_email_address
        _primary_email_address = self.email_addresses.primary().first()
        return _primary_email_address

    def set_primary_email_address(self, value) -> None:
        """
        Sets the primary email address for the emailable.
        """
        if isinstance(value, str):
            kwargs = {"email": value}
        elif isinstance(value, int):
            kwargs = {"id": value}
        elif isinstance(value, "EmailAddress"):
            kwargs = {"id": value.id}
        else:
            raise TypeError("Invalid value for primary email address, must be a string, int, or EmailAddress instance.")

        # Update the other email addresses related to the emailable instance.
        self.email_addresses.exclude(**kwargs).update(is_primary=False)

        self.email_addresses.filter(**kwargs).update(is_primary=True)
        self._primary_email_address = self.email_addresses.primary()

    primary_email_address = property(get_primary_email_address, set_primary_email_address)
