from uuid import uuid4

from django.db import models
from django.core.cache import cache


class BaseModel(models.Model):
    """
    Abstract model with behavior common to all models in this project.
    """

    id = models.UUIDField(primary_key=True, default=uuid4)

    class Meta:
        abstract = True


class DatesMixin(models.Model):
    """
    Mixin with date fields.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
