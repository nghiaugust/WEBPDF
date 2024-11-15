import uuid
from django.db import models

class PDFFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='pdfs/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    converted_file = models.FileField(upload_to='converted/', null=True, blank=True)
    lang = models.CharField(max_length=10, default="eng")
    status = models.CharField(max_length=10, default="pending")

    def __str__(self):
        return f"{self.file.name}"