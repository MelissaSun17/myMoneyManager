from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import ModelBase


# Create your models here.
class User(AbstractUser):
    userId = models.AutoField(primary_key=True)  # the unique user ID.
    username = models.CharField(max_length=30)  # The name set by user.
    password = models.CharField(max_length=200)  # The user’s password
    groupId = models.CharField(max_length=255)  # The IDs of groups that the user belongs to. IDs are split by ';'.
    email = models.CharField(max_length=32, unique=True)  # The Email the user will create an account \r\nwith.
    totalExpenses = models.IntegerField()  # The sum of the users transactions for the \r\nbudget period.
    status = models.IntegerField()  # Logging user login status 0.offline 1.online
    role = models.IntegerField()  # 0.admin 1.user
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'user'
        swappable = 'AUTH_USER_MODEL'
        # managed = False


class Group(models.Model):
    groupId = models.AutoField(primary_key=True)  # the unique group ID.
    name = models.CharField(max_length=255)  # The name of the group.
    adminId = models.IntegerField()  # The user ID of the administrator of the \r\ngroup. Foreign key referencing User.
    billList = models.CharField(max_length=255)  # A list of the group’s transactions.
    numMembers = models.IntegerField()  # The total number of members in the group.
    memberIds = models.CharField(max_length=255)  # The IDs of groups that the user belongs to. IDs are split by ';'.
    email_list = models.CharField(max_length=255, blank=True)  # The IDs of groups that the user belongs to. IDs are split by ';'.

    class Meta:
        # managed = False
        db_table = 'group'


class Transaction(models.Model):
    transactionId = models.AutoField(primary_key=True)  # the unique transaction ID.
    ownerId = models.CharField(
        max_length=255)  # The user IDs of the owner of the transaction. \r\nForeign key referencing User. IDs are split by ';'.
    values = models.FloatField()  # The amount of the transaction.
    category = models.IntegerField()  # 1.groceries 2.charity 3.eating out 4.entertainment 5.general 6.transport 7.other
    createTime = models.DateTimeField()  # When the transaction was added to the \r\napplication by the user.
    description = models.CharField(max_length=32)  # The additional note for the transaction.
    transactionType = models.IntegerField()  # 0.personal transaction 1.group transaction
    groupId = models.IntegerField(null=True)

    class Meta:
        # managed = False
        db_table = 'transaction'


class Budget(models.Model):
    budgetId = models.AutoField(primary_key=True)  # the unique budget ID.
    ownerId = models.IntegerField()  # The user ID of the owner of the budget. \r\nForeign key referencing User.
    setBudget = models.IntegerField()  # The total amount the user sets for their \r\nmonthly budget.
    startDate = models.DateTimeField()  # The date when the budget starts to take \r\neffect.
    modifyTime = models.DateTimeField()  # The last modified time of the budget \r\ninformation.

    class Meta:
        # managed = False
        db_table = 'budget'
