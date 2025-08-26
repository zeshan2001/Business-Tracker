from django.urls import path
from . import views

urlpatterns = [
    path("business/", views.business, name="business")
]
