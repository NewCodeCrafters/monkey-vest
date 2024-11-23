from django.urls import path

from . import views


urlpatterns = [
    path("notification-history", views.UserNotificationHistoryView.as_view()),
]
