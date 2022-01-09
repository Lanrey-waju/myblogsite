from django.db import models
from django.db.models.fields import DateTimeField
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', max_length=254, unique=True)
    first_name = models.CharField(verbose_name='first name', max_length=150)
    last_name = models.CharField(verbose_name='last name', max_length=150)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models,DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    