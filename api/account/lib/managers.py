import logging
from django.contrib.auth.base_user import BaseUserManager
from core.lib import ManagesPolymorphicRelationships, ManagesSoftDeletables, ManagesTimestamps
from typing import Optional, TYPE_CHECKING
from account.lib.utils import validate_password, normalize_email
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.conf import settings
from django.db.models import Manager
from account.lib.querysets import UserQueryset, PasswordQuerySet, EmailAddressQuerySet, RedeemableKeyQuerySet


if TYPE_CHECKING:
    from account.models import User
    from account.lib.model_mixins import IsPasswordProtected


class UserManager(ManagesSoftDeletables, ManagesTimestamps, BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    """

    use_for_related_fields = True

    def get_queryset(self):
        return UserQueryset(self.model, using=self._db)

    def create_user(self, email:str, username:Optional[str]=None, is_verified=False, raw_password:Optional[str]=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """

        email = normalize_email(email)
        if settings.ENABLE_USERNAMES:
            username = username or email
        elif username:
            logging.warning("Username was provided but ENABLE_USERNAMES is False. Ignoring username.")
        user = super().create(username=username, **extra_fields)
        if email:
            from account.models import EmailAddress
            user.email_addresses.create(
                email=normalize_email(email),
                is_verified=is_verified,
                emailable=user,
            )

        if raw_password:
            from account.models import Password
            Password.objects.create(
                protected=user,
                raw_password=raw_password,
            )
        return user

    create = create_user

    def create_superuser(self, *args, **kwargs):
        """
        Create and save a SuperUser with the given email and password.
        """
        user = self.create_user(*args, **kwargs)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def get_by_primary_email(self, email:str) -> "User":
        """Returns a user for a primary email address"""
        # Query email addresses for the given email and emailable type
        return self.model.email_addresses.filter(email=email).primary().first().emailable_user

    def get_by_natural_key(self, username:str):
        """Returns a user for a username"""
        return self.get(username=username)


class PasswordManager(ManagesSoftDeletables, ManagesTimestamps, ManagesPolymorphicRelationships, Manager):
    """
    Custom manager for the Password model.
    """

    use_for_related_fields = True

    def get_queryset(self):
        return PasswordQuerySet(self.model, using=self._db)

    def create(self, protected:"IsPasswordProtected", raw_password: str, validate=True, **kwargs):
        """
        Create and save a password with a given protected model instance and a hashable raw password.
        """
        if validate:
            validate_password(raw_password)
        kwargs['hash'] = make_password(raw_password)
        password = super().create(protected=protected, **kwargs)
        return password


class EmailAddressManager(ManagesTimestamps, ManagesPolymorphicRelationships, Manager):
    """
    Custom manager for the EmailAddress model.
    """

    use_for_related_fields = True

    def get_queryset(self):
        return EmailAddressQuerySet(self.model, using=self._db)

    def create(self, is_verified=False, **kwargs):
        # Check if the user already has a primary email address

        verified_at = timezone.now() if is_verified else None
        email_address = super().create(verified_at=verified_at, **kwargs)

        # Set the first email address as primary if the user doesn't have a primary email address
        if not email_address.emailable_user.email_addresses.primary().exists():
            email_address.set_primary()

        return email_address

    def primary(self):
        return self.get_queryset().primary()

    def get_by_natural_key(self, email:str):
        """Returns an email address for a given email"""
        return self.get_queryset().get(email=email)


class RedeemableKeyManager(ManagesTimestamps, ManagesPolymorphicRelationships, Manager):
    """
    Custom manager for the RedeemableKey model.
    """

    use_for_related_fields = True

    def get_queryset(self):
        return RedeemableKeyQuerySet(self.model, using=self._db)

    def redeem(self, uuid, user, *args, **kwargs):
        """
        Redeem a redeemable key.
        """
        redeemable_key = self.get(uuid=uuid)
        redeemable_key.redeem(user, *args, **kwargs)
        return redeemable_key
