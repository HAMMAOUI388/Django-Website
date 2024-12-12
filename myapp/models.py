from django.db import models
from django.contrib.auth.models import User



class UserLogin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    login_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.login_time} - {self.user_agent}"


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    expenses = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    savings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Wallet"

    def update_savings(self):
        """Update the user's savings automatically."""
        self.savings = self.salary - self.expenses
        self.save()

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction for {self.user.username} - {self.category} - ${self.amount}"


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.amount}"
