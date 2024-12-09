from django.shortcuts import render, redirect
from .models import Wallet, Transaction
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    # Get or create the user's wallet
    wallet, created = Wallet.objects.get_or_create(user=request.user)

    # Retrieve all transactions for the user
    transactions = Transaction.objects.filter(user=request.user)

    # Pass wallet and transactions data to the index.html
    return render(request, 'index.html', {
        'wallet': wallet,
        'transactions': transactions,
    })

@login_required
def add_salary(request):
    if request.method == 'POST':
        # Get the salary from the POST request
        salary = request.POST.get('salaryAmount')

        # Get or create the user's wallet and update salary
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        wallet.salary = float(salary)
        wallet.update_savings()

        return redirect('index')  # Redirect back to the index page
    return redirect('index')

@login_required
def add_expense(request):
    if request.method == 'POST':
        # Get category and amount from the POST request
        category = request.POST.get('expenseCategory')
        amount = request.POST.get('expenseAmount')

        # Create a new transaction
        Transaction.objects.create(
            user=request.user,
            amount=float(amount),
            category=category,
        )

        # Update the wallet's expense and savings
        wallet = Wallet.objects.get(user=request.user)
        wallet.expenses += float(amount)
        wallet.update_savings()

        return redirect('index')  # Redirect back to the index page
    return redirect('index')
