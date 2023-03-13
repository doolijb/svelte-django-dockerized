from typing import cast
from django.db import models
from abc import abstractmethod
from django.db.models import Manager
from core.lib.model_fields import PolymorphicFKRelationship
from core.lib.model_mixins import HasPolymorphicForeignKeys

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

    def _map_polymorphic_field_kwargs(self, **kwargs):
        relationships = self.model.get_polymorphic_relationships()
        for rel_field, rel_prop in relationships.items():
            print(f"rel_field_name: {rel_field}")
            if not rel_field:
                raise ValueError(f"Could not find relationship field name for relationship {rel_prop} in model {self.model}")
            if rel_field in kwargs:
                model_field_name = self.model.get_relationship_model_field_name(rel_prop, self.model)
                print(f"model_field_name: {model_field_name}")
                if not model_field_name:
                    raise ValueError(f"Could not foreign key field name for relationship {rel_field} and model {self.model}")
                kwargs[model_field_name] = kwargs.pop(rel_field)
        return kwargs

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
