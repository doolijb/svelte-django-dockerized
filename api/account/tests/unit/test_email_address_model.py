from django.forms import ValidationError
from account.models import User, EmailAddress

from core.lib import TestCase


class EmailAddressModelTestCase(TestCase):

    def test_create_email_address(self):
        user_args = self.get_user_args()
        user = User.objects.create_user(**user_args)
        email_address = user.primary_email_address
        self.assertEqual(email_address.email, user_args.get("email"))
        self.assertFalse(email_address.is_verified)
        self.assertTrue(email_address.is_primary)

    def test_primary_email_address(self):
        user_args = self.get_user_args()
        user = User.objects.create_user(**user_args)
        email_address1 = user.primary_email_address
        email_address2 = EmailAddress.objects.create(emailable=user, email="testemail2@example.com")

        self.assertTrue(email_address1.is_primary)
        self.assertFalse(email_address2.is_primary)

        email_address2.set_primary()

        # This instance is stale, so we need to refresh it from the database
        email_address1.refresh_from_db()

        self.assertFalse(email_address1.is_primary)
        self.assertTrue(email_address2.is_primary)

    def test_cannot_delete_primary_email_address(self):
        user_args = self.get_user_args()
        user = User.objects.create_user(**user_args)
        email_address = user.primary_email_address

        with self.assertRaises(ValidationError):
            email_address.delete()

    def test_cannot_delete_last_email_address(self):
        user_args = self.get_user_args()
        user = User.objects.create_user(**user_args)
        email_address = user.primary_email_address

        email_address2 = EmailAddress.objects.create(emailable=user, email="testemail2@example.com")

        email_address2.delete()

        with self.assertRaises(ValidationError):
            email_address.delete()

    def test_email_address_verification(self):
        user_args = self.get_user_args()
        user = User.objects.create_user(**user_args)
        email_address = user.primary_email_address
        self.assertFalse(email_address.is_verified)

        email_address.redeem(user=user)
        email_address.refresh_from_db()

        self.assertTrue(email_address.is_verified)

    def test_different_email_address_query_methods(self):
        user_args = self.get_user_args()
        user = User.objects.create_user(**user_args)

        email_address = user.primary_email_address

        # Check typical get methods
        self.assertEqual(email_address, EmailAddress.objects.get(pk=email_address.pk))
        self.assertEqual(email_address, EmailAddress.objects.get(email=email_address.email))
        # Test managers get_by_natural_key method
        self.assertEqual(email_address, EmailAddress.objects.get_by_natural_key(email_address.email))
        # Test querysets get_by_natural_key method
        self.assertEqual(email_address, EmailAddress.objects.all().get_by_natural_key(email_address.email))
        # Test managers primary method
        self.assertEqual(email_address, EmailAddress.objects.primary().filter(emailable=user).get())
        # Test querysets primary method
        self.assertEqual(email_address, EmailAddress.objects.filter(emailable=user).primary().get())
