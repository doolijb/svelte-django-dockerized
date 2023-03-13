from abc import abstractmethod
from inspect import Attribute
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from core.lib.types import ModelType
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from account.models import User, Password, EmailAddress
    from account.lib.managers import PasswordManager

"""
Here we are using generic types to make it easier to type hint without causing circular imports.
"""

class IsRedeemable(models.Model):
    """
    Mixin that adds support for RedeemableKey to a model.
    Adds the GenericRedeemable type to the model.
    """

    class meta:
        abstract = True

    redeemable_keys = GenericRelation(
        "account.RedeemableKey",
        related_query_name="redeemable"
        )

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

    class meta:
        abstract = True

    # Add this model to a global list of models that support passwords
    # This is used to dynamicall add foreign keys to the Password model
    # This is a list of strings to avoid circular imports
    if not 'models_with_passwords' in globals():
        globals()['models_with_passwords'] = {}
    globals()['models_with_passwords'][__name__] = f"__app_label__.{__name__}"

    # passwords: ForeignKeyManager["Password"]
    _password: Optional["Password"] = None

    def get_password(self) -> Optional["Password"]:
        """
        Returns the most recent password for the user.
        """
        if self._password:
            return self._password
        _set_password = self.passwords.by_newest().first()
        return _set_password


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

    def set_unusable_password(self) -> None:
        """
        Sets a value that will never be a valid hash.
        """
        password = self.passwords.by_newest().first()
        if password:
            password.delete()
        _password = None

    password = property(get_password, set_password, set_unusable_password)

    class Meta:
        # Index the active passwords for this mixin's model
        # indexes: list[models.Index] = [
        #     models.Index(fields=["passwords__is_active"]),
        # ]
        abstract=True

    def check_password(self, raw_password: str) -> bool:
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        if self.password:
            return self.password.validate(raw_password)
        return False


class IsEmailable(ModelType):
    """
    Mixin that adds support for EmailAddress to a model.
    """
    _primary_email_address: Optional["EmailAddress"] = None

    def get_primary_email_address(self) -> Optional["EmailAddress"]:
        """
        Returns the primary email address for the emailable.
        """
        if self._primary_email_address:
            return self._primary_email_address
        _primary_email_address = self.email_addresses.by_primary().first()
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
        self.email_addresses.filter(**kwargs).update(is_primary=True)
        self._primary_email_address = self.email_addresses.by_primary().first()

    primary_email_address = property(get_primary_email_address, set_primary_email_address)
