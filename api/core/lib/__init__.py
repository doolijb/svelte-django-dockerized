import sys
TESTING = sys.argv[1:2] == ['test']

from .polymorphic_fk import *
from .manager_mixins import *
from .model_mixins import *
from .pagination import *
from .views import *

if TESTING:
    from .tests import *
