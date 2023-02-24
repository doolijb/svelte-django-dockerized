from abc import abstractmethod
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from core.lib.types import ModelType
from typing import Optional

"""
Here we are using generic types to make it easier to type hint without causing circular imports.
"""


class IsRedeemable(models.Model):
    """
    Mixin that adds support for RedeemableKey to a model.
    Adds the GenericRedeemable type to the model.
    """

    redeemable_keys = GenericRelation("account.RedeemableKey", related_query_name="redeemable")

    @abstractmethod
    def get_is_redeemed(self) -> bool:
        """
        Return True if the model instance has been redeemed.
        """
        raise NotImplementedError

    @abstractmethod
    def redeem(self, redeemer: Optional["IsRedeemer"] = None, *args, **kwargs) -> bool:
        """
        Redeem the model instance.
        """
        raise NotImplementedError

    @abstractmethod
    def redeem_by_redeemer(self, redeemer:"IsRedeemer", *args, **kwargs) -> bool:
        """
        Redeem the model instance for a redeemer.
        """
        raise NotImplementedError

    class Meta:
        abstract: bool = True


class IsRedeemer(models.Model):
    """
    Mixin that adds support for RedeemableKey to a model.
    Adds the GenericRedeemer type to the model.
    """

    redeemable_keys = GenericRelation("account.RedeemableKey", related_query_name="redeemer")

    class Meta:
        abstract: bool = True

class IsPasswordProtected(models.Model):
    """
    Mixin that adds support for Password to a model.
    Adds the IsPasswordProtected type to the model.
    """

    passwords = GenericRelation("account.Password", related_query_name="password")

    class Meta:
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

    def set_password(self, raw_password: str) -> None:
        """
        Sets the password for the protected.
        """
        self.passwords.create(hashable=raw_password)

    class Meta:
        abstract: bool = True


class IsEmailable(models.Model):
    """
    Mixin that adds support for EmailAddress to a model.
    """

    email_addresses = GenericRelation("account.EmailAddress", related_query_name="emailable")

    class Meta:
        abstract: bool = True
