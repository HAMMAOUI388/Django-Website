from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserLogin, Wallet, Expense, Transaction

# Unregister the default User model from the admin
admin.site.unregister(User)

# Register the custom User model admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('username', 'email')

# Register the UserLogin model with the custom admin
@admin.register(UserLogin)
class UserLoginAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'login_time')
    search_fields = ('user__email', 'ip_address')
