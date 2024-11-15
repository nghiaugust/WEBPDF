from django import forms
from .models import PDFFile

class PDFUploadForm(forms.ModelForm):
    output_format = forms.ChoiceField(
        choices=[("pdf", "PDF"), ("word", "Word")],
        label="Chọn định dạng chuyển đổi",
    )

    class Meta:
        model = PDFFile
        fields = ['file', 'lang']