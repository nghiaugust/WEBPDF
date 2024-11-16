from rest_framework import serializers
from .models import PDFFile

class PDFFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFFile
        fields = '__all__'

class PDFConvertRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()