from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _

class EmailConfirmedChoices(IntegerChoices):
    """
    Redeemed choices.
    """
    NOT_CONFIRMED = 0, _('Not confirmed')
    CONFIRMED = 1, _('Confirmed')
