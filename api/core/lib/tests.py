from django.urls import reverse
from account.lib.factories import UserFactory
from django.test.client import Client as BaseClient
from rest_framework.response import Response
from typing import cast
from rest_framework.test import APITestCase as BaseAPITestCase, APIRequestFactory


class ApiTestCase(BaseAPITestCase):
    """
    Base class for API test cases.

    This class sets up the request factory and provides some helper methods.

    To use this class, set the url_name attribute in the child class.

    Example:
        class VerifyTokenApiTestCase(BaseApiTestCase):
            url_name = "tokens-verify"

    Helper Methods:
        login: Logs in the user in, returning a token pair.
        get_url_pattern: Gets the url pattern for a url name.
        get_url: Gets the url for a url name.
        get_view: Gets the view for a url name.

    @see https://www.django-rest-framework.org/api-guide/testing/
    """

    # Set these in the child class
    url_name = None  # The name of the url pattern relative to the app
    user_password = '123password'  # The unhashed password for the user
    user_args = {  # The arguments to pass to the user factory
        'email_addresses': [{'is_primary': True, 'is_verified': True}],
        'password': user_password,
        'username': 'testuser', 'first_name': 'Test', 'last_name': 'User',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set up the test case
        self.url_pattern = self.setUp()

        # Setup the request factory
        self.factory = APIRequestFactory()
        self.url = reverse(self.url_name)

    def get_view(self, url_pattern):
        """
        Gets the view for a url name.
        """
        return url_pattern.callback.cls.as_view()

    def setUp(self):
        """
        Sets up the test case.
        """
        # self.user = UserFactory.create(**self.user_args)

    def tearDown(self) -> None:
        return super().tearDown()

    # def login(self, username=None, password=None):
    #     """
    #     Logs in the user in, returning a token pair.
    #     """

    #     url_pattern = self.get_url_pattern('api:account:login-list')
    #     url = self.get_url(url_pattern)
    #     view = self.get_view(url_pattern)

    #     # Make request
    #     request = self.factory.post(
    #         url,
    #         data={
    #             'username': username or self.user.username,
    #             'password': password or self.user_password,
    #         },
    #     )

    #     # Send post request
    #     response = view(request)

    #     return response
