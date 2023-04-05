from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import *
from rest_framework import status
from .utils import *


# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def get_account_details(request, user_id):
    account = UserBankAccount.objects.get(user_id=user_id)

    if account is not None:
        acc_serializer = AccountDetailsSerializer(account)
        return Response(acc_serializer.data, status=status.HTTP_200_OK)

    return Response({"message": "No Account Details Found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def register_new_account(request):
    account_data = generate_account_data(request.data)

    new_acc_serializer = CreateAccountSerializer(data=account_data)

    if new_acc_serializer.is_valid():
        new_acc_serializer.save()
        return Response({"message": "New Account Created",
                         "Account Number": new_acc_serializer.data["account_no"],
                         "Username": new_acc_serializer.data['user']["username"],
                         "Password": account_data['user']['password']},
                        status=status.HTTP_200_OK)

    return Response({"error": new_acc_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def login_account(request):
#     username = request.data['username']
#     password = request.data['password']
#
#     user = User.objects.get(username=username)
#
#     if user is not None:
#         if user.check_password(password):
#             return Response({
#                 "username": username,
#                 "token": int(random.random() * 10**10)
#             })
#
#     return Response({"error": "Login Unsuccessful"})


@api_view(['PUT'])
@permission_classes([IsAuthenticated, ])
def deposit_amount(request, user_id):
    try:
        account = UserBankAccount.objects.get(user_id=user_id)

        acc_serializer = AccountDetailsSerializer(account, data=request.data, partial=True)

        if acc_serializer.is_valid():
            acc_serializer.save()
            return Response({
                "message": "Amount Deposited Successfully",
                "balance": acc_serializer.data['balance']
            }, status=status.HTTP_200_OK)

    except TypeError:
        return Response({
            "message": "Enter a Valid Amount"
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, ])
def transfer_amount(request, from_user_id):
    try:
        from_acc = UserBankAccount.objects.get(user_id=from_user_id)
        to_acc = UserBankAccount.objects.get(account_no=request.data['to_acc'])

        from_acc_data = {'balance': -float(request.data['balance'])}
        to_acc_data = {'balance': float(request.data['balance'])}

        from_acc_serializer = AccountDetailsSerializer(from_acc, data=from_acc_data, partial=True)
        to_acc_serializer = AccountDetailsSerializer(to_acc, data=to_acc_data, partial=True)

        if from_acc_serializer.is_valid() and to_acc_serializer.is_valid():
            from_acc_serializer.save()
            to_acc_serializer.save()
            return Response({
                "message": "Transaction Successful",
                "from_balance": from_acc_serializer.data['balance'],
                "to_balance": to_acc_serializer.data['balance']
            }, status=status.HTTP_200_OK)

    except TypeError:
        return Response({
            "message": "Transaction Unsuccessful"
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])
def add_or_deduct(request):
    account = UserBankAccount.objects.get(account_no=request.data['account_no'])
    data = None

    if request.data['action'] == "deduct":
        data = {
            'balance': -float(request.data['balance'])
        }
    elif request.data['action'] == "add":
        data = {
            'balance': float(request.data['balance'])
        }

    acc_serializer = AccountDetailsSerializer(account, data=data, partial=True)

    msg = "Amount " + ("Deducted" if request.data['action'] == "deduct" else "Added")
    if acc_serializer.is_valid():
        acc_serializer.save()
        return Response({
            "message": msg
        })

    return Response({"message": "Operation Failed"})

