from django.shortcuts import render
from main_app.models import Business 

# Create your views here.

def business(request):
    businesses=Business.objects.all()
    return render(request, 'business.html',{'businesses':businesses})

def business_detail(request,business_id):
    business=Business.objects.get(id=business_id)
    return render(request,'business_detail.html',{'business':business})

def profile(request):
    return render(request,'profile.html')