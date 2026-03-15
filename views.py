
from pyexpat.errors import messages
from django.contrib import messages
from django.shortcuts import redirect, render
from Home import models, utils
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login as auth_login
from .models import BankUser, UserTransaction
from .models import Loan
# Create your views here.

curremt_user = 0

def index(request):
    return render(request, 'index.html')

"""
def login(request):
    
    if request.method == 'POST':
        bank_number = request.POST.get('bank_number')
        password = request.POST.get('password')
        try:
            user_bank = models.UserBank.objects.get(UserAccountNo=bank_number)
            if password == user_bank.UserPassword:
                return redirect('dashboard')
            else:
                error_message = "User with provided Password does not exist"
                return render(request, 'login.html', {'error_message': error_message})
        except models.UserBank.DoesNotExist:
            error_message = "User with provided bank number does not exist"
            return render(request, 'login.html', {'error_message': error_message})
    else:
        print('Done')
    return render(request, 'login.html')
    """
def login(request):
    if request.method == 'POST':
        
        bank_number = request.POST.get('bank_number')
        password = request.POST.get('password')  
        
        # Corrected authenticate() usage
        user = authenticate(request, username=bank_number, password=password)
        if user is not None:
            
            # Corrected login() usage
            auth_login(request,user)

            return redirect('dashboard')
            
        else:
            error_message = "Authentication failed"
            return render(request, 'login.html', {'error_message': error_message})
    
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        # Data save In Custom Table 
    
        UserAccountName=request.POST.get('account_name')
        UserAccountNo=utils.generate_account_number()
        UserAddress=request.POST.get('address')
        UserEmail=request.POST.get('email')
        UserPhone=request.POST.get('phone')
        UserPassword=request.POST.get('password')
        UserConfromPassword=request.POST.get('comfrom_password')
        try:
            
            if UserPassword==UserConfromPassword:
            
                user=models.BankUser(UserAccountName=UserAccountName,UserAccountNo=UserAccountNo,UserAddress=UserAddress,UserEmail=UserEmail,UserPhone=UserPhone,UserPassword=UserPassword,UserConfromPassword=UserConfromPassword)
                user.save()
        
        # Data Save In PreDefine Table User
        
                my_user=User.objects.create_user(UserAccountNo,UserEmail,UserPassword)
                my_user.save()
            
                create_bank_account_for_user(user)
                return render(request, 'login.html')
            else:
                messages.error(request, 'Not authorized !' )
        except models.BankAccount.DoesNotExist:
            messages.error(request, 'System Not Respond!' )
            return redirect('signup')
    return render(request, 'signup.html')

def create_bank_account_for_user(user):
    # Create a BankAccount for the user
    models.BankAccount.objects.create(BankAccountNo=user,BankAccountBranch=101,CurrentAmmount=5000,CurrentLoanAmmount=0,UserLoanLimit=0)

 
""""
@login_required(login_url='login')
def dashboard(request):
    
    user_data = models.UserBank.objects.all()  # Example query to retrieve all user data
    
    # Pass data to template
    return render(request, 'dashboard.html', {'user_data': user_data})
    account_number = 1111
    try:
        # Retrieve the user's details from the database based on the account number
        user = models.UserBank.objects.get(UserAccountNo=account_number)
       
        # Pass the user's details to the template context
        context = {
            'account_no': user.UserAccountName,
            'account_number': user.UserAccountNo,
            'user_address': user.UserAddress,
            'user_email': user.UserEmail,
            'user_phone': user.UserPhone,
            # Add more user details as needed
        }
        contextData = {
            'user_name': "user.UserAccountName",
            'account_number': "user.UserAccountNo",
            'user_address': "user.UserAddress",
            'user_email': "user.UserEmail",
            'user_phone': "user.UserPhone",
            # Add more user details as needed
        }
        print(user.UserAccountName)
        return render(request, 'dashboard.html', context)
    
    except models.UserBank.DoesNotExist:
        # Handle the case where the user does not exist
        error_message = "User with provided account number does not exist."
        return render(request, 'dashboard.html', {'error_message': error_message})
    return render(request, 'dashboard.html')

"""

@login_required(login_url='login')
def dashboard(request):
    try:  
            
        current_user = request.user
        
        user_data = models.BankUser.objects.get(UserAccountNo=current_user.username)
        account_data = models.BankAccount.objects.get(BankAccountNo=current_user.username)
        branch=models.branch.objects.get(BranchId=account_data.BankAccountBranch)
        
    except models.BankUser.DoesNotExist:
        user_data = None
    return render(request, 'dashboard.html', {'user_data': user_data,'account_data': account_data,'branch': branch})

    
