from django.db import models

# Create your models here.
class VanBan(models.Model):
    # Các trường của VanBan
    ngay_ban_hanh = models.BigIntegerField()  # "dateIssued"
    id_api = models.IntegerField(unique=True)  # "id"
    so_ky_hieu = models.CharField(max_length=255)  # "numberOrSign"
    loai_van_ban = models.CharField(max_length=100)  # "docTypeName"
    nguoi_tao = models.CharField(max_length=100)  # "personEnterName"
    trich_yeu = models.TextField()  # "preview"
    don_vi_soan_thao = models.CharField(max_length=255)  # "orgCreateName"
    so_van_ban = models.CharField(max_length=255)  # "bookName"
    do_mat = models.CharField(max_length=50)  # "docSecurityName"
    do_khan = models.CharField(max_length=50)  # "docUrgentName"
    nguoi_ky = models.CharField(max_length=255)  # "signerName"
    so_luong_data = models.IntegerField(default=0)  
    active = models.BooleanField(default=True)  

    def __str__(self):
        return f"{self.so_ky_hieu} - {self.loai_van_ban}"


class Data(models.Model):
    # Trường liên kết với VanBan
    van_ban = models.ForeignKey(VanBan, on_delete=models.CASCADE, related_name='data')  
    # Các trường của Data
    name = models.CharField(max_length=255)  # "displayName"
    type = models.CharField(max_length=50)  # "type"
    original_file = models.FileField(upload_to='pdfdata/', blank=True, null=True)
    converted_file = models.FileField(upload_to='pdfconvert/', blank=True, null=True)
    text_content = models.TextField()  # Nội dung text
    active = models.BooleanField(default=True)  
    convert = models.BooleanField(default=False)  
    clean = models.BooleanField(default=False)  

    def __str__(self):
        return self.name