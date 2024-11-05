from rest_framework.serializers import ModelSerializer
from .models import DuLieu

class DuLieuSerializer(ModelSerializer):
    class Meta:
        model = DuLieu
        fields = ["id", "don_vi_soan_thao", "so_ky_hieu", "nguoi_ky", "ngay_ban_hanh"]