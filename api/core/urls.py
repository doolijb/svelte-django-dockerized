from django.contrib import admin
from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

app_name = "core"

schema_view = get_schema_view(
   openapi.Info(
      title="API Docs",
      default_version='v1',
      description="API Documentation for the Svelte Django Dockerized project.",
      terms_of_service="https://github.com/doolijb/svelte-django-dockerized",
      contact=openapi.Contact(email="jody@doolittle.me"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("api/account/", include("account.urls.public")),
    path("api/admin/account/", include("account.urls.admin"))
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'api/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        path('api/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    ]
