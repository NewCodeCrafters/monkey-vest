import uuid
from django.db import models

from django.contrib.auth import get_user_model

from .generators import generate_10_digit_number_starting_with_2

from .choices import ACCOUNT_TYPE_CHOICES, CURRENCY_CHOICES, STATUS_CHOICES

User = get_user_model()




class Accounts(models.Model):
    account_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_number = models.PositiveBigIntegerField(null=True, blank=True)
    account_type = models.CharField(max_length=30, choices=ACCOUNT_TYPE_CHOICES)
    account_title = models.CharField(max_length=50)
    currency = models.CharField(max_length=5, choices=CURRENCY_CHOICES)
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    interest_rate = models.DecimalField(decimal_places=2, max_digits=3, default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    account_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    last_transaction_date = models.DateTimeField(blank=True, null=True)
    withdrawal_limit = models.DecimalField(decimal_places=2, max_digits=10, default=1000000)
    deposit_limit = models.DecimalField(decimal_places=2, max_digits=10, default=1000000)
    maturity_date = models.PositiveSmallIntegerField(default=0)

    def __str__(self) -> str:
        return self.account_title

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = generate_10_digit_number_starting_with_2()
        return super().save(*args, **kwargs)