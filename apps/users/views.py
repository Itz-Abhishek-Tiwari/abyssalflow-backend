from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.models import UserProfile
from .serializers import UserProfileSerializer


class UserProfileView(APIView):
    def get(self, request):
        userProfile = UserProfile.objects.all()
        serializer = UserProfileSerializer(userProfile, many=True)
        return Response(serializer.data)
