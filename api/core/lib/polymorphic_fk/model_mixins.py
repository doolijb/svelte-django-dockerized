from .model_fields import PolymorphicFK, PolymorphicFKRelationship
from django.core.exceptions import ValidationError
from django.db.models import Model


class HasPolymorphicForeignKeys(Model):
    """
    A model mixin that adds safety checks for each PolymorphicRelationship that the model has.
    """

    class Meta:
        abstract: bool = True

    def _check_polymorphic_relationships(self):
        """
        Check that all PolymorphicRelationships have at most one PolymorphicFK that is populated.
        """
        for field in self._meta.fields:
            if isinstance(field, PolymorphicFKRelationship):
                related_fks = self.get_polymorphic_fks_for_relationship(field)
                related_fk_count = len(related_fks)
                if related_fk_count == 0 and not field.null:
                    raise ValidationError(f"{self.__class__.__name__}: {field} cannot be empty")
                elif related_fk_count > 1:
                    raise ValidationError(f"{self.__class__.__name__}: {field} has too many values")

    @classmethod
    def get_polymorphic_relationships(cls):
        """
        Return a list of all the PolymorphicRelationships associated with this model.
        """
        relationships = {}
        for c in cls.__mro__:
            for key, attr in c.__dict__.items():
                if isinstance(attr, PolymorphicFKRelationship):
                    relationships[key] = attr
        return relationships

    @classmethod
    def get_polymorphic_fks_for_relationship(cls, relationship_field):
        """
        Return a list of all the PolymorphicFK associated with a given PolymorphicRelationship.
        """
        return [
            f for f in cls._meta.fields
            if isinstance(f, PolymorphicFK) and f.relationship_field is relationship_field
        ]

    @classmethod
    def get_relationship_model_field_name(cls, relationship, model):
        """
        Return the field name of the PolymorphicFK associated with a given PolymorphicRelationship and model.
        """
        for field in cls._meta.fields:
            if isinstance(field, PolymorphicFK) and field.relationship_field is relationship and field.model is model:
                return field.name
        return None

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.full_clean()
        super().delete(*args, **kwargs)

    def clean(self):
        self._check_polymorphic_relationships()
        super().clean()
