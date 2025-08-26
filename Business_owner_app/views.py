from django.shortcuts import render

# Create your views here.

def business(request):
    return render(request, "business.html")

def profile(request):
    return render(request,'profile.html')