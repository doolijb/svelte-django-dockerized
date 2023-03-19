from rest_framework import routers

from account.views import (
    SessionViewSet,
    RegisterViewSet,
    UserViewSet,
    PasswordViewSet,
    EmailAddressViewSet,
    RedeemKeyViewSet,
)

app_name = "account"

router = routers.DefaultRouter()

router.register(r"sessions", SessionViewSet, basename="session")
router.register(r"register", RegisterViewSet, basename="register")
router.register(r"users", UserViewSet, basename="user")
router.register(r"passwords", PasswordViewSet, basename="password")
router.register(r"email-addresses", EmailAddressViewSet, basename="email-address")
router.register(r"redeemable-keys", RedeemKeyViewSet, basename="redeemable-key")

urlpatterns = router.urls
