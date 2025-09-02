from django.db import models
from django.contrib.auth.models import User


# Create your models for Business here.

REQUEST_CHOICE = (
    ("P", "Panding"),
    ("A", "Accepted"),
    ("R", "Rejected")
)

ROLE_CHOICE = (
    ("B", "Business Owner"),
    ("I", "Investor"),
    ("L", "Line Manager")
)

class Business(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    brand=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    image=models.ImageField(upload_to='main_app/static/uploads/', default='')
    init_cost=models.DecimalField(max_digits=12,decimal_places=3)

    def __str__(self):
        return f"{self.brand} (Owner: {self.user.username})"

class Balance_sheet(models.Model):
    business=models.ForeignKey(Business,on_delete=models.CASCADE,related_name='balance_sheets')
    current_assets=models.DecimalField(max_digits=12,decimal_places=2)
    non_current_assets=models.DecimalField(max_digits=12,decimal_places=2)
    cash_equivalents=models.DecimalField(max_digits=12,decimal_places=2)
    current_liabilities=models.DecimalField(max_digits=12,decimal_places=2)
    non_current_liabilities=models.DecimalField(max_digits=12,decimal_places=2)
    shareholders_equity=models.DecimalField(max_digits=12,decimal_places=2)
    year=models.CharField(max_length=4)

class Income_statement(models.Model):
    business=models.ForeignKey(Business,on_delete=models.CASCADE,related_name='income_statements')
    revenue=models.DecimalField(max_digits=12,decimal_places=2)
    non_cash_expense = models.DecimalField(max_digits=12, decimal_places=2)
    cogs=models.DecimalField(max_digits=12,decimal_places=2)
    operating_expenses=models.DecimalField(max_digits=12,decimal_places=2)
    net_income=models.DecimalField(max_digits=12,decimal_places=2)
    year=models.CharField(max_length=4)


class Bank(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)

    def __str__(self):
        return self.name

class Loan(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    loan_amount = models.DecimalField(max_digits=12 ,decimal_places=2)
    interest_rate = models.DecimalField(max_digits=3, decimal_places=2)
    start_date= models.DateField(auto_now_add=True)
    end_date = models.DateField(editable=False)

    def __str__(self):
        return f"Loan to {self.business.user.username} brand {self.business.brand}"

class Request(models.Model):
    business=models.ForeignKey(Business,on_delete=models.CASCADE)
    bank=models.ForeignKey(Bank,on_delete=models.CASCADE)
    borrow_amount=models.DecimalField(max_digits=12,decimal_places=2)
    description=models.CharField(max_length=255)
    status=models.CharField(max_length=1, choices=REQUEST_CHOICE, default=REQUEST_CHOICE[0][0])

    def __str__(self):
        return f"request from {self.business.user.username} brand {self.business.brand}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bank = models.OneToOneField(Bank, on_delete=models.CASCADE, null=True, blank=True)

    role = models.CharField(max_length=1, choices=ROLE_CHOICE, default=ROLE_CHOICE[0][0])
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)

    def __str__(self):
        return self.user.username