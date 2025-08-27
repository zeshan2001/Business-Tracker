from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileForm
from django.conf import settings
from .forms import ContactForm
import smtplib
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

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

                subject = f'Message from {email}'
                body = message

                subject_auto = "We Received Your Request"
                body_auto = "Thank you for reaching out to us. Our team will contact you soon."

                msg = f"Subject: {subject}\n\n{body}"
                msg_auto = f"Subject: {subject_auto}\n\n{body_auto}"

                smtp.sendmail(email, settings.EMAIL_HOST_USER, msg)

                smtp.sendmail(settings.EMAIL_HOST_USER, email, msg_auto)

            return redirect("")
    else:
        form = ContactForm()

        return render(request, "contact.html", {"form": form})