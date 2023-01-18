from django.db import models
from django.core.cache import cache


class BaseModelManager(models.Manager):
    """
    A base model manager that provides a method to serialize the queryset.
    """
    # Caches to manage when the model is saved or deleted.
    cache_names = []

    def to_dict_by_id(self, values_list, single=False, key="id"):
        """
        Return a dictionary of a single object or queryset keyed by id.
        """
        if single and len(values_list) == 0:
            raise self.model.DoesNotExist
        elif single:
            return values_list[0]
        else:
            return {item.get(key): item for item in values_list}

    def serialize(
        self, queryset=None, format="json", fields=[], single=False, **kwargs
    ):
        """
        Serialize the queryset.
        """

        # If cache_name is provided, check if the cache exists.
        cache_name = kwargs.pop("cache_name", None)
        if cache_name:
            cache_data = cache.get(cache_name)
            if cache_data:
                return cache_data

        if queryset is None:
            queryset = self.get_queryset()
        if fields:
            queryset = queryset.values(*fields)
        values_list = queryset.values_list()
        data = self.to_dict_by_id(values_list=values_list, single=single)

        # If cache_name is provided, set the cache.
        if cache_name:
            cache.set(cache_name, data)

        return data

    def clear_object_caches(self, instance=None, instances=None):
        """
        Clear all caches for this model.
        """
        if instance:
            instances = [instance]

        # Clear all caches for this model instance(s).
        for instance in instances:
            for cache_name in self.cache_names:
                if "<id>" in cache_name:
                    cache_name = cache_name.replace("<id>", str(instance.id)) # type: ignore
                cache.delete(cache_name)
