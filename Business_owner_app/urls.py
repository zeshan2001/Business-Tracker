from django.urls import path
from . import views

urlpatterns = [
    path("", views.business, name="business"),
    path('<int:business_id>/',views.business_detail, name='business_detail'),
    path('create/',views.business_Create.as_view(),name='business_Create'),
    path('create/<int:pk>/updata/',views.business_Updata.as_view(),name='business_updata'),
    path('<int:pk>/delete/',views.business_Delete.as_view(),name='business_delete'),
    path("profile", views.profile, name="Profile")
]
