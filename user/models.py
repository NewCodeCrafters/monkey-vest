from django.db import models

from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator

from .managers import UserManager



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=200, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, validators=[MinLengthValidator(11)])
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_("Date Joined"), auto_now_add=True)
    last_login = models.DateTimeField(_("Last Login Date"), auto_now=True)
     
     
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number"]

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.email}"
    
