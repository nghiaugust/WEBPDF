from django import forms
from .models import DuLieu

class DuLieuForm(forms.ModelForm):
    class Meta:
        model = DuLieu
        fields = ['don_vi_soan_thao', 'so_ky_hieu', 'nguoi_ky', 'ngay_ban_hanh']