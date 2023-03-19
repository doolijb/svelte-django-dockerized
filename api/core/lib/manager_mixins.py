from django.db import models
from django.db.models import Manager


class ManagesSoftDeletables(Manager):

    class Meta:
        abstract = True

    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(deleted_at__isnull=True)

    def any(self) -> models.QuerySet:
        return super().get_queryset()

    def all_deleted(self) -> models.QuerySet:
        return super().get_queryset().filter(deleted_at__isnull=False)


class ManagesTimestamps(Manager):

    class Meta:
        abstract = True

    def by_newest(self) -> models.QuerySet:
        return super().get_queryset().order_by('-created_at')

    def by_oldest(self) -> models.QuerySet:
        return super().get_queryset().order_by('created_at')
