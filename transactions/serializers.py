from rest_framework import serializers

from .models import Deposit, Transfer, Withdrawal


class CreateDepositSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deposit
        fields = ('amount', 'account_number')


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = "__all__"
