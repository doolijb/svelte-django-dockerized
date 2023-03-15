import logging
from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction
from django.db.models import Manager, Model
from core.lib.manager_mixins import ManagesPolymorphicRelationships, ManagesSoftDeletables, ManagesTimestamps
from typing import Optional, TYPE_CHECKING
from account.lib.utils import validate_password, normalize_email
from django.contrib.auth.hashers import make_password
from account.lib.model_mixins import IsEmailable, IsPasswordProtected
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

if TYPE_CHECKING:
    from account.models import User

class UserManager(ManagesSoftDeletables, ManagesTimestamps, BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    """

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
            EmailAddress.objects.create(
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

    def create(self, protected:IsPasswordProtected, raw_password: str, validate=True, **kwargs):
        """
        Create and save a password with a given protected model instance and a hashable raw password.
        """
        if validate:
            validate_password(raw_password)
        kwargs['hash'] = make_password(raw_password)
        password = super().create(protected=protected, **kwargs)
        return password

    def get_by_natural_key(self, password):
        return self.get(**{password: password})


class EmailAddressManager(ManagesTimestamps, ManagesPolymorphicRelationships, Manager):
    """
    Custom manager for the EmailAddress model.

    @method create: Create and save an EmailAddress with the given email and user.
    @method normalize_email: Normalize the email address by lowercasing the domain part of the email
    @method primary: Return the primary email address for a user.
    """

    use_for_related_fields = True

    def create(
            self,
            emailable:IsEmailable,
            email:str,
            is_verified=False,
            **kwargs,
        ):
        """
        Create and save an EmailAddress with the given email and user.

        @param emailable: The user, or IsEmailable to associate with the email address.
        @param email: The email address.
        @param is_primary: Whether or not the email address is the primary email address for the user.
        @param verified_at: The date and time the email address was verified.
        @param is_verified: Whether or not the email address is verified, if true, set verified_at.
        """

        verified_at = kwargs.get('verified_at')
        if type(is_verified) is bool and verified_at:
            raise ValueError("Cannot set verified_at and is_verified at the same time, simply use is_verified instead.")
        elif is_verified:
            verified_at = timezone.now()

        if 'is_primary' in kwargs.keys():
            raise ValueError("Cannot set is_primary directly, field is set automatically on creation.")

        return super().create(
            emailable=emailable,
            email=normalize_email(email),
            is_primary=self.get_queryset().filter(emailable=emailable, is_primary=True).first() is None,
            verified_at=verified_at,
        )

    def primary(self):
        """
        Return the primary email address for a user.
        """
        return self.get(is_primary=True)

    def get_by_natural_key(self, email):
        return self.get(**{email: email})


class RedeemableKeyManager(ManagesTimestamps, ManagesPolymorphicRelationships, Manager):
    """
    Custom manager for the RedeemableKey model.
    """

    def redeem(self, uuid, user, commit=True):
        """
        Redeem a redeemable key.
        """
        redeemable_key = self.get(uuid=uuid)
        redeemable_key.redeem(user, commit=commit)
        return redeemable_key

    ###
    # QuerySet methods
    ###

    def any(self):
        """
        Return a queryset of redeemable keys for any redeemable.
        """
        return super().all()

    def redeemable(self):
        """
        Return a queryset of redeemable keys for any redeemable.
        """
        return super().filter(expired_at__isnull=True, redeemed_at__isnull=True)

    def expired(self):
        """
        Return a queryset of expired redeemable keys.
        """
        return super().filter(expired_at__isnull=False)

    def redeemed(self):
        """
        Return a queryset of redeemed redeemable keys.
        """
        return super().filter(redeemed_at__isnull=False)
