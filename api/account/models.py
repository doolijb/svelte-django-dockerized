"""
Models for the account app.
"""

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext as _

from core.lib.models import BaseModel, DatesMixin

from .managers import UserManager


class User(BaseModel, AbstractBaseUser, PermissionsMixin, DatesMixin):
    """
    Model representing an authenticable user. Compared to the default Django
    user model, this User has no email field. Instead, it is closely tied to
    the EmailAddress model.
    """

    username = models.CharField(_("username"), max_length=30, unique=True)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, blank=True)
    is_active = models.BooleanField(_("active"), default=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
        """
        Meta options for the User model.
        """

        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        """String representation of the User model."""
        return str(self.username)

    @property
    def full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        return self.first_name + " " + self.last_name

    @property
    def short_name(self):
        """Return the short name for the user."""
        return self.first_name


class EmailAddress(BaseModel, DatesMixin):
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    is_primary = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "email")

    def __str__(self):
        return str(self.email)

    def save(self, *args, **kwargs):
        """ """
        if self.is_primary:
            EmailAddress.objects.filter(user=self.user).update(is_primary=False)
            if settings.ENABLE_USERNAMES and self.user.username != self.email:
                self.user.username = self.email
                self.user.save(commit=kwargs.get("commit", True))
        super().save(*args, **kwargs)


class Redeemable(BaseModel):
    used = models.BooleanField(default=False)
    user = models.ForeignKey(
        "account.User", on_delete=models.CASCADE, null=True, blank=True
    )
    date_expires = models.DateTimeField(null=True, blank=True)
    date_used = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        """ """
        if self.used:
            self.user = None
        super().save(*args, **kwargs)
