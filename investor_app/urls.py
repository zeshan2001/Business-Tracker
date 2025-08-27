from django.urls import path
from . import views

urlpatterns = [
    path("investor/", views.investor, name="investor"),
    path("investor/profie", views.investor, name="investor"),
]
