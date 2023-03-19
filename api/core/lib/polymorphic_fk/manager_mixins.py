from typing import Type
from django.db.models import Manager, QuerySet
from .model_mixins import HasPolymorphicForeignKeys
from .querysets import PolycapableQuerySet, map_polymorphic_field_kwargs


class ManagesPolymorphicRelationships(Manager):
    """
    Converts a polymorphic relationship into a queryset of the related models.
    """

    class Meta:
        abstract = True

    model: Type[HasPolymorphicForeignKeys]

    def _map_polymorphic_field_kwargs(self, **kwargs):
        return map_polymorphic_field_kwargs(self, **kwargs)

    def get_queryset(self) -> QuerySet:
        """ Uses PolycapableQueryset"""
        return PolycapableQuerySet(self.model, using=self._db)

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
        return super().create(*args, **kwargs)

    def get_or_create(self, *args, **kwargs):
        """
        Get or create a model instance.
        """
        kwargs = self._map_polymorphic_field_kwargs(**kwargs)
        return super().get_or_create(*args, **kwargs)
