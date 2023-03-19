from account.models import User, EmailAddress, RedeemableKey

from core.lib import TestCase

class RedeemableKeyTestCase(TestCase):

    def create_user(self):
        user_args = self.get_user_args()
        return User.objects.create_user(**user_args)

    def create_email_address(self, user):
        return EmailAddress.objects.create(emailable=user, email="testemail@example.com")

    def create_redeemable_key(self, redeemable):
        return RedeemableKey.objects.create(redeemable=redeemable)

    def test_create_redeemable_key(self):
        user = self.create_user()
        email_address = self.create_email_address(user)
        redeemable_key = self.create_redeemable_key(email_address)

        self.assertEqual(redeemable_key.redeemable, email_address)
        self.assertFalse(redeemable_key.is_redeemed)
        self.assertIsNone(redeemable_key.redeemed_at)
        self.assertIsNotNone(redeemable_key.expires_at)

    def test_expire_redeemable_key(self):
        user = self.create_user()
        email_address = self.create_email_address(user)
        redeemable_key = self.create_redeemable_key(email_address)

        redeemable_key.expire()
        self.assertTrue(redeemable_key.is_expired)

    def test_redeem_redeemable_key(self):
        user = self.create_user()
        email_address = self.create_email_address(user)
        redeemable_key = self.create_redeemable_key(email_address)

        class RedeemableEmail(IsRedeemable):
            def get_is_redeemed(self) -> bool:
                return self.is_verified

            def is_valid_redemption(self, user: Optional[User] = None, *args, **kwargs) -> bool:
                return True

            def redeem(self, user: Optional[User] = None, *args, **kwargs) -> bool:
                self.is_verified = True
                self.save()
                return True

        email_address.__class__ = RedeemableEmail

        redeemable_key.stage_redemption(user=user)
        result = redeemable_key.redeem()
        email_address.refresh_from_db()

        self.assertTrue(result)
        self.assertTrue(redeemable_key.is_redeemed)
        self.assertIsNotNone(redeemable_key.redeemed_at)
        self.assertTrue(email_address.is_verified)
