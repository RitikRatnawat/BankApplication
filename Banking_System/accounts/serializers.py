from rest_framework.serializers import ModelSerializer
from .models import UserBankAccount, User
from .validators import *


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class CreateAccountSerializer(ModelSerializer):
    account_holder_name = serializers.CharField(validators=[is_valid_string])
    account_type = serializers.CharField(validators=[is_valid_string])
    fathers_name = serializers.CharField(validators=[is_valid_string])
    address = serializers.CharField(style={'base_template': 'textarea.html'}, validators=[is_valid_address])
    identity_proof = serializers.IntegerField(validators=[is_valid_aadhar])
    contact = serializers.CharField(validators=[is_valid_contact])
    user = UserSerializer()

    class Meta:
        model = UserBankAccount
        fields = "__all__"
        depth = 1

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        new_user = User.objects.create_user(**user_data)
        new_account = UserBankAccount.objects.create(user=new_user, **validated_data)
        return new_account


class AccountDetailsSerializer(serializers.ModelSerializer):
    balance = serializers.FloatField(validators=[is_valid_amount, ])

    class Meta:
        model = UserBankAccount
        fields = ["account_no", "account_holder_name", "account_type", "balance"]

    def update(self, instance, validated_data):
        instance.balance += validated_data['balance']
        instance.save()

        return instance
