from django.urls import path
from . import views

urlpatterns = [
    path("", views.bank, name="bank"),
    path("request/", views.request_view, name="request"),
    path("request/<int:request_id>", views.request_detail, name="request_detail"),
    path("create_loan/", views.LoanCreate.as_view(), name="create_loan"),
]
