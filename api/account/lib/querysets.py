from core.lib import PolycapableQuerySet
from django.db.models import QuerySet

class UserQueryset(QuerySet):
    pass


class PasswordQuerySet(PolycapableQuerySet):
    pass


class EmailAddressQuerySet(PolycapableQuerySet):
    def primary(self):
        return self.filter(is_primary=True)

    def verified(self):
        return self.filter(verified_at__isnull=False)

    def unverified(self):
        return self.filter(verified_at__isnull=True)

    def get_by_natural_key(self, email):
        return self.get(email=email)


class RedeemableKeyQuerySet(PolycapableQuerySet):
    def any(self):
        return self.all()

    def redeemable(self):
        return self.filter(expired_at__isnull=True, redeemed_at__isnull=True)

    def expired(self):
        return self.filter(expired_at__isnull=False)

    def redeemed(self):
        return self.filter(redeemed_at__isnull=False)
