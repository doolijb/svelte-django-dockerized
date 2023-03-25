from typing import Type, TYPE_CHECKING
from django.db.models import QuerySet


if TYPE_CHECKING:
    from .model_mixins import HasPolymorphicForeignKeys


class PolycapableQuerySet(QuerySet):
    """
    A queryset that can be used to filter by polymorphic relationships.
    """

    model: Type["HasPolymorphicForeignKeys"]

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

    def _map_polymorphic_field_kwargs(self, **kwargs):
        return map_polymorphic_field_kwargs(self, **kwargs)


def map_polymorphic_field_kwargs(self, **kwargs):
    relationships = self.model.get_polymorphic_relationships()
    for rel_field, rel_prop in relationships.items():
        if not rel_field:
            raise ValueError(f"Could not find relationship field name for relationship {rel_prop} in model {self.model}")

        if rel_field in kwargs:
            # Get PolymorphicFK belonging to the relationship, and the model type
            model_field_name = self.model.get_relationship_model_field_name(rel_prop, type(kwargs[rel_field]))
            if not model_field_name:
                raise ValueError(f"Could not foreign key field name for relationship {rel_field} and model {self.model}")

            kwargs[model_field_name] = kwargs.pop(rel_field)

    return kwargs
