from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Image
from .serializers import ImageSerializer
from django.shortcuts import render

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

def get_image(request):
    return render(request, 'testimage/image.html')
