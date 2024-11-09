from django.urls import path

from . import views

urlpatterns = [
    path("main-account/", views.GetMainAccountView.as_view()),
    path("all-my-accounts/", views.GetAllUsersAccountView.as_view()),
    path("create-new-account-type/", views.CreateNewAccountView.as_view()),
]
