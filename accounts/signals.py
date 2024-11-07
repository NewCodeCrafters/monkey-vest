from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model
from .models import Accounts

User = get_user_model()


@receiver(post_save, sender=User)
def create_main_account(sender, instance, created, **kwargs):
    if created:
        Accounts.objects.create(
            user = instance,
            account_type = "MAIN",
            account_title = "Main Account",
            currency = "NGN",
            balance = 0.00,
            interest_rate = 0.04,
            account_status = "ACTIVE",
            withdrawal_limit = 1000000.00,
            deposit_limit = 1000000.00
        )