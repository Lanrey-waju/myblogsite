from core.models import TimeStampedModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager

# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    email = models.EmailField("email address", max_length=254, unique=True)
    first_name = models.CharField(verbose_name="first name", max_length=150)
    last_name = models.CharField(verbose_name="last name", max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email

    def get_full_name(self):
        """returns the first name and the last name of the user

        Returns:
            str: [description]
        """
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        """returns only the first name of the user"""
        return f"{self.first_name}"
