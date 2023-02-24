from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.documentation import include_docs_urls

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework import routers


api_urlpatterns = [
    path("account/", include("account.api_urls"), name="account"),
    path("docs/", include_docs_urls(title="My API title", public=True)),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_urlpatterns), name="api"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
