# Import django logger
from logging import getLogger
from django.conf import settings
from account.models import User, EmailAddress
from typing import cast
from rest_framework.response import Response

from core.lib.tests import ApiTestCase

logger = getLogger(__name__)


class RegisterTestCase(ApiTestCase):

    url_name = "account:register-list"

    def test_register_success(self):
        """
        Tests a successful registration.
        """

        data = {
            "email": 'jack.sparrow@example.com',
            "username": 'jack.sparrow',
            "first_name": 'jack',
            "last_name": 'sparrow',
            "password": '$allyS@lly',
            "password_confirm": '$allyS@lly'
        }

        if not settings.ENABLE_USERNAMES:
            del data["username"]

        response = cast(Response, self.client.post(self.url, data))

        self.assertEqual(response.status_code, 201, response.data)
        user = User.objects.filter(email_addresses__email=data["email"]).first()
        if not user:
            self.fail("User not created.")
        email = user.email_addresses.filter(email=data["email"]).first()
        if not email:
            self.fail("Email not created.")
        self.assertEqual(user.first_name, data["first_name"])
        self.assertEqual(user.last_name, data["last_name"])
        self.assertTrue(user.check_password(data["password"]))
        self.assertTrue(user.email_addresses.filter(email=data["email"]).exists())
        self.assertTrue(user.email_addresses.filter(email=data["email"]).first().is_primary)
        try:
            user.check_password(data["password"])
        except Exception as e:
            self.fail("Password not set.")


    def test_register_fail_with_common_password(self):
        """
        Tests a successful registration.
        """
        data = {
            "email": 'jack.mack@example.com',
            "username": 'jack.mack',
            "first_name": 'jack',
            "last_name": 'mack',
            "password": '123password',
            "password_confirm": '123password'
        }

        if not settings.ENABLE_USERNAMES:
            del data["username"]

        response = cast(Response, self.client.post(self.url, data))

        self.assertEqual(response.status_code, 400, response.data)
        self.assertTrue(response.data and 'password' in response.data.keys(), response.data)
        user = User.objects.filter(email_addresses__email=data["email"]).first()
        email = EmailAddress.objects.filter(email=data["email"]).first()
        if user:
            self.fail("User was created during bad request.")
        if email:
            self.fail("Email was created during bad request.")


    def test_register_fail_with_bad_password_conf(self):
        """
        Tests a failed registration with a bad password.
        """
        data = {
            "email": 'jack.charltan@example.com',
            "username": 'jack.charltan',
            "first_name": 'jack',
            "last_name": 'sparrow',
            "password": '$allyS@lly',
            "password_confirm": '$allyS@lly2',
        }

        if not settings.ENABLE_USERNAMES:
            del data["username"]

        response = cast(Response, self.client.post(self.url, data))

        self.assertEqual(response.status_code, 400, response.data)
        self.assertTrue('password_confirm' in response.data.keys(), response.data)
