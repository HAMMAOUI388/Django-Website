from django.shortcuts import render, redirect
from networkx import reverse
from .models import Wallet, Transaction
from .forms import ExpenseForm
from .models import Expense
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import UserLogin
from django.http import HttpResponse
from .forms import RegisterForm
from django.contrib.auth.models import User
from .forms import EmailAuthenticationForm



def dashboard_view(request):
    user_wallet = Wallet.objects.get(user=request.user)
    return render(request, 'myapp/index.html', {'wallet': user_wallet})




def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Log user login attempt with IP address
            UserLogin.objects.create(
                user=user,
                ip_address=request.META.get('REMOTE_ADDR')
            )

            # Redirect to 'next' or default to the dashboard
            next_url = request.GET.get('next', 'index')
            if not next_url.startswith('/'):  # Prevent redirect loops
                next_url = 'index'
            return redirect(next_url)
        else:
            errors = [error for error_list in form.errors.values() for error in error_list]
            for error in errors:
                messages.error(request, error)
    else:
        form = EmailAuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})



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

        # Success message
        messages.success(request, "Account created successfully! Please log in below.")
        return redirect('login')

    return render(request, 'myapp/register.html')
