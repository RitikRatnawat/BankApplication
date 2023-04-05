from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager


# Create your models here.
class User(AbstractBaseUser):
    username = models.CharField(max_length=20, primary_key=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    objects = UserManager()


class UserBankAccount(models.Model):
    account_no = models.PositiveBigIntegerField(primary_key=True)
    account_type = models.CharField(max_length=10)
    account_holder_name = models.CharField(max_length=30)
    fathers_name = models.CharField(max_length=30)
    address = models.TextField()
    identity_proof = models.PositiveBigIntegerField()
    contact = models.CharField(max_length=10)
    has_debit_card = models.BooleanField()
    balance = models.FloatField(default=0, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
