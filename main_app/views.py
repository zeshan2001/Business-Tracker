from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileForm
# Create your views here.

class CustomLoginView(LoginView):
    template_name = "registration/login.html"

    def get_success_url(self):
        print("CustomLoginView get_success_url called") 
        user = self.request.user
        profile = getattr(user, "profile", None) # get related Profile

        if profile:
            if profile.role == "B":
                return reverse_lazy("business")
            elif profile.role == "I":
                return reverse_lazy("investor")
            elif profile.role == "L":
                return reverse_lazy("bank")
            
        return reverse_lazy("home")

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request, "contact.html")

def signup(request):
    error_message = ""
    if request.method == "POST":
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            login(request, user)
            if (profile.role == "B"):
                return redirect("/business/")
            elif(profile.role == "I"):
                return redirect("/investor/")
        else:
            error_message = "Invalid Signup - Try Again..."
    else:
        user_form = UserCreationForm()
        profile_form = ProfileForm()

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
        "error_message": error_message,
    }
    return render(request, "registration/signup.html", context)

