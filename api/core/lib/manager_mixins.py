from typing import Type, cast
from django.db import models
from abc import abstractmethod
from django.db.models import Manager
from core.lib.model_fields import PolymorphicFKRelationship
from core.lib.model_mixins import HasPolymorphicForeignKeys
from core.lib.querysets import PolycapableQueryset, map_polymorphic_field_kwargs

class ManagesSoftDeletables(Manager):

    class Meta:
        abstract = True

    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(deleted_at__isnull=True)

    def any(self) -> models.QuerySet:
        return super().get_queryset()

    def all_deleted(self) -> models.QuerySet:
        return super().get_queryset().filter(deleted_at__isnull=False)


class ManagesTimestamps(Manager):

    class Meta:
        abstract = True

    def by_newest(self) -> models.QuerySet:
        return super().get_queryset().order_by('-created_at')

    def by_oldest(self) -> models.QuerySet:
        return super().get_queryset().order_by('created_at')


class ManagesPolymorphicRelationships(Manager):
    """
    Converts a polymorphic relationship into a queryset of the related models.
    """

    class Meta:
        abstract = True

    model: Type[HasPolymorphicForeignKeys]

    def _map_polymorphic_field_kwargs(self, **kwargs):
        return map_polymorphic_field_kwargs(self, **kwargs)

    def get_queryset(self) -> models.QuerySet:
        """ Uses PolycapableQueryset"""
        return PolycapableQueryset(self.model, using=self._db)

    def get(self, *args, **kwargs):
        """
        Get a model by its primary key.
        """
        kwargs = self._map_polymorphic_field_kwargs(**kwargs)
        return super().get(*args, **kwargs)

    def filter(self, *args, **kwargs):
        """
        Filter models by a set of criteria.
        """
        kwargs = self._map_polymorphic_field_kwargs(**kwargs)
        return super().filter(*args, **kwargs)

    def exclude(self, *args, **kwargs):
        """
        Exclude models by a set of criteria.
        """
        kwargs = self._map_polymorphic_field_kwargs(**kwargs)
        return super().exclude(*args, **kwargs)

    def create(self, *args, **kwargs):
        """
        Create a new model instance.
        """
        kwargs = self._map_polymorphic_field_kwargs(**kwargs)
        try:
            instance = super().create(*args, **kwargs)
        except Exception as e:
            raise e
        return instance

    def get_or_create(self, *args, **kwargs):
        """
        Get or create a model instance.
        """
        kwargs = self._map_polymorphic_field_kwargs(**kwargs)
        return super().get_or_create(*args, **kwargs)
