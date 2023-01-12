from django.urls import path

from . import views

urlpatterns = [
    path("", views.AccountAPIView.as_view(), name="account"),
    path("csrf/", views.CSRFTokenAPIView.as_view(), name="csrf"),
    # path("login/", views.AccountLoginAPIView.as_view(), name="login"),
    # path("logout/", views.AccountLogoutAPIView.as_view(), name="logout"),
    # path("register/", views.AccountRegisterAPIView.as_view(), name="register"),
]
