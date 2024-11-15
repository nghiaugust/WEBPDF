import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from .models import PDFFile
from django.conf import settings  # Giả sử config của bạn nằm trong api/settings.py
from .document import Document  # Import class Document từ nơi bạn định nghĩa

def perform_ocr(pdf_file: PDFFile, output_format="pdf"):
    # Đường dẫn file đầu vào và đầu ra
    input_path = Path(pdf_file.file.path)
    output_dir = Path("media/converted")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{pdf_file.id}.{output_format}"
    output_json_path = output_dir / f"{pdf_file.id}.json"
    output_txt_path = output_dir / f"{pdf_file.id}.txt"

    # Khởi tạo Document
    document = Document(
        pid=pdf_file.id,
        lang={pdf_file.lang},
        status="pending",
        input=input_path,
        output=output_path,
        output_json=output_json_path,
        output_txt=output_txt_path,
        created=datetime.now(),
        expire=datetime.now() + timedelta(days=1)
    )

    # Thực hiện OCR
    document.ocr(output_format=output_format)
    
    # Cập nhật model với trạng thái và đường dẫn file đầu ra
    pdf_file.status = document.status
    pdf_file.converted_file.name = f"converted/{pdf_file.id}.{output_format}"
    pdf_file.save()