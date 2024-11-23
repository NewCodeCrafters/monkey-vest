from django.db import transaction
from transactions.utils import convert_ngn_to_usd_static, convert_usd_to_ngn_static
from .serializers import (
    CreateDepositSerializer,
    CreateTransferSerializer,
    DepositSerializer,
    CreateWithdrawalSerializer,
    TransferSerializer,
    WithdrawalSerializer,
)
from rest_framework import status, permissions, views, response
from .models import Deposit, Transfer, Withdrawal
from decimal import Decimal
from drf_yasg.utils import swagger_auto_schema
from accounts.models import Accounts
from notification.models import Notification

# View for retrieving user-specific deposit history
class UserDepositView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access
    serializer_class = DepositSerializer  # Serializer to format response data

    def get(self, request):
        # Get the current logged-in user
        user = request.user
        # Retrieve all deposit records for the user
        deposit_history = Deposit.objects.filter(user=user)
        # Serialize the deposit records
        serializer = DepositSerializer(deposit_history, many=True)
        # Return the serialized data with an HTTP 200 OK response
        return response.Response(serializer.data, status=status.HTTP_200_OK)

# View for creating a new deposit
class CreateDepositView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access
    serializer_class = CreateDepositSerializer  # Serializer to validate and process input data

    @swagger_auto_schema(request_body=CreateDepositSerializer)
    def post(self, request):
        user = request.user  # Get the current logged-in user
        data = request.data  # Retrieve input data from the request

        # Extract and convert account number and amount from input data
        account_number = int(data.get('account_number'))
        amount = Decimal(data.get('amount'))

        # Validate the serializer to ensure data integrity
        serializer = CreateDepositSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Use a transaction to ensure database consistency
        with transaction.atomic():
            try:
                # Retrieve the account based on the account number
                user_account = Accounts.objects.get(account_number=account_number)

                # Check if the account belongs to the current user
                if user_account.user != user:
                    return response.Response(
                        {"error": "You can't deposit to another person's account"},
                        status=status.HTTP_403_FORBIDDEN
                    )

                # Update account balance
                user_account.balance += amount
                remark = f"You deposited {amount} to your {user_account.account_type}"

                # Create a notification for the deposit
                Notification.objects.create(user=user, amount=amount, remark=remark)

                # Update user balance
                user.balance += amount
                user_account.save()
                user.save()

                # Save the deposit record with status "SUCCESSFUL"
                serializer.save(user=user, status="SUCCESSFUL")
                return response.Response(serializer.data, status=status.HTTP_201_CREATED)

            except Accounts.DoesNotExist:
                # Handle invalid account numbers
                return response.Response(
                    {"error": "Account does not exist"},
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                # Handle unexpected errors
                return response.Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

# View for retrieving user-specific withdrawal history
class UserWithdrawalView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access
    serializer_class = WithdrawalSerializer  # Serializer to format response data

    def get(self, request):
        user = request.user  # Get the current logged-in user
        # Retrieve all withdrawal records for the user
        withdrawal_history = Withdrawal.objects.filter(user=user)
        # Serialize the withdrawal records
        serializer = WithdrawalSerializer(withdrawal_history, many=True)
        # Return the serialized data with an HTTP 200 OK response
        return response.Response(serializer.data, status=status.HTTP_200_OK)

# View for creating a new withdrawal
class CreateWithdrawalView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access
    serializer_class = CreateWithdrawalSerializer  # Serializer to validate and process input data

    @swagger_auto_schema(request_body=CreateWithdrawalSerializer)
    def post(self, request):
        user = request.user  # Get the current logged-in user
        data = request.data  # Retrieve input data from the request

        # Extract account number and amount from input data
        account_number = data.get('account_number')
        amount = Decimal(data.get('amount'))

        # Validate the serializer to ensure data integrity
        serializer = CreateWithdrawalSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Use a transaction to ensure database consistency
        with transaction.atomic():
            try:
                # Retrieve the account based on the account number
                account = Accounts.objects.get(account_number=account_number)

                # Ensure the account belongs to the current user
                if account.user != user:
                    return response.Response(
                        {"error": "You can't withdraw from another person's account"},
                        status=status.HTTP_403_FORBIDDEN
                    )

                # Check if the account has sufficient balance
                if account.balance < amount:
                    return response.Response(
                        {"error": "Insufficient funds in account"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Deduct the withdrawal amount from the account balance
                account.balance -= amount
                user.balance -= amount
                account.save()
                user.save()

                # Create the withdrawal record
                withdrawal_instance = Withdrawal(
                    user=user,
                    account=account,
                    amount=amount,
                    status="SUCCESSFUL"
                )
                withdrawal_instance.save()

                # Create a notification for the withdrawal
                remark = f"You withdrew {amount} from your {account.account_type}"
                Notification.objects.create(user=user, amount=amount, remark=remark)

                # Return the response with withdrawal details
                return response.Response(WithdrawalSerializer(withdrawal_instance).data, status=status.HTTP_201_CREATED)

            except Accounts.DoesNotExist:
                # Handle invalid account numbers
                return response.Response(
                    {"error": "Account does not exist"},
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                # Handle unexpected errors
                return response.Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

# View for retrieving user-specific transfer history
class UserTransferViews(views.APIView):
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access
    serializer_class = TransferSerializer  # Serializer to format response data

    def get(self, request, source_account_number: int):
        user = request.user  # Get the current logged-in user
        # Retrieve all transfer records for the specified account and user
        transfers = Transfer.objects.filter(source_account_number=str(source_account_number), user=user)
        # Serialize the transfer records
        serializer = TransferSerializer(transfers, many=True)
        # Return the serialized data with an HTTP 200 OK response
        return response.Response(serializer.data, status=status.HTTP_200_OK)

# View for creating a new transfer
class CreateTransferView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can access
    serializer_class = CreateTransferSerializer  # Serializer to validate and process input data

    @swagger_auto_schema(request_body=CreateTransferSerializer)
    def post(self, request, source_account_number: int):
        user = request.user  # Get the current logged-in user
        data = request.data  # Retrieve input data from the request

        # Extract transfer details
        amount = Decimal(data.get('amount'))
        destination_account_number = data.get('destination_account_number')

        try:
            # Retrieve source and destination accounts
            source_account = Accounts.objects.get(account_number=source_account_number)
            destination_account = Accounts.objects.get(account_number=destination_account_number)

            # If the accounts are of the same type, transfer directly
            if source_account.account_type == destination_account.account_type:
                source_account.balance -= amount
                destination_account.balance += amount

            # Handle conversion for USD to NGN
            elif source_account.account_type == "USD":
                dollar_value = convert_usd_to_ngn_static(amount)
                source_account.balance -= dollar_value
                destination_account.balance += dollar_value

            # Handle conversion for NGN to USD
            else:
                naira_value = convert_ngn_to_usd_static(amount)
                source_account.balance -= naira_value
                destination_account.balance += naira_value

            # Update balances for users
            sender = source_account.user
            receiver = destination_account.user
            sender.balance -= amount
            receiver.balance += amount

            # Save all changes
            sender.save()
            receiver.save()
            source_account.save()
            destination_account.save()

            # Create notifications for both sender and receiver
            Notification.objects.create(
                user=sender,
                amount=amount,
                remark=f"You sent {amount} from {source_account.account_type} to {destination_account.account_number}"
            )
            Notification.objects.create(
                user=receiver,
                amount=amount,
                remark=f"You received {amount} to {destination_account.account_type} from {source_account.account_number}"
            )

            return response.Response({"message": "Transfer successful"}, status=status.HTTP_201_CREATED)

        except Accounts.DoesNotExist:
            # Handle invalid account numbers
            return response.Response(
                {'error': f"{source_account_number} is not a valid account number."},
                status=status.HTTP_404_NOT_FOUND
            )
