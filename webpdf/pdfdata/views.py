import os
from django.conf import settings
from django.shortcuts import render
import requests
from django.http import HttpResponse
from .models import PDFFile
from database.models import VanBan, Data
import logging
from django.views.decorators.csrf import csrf_exempt
import urllib3
from django.http import JsonResponse
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

# Hàm đăng nhập và lấy token
def login_and_get_token():
    login_url = 'https://backend8181.bcy.gov.vn/api/users/login'
    login_data = {'userName': 'ldthuan@bcy.gov.vn', 'password': '123456'}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'PostmanRuntime/7.42.0',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }
    try:
        response = requests.post(login_url, data=login_data, headers=headers, verify=False)
        response.raise_for_status()
        return response.json()['data']['tokenInfo']['accessToken']
    except requests.exceptions.RequestException as e:
        logging.error("Lỗi khi kết nối: %s", e)
        raise

# Hàm tải tài liệu theo từng trang-> lấy json của api ngoài
def download_documents(headers, page, size):
    base_url = 'https://backend8181.bcy.gov.vn/api/document_out/knowable'
    params = {
        'page': page,
        'sortBy': '',
        'direction': 'DESC',
        'size': size,
        'read': False
    }
    try:
        response = requests.get(base_url, headers=headers, params=params, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error("Lỗi khi lấy tài liệu tại trang %d: %s", page, e)
        raise

#Hàm lấy json của api trong
def download_json_trong(headers, id_data):
    base_url = f'https://backend8181.bcy.gov.vn/api/document_out/getDetailToShow/{id_data}'

    try:
        # Gửi yêu cầu GET tới API
        response = requests.get(base_url, headers=headers, verify=False)
        response.raise_for_status()  # Kiểm tra lỗi HTTP

        # Trả về JSON từ phản hồi
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error("Lỗi khi lấy chi tiết tài liệu với ID %s: %s", id_data, e)
        raise
# Hàm tải và lưu file
def save_file(headers, name, download_url, id_data, van_ban, type):
    try:
        # Gửi yêu cầu tải file
        response = requests.get(download_url, headers=headers, verify=False)
        response.raise_for_status()

        if response.status_code == 200:
            clean_name = name.split('__')[0]  # Làm sạch tên file

            # Xây dựng đường dẫn đến thư mục đích `pdfdata`
            pdfdata_dir = os.path.join(settings.MEDIA_ROOT, 'pdfdata')
            if not os.path.exists(pdfdata_dir):  # Kiểm tra nếu thư mục chưa tồn tại
                os.makedirs(pdfdata_dir)  # Tạo thư mục

            # Đường dẫn đầy đủ của file
            file_path = os.path.join(pdfdata_dir, clean_name)

            # Lưu file vào hệ thống
            with open(file_path, 'wb') as file:
                file.write(response.content)

            # Lưu thông tin Data vào cơ sở dữ liệu
            Data.objects.create(van_ban = van_ban, name = clean_name, type = type, original_file = file_path)
            #PDFFile.objects.create(name=clean_name, pdf_url=download_url, file_path=file_path)

            logging.info("Tải thành công và lưu file: %s", clean_name)
    except requests.exceptions.RequestException as e:
        logging.error("Lỗi khi tải file %s: %s", name, e)
    except Exception as e:
        logging.error("Lỗi không xác định khi lưu file %s: %s", name, e)
        
# Hàm chính
@csrf_exempt
def download_all_pdf(request):
    if request.method != 'POST':
        return HttpResponse("Invalid request", status=405)

    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

         # Sử dụng request.data để lấy dữ liệu
        start_date = request.data.get('startDate')
        end_date = request.data.get('endDate')

        if not start_date or not end_date:
            return JsonResponse({"error": "Missing startDate or endDate"}, status=400)
        
        access_token = login_and_get_token()
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        print("dang nhap thanh cong")
        page = 1
        size = 1

        while True:
            data = download_documents(headers, page, size)

            if not data.get('data') or not data['data'].get('content'):
                logging.info("Không còn dữ liệu ở trang %d. Kết thúc.", page)
                break

            logging.info("Đang xử lý trang %d với %d tài liệu.", page, len(data['data']['content']))
            # kiểm tra ngày
            dateIssued = data['data']['content']['dateIssued']
            if dateIssued < start_date:
                break
            if dateIssued > end_date:
                page += 1
                continue

            id_data = data['data']['content']['id']
            # tạo database VanBan
            dataVanBan = download_json_trong(headers, id_data)
            dataVanBan_data =dataVanBan['data']

            van_ban = VanBan.objects.create(
                ngay_ban_hanh = dataVanBan_data.get('dateIssued'),
                id_api = dataVanBan_data.get('id'),
                so_ky_hieu = dataVanBan_data.get('numberOrSign'),
                loai_van_ban = dataVanBan_data.get('docTypeName'),
                nguoi_tao = dataVanBan_data.get('personEnterName'),
                trich_yeu = dataVanBan_data.get('preview'),
                don_vi_soan_thao = dataVanBan_data.get('orgCreateName'),
                so_van_ban = dataVanBan_data.get('bookName'),
                do_mat = dataVanBan_data.get('docSecurityName'),
                do_khan = dataVanBan_data.get('docUrgentName'),
                nguoi_ky = dataVanBan_data.get('signerName')
            )

            content = data['data']['content']
            so_luong_data =0
            for attachment in content.get('attachments', []):
                name = attachment['name']
                download_url = f'https://backend8181.bcy.gov.vn/api/doc_out_attach/download/{name}'
                type = attachment['type']
                save_file(headers, name, download_url, id_data, van_ban, type)
                so_luong_data += 1
            van_ban.so_luong_data = so_luong_data
            van_ban.save()

            if len(data['data']['content']) < size:
                logging.info("Trang cuối cùng được xử lý (trang %d). Kết thúc.", page)
                break

            page += 1
        return HttpResponse("All files downloaded and saved successfully")
    except Exception as e:
        logging.critical("Lỗi không xác định: %s", e)
        return HttpResponse(f"Lỗi không xác định: {e}", status=500)