from django.urls import path
from . import views

urlpatterns = [
    path("", views.business, name="business"),
    path('<int:business_id>/',views.business_detail, name='business_detail'),
    path('income_statement/create/<int:business_id>/',views.income_statement.as_view(), name='income_statement'),
    path('balance_sheet/create/<int:business_id>/',views.balance_sheet.as_view(), name='balance_sheet'),
    path('balance_sheet/updata/<int:pk>/',views.balance_sheet_Update.as_view(), name='balance_sheet_Update'),
    path('balance_sheet/delete/<int:pk>/',views.balance_sheet_Delete.as_view(), name='balance_sheet_Delete'),
    path('create/',views.business_Create.as_view(),name='business_Create'),
    path('create/<int:pk>/updata/',views.business_Updata.as_view(),name='business_updata'),
    path('<int:pk>/delete/',views.business_Delete.as_view(),name='business_delete'),
    path("profile", views.profile, name="Profile")
]
