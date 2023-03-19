import sys
TESTING = sys.argv[1:2] == ['test']

from .model_mixins import *
from .permissions import *
from .utils import *
from .managers import *
from .querysets import *

if TESTING:
    from .factories import *
