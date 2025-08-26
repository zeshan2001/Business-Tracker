from django.db import models
from django.contrib.auth.models import User

# Create your models for Business here.
class Business(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    brand=models.CharField(max_length=255)




class Balance_sheet(models.Model):
    business_id=models.ForeignKey(Business.business_id,on_delete=models.CASCADE)
    current_assets=models.DecimalField(max_digits=12,decimal_places=2)
    non_current_assets=models.DecimalField(max_digits=12,decimal_places=2)
    cash_equivalents=models.DecimalField(max_digits=12,decimal_places=2)
    current_liabilities=models.DecimalField(max_digits=12,decimal_places=2)
    non_current_liabilities=models.DecimalField(max_digits=12,decimal_places=2)
    shareholders_equity=models.DecimalField(max_digits=12,decimal_places=2)

class income_statement(models.Model):
    business_id=models.ForeignKey(Business.business_id,on_delete=models.CASCADE)
    revenue=models.DecimalField(max_digits=12,decimal_places=2)
    cogs=models.DecimalField(max_digits=12,decimal_places=2)
    operating_expenses=models.DecimalField(max_digits=12,decimal_places=2)
    net_income=models.DecimalField(max_digits=12,decimal_places=2)
