# Import django logger
from logging import getLogger

from core.lib.tests import BaseApiTestCase

logger = getLogger(__name__)


class TokenObtainPairApiTestCase(BaseApiTestCase):
    url_name = 'tokens'

    def test_post_200_for_valid_login(self):
        """
        Tests that we can get a token pair.
        """

        # If settings.ENABLE_USERNAMES is True, then the username field is required

        response = self.login()

        # Check response
        self.assertEqual(response.status_code, 200)

        # Check response headers
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_post_401_for_bad_username(self):
        """
        Tests that we get a 401 response if we use a bad username.
        """

        # Send request
        response = self.login(username='bad_username')

        # Check response
        self.assertEqual(response.status_code, 401)
        self.assertNotIn('access', response.data)  # type: ignore
        self.assertNotIn('refresh', response.data)  # type: ignore


class RefreshTokenApiTestCase(BaseApiTestCase):
    url_name = 'tokens-refresh'

    def test_post_200_for_valid_refresh_token(self):
        """
        Test that we can get a new access token with a refresh token.
        """

        # Get the token pair
        login_response = self.login()

        # Make request
        request = self.factory.post(
            self.url, data={'refresh': login_response.data['refresh']}  # type: ignore
        )

        # Send request
        response = self.view(request)

        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertNotIn('refresh', response.data)

    def test_post_401_for_bad_refresh_token(self):
        """
        Test that we get a 401 response if we use a bad refresh token.
        """

        # Make request
        request = self.factory.post(self.url, data={'refresh': 'bad_refresh'})
        response = self.view(request)

        # Check response
        self.assertEqual(response.status_code, 401)


class VerifyTokenApiTestCase(BaseApiTestCase):

    url_name = 'tokens-verify'

    def test_post_200_for_valid_access_token(self):
        """
        Test that we can verify an access token.
        """
        # Get the token pair
        login_response = self.login()

        # Make request for access token
        request = self.factory.post(
            self.url,
            data={'token': login_response.data.get('access', '')},  # type: ignore
        )

        # Send request
        response = self.view(request)

        # Check response
        self.assertEqual(response.status_code, 200)

    def test_post_200_for_valid_refresh_token(self):
        """
        Test that we can verify a refresh token.
        """
        # Get the token pair
        login_response = self.login()

        # Make request for refresh token
        request = self.factory.post(
            self.url,
            data={'token': login_response.data.get('refresh', '')},  # type: ignore
        )

        # Send request
        response = self.view(request)

        # Check response
        self.assertEqual(response.status_code, 200)

    def test_post_401_for_bad_token(self):
        """
        Test that we get a 401 response if we use a bad token.
        """

        # Make request
        request = self.factory.post(self.url, data={'token': 'bad_token'})

        # Send request
        response = self.view(request)

        # Check response
        self.assertEqual(response.status_code, 401)


# # Test the CurrentUserApiView
# class CurrentUserApiTestCase(BaseApiTestCase):

#     url_name = "users-current"

#     def test_get(self):
#         """
#         Tests the GET method.
#         """

#         # Login
#         login_response = self.login()

#         # Make request
#         request = self.factory.get(self.url)
#         request.META["HTTP_AUTHORIZATION"] = f"Bearer {login_response.data['access']}"  # type: ignore

#         # Send request
#         response = self.view(request)

#         # Check response
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(UUID(response.data["id"]), self.user.id)
#         self.assertEqual(response.data["username"], self.user.username)
#         self.assertEqual(response.data["first_name"], self.user.first_name)
#         self.assertEqual(response.data["last_name"], self.user.last_name)
#         self.assertIn("email_addresses", response.data)
#         self.assertEqual(
#             len(response.data["email_addresses"]), self.user.email_addresses.count()
#         )
#         self.assertEqual(
#             UUID(response.data["email_addresses"][0]["id"]),
#             self.user.email_addresses.all().first().id,
#         )
#         self.assertEqual(
#             response.data["email_addresses"][0]["email"],
#             self.user.email_addresses.all().first().email,
#         )
#         self.assertEqual(
#             response.data["email_addresses"][0]["is_primary"],
#             self.user.email_addresses.all().first().is_primary,
#         )
#         self.assertEqual(
#             response.data["email_addresses"][0]["is_verified"],
#             self.user.email_addresses.all().first().is_verified,
#         )

#         # Check that the password is not in the response
#         self.assertNotIn("password", response.data)


# class EmailAddressesesApiTestCase(BaseApiTestCase):

#     url_name = "email_addresses"

#     def test_get(self):
#         """
#         Tests the GET method.
#         """

#         # Login
#         login_response = self.login()

#         # Make request
#         request = self.factory.get(self.url)
#         request.META["HTTP_AUTHORIZATION"] = f"Bearer {login_response.data['access']}"  # type: ignore

#         # Send request
#         response = self.view(request)

#         # Check response
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.data), self.user.email_addresses.count())
#         self.assertEqual(
#             UUID(response.data[0]["id"]), self.user.email_addresses.all().first().id
#         )
#         self.assertEqual(
#             response.data[0]["email"], self.user.email_addresses.all().first().email
#         )
#         self.assertEqual(
#             response.data[0]["is_primary"],
#             self.user.email_addresses.all().first().is_primary,
#         )
#         self.assertEqual(
#             response.data[0]["is_verified"],
#             self.user.email_addresses.all().first().is_verified,
#         )

# def test_post(self):
#     """
#     Tests the POST method.
#     """

#     # Login
#     login_response = self.login()

#     # Make request
#     request = self.factory.post(self.url, data={
#         "email": ""
