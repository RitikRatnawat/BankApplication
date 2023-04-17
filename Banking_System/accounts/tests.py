from django.test import TestCase
from rest_framework.test import APIClient
from .models import User
from .utils import generate_account_data
from .serializers import CreateAccountSerializer
from rest_framework.authtoken.models import Token
import json

data = {
    "account_holder_name": "Test User",
    "account_type": "Savings",
    "fathers_name": "My Father",
    "address": "My address",
    "identity_proof": 204764692414,
    "contact": "1234567890",
    "has_debit_card": "True"
}


# Create your tests here.
class APITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        account_data = generate_account_data(data)
        new_acc_serializer = CreateAccountSerializer(data=account_data)
        if new_acc_serializer.is_valid():
            new_acc_serializer.save()

        self.username = str(new_acc_serializer.data['user']["username"])
        self.password = account_data['user']['password']
        self.account_number = str(new_acc_serializer.data['account_no'])

        user = User.objects.get(username=self.username)
        self.client.force_authenticate(user=user)

    def test_register_new_account(self):
        self.client.credentials()
        response = self.client.post("/my-bank/account/new/", data=data, format="json")
        result = response.data
        keys = {"message", "Account Number", "Username", "Password"}
        self.assertTrue(keys == result.keys())
        self.assertTrue(str(result["Account Number"]).isdigit())

    def test_login(self):
        login_data = {
            'username': self.username,
            'password': self.password
        }

        self.client.credentials()
        response = self.client.post("/my-bank/account/login/", data=login_data, format="json")
        self.assertTrue("token" in response.data)

    def test_get_account_details(self):
        response = self.client.get("/my-bank/account/" + self.username)
        result = response.data
        keys = {"account_no", "account_holder_name", "account_type", 'balance'}
        self.assertEqual(result.keys(), keys)
        self.assertTrue(str(result['account_no']).isdigit())

    def test_deposit_amount(self):
        deposit_data = {"balance": float(1000)}
        response = self.client.put("/my-bank/account/deposit/" + self.username, data=deposit_data, format="json")
        result = response.data
        keys = {"message", "balance"}
        self.assertEqual(result.keys(), keys)
        self.assertEqual(result['message'], "Amount Deposited Successfully")

    def test_transfer_amount(self):
        transfer_data = {
            "to_acc": self.account_number,
            "balance": float(1000)
        }

        response = self.client.put("/my-bank/account/transfer/" + self.username, data=transfer_data, format="json")
        result = response.data
        keys = {"message", "avail_balance"}
        self.assertEqual(result.keys(), keys)
        self.assertEqual(result["message"], "Transaction Successful")


