from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("contact/", views.contact, name="contact"),
    path("accounts/signup", views.signup, name="signup"),
    path("test/", views.test, name="test")
]
