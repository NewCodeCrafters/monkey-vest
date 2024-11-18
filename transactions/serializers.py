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
        model = Withdrawal
        fields = '__all__'


class CreateWithdrawalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Withdrawal
        fields = ('account_number','amount') 

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'


class CreateTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ('amount', 'destination_account_number', 'source_account_number', 'status')
                            
