from django.shortcuts import render

from rest_framework import status, permissions, views, generics, parsers, response

from .models import Profile

from .serializers import UserProfileSerializer


class UserProfileUpdateView(views.APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserProfileSerializer
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]

    def get(self, request, id):
        profile = Profile.objects.get(id=id)
        serializer = UserProfileSerializer(profile)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        profile = Profile.objects.get(id=id)
        serializer = UserProfileSerializer(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_200_OK)
    
    