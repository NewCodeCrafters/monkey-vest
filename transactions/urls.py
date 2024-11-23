from django.urls import path

from . import views

urlpatterns = [
    path('deposit-history/', views.UserDepositView.as_view()),
    path('deposit/', views.CreateDepositView.as_view()),
    path('withdrawal/', views.CreateWithdrawalView.as_view()),
    path('withdrawal-history/', views.UserWithdrawalView.as_view()),
    path('my-transfers/<int:source_account_number>/', views.UserTransferViews.as_view()),
    path('create-transfer/<int:source_account_number>/', views.CreateTransferView.as_view()),
    
]
