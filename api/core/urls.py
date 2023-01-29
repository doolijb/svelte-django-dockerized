from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.documentation import include_docs_urls

api_urlpatterns = [
    path("account/", include("account.api_urls"), name="account"),
    path("docs/", include_docs_urls(title="My API title", public=True)),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_urlpatterns), name="api"),
]