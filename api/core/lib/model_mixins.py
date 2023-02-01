from django.db import models
from uuid import uuid4


# Mixin that adds a UUID primary key to a model.
class HasUuidId(models.Model):
    """
    Mixin that adds a UUID primary key to a model.
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
