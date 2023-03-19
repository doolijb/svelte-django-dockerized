from rest_framework import routers

from account.views import (
    UserViewSet,
    PasswordViewSet,
    EmailAddressViewSet,
    RedeemableKeyViewSet,
)

app_name = "account:admin"

router = routers.DefaultRouter()

router.register(r"users", UserViewSet, basename="user")
router.register(r"passwords", PasswordViewSet, basename="password")
router.register(r"email-addresses", EmailAddressViewSet, basename="email-address")
router.register(r"redeemable-keys", RedeemableKeyViewSet, basename="redeemable-key")

urlpatterns = router.urls
