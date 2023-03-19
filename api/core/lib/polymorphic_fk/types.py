from typing import Any, Callable
from django.db.models import Model
from django.db.models.deletion import Collector
from typing import Callable, Any, Sequence

OnDeleteType = Callable[[Collector, Any, Sequence[Model], str], None]
