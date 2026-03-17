from rest_framework import serializers
from .models import UserFile

class UserFileSerializer(serializers.ModelSerializer):
    file_size = serializers.IntegerField(source='file.file_size')

    class Meta:
        model = UserFile
        fields = ['id', 'file_name', 'file_size', 'uploaded_at']