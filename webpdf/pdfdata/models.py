from django.db import models

# Create your models here.
class PDFFile(models.Model):
    name = models.CharField(max_length=50)
    pdf_url = models.URLField()  # URL của file PDF
    file_path = models.FileField(upload_to='pdfs/', null=True, blank=True)  # Đường dẫn lưu trữ file PDF

    def __str__(self):
        return self.name