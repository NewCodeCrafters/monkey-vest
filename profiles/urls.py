from django.urls import path

from . import views

urlpatterns = [
    path("update-profile/<int:id>/", views.UserProfileUpdateView.as_view()),
]
