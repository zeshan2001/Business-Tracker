from django.urls import path
from . import views

urlpatterns = [
    path("", views.business, name="Business"),
    path("profile", views.profile, name="Profile")
]
