"""
These types are used to improve type hinting without causing circular imports
and class inheritance conflicts with mixins.
"""

from typing import TYPE_CHECKING, TypedDict, Callable

ManagerType = object
ModelType = object
ViewSetType = object

if TYPE_CHECKING:
    from django.db.models import Manager, Model, CASCADE, PROTECT, SET_NULL, SET_DEFAULT, SET
    from rest_framework.viewsets import ViewSet
    ManagerType = type("Manager")
    ModelType = type("Model")
    ViewSetType = type("ViewSet")


# class ManyToOneForeignKeyDict(TypedDict):
#     name: str
#     model: Model | str | tuple[str, str]


# class ManyToOneGroupDict(TypedDict):
#     type_class: "Model" # The mixin class that defines the reverse relationship
#     models: ManyToOneForeignKeyDict
#     on_delete: Callable # The on_delete behavior for the foreign keyz
#     null: bool # Whether this ManyToOne relationship is nullable
#     related_name: str # The name of the reverse relationship


# class ManyToOneGroupsDict(TypedDict):
#     property: ManyToOneGroupDict
