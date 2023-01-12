"""
Custom model managers for the account app.
"""

from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction
from django.db.models import Manager


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    """

    def create_user(self, email, is_verified=False, password=None):
        """
        Create and save a User with the given email and password.
        """

        # Transaction atomic is used to ensure that the user and email address
        # are created in the same transaction. If the email address creation
        # fails, the user will not be created.
        with transaction.atomic():
            user = self.model()
            user.set_password(password)
            user.save(using=self._db)
            user.email_address_set.create(
                email=email, is_primary=True, is_verified=is_verified
            )

        return user

    def create_superuser(self, *args, **kwargs):
        """
        Create and save a SuperUser with the given email and password.
        """
        user = self.create_user(*args, **kwargs)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def get_by_primary_email(self, email):
        """Returns a user for a primary email address"""
        EmailAddress = self.model.email_address_set.related.model
        return EmailAddress.objects.get_by_natural_key(email).user


class EmailAddressManager(Manager):
    """
    Custom manager for the EmailAddress model.

    @method create: Create and save an EmailAddress with the given email and user.
    @method normalize_email: Normalize the email address by lowercasing the domain part of the email
    @method primary: Return the primary email address for a user.
    """

    def create(self, user, email, is_primary=False, is_verified=False):
        """
        Create and save an EmailAddress with the given email and user.
        """
        email_address = self.model(
            user=user,
            email=self.normalize_email(email),
            is_primary=is_primary,
            is_verified=is_verified,
        )
        email_address.save(using=self._db)

    @staticmethod
    def normalize_email(email):
        """
        Normalize the email address by lowercasing the domain part of the email
        """
        return email.lower().strip()

    def primary(self):
        """
        Return the primary email address for a user.
        """
        # Raise exception if not called from user instance relation.
        if "user" not in self.query.fields:  # type: ignore
            raise ValueError("Must be called on a user instance realtion.")

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

    def all(self):
        """
        Return a queryset of redeemable keys for any redeemable.
        """
        return super().filter(expired_at__isnull=True)

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
        return self.filter(redeemable_content_type__model="emailaddress")
