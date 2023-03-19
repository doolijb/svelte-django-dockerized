from ast import Mod
from typing import Any, cast
from django.apps import apps
from django.db import models
from uuid import uuid4
from django.utils import timezone
from typing import cast
from core.lib.polymorphic_fk.model_fields import PolymorphicFK, PolymorphicFKRelationship
from django.core.exceptions import ValidationError

# Mixin that adds a UUID primary key to a model.
class HasUuidId(models.Model):
    """
    Mixin that adds a UUID primary key to a model.

    @attr id: The UUID primary key.
    """

    class Meta:
        abstract: bool = True

    id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid4, editable=False)


class HasTimestamps(models.Model):
    """
    @attr created_at: The date and time the model was created.
    @attr updated_at: The date and time the model was last updated.
    """

    class Meta:
        abstract: bool = True

    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)


class HasSoftDelete(models.Model):
    """
    Mixin that adds a `deleted_at` field to a model.

    @attr deleted_at: The date and time the model was deleted.
    """

    class Meta:
        abstract: bool = True

    deleted_at: models.DateTimeField = models.DateTimeField(null=True, blank=True)

    def delete(self, *args, **kwargs) -> None:
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self, *args, **kwargs) -> None:
        super().delete(*args, **kwargs)

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
