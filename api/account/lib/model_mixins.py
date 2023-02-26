from abc import abstractmethod
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from core.lib.types import ModelType
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from account.models import User

"""
Here we are using generic types to make it easier to type hint without causing circular imports.
"""


class IsRedeemable(models.Model):
    """
    Mixin that adds support for RedeemableKey to a model.
    Adds the GenericRedeemable type to the model.
    """

    redeemable_keys = GenericRelation("account.RedeemableKey", related_query_name="redeemable")

    class Meta:
        abstract: bool = True

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

    def get_password(self) -> str:
        """
        Returns the password for the protected.
        """
        password = self.passwords.first()
        if password:
            return password.hash
        return ""

    def set_password(self, raw_password: str, validate=True) -> None:
            """
            Sets the password for the protected.
            """
            self.passwords.create(hashable=raw_password, validate=validate)

    passwords = GenericRelation("account.Password", related_query_name="password")
    password = property(fset=set_password, fget=get_password)

    class Meta:
        abstract: bool = True
        # Index the active passwords for this mixin's model
        indexes: list[models.Index] = [
            models.Index(fields=["passwords__is_active"]),
        ]

    def set_unusable_password(self) -> None:
        """
        Sets a value that will never be a valid hash.
        """
        password = self.passwords.first()
        if password:
            password.delete()

    def check_password(self, raw_password: str) -> bool:
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        password = self.passwords.first()
        if password:
            return password.validate(raw_password)
        return False


class IsEmailable(models.Model):
    """
    Mixin that adds support for EmailAddress to a model.
    """

    email_addresses = GenericRelation("account.EmailAddress", related_query_name="emailable")

    class Meta:
        abstract: bool = True

    def set_primary_email(self, email: str) -> None:
        """
        Sets the primary email address for the emailable.
        """
        self.email_addresses.filter(email=email).update(is_primary=True)
