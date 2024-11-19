from django.db import models

class PDFFile(models.Model):
    name = models.CharField(max_length=255)
    original_file = models.FileField(upload_to='pdfdata/')
    converted_file = models.FileField(upload_to='pdfconvert/', blank=True, null=True)
    text_content = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name