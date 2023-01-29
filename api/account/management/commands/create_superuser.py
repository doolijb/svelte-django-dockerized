from django.contrib.auth.management.commands.createsuperuser import (
    Command as SuperUserCommand,
)
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class Command(SuperUserCommand):
    """
    Creates a superuser.

    Overrides the built-in command.
    """

    def handle(self, *args, **kwargs):
        """
        Creates a superuser.

        Overrides the built-in command.
        """

        # Username
        username = input('Username: ') if settings.ENABLE_USERNAMES else ''

        # Email
        email = input('Email: ')
        if not username:
            username = email

        # Password
        password = input('Password: ')

        # Create the user
        user = User.objects.create_superuser()
