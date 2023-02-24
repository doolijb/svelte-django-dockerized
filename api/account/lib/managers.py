from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction
from django.db.models import Manager
from core.lib.manager_mixins import ManagesSoftDeletables
from typing import Optional, TYPE_CHECKING
from account.lib.utils import is_hashed
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from account.lib.model_mixins import IsPasswordProtected
from account.lib.utils import normalize_email
from django.db.models import Q

if TYPE_CHECKING:
    from account.models import User

class UserManager(BaseUserManager, ManagesSoftDeletables):
    """
    Custom user model manager where email is the unique identifiers
    """

    def create_user(self, username:Optional[str]=None, email:Optional[str]=None, is_verified=False, password:Optional[str]=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """

        with transaction.atomic():
            user = self.model(**extra_fields)
            if username:
                user.username = username
            user.save(using=self._db)
            if email:
                user.email_addresses.create(email=email, emailable=user, is_verified=is_verified)
            if password:
                user.passwords.create(protected=user, raw_password=password)
        return user

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
        return self.model.email_addresses.through.objects.get(
            email=normalize_email(email),
            emailable_type=self.model._meta.label
        )

    def get_by_natural_key(self, username:str):
        """Returns a user for a username"""
        return self.get(username=username)


class PasswordManager(Manager, ManagesSoftDeletables):
    """
    Custom manager for the Password model.
    """

    use_for_related_fields = True

    def create(self, protected: "IsPasswordProtected", raw_password: str, **kwargs):
        """
        Create and save a password with a given protected model instance and a hashable raw password.
        """
        assert not is_hashed(raw_password), "Raw password must not be already hashed"
        validate_password(raw_password)
        hash = make_password(raw_password)
        instance = self.model(
            protected=protected,
            hash=hash,
            **kwargs,
        )
        instance.save(using=self._db)
        return instance

    def get_by_natural_key(self, password):
        return self.get(**{password: password})


class EmailAddressManager(Manager):
    """
    Custom manager for the EmailAddress model.

    @method create: Create and save an EmailAddress with the given email and user.
    @method normalize_email: Normalize the email address by lowercasing the domain part of the email
    @method primary: Return the primary email address for a user.
    """

    use_for_related_fields = True

    def create(self, emailable, email, is_primary=False, is_verified=False):
        """
        Create and save an EmailAddress with the given email and user.
        """
        email_address = self.model(
            emailable=emailable,
            email=normalize_email(email),
            is_primary=is_primary,
            is_verified=is_verified,
        )
        email_address.save(using=self._db)

    def primary(self):
        """
        Return the primary email address for a user.
        """
        return self.get(is_primary=True)

    def get_by_natural_key(self, email):
        return self.get(**{email: email})


class RedeemableKeyManager(Manager):
    """
    Custom manager for the RedeemableKey model.
    """

    def create(self, user, redeemable, date_expires=None):
        """
        Create and save a RedeemableKey with the given user and redeemable.
        """
        redeemable_key = self.model(
            user=user,
            redeemable=redeemable,
            date_expires=date_expires,
        )
        redeemable_key.save(using=self._db)
        return

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

    def email_addresses(self):
        """
        Return a queryset of redeemable keys for email addresses.
        """
        return self.filter(redeemable_content_type__model='emailaddress')
