from rest_framework import serializers


from .models import Accounts




class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = [
            user = 'The user',
            currency = 'NGN',
            account_type = 'MAIN',
            account_status = 'ACTIVE',
        ]  
            
        
        