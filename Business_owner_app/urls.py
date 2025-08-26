from django.urls import path
from . import views

urlpatterns = [
    path("", views.business, name="business"),
    path('<int:business_id>/',views.business_detail, name='business_detail'),
    path('create/',views.business_Create.as_view(),name='business_Create'),
    path("profile", views.profile, name="Profile")
]
