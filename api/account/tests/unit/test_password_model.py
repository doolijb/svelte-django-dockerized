from django.conf import settings
from django.core.exceptions import ValidationError
from account.models import User, Password
from typing import cast
from rest_framework.response import Response

from core.lib import TestCase


class PasswordModelTestCase(TestCase):
    """
    Test that the password model works correctly.  Also stress tests the polymorphic foreign key mixin.
    """

    def test_create_password_with_user_success(self):
        """
        Tests a successful password creation.
        """
        user_args = self.get_user_args()
        user = User.objects.create_user(
            email=user_args['email'],
            raw_password=user_args['raw_password'],
            first_name=user_args['first_name'],
            last_name=user_args['last_name'],
        )
        user = User.objects.get(id=user.id)
        password = cast(Password, user.password)
        password.save()
        self.assertIsInstance(password, Password)
        self.assertIsNotNone(password.id)
        self.assertIsNotNone(password.hash)
        self.assertEqual(password.protected, user)
        self.assertEqual(user.id, cast(User, password.protected).id)
        self.assertEqual(user.id, cast(User, password.protected_user).id)
        self.assertEqual(user.id, password.protected_user_id) # TODO - needing typing for polymorphic foreign key mixin
        self.assertTrue(password.validate(password=user_args['raw_password']))

    def test_create_bad_password_with_user_fail(self):
        """
        Tests a failed password creation with a common password.
        """
        user_args = self.get_user_args()
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email=user_args['email'],
                raw_password="123password",
                first_name=user_args['first_name'],
                last_name=user_args['last_name'],
            )

    def test_create_password_without_protected_fails(self):
        """
        Tests a failed password creation without a protected object.
        """
        with self.assertRaises(TypeError):
            Password.objects.create(raw_password=self.fake.password()) # type: ignore

    def test_create_password_with_bad_protected_is_not_model_fails(self):
        """
        Tests a failed password creation with a protected object that is not a user.
        """
        with self.assertRaises(ValueError):
            Password.objects.create(raw_password=self.fake.password(), protected=self.fake.email())

    def test_soft_delete_password_for_user_success(self):
        """
        Tests a successful password deletion.
        """
        user_args = self.get_user_args()
        user = User.objects.create_user(
            email=user_args['email'],
            raw_password=user_args['raw_password'],
            first_name=user_args['first_name'],
            last_name=user_args['last_name'],
        )
        password = cast(Password, user.password)
        password.delete()
        user.refresh_from_db()
        self.assertIsNotNone(password.deleted_at)
        self.assertIsNone(user.password)
