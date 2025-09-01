from django.urls import path
from . import views

urlpatterns = [
    # dashborad
    path("", views.investor_dashborad, name="investor_dashborad"), 
    # investment detail
    path('investments/<int:business_id>', views.investment_detail, name='investment_detail'), 
    # profile
    # path("profile/<int:user_id>", views.investor_detail, name="investor_profile"),
    path("profile/", views.ProfileDetail.as_view(), name="Investor_Profile"),
    path("profile/update/", views.ProfileUpdate.as_view(), name="Investor_Profile_Update"),
    path("profile/delete/", views.ProfileDelete.as_view(), name="Investor_Profile_Delete"),
]

