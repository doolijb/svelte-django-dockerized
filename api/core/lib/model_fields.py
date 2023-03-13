from typing import Any, Optional
from django.db.models import ForeignKey, CASCADE, PROTECT, SET_NULL, SET_DEFAULT, SET


class PolymorphicFKRelationship():
    """
    Defines a relationship between a group of polymorphic foreign keys
    """

    populated_fk: Optional[ForeignKey] = None
    populated_type: Optional[Any] = None
    _related_fks = []

    def __init__(self, null: bool, on_delete: Any, related_name: str):
        self.null = null
        self.on_delete = on_delete
        self.related_name = related_name

    def __repr__(self) -> str:
        return f"PolymorphicRelationship(null={self.null}, on_delete={self.on_delete}, related_name='{self.related_name}')"

    def __get__(self, instance, owner):
        if self.populated_fk is not None:
            return self.populated_fk.__get__(instance, owner)
        else:
            return None

    def __set__(self, instance, value):
        for fk in instance._meta.fields:
            if isinstance(fk, PolymorphicFK) and fk.relationship_field == self:
                if value is None and self.null:
                    fk.__set__(instance, None)
                    self._set_populated_to_none()
                elif isinstance(value, fk.related_model):
                    fk.__set__(instance, value)
                    self._set_populated(fk)
                elif value is None:
                    if not self.null:
                        raise ValueError(f"PolymorphicFKRelationship {self.related_name} cannot be empty")
                    self._set_populated_to_none()
                else:
                    raise ValueError(f"Invalid value {value} for PolymorphicFK")

    def _set_populated_to_none(self):
        self.populated_fk = None
        self.populated_type = None

    def _set_populated(self, fk: "PolymorphicFK"):
        self.populated_fk = fk
        self.populated_type = fk.related_model

    def _add_related_fk(self, fk: "PolymorphicFK"):
        """
        Add a related foreign key to the relationship
        """
        for existing_fk in self._related_fks:
            if existing_fk == fk:
                raise ValueError(f"Model {fk.model.__name__} for field {fk.name} already exists in {existing_fk.name} for relationship {self.related_name}")
        self._related_fks.append(fk)

    def get_field_for_model(self, model: Any):
        """
        Return the PolymorphicFK for a given model
        """
        for fk in self._related_fks:
            if fk.related_model == model:
                return fk
        return None

    def delete(self):
        """
        Delete the relationship by setting all related foreign keys to None
        """
        for fk in self._related_fks:
            setattr(fk, fk.name, None)


class PolymorphicFK(ForeignKey):
    """
    A polymorphic foreign key that can be used to create a polymorphic relationship.
    This should not be used directly. Instead, use the PolymorphicFK function. This is because
    child classes inherit parent constructor arguments, which we do not want.
    """
    relationship_field:PolymorphicFKRelationship

    def __set__(self, instance, value):
        if value is None:
            self.relationship_field._set_populated_to_none()

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return super().__get__(instance, owner)


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
