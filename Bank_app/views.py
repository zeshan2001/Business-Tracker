from django.shortcuts import render
from main_app.models import Bank
# Create your views here.

def bank(request):
    
    return render(request, "bank.html")