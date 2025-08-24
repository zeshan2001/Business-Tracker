from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="contact"),
    path("sign-up/", views.sign_up, name="sign-up"),
    path("sign-in/", views.sign_in, name="sign-in")
]
