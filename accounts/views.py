from django.shortcuts import render

from rest_framework import response, status, permissions, views

from accounts.models import Accounts

from .serializers import AccountsSerializer, GetMainAccountsSerializer

class GetMainAccountView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetMainAccountsSerializer
    
    def get(self, request):
        user = request.user
        main_account = Accounts.objects.filter(user=user, account_type='MAIN').first()
        serializer = GetMainAccountsSerializer(main_account)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    
    