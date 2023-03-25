from typing import Any, Optional, Type, cast
from django.db.models import ForeignKey, Model
from typing import Any
from .types import OnDeleteType


class PolymorphicFKRelationship():
    """
    Defines a relationship between a group of polymorphic foreign keys
    """

    def __init__(self, null: bool, on_delete: OnDeleteType, related_name: str):
        self.null = null
        self.on_delete = on_delete
        self.related_name = related_name
        self.related_fields = []
        # TODO: FIX - This is behaving like a class property instead of a class instance property...
        # self._populated_field: Optional["PolymorphicFK"] = None

    def __repr__(self) -> str:
        return f"PolymorphicRelationship(null={self.null}, on_delete={self.on_delete}, related_name='{self.related_name}')"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        # Disabling _populated_field for now until it's fixed...
        # For now this will be slightly inefficient and will loop through all related fields
        # elif not self._populated_field:
        for fk in self.related_fields:
            result = fk.__get__(instance, owner)
            if result is not None:
                self._populated_field = fk
                return result
        # else:
        #     return self.populated_field.__get__(instance, owner)
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
            found_matching_model = False
            for fk in instance._meta.fields:
                # Make sure the field is a PolymorphicFK and that it is related to this relationship
                if not isinstance(fk, PolymorphicFK) or fk.relationship_field != self:
                    continue

                # If value is a model instance
                if isinstance(value, fk.related_model):
                    if propagate_down:
                        fk.__set__(instance, value, propagate_up=False)
                    self._set_populated_field(fk)
                    found_matching_model = True
                    break

            if not found_matching_model:
                raise ValueError(f"Invalid value {value} for PolymorphicFK")

    # def _get_populated_field(self):
    #     return self._populated_field

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
                raise ValueError(f"Model {fk.related_model.__name__} for field {fk.name} already exists in {existing_fk.name} for relationship {self.related_name}")
        self.related_fields.append(fk)

    # populated_field = property(_get_populated_field, _set_populated_field, _set_populated_field_to_none)
    populated_type: Optional[Type[Model]] = None # TODO: Needs getter, setter

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

    def __init__(self, *args, **kwargs):
        self.relationship_field:Optional[PolymorphicFKRelationship] = None
        super().__init__(*args, **kwargs)

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
        pk = instance.__dict__[self.attname] if self.attname in instance.__dict__ else None
        if pk:
            return self.related_model.objects.get(pk=pk)
        return None


def PolymorphicForeignKey(model:Type[Model], relationship_field:PolymorphicFKRelationship):
    """
    A polymorphic foreign key that can be used to create a polymorphic relationship
    between two models. Returns a Django ForeignKey.
    """

    kwargs = dict(
        to=model,
        on_delete=relationship_field.on_delete,
        null=True,
        blank=True,
        related_name=relationship_field.related_name,
    )

    fk = PolymorphicFK(**kwargs) # type: ignore
    relationship_field._add_related_fk(fk)
    fk.relationship_field = relationship_field # type: ignore
    return fk
