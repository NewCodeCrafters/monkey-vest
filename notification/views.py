from django.shortcuts import render

from rest_framework import permissions, response, status, views

from .serializers import NotificationSerializer
from .models import Notification


class UserNotificationHistoryView(views.APIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(user=user)
        serializer = NotificationSerializer(notifications, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

