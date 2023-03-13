from ast import Mod
from typing import Any, cast
from django.apps import apps
from django.db import models
from uuid import uuid4
from django.utils import timezone
from core.lib.types import ModelType
from typing import cast
from core.lib.model_fields import PolymorphicFK, PolymorphicFKRelationship
from django.core.exceptions import ValidationError

# Mixin that adds a UUID primary key to a model.
class HasUuidId(ModelType):
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


class HasPolymorphicForeignKeys(models.Model):
    """
    A model mixin that adds safety checks for each PolymorphicRelationship that the model has.
    """

    class Meta:
        abstract: bool = True

    def __init__(self, *args, **kwargs) -> None:

        for key in self.get_polymorphic_relationships().keys():
                new_value = kwargs.pop(key, None)
                if new_value:
                    setattr(self, key, new_value)
        super().__init__(*args, **kwargs)

    def _check_polymorphic_relationships(self):
        """
        Check that all PolymorphicRelationships have at most one PolymorphicFK that is populated.
        """
        for field in self._meta.fields:
            if isinstance(field, PolymorphicFKRelationship):
                related_fks = self.get_polymorphic_fks_for_relationship(field)
                related_fk_count = len(related_fks)
                if related_fk_count == 0 and not field.null:
                    raise ValidationError(f"{self.__class__.__name__}: {field} cannot be empty")
                elif related_fk_count > 1:
                    raise ValidationError(f"{self.__class__.__name__}: {field} has too many values")

    @classmethod
    def get_polymorphic_relationships(cls):
        """
        Return a list of all the PolymorphicRelationships associated with this model.
        """
        relationships = {}
        for c in cls.__mro__:
            for key, attr in c.__dict__.items():
                if isinstance(attr, PolymorphicFKRelationship):
                    relationships[key] = attr
        return relationships

    @classmethod
    def get_polymorphic_fks_for_relationship(cls, relationship_field):
        """
        Return a list of all the PolymorphicFK associated with a given PolymorphicRelationship.
        """
        return [
            f for f in cls._meta.fields
            if isinstance(f, PolymorphicFK) and f.relationship_field is relationship_field
        ]


    @classmethod
    def get_relationship_model_field_name(cls, relationship, model):
        """
        Return the field name of the PolymorphicFK associated with a given PolymorphicRelationship and model.
        """
        for field in cls._meta.fields:
            if isinstance(field, PolymorphicFK) and field.relationship_field is relationship and field.model is model:
                return field.name
        return None

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.full_clean()
        super().delete(*args, **kwargs)

    def clean(self):
        self._check_polymorphic_relationships()
        super().clean()
