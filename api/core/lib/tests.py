from django.test import TestCase
from account.factories import UserFactory
from rest_framework.test import APIRequestFactory
from ..urls import urlpatterns


class BaseApiTestCase(TestCase):
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
    user_password = "123password"  # The unhashed password for the user
    user_args = {  # The arguments to pass to the user factory
        "email_addresses": [{"is_primary": True, "is_verified": True}],
        "password": user_password,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set up the test case
        self.url_pattern = self.setUp()

        # Setup the request factory
        self.factory = APIRequestFactory()

        self.url_pattern = self.get_url_pattern(self.url_name)
        self.url = self.get_url(self.url_pattern)
        self.view = self.get_view(self.url_pattern)

    def get_url_pattern(self, url_name):
        """
        Gets the url pattern for a url name.
        """
        for url_pattern in urlpatterns:
            if url_pattern.name == url_name:  # type: ignore
                return url_pattern

        raise Exception(f"Url pattern '{url_name}' not found.")

    def get_url(self, url_pattern):
        """
        Gets the url for a url name.
        """
        return url_pattern.pattern.regex.pattern

    def get_view(self, url_pattern):
        """
        Gets the view for a url name.
        """
        return url_pattern.callback.cls.as_view()

    def setUp(self):
        """
        Sets up the test case.
        """
        self.user = UserFactory.create(**self.user_args)

    def login(self, username=None, password=None):
        """
        Logs in the user in, returning a token pair.
        """

        url_pattern = self.get_url_pattern("account:tokens")
        url = self.get_url(url_pattern)
        view = self.get_view(url_pattern)

        # Make request
        request = self.factory.post(
            url,
            data={
                "username": username or self.user.username,
                "password": password or self.user_password,
            },
        )

        # Send post request
        response = view(request)

        return response
