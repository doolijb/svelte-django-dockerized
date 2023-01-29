from django.urls import path, re_path, include

from .api_views import (
    CurrentUserView,
    EmailAddressesView,
    RedeemKeyView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

###
# API Nested Routes
###

email_addresses = [
    re_path(r"(?P<email_address_id>/>\d+)/", EmailAddressesView.as_view()),
]

redeemable_keys = [
    path("redeem/<uuid:redeemable_key_id>", RedeemKeyView.as_view(), name="redeem"),
]

tokens = [
    path("", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("verify/", TokenVerifyView.as_view(), name="verify"),
]

users = [
    path(
        "current/",
        CurrentUserView.as_view(),
        name="users_current",
    ),
]

###
# API Routes for the Account App
###

urlpatterns = [
    path("email-addresses/", include(email_addresses), name="email_addresses"),
    path("redeemable-keys/", include(redeemable_keys), name="redeemable_keys"),
    path("tokens/", include(tokens), name="tokens"),
    path("users/", include(users), name="users"),
]
