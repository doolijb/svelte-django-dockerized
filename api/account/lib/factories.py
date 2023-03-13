import random

import factory
import factory.django
from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from faker import Faker

from account.lib.managers import EmailAddressManager

###
# Models
###

User = get_user_model()
EmailAddress = apps.get_model('account', 'EmailAddress')

###
# Factories
###

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory for the User model.
    """

    class Meta:
        model = User

    username = factory.Faker('user_name') if settings.ENABLE_USERNAMES else ''
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.PostGenerationMethodCall('set_password', 'password')

    @factory.post_generation
    def email_addresses(user, create, extracted):
        """
        Create email addresses for the user.
        """
        if not create:
            return
        # Get extracted email addresses or create a random number of email addresses
        email_addresses = extracted or [{}] * int(fake.pyint(min_value=1, max_value=3))

        # Keep track of whether a primary email address has been created yet
        has_primary = False

        # Create the email addresses
        for email_address in email_addresses:
            email_address['emailable'] = user
            email_address.setdefault('email', factory.Faker('email'))
            email_address.setdefault('is_primary', (not has_primary))
            has_primary: bool = (
                has_primary if has_primary else email_address['is_primary']
            )

            # If we have more than one email, then the primary email is verified
            if len(email_addresses) > 1 and not has_primary:
                email_address.setdefault('is_verified', True)
            EmailAddressFactory(**email_address)


class SuperUserFactory(UserFactory):
    is_staff = True
    is_superuser = True


class EmailAddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EmailAddress

    email = factory.Faker('email')
    # Verified 75% of the time by default
    is_verified = bool(int(random.random() <= 0.75))
