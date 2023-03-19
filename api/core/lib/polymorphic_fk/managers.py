from django.db import models
from django.contrib.contenttypes.models import ContentType


class PolymorphicRelatedManager(models.Manager):
    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = instance

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.instance:
            content_type = ContentType.objects.get_for_model(self.instance)
            queryset = queryset.filter(**{
                f"{self.field_name}__content_type": content_type,
                f"{self.field_name}__object_id": self.instance.pk,
            })
        return queryset

    def for_instance(self, instance):
        """
        Set the instance and return self to allow chained calls.
        """
        self.instance = instance
        return self
