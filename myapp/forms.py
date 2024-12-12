from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'placeholder': 'e.g., 200'}),
            'category': forms.TextInput(attrs={'placeholder': 'e.g., Food, Rent'}),
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email address',
    }))

class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'autofocus': True}),
        error_messages={'required': 'Email is required.'}
    )

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
