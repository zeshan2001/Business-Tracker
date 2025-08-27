from django.urls import path
from . import views

urlpatterns = [
    # dashborad
    path("", views.investor_dashborad, name="investor_dashborad"), 
    # investment detail
    path('investments/', views.investment_detail, name='investment_detail'), 
    path('investments/<int:user_id>', views.investment_detail, name='investment_detail'), 
    # profile
    path("profile/", views.investor_detail, name="investor_profile"),
    path("profile/<int:user_id>", views.investor_detail, name="investor_profile"),
]

