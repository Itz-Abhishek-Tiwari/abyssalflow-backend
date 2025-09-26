from rest_framework.response import Response
from rest_framework.views import APIView
from apps.files.models import FileUploadModel
from .serializers import FilesSerializers
from rest_framework import status


class FileUploadView(APIView):
    def post(self, requests):
        serializer = FilesSerializers(data=requests.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        uploads = FileUploadModel.objects.all()
        serializer = FilesSerializers(uploads, many=True)
        return Response(serializer.data)
