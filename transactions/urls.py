from django.urls import path

from . import views

urlpatterns = [
    path('deposit-history/', views.UserDepositView.as_view()),
    path('deposit/', views.CreateDepositView.as_view()),

]
