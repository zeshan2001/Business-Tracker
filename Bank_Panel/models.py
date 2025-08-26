from django.db import models
from ..Business_owner.models import Business
from datetime import date
# Create your models for Bank Panel here.

class Bank(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.IntegerField(max_length=12)

class Loan(models.Model):
    business_id = models.ForeignKey(Business)
    bank_id = models.ForeignKey(Bank)
    loan_amount = models.DecimalField(max_digits=12 ,decimal_places=2)
    interest_rate = models.DecimalField(max_digits=1, decimal_places=2)
    start_date= models.DateField
    end_date = models.DateField
