from django.db import models
from django.contrib.auth.models import User

# Create your models for Business here.
class Business(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    brand=models.CharField(max_length=255)




class Balance_sheet(models.Model):
    business_id=models.ForeignKey(Business.business_id,on_delete=models.CASCADE)
    current_assets=models.FloatField()