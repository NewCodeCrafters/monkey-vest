from django.db import transaction
from .serializers import CreateDepositSerializer, DepositSerializer,CreateWithdrawalSerializer,WithdrawalSerializer
from rest_framework import status, permissions, views, response
from .models import Deposit,Withdrawal
from decimal import Decimal
from drf_yasg.utils import swagger_auto_schema
from accounts.models import Accounts

class UserDepositView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DepositSerializer

    def get(self, request):
        user = request.user
        deposit_history = Deposit.objects.filter(user=user)
        serializer = DepositSerializer(deposit_history, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class CreateDepositView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateDepositSerializer

    @swagger_auto_schema(request_body=CreateDepositSerializer)
    def post(self, request):
        user = request.user
        data = request.data
        account_number = data.get('account_number')
        account_number = int(account_number)
        amount = Decimal(data.get('amount'))


        # Validate the serializer first
        serializer = CreateDepositSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Start an atomic transaction to ensure consistency
        with transaction.atomic():
            try:
                user_account = Accounts.objects.get(account_number=account_number)

                # Check if the account belongs to the authenticated user
                if user_account.user != user:
                    return response.Response(
                        {"error": "You can't deposit to another person's account"},
                        status=status.HTTP_403_FORBIDDEN
                    )

                # Update account balance
                user_account.balance += amount
                user_account.save()

                # Save the deposit transaction
                serializer.save(user=user, status="SUCCESSFUL")
                return response.Response(serializer.data, status=status.HTTP_201_CREATED)

            except Accounts.DoesNotExist:
                return response.Response(
                    {"error": "Account does not exist"},
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return response.Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )


#  VIEW FOR WITHDRAWAL SERIALIZER

class UserWithdrawalView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WithdrawalSerializer

    def get(self,request):
        user =  request.user
        withdrawal_history = Withdrawal.objects.filter(user=user)
        serializer = WithdrawalSerializer(withdrawal_history, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    

class CreateWithdrawalView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateWithdrawalSerializer

    @swagger_auto_schema(request_body=CreateWithdrawalSerializer)
    def post(self, request):
        user = request.user
        data = request.data
        account_number = data.get('account_number')
        amount = Decimal(data.get('amount'))

        # Validate the serializer first
        serializer = CreateWithdrawalSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Start an atomic transaction to ensure consistency
        with transaction.atomic():
            try:
                
                account = Accounts.objects.get(account_number=account_number)

                # Check if the account belongs to the authenticated user
                if account.user != user:
                    return response.Response(
                        {"error": "You can't withdraw from another person's account"},
                        status=status.HTTP_403_FORBIDDEN
                    )

            # update the balance
                if account.balance < amount:
                    return response.Response(
                        {"error": "Insufficient funds in account"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Update the account balance by deducting the withdrawal amount
                account.balance -= amount
                account.save()

                # Create the withdrawal record
                withdrawal_instance = Withdrawal(
                    user=user,
                    account=account,
                    amount=amount,
                    status="SUCCESSFUL"
                )
                withdrawal_instance.save()

                # Return the response with the withdrawal details
                return response.Response(WithdrawalSerializer(withdrawal_instance).data, status=status.HTTP_201_CREATED)

            except Accounts.DoesNotExist:
                return response.Response(
                    {"error": "Account does not exist"},
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return response.Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )    

