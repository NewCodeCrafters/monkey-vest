from django.shortcuts import render

from rest_framework import response, status, permissions, views

from drf_yasg.utils import swagger_auto_schema

from accounts.models import Accounts

from .serializers import AccountsSerializer, GetMainAccountsSerializer, UserUpdateAccountSerializer

class GetMainAccountView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetMainAccountsSerializer
    
    def get(self, request):
        user = request.user
        main_account = Accounts.objects.filter(user=user, account_type='MAIN').first()
        serializer = GetMainAccountsSerializer(main_account)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class GetAccountView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetMainAccountsSerializer
    
    def get(self, request, account_number):
        account_number = str(account_number)
        account = Accounts.objects.get(account_number=account_number)
        serializer = GetMainAccountsSerializer(account)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class GetAllUsersAccountView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetMainAccountsSerializer
    
    def get(self, request):
        user = request.user
        accounts = Accounts.objects.filter(user=user)
        serializer = GetMainAccountsSerializer(accounts, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    
class CreateNewAccountView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountsSerializer

    @swagger_auto_schema(request_body=AccountsSerializer)
    def post(self, request):
        user = request.user
        data = request.data
        account_type = data.get('account_type') 
        same_account = Accounts.objects.filter(account_type=account_type, user=user).exists()
        if same_account: # If account exists
            return response.Response(
                {"error": f"You can only create one account of type {account_type}. exists."},
                status=status.HTTP_403_FORBIDDEN)
        else:
            serializer = AccountsSerializer(data=data)
            if serializer.is_valid():
                
                serializer.save(user=user)
                return response.Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAccountUpdateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserUpdateAccountSerializer

    @swagger_auto_schema(request_body=UserUpdateAccountSerializer)
    # @swagger_auto_schema(request_body=AdminLyricsSerializer)
    def put(self, request, account_number, *args, **kwargs):
        account_number = str(account_number)
        account = Accounts.objects.get(account_number=account_number)
        serializer = UserUpdateAccountSerializer(account, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)


