from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.models import UserProfile
from rest_framework import status
from integrations.supabase_client import upload_avatar
from .serializers import UserProfileSerializer


class UserProfileView(APIView):
    def get(self, request):
        users = UserProfile.objects.all()
        serializer = UserProfileSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        avatar_file = request.FILES.get("avatar")
        if avatar_file:
            avatar_url = upload_avatar(avatar_file, avatar_file.name)
            request.data["avatar"] = avatar_url

        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
