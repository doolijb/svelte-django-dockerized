from django.core.management.base import BaseCommand, CommandError
from ...factories import UserFactory
from django.db.transaction import atomic


class Command(BaseCommand):
    """
    Seeds the database with random users.
    """

    help = 'Seeds the database with random users.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-c',
            '--count',
            type=int,
            default=10,
            help='The number of users to create.',
        )

    def handle(self, *args, **options):

        # Arguments
        count = options['count']

        self.stdout.write(f'Creating {count} random users...')

        with atomic():

            # Create users
            for _ in range(count):
                UserFactory()

        self.stdout.write(self.style.SUCCESS('Done.'))
