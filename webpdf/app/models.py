from django.db import models

# Create your models here.
class DuLieu(models.Model):
    don_vi_soan_thao = models.CharField(max_length=100)
    so_ky_hieu = models.CharField(max_length=30)
    nguoi_ky = models.CharField(max_length=100)
    ngay_ban_hanh = models.DateField()

    def __str__(self):
        return self.nguoi_ky