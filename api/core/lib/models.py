from uuid import uuid4

from django.db import models


class BaseModel(models.Model):
    """
    Abstract model with behavior common to all models in this project.
    """

    uuid = models.UUIDField(primary_key=True, default=uuid4)

    class Meta:
        abstract = True


class DatesMixin:
    """
    Mixin with date fields.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
