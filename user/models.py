from django.db import models

from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator

from .managers import UserManager
import random
import string

STATUS = (
    ("Paid","Paid")
    ("unpaid","unpaid")
)



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
    

class Profile(models.Model):
    user = models.OneToOneField()
    account = models.OneToOneField()
    pic = models.ImageField(upload_to="media")
    dob = models.CharField(max_length=20)
    balance = models.IntegerField(default=0)


class Loan(models.Model):
    amount = models.CharField(max_length=30)
    status = models.CharField(max_length=50, choices=STATUS)

class Deposits(models.Model):
    time_paid = models.DateTimeField(_("Date of deposit"), auto_now_add=True)
    amount = models.CharField(max_length=30)

class Withdrawal(models.Model):
    time_taken = models.DateTimeField(_("you withdrew"), auto_now_add=True)
    amount = models.CharField(max_length=30)

class Investment(models.Model):
    time_invested = models.DateTimeField(_("you inveted"), auto_now_add=True)
    invested = models.CharField(max_length=30)





