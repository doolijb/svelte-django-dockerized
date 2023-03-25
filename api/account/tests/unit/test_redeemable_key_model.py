from datetime import timedelta
from account.models import User, EmailAddress, RedeemableKey
from django.utils import timezone

from core.lib import TestCase

class RedeemableKeyTestCase(TestCase):

    def test_redeem_redeemable_key_for_user(self):
        user_args = self.get_user_args()
        user = User.objects.create_user(**user_args)
        redeemable_key = RedeemableKey.objects.create(redeemable=user)
        self.assertEqual(redeemable_key.redeemable, user)
        self.assertFalse(redeemable_key.is_redeemed)
        self.assertIsNone(redeemable_key.redeemed_at)

    def test_create_redeemable_key_for_email_address(self):
        user_args = self.get_user_args()
        user = User.objects.create_user(**user_args)
        email_address = user.primary_email_address
        redeemable_key = RedeemableKey.objects.create(
            redeemable=email_address,
            expires_at=timezone.now() + timedelta(days=1)
            )
        self.assertEqual(redeemable_key.redeemable, email_address)
        self.assertFalse(redeemable_key.is_redeemed)
        self.assertIsNone(redeemable_key.redeemed_at)
        self.assertIsNotNone(redeemable_key.expires_at)
        self.assertFalse(redeemable_key.is_expired)

    def test_expire_redeemable_key(self):
        user_args = self.get_user_args()
        user = User.objects.create_user(**user_args)
        email_address = user.primary_email_address
        redeemable_key = RedeemableKey.objects.create(redeemable=email_address)

        redeemable_key.expire()
        self.assertTrue(redeemable_key.is_expired)

        with self.assertRaises(Exception):
            redeemable_key.redeem()
