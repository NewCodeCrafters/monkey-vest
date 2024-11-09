from rest_framework import serializers


from .models import Accounts



class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ["account_type", "account_title", 'currency']  

class GetMainAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = "__all__"
        
        