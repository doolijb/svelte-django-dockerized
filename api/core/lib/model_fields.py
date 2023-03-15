from typing import Any, Optional, cast
from django.db.models import ForeignKey, CASCADE, PROTECT, SET_NULL, SET_DEFAULT, SET, Model


class PolymorphicFKRelationship():
    """
    Defines a relationship between a group of polymorphic foreign keys
    """

    _populated_field: Optional["PolymorphicFK"] = None

    def __init__(self, null: bool, on_delete: Any, related_name: str):
        self.null = null
        self.on_delete = on_delete
        self.related_name = related_name

    def __repr__(self) -> str:
        return f"PolymorphicRelationship(null={self.null}, on_delete={self.on_delete}, related_name='{self.related_name}')"

    def __get__(self, instance, owner):
        if self.populated_field:
            return self.populated_field.__get__(instance, owner)
        return None

    def __set__(self, instance, value: Optional[Model], propagate_down=True):
        """
        Set the value of the relationship field matching the model type of the value.
        """

        # Check if null and nullable
        if value is None and self.null:
            self._set_populated_field_to_none(propagate_down=propagate_down)
        # Else if null and not nullable
        elif value is None:
            if not self.null:
                raise ValueError(f"PolymorphicFKRelationship {self.related_name} cannot be empty")
            self._set_populated_field_to_none(propagate_down=propagate_down)
        else:
            raise ValueError(f"Invalid value {value} for PolymorphicFK")

        for fk in instance._meta.fields:
            # Make sure the field is a PolymorphicFK and that it is related to this relationship
            if not isinstance(fk, PolymorphicFK) or fk.relationship_field != self:
                raise ValueError(f"Invalid field {fk} for PolymorphicFKRelationship")

            # If value is a model instance
            if isinstance(value, fk.related_model):
                if propagate_down:
                    fk.__set__(instance, value, propagate_up=False)
                self._set_populated_field(fk)
            # Otherwise, null
            else:
                fk.__set__(instance, None, propagate_up=False)

    def _get_populated_field(self):
        if not self._populated_field:
            for fk in self.related_fields:
                if fk:
                    self._populated_field = fk
                    break
        return self._populated_field

    def _set_populated_field_to_none(self, propagate_down=True):
        self.__set__(None, None, propagate_down=propagate_down)

    def _set_populated_field(self, fk: "PolymorphicFK"):
        self._populated_field = fk
        self.populated_type = fk.related_model # TODO: Needs setter

    def _add_related_fk(self, fk: "PolymorphicFK"):
        """
        Add a related foreign key to the relationship
        """
        for existing_fk in self.related_fields:
            if existing_fk == fk:
                raise ValueError(f"Model {fk.model.__name__} for field {fk.name} already exists in {existing_fk.name} for relationship {self.related_name}")
        self.related_fields.append(fk)

    populated_field = property(_get_populated_field, _set_populated_field, _set_populated_field_to_none)
    populated_type: Optional[Any] = None # TODO: Needs getter, setter
    related_fields = []

    def get_prep_value(self, value):
        if isinstance(value, PolymorphicFKRelationship):
            return value.pk
        return super().get_prep_value(value)

    def get_field_for_model(self, model: Any):
        """
        Return the PolymorphicFK for a given model
        """
        for fk in self.related_fields:
            if fk.related_model == model:
                return fk
        return None

    def delete(self):
        """
        Delete the relationship by setting all related foreign keys to None
        """
        for fk in self.related_fields:
            setattr(fk, fk.name, None)


class PolymorphicFK(ForeignKey):
    """
    A polymorphic foreign key that can be used to create a polymorphic relationship.
    This should not be used directly. Instead, use the PolymorphicFK function. This is because
    child classes inherit parent constructor arguments, which we do not want.
    """
    relationship_field:PolymorphicFKRelationship

    def __set__(self, instance, value: Optional[Any], propagate_up: bool = True):
        if propagate_up:
            if value is None:
                cast(PolymorphicFKRelationship, self.relationship_field)._set_populated_field_to_none(propagate_down=False)
            else:
                cast(PolymorphicFKRelationship, self.relationship_field)._set_populated_field(self)
        setattr(instance, self.attname, value)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        pk = getattr(instance, self.attname) if hasattr(instance, self.attname) else None
        if pk:
            return self.related_model.objects.get(pk=pk)
        return None


def PolymorphicForeignKey(model:Any, relationship_field:PolymorphicFKRelationship):
    """
    A polymorphic foreign key that can be used to create a polymorphic relationship
    between two models. Returns a Django ForeignKey.
    """
    fk = PolymorphicFK(
        model,
        on_delete=relationship_field.on_delete,
        null=True, # type: ignore
        blank=True,
        related_name=relationship_field.related_name
    )
    relationship_field._add_related_fk(fk)
    fk.relationship_field = relationship_field
    return fk
