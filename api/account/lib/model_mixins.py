from abc import abstractmethod
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from typing import TYPE_CHECKING,Any, Type, TypeVar, Literal, Generic
from abc import abstractmethod


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
    def redeem(self, *args, **kwargs) -> bool:
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
