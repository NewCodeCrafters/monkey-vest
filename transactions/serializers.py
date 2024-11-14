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

class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'

class CreateWithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('account_number','amount')                 
