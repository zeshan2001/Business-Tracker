from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models for Business here.

REQUEST_CHOICE = (
    ("P", "Panding"),
    ("A", "Accepted"),
    ("R", "Rejected")
)

class Business(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    brand=models.CharField(max_length=255)

    def __str__(self):
        return self.brand

class Balance_sheet(models.Model):
    business_id=models.ForeignKey(Business,on_delete=models.CASCADE)
    current_assets=models.DecimalField(max_digits=12,decimal_places=2)
    non_current_assets=models.DecimalField(max_digits=12,decimal_places=2)
    cash_equivalents=models.DecimalField(max_digits=12,decimal_places=2)
    current_liabilities=models.DecimalField(max_digits=12,decimal_places=2)
    non_current_liabilities=models.DecimalField(max_digits=12,decimal_places=2)
    shareholders_equity=models.DecimalField(max_digits=12,decimal_places=2)

class Income_statement(models.Model):
    business_id=models.ForeignKey(Business,on_delete=models.CASCADE)
    revenue=models.DecimalField(max_digits=12,decimal_places=2)
    cogs=models.DecimalField(max_digits=12,decimal_places=2)
    operating_expenses=models.DecimalField(max_digits=12,decimal_places=2)
    net_income=models.DecimalField(max_digits=12,decimal_places=2)


class Bank(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)

    def __str__(self):
        return self.name

class Loan(models.Model):
    business_id = models.ForeignKey(Business, on_delete=models.CASCADE)
    bank_id = models.ForeignKey(Bank, on_delete=models.CASCADE)
    loan_amount = models.DecimalField(max_digits=12 ,decimal_places=2)
    interest_rate = models.DecimalField(max_digits=3, decimal_places=2)
    start_date= models.DateField
    end_date = models.DateField

    def __str__(self):
        return f"Loan to {self.business_id.user_id.username} brand {self.business_id.brand}"

class Request(models.Model):
    business_id=models.ForeignKey(Business,on_delete=models.CASCADE)
    bank_id=models.ForeignKey(Bank,on_delete=models.CASCADE)
    borrow_amount=models.DecimalField(max_digits=12,decimal_places=2)
    description=models.CharField(max_length=255)
    status=models.CharField(max_length=1, choices=REQUEST_CHOICE, default=REQUEST_CHOICE[0][0])

    def __str__(self):
        return f"request from {self.business_id.user_id.username} brand {self.business_id.brand}"