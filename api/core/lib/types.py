"""
These types are used to improve type hinting without causing circular imports
and class inheritance conflicts with mixins.
"""

from typing import TYPE_CHECKING

ManagerType = object
ModelType = object
ViewSetType = object

if TYPE_CHECKING:
    from django.db.models import Manager, Model
    from rest_framework.viewsets import ViewSet
    ManagerType = type(Manager)
    ModelType = type(Model)
    ViewSetType = type(ViewSet)
