from django.urls import path
from . import views

app_name = "pdf_converter"

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.file_list, name='file_list'),  # URL để xem danh sách file
]