@login_required(login_url='login')
def about(request):
    
    current_user = request.user
    user_data = models.BankUser.objects.get(UserAccountNo=current_user.username)
    user_account=models.BankAccount.objects.get(BankAccountNo=user_data)

    if request.method == 'POST':
        pay_amount = int(request.POST.get('amount'))
        
        if pay_amount <= 0:
            messages.error(request, 'The payment amount must be greater than zero.')
        elif pay_amount > user_account.CurrentAmmount:
            messages.error(request, 'Insufficient funds in the bank account.')
        else:
            user_account.CurrentAmmount =user_account.CurrentAmmount-pay_amount
            user_account.CurrentLoanAmmount =user_account.CurrentLoanAmmount-pay_amount
            user_account.CurrentLoanAmmount =user_account.CurrentLoanAmmount-pay_amount
            user_account.UserLoanLimit=user_account.UserLoanLimit-pay_amount
            user_account.save()
            
            loan=models.Loan(BankAccountNo=user_account.BankAccountNo,LoanAmmount=pay_amount,LoanPurpose='Pay Loan')
            loan.save()
                        

            messages.success(request, 'Loan payment successful.')
            return redirect('about')

    return render(request, 'about.html')

@login_required(login_url='login')
def customersupport(request):
    if request.method == 'POST':
        try:
            user_message=request.POST.get('message')
            current_user = request.user
            user_data = models.BankUser.objects.get(UserAccountNo=current_user.username)
            data=models.Contact(UserAccountNo=user_data,UserName=user_data.UserAccountName,UserEmail=user_data.UserEmail,UserPhone=user_data.UserPhone,UserMessage=user_message)
            data.save()
        except models.BankAccount.DoesNotExist:
            messages.success(request, 'Customer Support application Error!')
    return render(request, 'customersupport.html')


@login_required(login_url='login')
def transfer(request): 
    
    if request.method == 'POST':
        
        receiver_account_number = request.POST.get('bank_number')
        amount=float(request.POST.get('amount', 0))
        category = request.POST.get('category')
        
        current_user = request.user
        user_data = models.BankUser.objects.get(UserAccountNo=current_user.username)
        sender_account_number=user_data.UserAccountNo
        if sender_account_number==receiver_account_number:
            messages.success(request, 'Change Account Number')
            return redirect('transfer')
        else:    
            try:
                sender_account =models.BankAccount.objects.get(BankAccountNo=sender_account_number)
                receiver_account = models.BankAccount.objects.get(BankAccountNo=receiver_account_number)
                if amount>=25000:
                    messages.success(request, 'transfer Amount Limit Is 25000!')
                else:    
                    if sender_account.CurrentAmmount >= amount and amount > 0:
                        sender_account.CurrentAmmount -= amount
                        receiver_account.CurrentAmmount += amount
                        sender_account.save()
                        receiver_account.save()
                
                        transfer=models.UserTransaction(BankAccountNo=sender_account.BankAccountNo,ReceiverUserAccountNo=receiver_account.BankAccountNo,Ammount=amount,TransactionPurpose=category)
                        transfer.save()
                        messages.success(request, 'Transaction Completed Successfully!')
                    else:
                        print('error')
                        messages.success(request, 'Less Amount In Your Account!')
            except models.BankAccount.DoesNotExist:
                messages.success(request, 'Transaction Error!')
                return redirect('transfer') 
    
    return render(request, 'transfer.html')


@login_required(login_url='login')
def loan(request):
        if request.method == 'POST':
            
            amount=float(request.POST.get('amount', 0))
            category = request.POST.get('category')
            
            current_user = request.user
            user_data = models.BankAccount.objects.get(BankAccountNo=current_user.username)
            try:

                if amount < 25000:
                    
                    if user_data.CurrentAmmount<=150000:
                        
                        if user_data.UserLoanLimit<=50000:
                            user_data.CurrentAmmount=user_data.CurrentAmmount+amount
                            user_data.CurrentLoanAmmount=user_data.CurrentLoanAmmount+amount
                            user_data.UserLoanLimit=user_data.UserLoanLimit+amount
                            user_data.save()
                            loan=models.Loan(BankAccountNo=user_data.BankAccountNo,LoanAmmount=amount,LoanPurpose=category)
                            loan.save()
                        
                            messages.error(request, 'Loan application submitted successfully!')
                            return redirect('loan')
                        else:
                            messages.error(request, 'You Cross The Max Loan Limit!')
                            return redirect('loan')
                    else:
                        messages.error(request, 'You Have Much Amount In Your Account!')
                        return redirect('loan')
                else:
                    messages.success(request, 'Loan Amount Must Less Then 25,00!')
                    return redirect('loan')
            except models.BankAccount.DoesNotExist:
                messages.success(request, 'Loan application Error!')
            return redirect('loan')
        return render(request, 'loan.html')

def logoutPage(request):
    logout(request)
    return redirect('index')

@login_required(login_url='login')
def history(request):
    
    current_user = request.user
    user_data = models.BankUser.objects.get(UserAccountNo=current_user.username)
    
    transactions = UserTransaction.objects.filter(BankAccountNo=user_data).order_by('-TransactionDate')
    loans = Loan.objects.filter(BankAccountNo=user_data).order_by('-LoanDate')
    return render(request, 'history.html', {'transactions': transactions, 'loans': loans})
    
