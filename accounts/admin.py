from django.contrib import admin

from .models import Accounts

@admin.register(Accounts)
class AccountsAdmin(admin.ModelAdmin):
    list_display = ["account_id", "account_number","currency", "account_status"]
    list_filter = ["account_id", "account_number","currency", "account_status"]
    search_fields = list_display
