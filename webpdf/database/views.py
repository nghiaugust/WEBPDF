from rest_framework import generics
from .models import VanBan
from .serializers import VanBanSerializer
from .models import Data
from .serializers import DataSerializer

# Thêm mới và xem danh sách các VanBan

class VanBanListCreateView(generics.ListCreateAPIView):
    queryset = VanBan.objects.all()
    serializer_class = VanBanSerializer

# Xem, sửa, xóa một VanBan cụ thể
class VanBanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = VanBan.objects.all()
    serializer_class = VanBanSerializer

# Thêm mới và xem danh sách các Data
class DataListCreateView(generics.ListCreateAPIView):
    queryset = Data.objects.all()
    serializer_class = DataSerializer

# Xem, sửa, xóa một Data cụ thể
class DataDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Data.objects.all()
    serializer_class = DataSerializer