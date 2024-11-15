from django.shortcuts import render, redirect
from .forms import PDFUploadForm
from .models import PDFFile
from .tasks import perform_ocr

def upload_file(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.save(commit=False)
            output_format = form.cleaned_data["output_format"]
            pdf_file.save()  # Lưu lại PDFFile trước khi chuyển đổi
            print("luu thanh cong")
            # Thực hiện OCR và chuyển đổi
            perform_ocr(pdf_file, output_format=output_format)
            print("chuyen doi thanh cong")
            return redirect('pdf_converter:file_list')  # Chuyển đến trang danh sách file
    else:
        form = PDFUploadForm()
    return render(request, 'ocr/upload.html', {'form': form})

def file_list(request):
    files = PDFFile.objects.all()
    return render(request, 'ocr/file_list.html', {'files': files})