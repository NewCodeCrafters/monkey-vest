from django.urls import path

from . import views

urlpatterns = [
    path('deposit-history/', views.UserDepositView.as_view()),
    path('deposit/', views.CreateDepositView.as_view()),
    path('withdrawal/', views.CreateWithdrawalView.as_view()),
    path('withdrawal-history/', views.UserWithdrawalView.as_view()),
    path('transfer/', views.UserTransferView.as_view()),
    path('transfer-history/', views.CreateTransferView.as_view())

]
