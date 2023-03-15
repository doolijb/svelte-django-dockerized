# Import django logger
from logging import getLogger
from django.conf import settings
from account.models import User
from typing import cast
from rest_framework.response import Response

from core.lib.tests import ApiTestCase

logger = getLogger(__name__)
