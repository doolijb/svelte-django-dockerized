from django.db import models
from abc import abstractmethod
from core.lib.types import ManagerType

class ManagesSoftDeletables(ManagerType):

    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(deleted_at__isnull=True)

    def any(self) -> models.QuerySet:
        return super().get_queryset()

    def all_deleted(self) -> models.QuerySet:
        return super().get_queryset().filter(deleted_at__isnull=False)
