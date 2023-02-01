from uuid import uuid4
from django.db import models


class AbstractModel(models.Model):
    """
    Abstracts models.Model to allow model composition.
    """

    class Meta:
        abstract = True
