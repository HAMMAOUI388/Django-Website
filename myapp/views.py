import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .models import Wallet, Expense
from .forms import ExpenseForm

def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError("Type not serializable")

@login_required
def dashboard_view(request):
    # Check if the user has a wallet
    user_wallet, created = Wallet.objects.get_or_create(user=request.user, defaults={
        'salary': 0.00,
        'expenses': 0.00,
        'savings': 0.00,
    })

    # Fetch monthly expenses inside the view
    monthly_expenses = Expense.objects.filter(user=request.user) \
        .annotate(month=TruncMonth('date')) \
        .values('month') \
        .annotate(expenses=Sum('amount'))

    monthly_data = {'labels': [], 'expenses': [], 'savings': []}
    for month_data in monthly_expenses:
        monthly_data['labels'].append(month_data['month'].strftime('%Y-%m'))  # Format month
        monthly_data['expenses'].append(decimal_to_float(month_data['expenses']))
        monthly_data['savings'].append(decimal_to_float(user_wallet.savings))

    # Handle POST requests for salary and expenses
    if request.method == 'POST':
        if 'save_salary' in request.POST:
            # Handle salary input
            salary_amount = request.POST.get('salaryAmount')
            if salary_amount:
                user_wallet.salary = float(salary_amount)
                user_wallet.savings = user_wallet.salary  # Set savings equal to salary initially
                user_wallet.save()
                messages.success(request, "Salary updated successfully!")

        elif 'add_expense' in request.POST:
            # Handle expense input
            expense_form = ExpenseForm(request.POST)
            if expense_form.is_valid():
                expense = expense_form.save(commit=False)
                expense.user = request.user
                expense.save()

                # Update the user's wallet
                user_wallet.expenses += expense.amount
                user_wallet.savings -= expense.amount  # Reduce savings based on the expense
                user_wallet.save()

                messages.success(request, "Expense added successfully!")

    # Fetch expense data
    expenses = Expense.objects.filter(user=request.user).all()

    # Prepare data for charts
    categories = Expense.objects.filter(user=request.user).values('category').annotate(total=Sum('amount'))
    category_data = {'labels': [], 'values': []}
    for category in categories:
        category_data['labels'].append(category['category'])
        category_data['values'].append(decimal_to_float(category['total']))

    return render(request, 'myapp/index.html', {  # Render the 'index.html' template
        'wallet': user_wallet,
        'expense_form': ExpenseForm(),
        'expenses': expenses,
        'category_data': json.dumps(category_data),
        'monthly_data': json.dumps(monthly_data)
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'myapp/login.html')

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Create a wallet for the new user
        if not Wallet.objects.filter(user=user).exists():
            wallet = Wallet(user=user)
            wallet.save()

        # Success message
        messages.success(request, "Account created successfully! Please log in below.")
        return redirect('login')

    return render(request, 'myapp/register.html')
