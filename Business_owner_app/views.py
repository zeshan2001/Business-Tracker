from django.shortcuts import render,get_object_or_404
from main_app.models import Business 

# Create your views here.

def business(request):
    businesses=Business.objects.all()
    return render(request, 'business.html',{'businesses':businesses})

def business_detail(request, business_id):
    business = get_object_or_404(Business, id=business_id)
    balance_sheets = business.balance_sheets.all()  
    income_statements = business.income_statements.all()
    context = {
        'business': business,
        'balance_sheets': balance_sheets,
        'income_statements': income_statements,
    }
    return render(request, 'business_detail.html', context)

def profile(request):
    return render(request,'profile.html')