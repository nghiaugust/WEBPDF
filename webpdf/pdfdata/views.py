import os
from django.conf import settings
from django.shortcuts import render
import requests
from django.http import HttpResponse
from .models import PDFFile
# Create your views here.
def pdfdata(request):
    return render(request, 'pdfdata/pdfdata.html')

def download_pdf(request):
    if request.method == 'POST':
        try:
            # Đăng nhập để lấy access token
            login_url = 'https://backend8181.bcy.gov.vn/api/users/login'
            login_data = {'userName': 'ldthuan@bcy.gov.vn', 'password': '123456'}
            response = requests.post(login_url, json=login_data, verify=False)
            response.raise_for_status()  # Kiểm tra mã trạng thái HTTP để phát hiện lỗi
            
            if response.status_code == 200:
                json_response = response.json()
                access_token = json_response['data']['tokenInfo']['accessToken']
                headers = {
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                }

                # Gọi API để lấy danh sách tài liệu
                try:
                    documents_url = 'https://backend8181.bcy.gov.vn/api/document_out/knowable?page=2&sortBy=&direction=DESC&size=10&read=false'
                    response_docs = requests.get(documents_url, headers=headers, verify=False)
                    response_docs.raise_for_status()  # Kiểm tra mã trạng thái của tài liệu
                except requests.exceptions.RequestException as e:
                    print("Không thể lấy danh sách tài liệu:", e)
                    return HttpResponse("Lỗi khi lấy danh sách tài liệu")

                # Kiểm tra dữ liệu phản hồi của tài liệu
                if response_docs.status_code == 200:
                    data = response_docs.json()
                    # Lặp qua từng file trong danh sách và tải về
                    for obj in data['data']['content']:
                        for attachment in obj['attachments']:
                            name = attachment['name']
                            download_url = f'https://backend8181.bcy.gov.vn/api/doc_out_attach/download/{name}'
                            
                            try:
                                response_download = requests.get(download_url, headers=headers, verify=False)
                                response_download.raise_for_status()  # Kiểm tra mã trạng thái của từng file
                            except requests.exceptions.RequestException as e:
                                print(f"Lỗi khi tải file {name}:", e)
                                continue  # Bỏ qua file lỗi và tiếp tục với file tiếp theo

                            # Nếu tải thành công, lưu file vào hệ thống
                            if response_download.status_code == 200:
                                try:
                                    clean_name = name.split('__')[0]  # Lấy tên file sau khi làm sạch
                                    file_path = os.path.join(settings.MEDIA_ROOT, clean_name)
                                    with open(file_path, 'wb') as file:
                                        file.write(response_download.content)
                                    
                                    # Lưu thông tin file vào cơ sở dữ liệu
                                    PDFFile.objects.create(name=clean_name, pdf_url=download_url, file_path=file_path)
                                except Exception as e:
                                    print(f"Lỗi khi lưu file {clean_name}:", e)
                                    continue  # Bỏ qua nếu có lỗi khi lưu file
                    return HttpResponse("All files downloaded and saved successfully")
                else:
                    return HttpResponse("Failed to retrieve document list")
            else:
                return HttpResponse("Login failed")
        except requests.exceptions.RequestException as e:
            print("Không thể truy cập vào trang web hoặc lỗi kết nối:", e)
            return HttpResponse("Không thể truy cập vào trang đăng nhập")
    return HttpResponse("Invalid request")

