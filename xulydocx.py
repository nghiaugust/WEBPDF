from docx import Document
import os
from PIL import Image
import pytesseract
from io import BytesIO

def extract_text_from_image(image_data):
    """Trích xuất văn bản từ dữ liệu ảnh bằng OCR."""
    try:
        image = Image.open(BytesIO(image_data))  # Mở ảnh từ dữ liệu nhị phân
        text = pytesseract.image_to_string(image, lang='eng+vie')  # Hỗ trợ tiếng Anh và tiếng Việt
        return text.strip()
    except Exception as e:
        return f"Error reading image: {e}"

def process_docx(file_path, output_text_file):
    """Đọc văn bản và văn bản trong ảnh từ file .docx và ghi vào file .txt."""
    doc = Document(file_path)

    with open(output_text_file, 'w', encoding='utf-8') as output_file:
        text_found = False  # Biến đánh dấu có văn bản hay không

        # Duyệt qua từng đoạn văn và ghi nội dung vào file
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():  # Nếu có văn bản trong đoạn
                output_file.write(paragraph.text + '\n')
                text_found = True

        # Nếu không tìm thấy văn bản, ghi thông báo
        if not text_found:
            output_file.write("[No text found in document. Checking for images...]\n")

        # Duyệt qua từng thành phần liên quan (images)
        for rel in doc.part.rels.values():
            if "image" in rel.target_ref:  # Tìm các liên kết liên quan đến ảnh
                try:
                    # Lấy dữ liệu ảnh từ các liên kết
                    image_part = doc.part.related_parts[rel.target_ref]
                    image_data = image_part.blob

                    # OCR ảnh và ghi kết quả
                    ocr_text = extract_text_from_image(image_data)
                    output_file.write('\n[Extracted text from image]\n')
                    output_file.write(ocr_text + '\n')
                except Exception as e:
                    output_file.write(f"\n[Error processing image: {e}]\n")

# Đường dẫn file đầu vào và file đầu ra
docx_file = 'input.docx'  # Thay bằng đường dẫn file .docx của bạn
output_text_file = 'output.txt'

# Cấu hình pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Đường dẫn tới Tesseract

# Gọi hàm xử lý
process_docx(docx_file, output_text_file)

print(f'Hoàn tất xử lý file {docx_file}. Kết quả được lưu ở {output_text_file}.')
