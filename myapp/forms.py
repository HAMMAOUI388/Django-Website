from django import forms
from .models import Expense
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

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
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'autofocus': True}))

    def clean_username(self):
        email = self.cleaned_data.get('username')
        user = get_user_model().objects.filter(email=email).first()
        
        if not user:
            raise forms.ValidationError("No user found with that email address.")
        if not user.is_active:
            raise forms.ValidationError("This account is inactive.")
        return email
