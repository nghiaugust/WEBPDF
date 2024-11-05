from django.shortcuts import render
from .models import DuLieu
from .forms import DuLieuForm
from rest_framework import viewsets
from .serializers import DuLieuSerializer
# Create your views here.

class DuLieuViewSet(viewsets.ModelViewSet):
    queryset = DuLieu.objects.all()
    serializer_class = DuLieuSerializer

def home(request):
    dulieu_list = DuLieu.objects.all()   
    dulieu = DuLieu.objects.first()
    form = DuLieuForm(instance = dulieu)
    return render(request, 'app/home.html', {'dulieu_list': dulieu_list, 'form':form})
