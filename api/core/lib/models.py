from uuid import uuid4

from django.db import models
from django.core.cache import cache


class BaseModel(models.Model):
    """
    Abstract model with behavior common to all models in this project.
    """

    id = models.UUIDField(primary_key=True, default=uuid4)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Grab the manager for easier access.
        self._manager = self.__class__.objects

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Saves the model and clears all caches.
        """
        self.clear_caches()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Deletes the model and clears all caches.
        """
        self.clear_caches()
        super().delete(*args, **kwargs)

    def clear_caches(self):
        """
        Clears all caches for this model.
        """
        self._manager.clear_caches(object=self)  # type: ignore


class DatesMixin(models.Model):
    """
    Mixin with date fields.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
