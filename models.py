import random
import uuid
from django.db import models

# Create your models her

# User Detals Table-------------
class BankUser(models.Model):
    UserAccountName=models.CharField(max_length=100)
    UserAccountNo=models.CharField(max_length=100,primary_key=True)
    UserAddress=models.CharField(max_length=100)
    UserEmail=models.CharField(max_length=100)
    UserPhone=models.CharField(max_length=50)
    UserPassword=models.CharField(max_length=50)
    UserConfromPassword=models.CharField(max_length=50)
    class Meta:
        db_table = "User_Info"

# Contact information Table ---------------
class Contact(models.Model):
    ContactId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    UserAccountNo  =models.ForeignKey(BankUser, on_delete=models.CASCADE, to_field='UserAccountNo')
    UserName=models.CharField(max_length=100)
    UserEmail=models.CharField(max_length=100)
    UserPhone=models.CharField(max_length=100)
    UserMessage=models.CharField(max_length=500)
    ContactDate = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "User_Contact_Info"

# Bank Branch Details Table -------------- 
class branch(models.Model):
    BranchId = models.IntegerField(primary_key=True,editable=False)
    BranchName=models.CharField(max_length=100)
    BranchAddress=models.CharField(max_length=100)
    class Meta:
        db_table = "bank_branch"

# Bnak Account Details Table --------------       
class BankAccount(models.Model):
    
    BankAccountNo  =  models.ForeignKey(BankUser, on_delete=models.CASCADE, to_field='UserAccountNo')
    BankAccountBranch  =  models.IntegerField()
    CurrentAmmount=models.IntegerField()
    CurrentLoanAmmount=models.IntegerField()
    UserLoanLimit=models.IntegerField()
    
    class Meta:
        db_table = "User_Account"

# Transaction Details Table -------------- 
class UserTransaction(models.Model):
    
    TransactionId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    BankAccountNo = models.CharField(max_length=100)
    ReceiverUserAccountNo = models.ForeignKey(BankUser, on_delete=models.CASCADE, to_field='UserAccountNo')
    Ammount=models.IntegerField()
    TransactionPurpose= models.CharField(max_length=100)
    TransactionDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "User_Transaction"
 

# Loan Details Table --------------       
class Loan(models.Model):
    
    LoanId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    BankAccountNo  = models.ForeignKey(BankUser, on_delete=models.CASCADE, to_field='UserAccountNo')
    LoanAmmount=models.IntegerField()
    LoanPurpose= models.CharField(max_length=100)
    LoanDate = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "User_Loan"
        
