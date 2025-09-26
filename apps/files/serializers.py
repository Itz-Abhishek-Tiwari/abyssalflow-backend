from rest_framework import serializers
from apps.files.models import FileUploadModel


class FilesSerializers(serializers.ModelSerializer):
    class Meta:
        model = FileUploadModel
        fields = "__all__"
