from django.urls import path

from . import views

urlpatterns = [
    path("main-account/", views.GetMainAccountView.as_view()),
]
