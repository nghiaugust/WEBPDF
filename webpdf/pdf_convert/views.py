from rest_framework import viewsets
from .models import PDFFile
from .serializers import PDFFileSerializer

class PDFFileViewSet(viewsets.ModelViewSet):
    queryset = PDFFile.objects.all()
    serializer_class = PDFFileSerializer