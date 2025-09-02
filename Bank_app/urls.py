from django.urls import path
from . import views

urlpatterns = [
    path("", views.bank, name="bank"),
    path("request/", views.request_view, name="request"),
    path("request/<int:request_id>", views.request_detail, name="request_detail"),
    path("create_loan/", views.LoanCreate.as_view(), name="create_loan"),
    path("request/<int:pk>/update", views.RequestUpdate.as_view(), name="request_update"),
    path("request-detail/<int:business_id>/", views.RequstDetail.as_view(), name="request_detail_loan"),
    path("profile/", views.ProfileDetail.as_view(), name="Bank_Profile"),
    path("profile/update/", views.ProfileUpdate.as_view(), name="Bank_Profile_Update"),
]
