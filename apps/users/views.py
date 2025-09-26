import rest_framework
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.models import UserProfile
from .serializers import UserProfileSerializer
from rest_framework import status


class UserProfileView(APIView):
    def get(self, request):
        userProfile = UserProfile.objects.all()
        serializer = UserProfileSerializer(userProfile, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
