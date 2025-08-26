from django.urls import path
from . import views

urlpatterns = [
    path("", views.business, name="Business"),
    path('<int:business_id>/',views.business_detail, name='business_detail'),
    path("profile", views.profile, name="Profile")
]
