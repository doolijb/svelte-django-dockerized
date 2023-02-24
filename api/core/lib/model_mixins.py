from django.db import models
from uuid import uuid4
from django.utils import timezone


# Mixin that adds a UUID primary key to a model.
class HasUuidId(models.Model):
    """
    Mixin that adds a UUID primary key to a model.

    @attr id: The UUID primary key.
    """

    id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract: bool = True

class HasTimestamps(models.Model):
    """
    @attr created_at: The date and time the model was created.
    @attr updated_at: The date and time the model was last updated.
    """

    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        abstract: bool = True

class HasSoftDelete(models.Model):
    """
    Mixin that adds a `deleted_at` field to a model.

    @attr deleted_at: The date and time the model was deleted.
    """

    deleted_at: models.DateTimeField = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract: bool = True

    def delete(self, *args, **kwargs) -> None:
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self, *args, **kwargs) -> None:
        super().delete(*args, **kwargs)

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
