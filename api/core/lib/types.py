"""
These types are used to improve type hinting without causing circular imports
and class inheritance conflicts with mixins.
"""

from typing import TYPE_CHECKING

ManagerType = object
ModelType = object

if TYPE_CHECKING:
    from django.db.models import Manager, Model
    ManagerType = type(Manager)
    ModelType = type(Model)
