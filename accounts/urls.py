from django.urls import path

from . import views

urlpatterns = [
    path("main-account/", views.GetMainAccountsSerializer.as_view()),
]
