from django.shortcuts import render

# Create your views here.

def investor(request):
    return render(request, "investor.html")