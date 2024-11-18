from django.db import transaction
from .serializers import CreateDepositSerializer, DepositSerializer,CreateWithdrawalSerializer,WithdrawalSerializer,TransferSerializer,CreateTransferSerializer
from rest_framework import status, permissions, views, response
from .models import Deposit,Withdrawal,Transfer
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


# VIEW FOR TRANSFER SERIALIZER

class UserTransferView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransferSerializer

    def get(self,request):
        user =  request.user
        transfer_history = Transfer.objects.filter(user=user)
        serializer = WithdrawalSerializer(transfer_history, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)



class CreateTransferView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateTransferSerializer

    @swagger_auto_schema(request_body=CreateTransferSerializer)
    def post(self, request):
        user = request.user
        data = request.data
        sender_account_number = data.get('sender_account_number')
        receiver_account_number = data.get('receiver_account_number')
        amount = Decimal(data.get('amount'))

        # Validate the serializer first
        serializer = CreateTransferSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Start an atomic transaction to ensure consistency
        with transaction.atomic():
            try:
                # Fetch the sender account
                sender_account = Accounts.objects.get(account_number=sender_account_number)

                # Check if the sender account belongs to the authenticated user
                if sender_account.user != user:
                    return response.Response(
                        {"error": "You can't transfer from another person's account"},
                        status=status.HTTP_403_FORBIDDEN
                    )

                # Check if the sender has sufficient funds
                if sender_account.balance < amount:
                    return response.Response(
                        {"error": "Insufficient funds in sender account"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Fetch the receiver account
                receiver_account = Accounts.objects.get(account_number=receiver_account_number)

                # Check if the receiver account exists
                if receiver_account is None:
                    return response.Response(
                        {"error": "Receiver account does not exist"},
                        status=status.HTTP_404_NOT_FOUND
                    )

                # Deduct the amount from sender's account
                sender_account.balance -= amount
                sender_account.save()

                # Add the amount to receiver's account
                receiver_account.balance += amount
                receiver_account.save()

                # Create the transfer record
                transfer_instance = Transfer(
                    sender=sender_account,
                    receiver=receiver_account,
                    amount=amount,
                    status="SUCCESSFUL"
                )
                transfer_instance.save()

                # Return the response with the transfer details
                return response.Response(TransferSerializer(transfer_instance).data, status=status.HTTP_201_CREATED)

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


